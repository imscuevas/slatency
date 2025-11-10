# slatency - Entities and Value-Added Objects

This document outlines the core entities and value-added objects for the slatency project.

## Entities

### Request

A `Request` represents an HTTP request to be sent to a target service.

- **Attributes:**
    - `url`: A `URL` object representing the target service's endpoint.
    - `method`: The HTTP method (e.g., GET, POST, PUT, DELETE).
    - `headers`: A dictionary of HTTP headers.
    - `body`: The request payload.
    - `timeout`: The timeout for the request in seconds.

### Response

A `Response` represents the HTTP response received from the target service.

- **Attributes:**
    - `status_code`: The HTTP status code.
    - `headers`: A dictionary of HTTP headers.
    - `body`: The response payload.
    - `latency`: The time taken to receive the response after the request was sent (in milliseconds).
    - `timestamp`: The time at which the response was received.

### Test

A `Test` represents a collection of requests and their corresponding responses for a specific scenario.

- **Attributes:**
    - `test_id`: A unique identifier for the test.
    - `name`: A descriptive name for the test.
    - `description`: A more detailed description of the test's purpose.
    - `requests`: A list of `Request` objects.
    - `responses`: A list of `Response` objects.
    - `creation_date`: The date and time the test was created.

## Value-Added Objects

### URL

A `URL` represents a Uniform Resource Locator.

- **Attributes:**
    - `protocol`: The protocol (e.g., http, https).
    - `host`: The hostname or IP address.
    - `port`: The port number.
    - `path`: The path of the resource.
    - `query_params`: A dictionary of query parameters.

### LatencyReport

A `LatencyReport` provides aggregated latency data for a `TestRun`.

- **Attributes:**
    - `test_run_id`: The ID of the `TestRun` this report is for.
    - `min_latency`: The minimum latency observed.
    - `max_latency`: The maximum latency observed.
    - `average_latency`: The average latency.
    - `p95_latency`: The 95th percentile latency.
    - `p99_latency`: The 99th percentile latency.

### TestRun

A `TestRun` represents a single execution of a `Test`.

- **Attributes:**
    - `test_run_id`: A unique identifier for the test run.
    - `test_id`: The ID of the `Test` that was run.
    - `timestamp`: The time at which the test run was initiated.
    - `responses`: A collection of `Response` objects from the run.

## Domain Services

### TestRunnerService

This service is responsible for executing a `Test`. It takes a `Test` object, sends the defined HTTP requests, and records the `Response` objects.

### LatencyAnalysisService

This service takes a `TestRun` and generates a `LatencyReport`. It encapsulates the logic for calculating latency statistics.

### TestRepository

This service handles the persistence of `Test` objects. It provides methods to create, retrieve, update, and delete tests from a data store.
