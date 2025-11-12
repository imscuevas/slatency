# Slatency - Application Layer Documentation

The Application Layer is the heart of the `slatency` application's logic. It contains the specific rules and use cases that define what the application can do. Its primary responsibility is to orchestrate the flow of data between the outer layers (like the command-line interface) and the inner Domain Layer.

By acting as a mediator, this layer decouples the core domain models from the infrastructure details (e.g., how requests are sent or how data is stored), making the system more modular, testable, and maintainable.

---

## Core Components

The Application Layer is built from several key components that work together to execute application-specific tasks.

### 1. Use Cases (Interactors)

Use Cases are classes that encapsulate a single, specific task that a user can perform, such as "create a new test" or "run a test". They represent the application's capabilities and orchestrate the necessary domain entities and services to achieve their goal.

**Key Responsibilities:**
- Validate input data (via DTOs).
- Authorize actions (if applicable).
- Interact with domain models and services through Ports.
- Return a result (success or failure) to the presentation layer.

**Implemented Use Cases (`slatency/application/use_cases/`):**
- **`CreateTestUseCase`**: Creates a new `Test` entity based on user input and persists it.
- **`ListTestsUseCase`**: Retrieves a list of all existing tests.
- **`GetTestUseCase`**: Retrieves a single `Test` by its ID.
- **`RunTestUseCase`**: Executes the probes for a given test, collects responses, and generates a latency report.

### 2. Ports (Interfaces)

In Clean Architecture, a Port is an interface that defines a contract for a dependency. This allows the use case to depend on an abstraction rather than a concrete implementation. The actual implementation (the "Adapter") lives in the outer infrastructure layer.

**Key Responsibilities:**
- Define the methods a use case needs from an external service (e.g., a database, a network client, a file writer).
- Invert the dependency, so the Application Layer doesn't depend on the Infrastructure Layer.

**Defined Ports:**
- **`TestRepository`** (`slatency/application/repositories/`): Defines the contract for storing and retrieving `Test` entities (e.g., `save()`, `find_by_id()`, `get_all()`). The implementation could be an in-memory store, a file system, or a database.
- **`TestRunner`** (`slatency/application/service_ports/`): Defines the contract for executing the HTTP requests of a `Test` entity. The implementation will wrap a library like `pycurl`.
- **`OutputPersistence`** (`slatency/application/service_ports/`): Defines the contract for persisting output data, such as a final report. The implementation will handle file I/O (e.g., writing a JSON file).

### 3. Data Transfer Objects (DTOs)

DTOs are simple data structures used to transfer data between layers. They are crucial for maintaining loose coupling, as they prevent the domain models from "leaking" into the presentation layer and vice-versa.

**Key Responsibilities:**
- Carry data into the application layer from the user (Input DTOs).
- Carry data out of the application layer to be displayed to the user (Output DTOs).

**Example DTOs (`slatency/application/dtos/`):**
- **Input DTO:** `CreateTestRequestDTO`
  - Contains raw data from the user to create a new test (URL, method, probe count, etc.).
- **Output DTOs:**
  - `TestDTO`: A safe representation of a `Test` entity to be shown to the user.
  - `LatencyReportDTO`: A structured representation of the final statistical analysis, ready for display or serialization.

### 4. Error Handling with `Result`

To avoid using exceptions for control flow, all use cases return a `Result` object. This pattern makes error handling explicit and predictable. The `Result` object is a container that holds either a successful outcome or an error.

**Components (`slatency/application/common/result.py`):**
- **`Result`**: The generic container.
- **`Success(value)`**: Wraps the successful output data (usually a DTO).
- **`Failure(error)`**: Wraps an `Error` object containing details about what went wrong.
- **`Error`**: A simple class holding an error message and type, providing context for the failure (e.g., `NOT_FOUND`, `VALIDATION_ERROR`).

---

## Example Workflow: `RunTestUseCase`

This workflow illustrates how the components work together to execute a latency test:

1.  **Input**: The CLI layer calls `RunTestUseCase.execute()` with a DTO containing the `test_id`.

2.  **Fetch**: The use case calls `test_repository.find_by_id(test_id)` (using the `TestRepository` port) to retrieve the `Test` domain entity. If not found, it returns a `Failure(Error(type='NOT_FOUND', ...))`.

3.  **Execute**: The use case passes the `Test` entity to the `test_runner.run(test)` method (using the `TestRunner` port).
    - The `pycurl`-based adapter for `TestRunner` (in the Infrastructure layer) executes all HTTP requests and populates the `Test` entity with `Response` objects.

4.  **Analyze**: The use case then calls a domain service, `LatencyAnalysisService.analyze(test)`, which processes the `Response` objects within the `Test` entity and returns a `LatencyReport` domain object.

5.  **Update & Persist**: The use case updates the `Test` entity with the new responses and calls `test_repository.save(test)` to persist the completed test results.

6.  **Format Output**: The `LatencyReport` domain object is mapped to a `LatencyReportDTO`.

7.  **Return**: The use case returns `Success(latency_report_dto)`, which the CLI layer then uses to display the results to the user.
