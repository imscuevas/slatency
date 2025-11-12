# Slatency - Application Layer

This document outlines the Application Business Rules (Interactors/Use Cases) for the `slatency` project. This layer orchestrates the domain entities and value objects to perform specific application tasks.

## Core Concepts

### Result Pattern

All interactor methods (use cases) MUST return a `Result` object. This provides a standardized way to handle both success and failure scenarios without relying on exceptions for control flow.

- **`Result[S, E]`**: A generic container that holds either a success value (`S`) or an error value (`E`).
- **`Success(value: S)`**: Represents a successful operation, containing the resulting data.
- **`Failure(error: E)`**: Represents a failed operation, containing an error object.

### Application Error Hierarchy

All errors returned by interactors will be subtypes of a base `AppError`.

- **`AppError`**: The base class for all application-level errors.
  - **`ValidationError(message: str, field: str)`**: Used when input data fails validation (e.g., invalid URL format, negative probe count).
  - **`InfrastructureError(message: str, underlying_error: Exception)`**: Used for failures in external systems like the network, filesystem, or external APIs (e.g., a `pycurl` connection error).
  - **`NotFoundError(message: str, resource_id: str)`**: Used when a requested resource (like a test result file) cannot be found.

---

## Interactors (Application Services)

### 1. TestApplicationService

*   **Purpose:** Executes a new latency test against a specified endpoint. It orchestrates the creation of a `Test` object, runs the HTTP requests via an external service, and returns the completed `Test` with all its `Response` objects.

*   **Input DTO (Request): `NewTestRequestDTO`**
    *   `url: str`: The target URL for the test.
    *   `method: str`: The HTTP method (e.g., 'GET', 'POST').
    *   `headers: dict[str, str] | None`: Optional HTTP headers.
    *   `body: str | None`: Optional request body.
    *   `probes: int`: The number of requests to send.
    *   `connect_timeout: int`: Connection timeout in seconds.
    *   `total_timeout: int`: Total request timeout in seconds.

*   **Output DTO (Success Response): `TestResultDTO`**
    *   `test_id: str`: The unique identifier for the test.
    *   `request: dict`: A dictionary representing the `Request` entity used for the test.
    *   `responses: list[dict]`: A list of dictionaries, where each represents a `Response` entity (either successful or failed).

*   **Ports (Dependencies):**
    *   `ITestRunnerService`: An interface to a domain service responsible for executing the HTTP requests for a given `Test` object and returning the collected `Response` objects. This abstracts away the `pycurl` implementation details.

*   **Method Signature:**
    `execute_test(dto: NewTestRequestDTO) -> Result[TestResultDTO, AppError]`

### 2. LatencyAnalysisApplicationService

*   **Purpose:** Analyzes the results of a completed test to generate a statistical latency report. It takes the raw response data from a `Test` and calculates aggregate metrics.

*   **Input DTO (Request): `LatencyAnalysisRequestDTO`**
    *   `test_result: TestResultDTO`: The complete result of a test, as produced by the `TestApplicationService`.

*   **Output DTO (Success Response): `LatencyReportDTO`**
    *   This DTO directly mirrors the `LatencyReport` value object from the domain layer.
    *   `total_requests: int`: The total number of probes in the test.
    *   `successful_requests: int`: The count of successful requests.
    *   `failed_requests: int`: The count of failed requests.
    *   `error_rate_percentage: float`: The overall error rate.
    *   `errors_by_phase: dict[str, int]`: A breakdown of failure counts by `FailurePhase` (e.g., `{"DNS": 5, "TCP Connection": 2}`).
    *   `latency_statistics: dict[str, dict]`: A dictionary where keys are latency phases (`dns`, `connect`, `total`, etc.) and values are dictionaries representing the `LatencyStatistics` value object (`min`, `max`, `average`, `p90`, `p95`, `p99`).

*   **Ports (Dependencies):**
    *   `ILatencyAnalysisService`: An interface to a domain service that takes a `Test` object and is responsible for the business logic of calculating the `LatencyReport`.

*   **Method Signature:**
    `analyze_latency(dto: LatencyAnalysisRequestDTO) -> Result[LatencyReportDTO, AppError]`

### 3. TestOutputPersistenceApplicationService

*   **Purpose:** Persists the raw results of a latency test to a specified output, such as a JSON file. This decouples the core application logic from the details of file I/O.

*   **Input DTO (Request): `TestPersistenceRequestDTO`**
    *   `test_result: TestResultDTO`: The complete result of a test to be saved.
    *   `output_path: str`: The file path where the results should be saved.
    *   `format: str`: The desired output format (e.g., 'json').

*   **Output DTO (Success Response): `PersistenceSuccessDTO`**
    *   `output_path: str`: The final path where the file was saved.
    *   `bytes_written: int`: The number of bytes written to the file.

*   **Ports (Dependencies):**
    *   `ITestOutputPersistenceService`: An interface to a domain service responsible for serializing and writing the test data to a persistent medium. This abstracts away the `json.dump` and `open()` calls.

*   **Method Signature:**
    `save_results(dto: TestPersistenceRequestDTO) -> Result[PersistenceSuccessDTO, AppError]`