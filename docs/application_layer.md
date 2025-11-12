# Application Layer

## The `Result` type

To handle operations that can either succeed or fail, we will use a `Result` type. This is a generic class that will represent either a `Success` or a `Failure`.

### `Result[S, E]`

- **Type parameters:**
    - `S`: The type of the value on success.
    - `E`: The type of the error on failure.

The `Result` will have two possible states:

- `Success(S)`: Contains the successful result of the operation.
- `Failure(E)`: Contains an error object describing what went wrong.

### Example Usage

```python
from typing import Union

class Success[S, E]:
    def __init__(self, value: S):
        self.value = value

class Failure[S, E]:
    def __init__(self, error: E):
        self.error = error

Result = Union[Success[S, E], Failure[S, E]]

# Example of a function that returns a Result
def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Failure("Cannot divide by zero")
    return Success(a / b)

# Usage
result = divide(10, 2)
if isinstance(result, Success):
    print(f"Result: {result.value}")
else:
    print(f"Error: {result.error}")
```

## Error Hierarchy

To provide clear and structured error handling, we will define a hierarchy of error types.

### `AppError`

This is the base class for all application-specific errors.

- **Attributes:**
    - `message`: A human-readable error message.

```python
class AppError(Exception):
    def __init__(self, message: str):
        self.message = message
```

### `ValidationError`

This error is used when input data fails validation.

- **Inherits from:** `AppError`
- **Attributes:**
    - `field_errors`: A dictionary mapping field names to a list of validation error messages.

```python
from typing import Dict, List

class ValidationError(AppError):
    def __init__(self, message: str, field_errors: Dict[str, List[str]]):
        super().__init__(message)
        self.field_errors = field_errors
```

### `InfrastructureError`

This error is used for failures in external systems, such as network issues or database connection errors.

- **Inherits from:** `AppError`
- **Attributes:**
    - `original_exception`: The original exception that was caught.

```python
class InfrastructureError(AppError):
    def __init__(self, message: str, original_exception: Exception):
        super().__init__(message)
        self.original_exception = original_exception
```

### `DomainError`

This error is used when a domain rule is violated.

- **Inherits from:** `AppError`

```python
class DomainError(AppError):
    pass
```

## Application Services

Application services orchestrate the domain logic and are the entry points for the application's use cases.

### TestApplicationService

This service is responsible for executing a `Test`. It takes a `Test` object, sends the defined HTTP requests, and records the `Response` objects.

### LatencyAnalysisApplicationService

This service takes a `Test` and generates a `LatencyReport`. It encapsulates the logic for calculating latency statistics.

### TestOutputPersistenceApplicationService

This service is responsible for saving the output of a test. It handles persisting the `Test` object, which includes the raw `Response` data.
