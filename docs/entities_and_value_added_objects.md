# slatency - Entities and Value-Added Objects

This document outlines the core entities and value-added objects for the slatency project.

## Entities

### Request

A `Request` represents an HTTP request to be sent to a target service.

- **Attributes:**
    - `request_id`: A unique identifier for the request.
    - `url`: A `URL` object representing the target service's endpoint.
    - `method`: An `HTTPMethod` object representing the HTTP method.
    - `headers`: A dictionary of HTTP headers.
    - `body`: The request payload.
    - `timeout`: The timeout for the request in seconds (default: 10).

### Response

A `Response` represents the outcome of an HTTP request, which can be either a success or a failure.

- **Attributes:**
    - `response_id`: A unique identifier for the response.
    - **For successful responses:**
        - `status_code`: The HTTP status code.
        - `latency`: A `Latency` object containing detailed timing information.
        - `flow`: A `Flow` object containing network flow information.
    - **For failed responses:**
        - `failure_phase`: The stage at which the request failed (e.g., DNS, TCP Connection, TLS Handshake, Request, Response).
        - `error_message`: A message describing the error.

- **Example:**

    - **Successful Response:**
      ```json
      {
        "status_code": 200,
        "latency": {
          "queue": 2,
          "dns": 10,
          "connect": 50,
          "tls": 100,
          "send_first_byte": 1,
          "send_last_byte": 4,
          "receive_first_byte": 195,
          "total": 362
        },
        "flow": {
          "source_ip": "192.168.1.100",
          "source_port": 51234,
          "destination_ip": "93.184.216.34",
          "destination_port": 443
        }
      }
      ```

    - **Failed Response:**
      ```json
      {
        "failure_phase": "DNS",
        "error_message": "Host not found"
      }
      ```

### Test

A `Test` represents a scenario for sending a specific request multiple times and collecting its responses.

- **Attributes:**
    - `test_id`: A unique identifier for the test.
    - `request`: The `Request` object to be sent.
    - `expected_responses`: The number of times the request should be sent.
    - `responses`: A list of `Response` objects.

## Value-Added Objects

### URL

A `URL` represents a Uniform Resource Locator.

- **Attributes:**
    - `protocol`: The protocol (must be `http` or `https`).
    - `host`: The hostname or IP address.
    - `port`: The port number (must be between 0 and 65535).
    - `path`: The path of the resource.
    - `query_params`: A dictionary of query parameters.

### HTTPMethod

An `HTTPMethod` is an enumeration of supported HTTP methods.

- **Values:** `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `HEAD`, `OPTIONS`.

### FailurePhase

A `FailurePhase` is an enumeration of the possible stages at which a request can fail.

- **Values:** `DNS`, `TCP Connection`, `TLS Handshake`, `Request`, `Response`.

### Flow

A `Flow` object contains the network flow information for a request.

- **Attributes:**
    - `source_ip`: The source IP address of the request.
    - `source_port`: The source port of the request.
    - `destination_ip`: The destination IP address of the request.
    - `destination_port`: The destination port of the request.

### Latency

A `Latency` object holds detailed timing information for a successful request, broken down into phases.

- **Attributes:**
    - `queue`: Time spent in the queue before the request was sent (in milliseconds).
    - `dns`: Time spent in DNS lookup (in milliseconds).
    - `connect`: Time spent connecting to the server (in milliseconds).
    - `tls`: Time spent performing the TLS handshake (in milliseconds).
    - `send_first_byte`: Time taken to send the first byte of the request (in milliseconds).
    - `send_last_byte`: Time taken from sending the first byte to sending the last byte of the request (in milliseconds).
    - `receive_first_byte`: Time spent waiting for the first byte of the response (in milliseconds).
    - `total`: Total time for the request (in milliseconds).

### LatencyReport

A `LatencyReport` provides aggregated latency data for a `Test`, with a breakdown for each phase.

- **Attributes:**
    - `queue`: A `LatencyStatistics` object for the time spent in queue.
    - `dns`: A `LatencyStatistics` object for the DNS lookup phase.
    - `connect`: A `LatencyStatistics` object for the connection phase.
    - `tls`: A `LatencyStatistics` object for the TLS handshake phase.
    - `send_first_byte`: A `LatencyStatistics` object for the time to send the first byte.
    - `send_last_byte`: A `LatencyStatistics` object for the time to send the last byte.
    - `receive_first_byte`: A `LatencyStatistics` object for the time to receive the first byte.
    - `total`: A `LatencyStatistics` object for the total request time.

### LatencyStatistics

A `LatencyStatistics` object holds aggregated data for a single latency metric.

- **Attributes:**
    - `min`: The minimum value observed (in milliseconds).
    - `max`: The maximum value observed (in milliseconds).
    - `average`: The average value (in milliseconds).
    - `p90`: The 90th percentile value (in milliseconds).
    - `p95`: The 95th percentile value (in milliseconds).
    - `p99`: The 99th percentile value (in milliseconds).

## Domain Services

### TestRunnerService

This service is responsible for executing a `Test`. It takes a `Test` object, sends the defined HTTP requests, and records the `Response` objects.

### LatencyAnalysisService

This service takes a `Test` and generates a `LatencyReport`. It encapsulates the logic for calculating latency statistics.

### TestOutputPersistenceService

This service is responsible for saving the output of a test. It handles persisting the `Test` object, which includes the raw `Response` data.
