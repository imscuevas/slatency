# 📊 slatency

**slatency** is a high-performance command-line tool for statistically analyzing the latency of HTTP and HTTPS endpoints. Utilizing Python's `pycurl` library for concurrent requests, `pandas`, and `numpy`, **slatency** goes beyond simple averages to identify performance bottlenecks, measure variability (*jitter*), and provide a detailed breakdown of timing across DNS, connection, TLS handshake, server processing, and transfer time.

## ✨ Features

  * **Granular Timing:** Reports latency for every stage: DNS lookup, TCP connection, TLS handshake, Server Processing, and Total Time.
  * **Statistical Depth:** Calculates Min, Max, Mean, P50, P90, P95, P99, and Standard Deviation.
  * **Concurrent Testing:** Uses `pycurl.CurlMulti` for parallel request execution to simulate load.
  * **Sequential Option:** Defaults to sequential requests if concurrency is not specified.
  * **Detailed Failure Analysis:** Reports counts and types of connection errors, timeouts, and non-2xx/3xx HTTP responses.
  * **Advanced HTTP Control:** Supports custom headers, methods (POST, PUT, etc.), request body (`--data`), client certificates, and **DNS injection** (`--resolve`) for targeted testing.

-----

## 🚀 Installation

**slatency** requires Python 3.8 or newer. Since `pycurl` is a dependency, you must ensure the **libcurl development libraries** are installed on your system *before* running `pip install`.

### Prerequisites

| OS/Distribution | Command |
| :--- | :--- |
| **Linux (Debian/Ubuntu)** | `sudo apt-get install libcurl4-openssl-dev libssl-dev` |
| **Linux (Red Hat/CentOS)**| `sudo yum install libcurl-devel openssl-devel` |
| **macOS (Homebrew)** | `brew install curl` (usually sufficient) |

### Steps

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/YourUsername/slatency.git
    cd slatency
    ```

2.  **Create and Activate a Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Use 'venv\Scripts\activate' on Windows
    ```

3.  **Install Dependencies:**

    ```bash
    pip install pycurl pandas numpy
    ```

-----

## 💻 Usage

Run **slatency** from the command line, providing the target URL and optional parameters.

```bash
slatency <URL> [OPTIONS]
```

### Examples

#### 1\. Simple Sequential Test (Default)

Runs 1000 requests sequentially to gather a statistical sample.

```bash
slatency https://api.example.com/status --requests 1000 
```

#### 2\. Parallel Load Test

Runs 1000 requests with 50 concurrent connections.

```bash
slatency https://api.example.com/status --requests 1000 --concurrency 50
```

#### 3\. Advanced Debugging (POST, Headers, DNS Injection)

Runs a parallel test that sends a POST request with a custom header, a 10-second timeout, and forces the domain name to resolve to a specific IP (`192.168.1.5`) for testing a specific backend server.

```bash
slatency https://api.staging.com/data \
    --requests 500 \
    --concurrency 10 \
    --method POST \
    --header "Content-Type: application/json" \
    --data '{"id": 42}' \
    --resolve "api.staging.com:443:192.168.1.5" \
    --timeout 10
```

-----

## ⚙️ Command-Line Options

| Option | Default | Description |
| :--- | :--- | :--- |
| **`<URL>`** | *(Required)* | The target endpoint (HTTP or HTTPS). |
| **`--requests N`** | `1000` | Total number of requests to perform. |
| **`--concurrency N`** | `1` | Max number of concurrent requests. **Default is 1 (sequential).** |
| **`--method <METHOD>`** | `GET` | Sets the HTTP method (`POST`, `PUT`, `DELETE`, etc.). |
| **`--header <H>`** | *(None)* | Inject custom HTTP headers. Can be specified multiple times. |
| **`--timeout <T>`** | *(pycurl default)*| Max time (in seconds) the entire request is allowed to take. |
| **`--data <D>`** | *(None)* | Data to send in the request body (implies `POST`). |
| **`--resolve <H:P:IP>`** | *(None)* | **DNS Injection:** Force a specific IP address for a hostname:port combination. |
| **`--cert <FILE>`** | *(None)* | Path to a client SSL certificate file. |
| **`--insecure`** | *(False)* | Disables SSL peer verification (for testing against self-signed certs). |

-----

## 📈 Output Report Structure

The output is presented in a structured console report with three sections:

### 1\. Execution Overview

A summary of the test run, including overall success rate.

| Metric | Example Value |
| :--- | :--- |
| **Total Requests** | 1000 |
| **Success Count** | 985 |
| **Failure Count** | 15 |
| **Success Rate** | 98.5% |

### 2\. Summary Statistics Table (Successful Requests)

Detailed statistical breakdown for each timing metric. All times are in seconds.

| Timing Metric | Min | P50 (Median) | Mean | P95 | P99 | StdDev |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DNS Lookup** | 0.001 | 0.002 | 0.003 | 0.005 | 0.008 | 0.001 |
| **TCP Connect** | 0.010 | 0.012 | 0.015 | 0.020 | 0.025 | 0.005 |
| **TLS Handshake** | 0.050 | 0.060 | 0.065 | 0.080 | 0.090 | 0.010 |
| **Server Processing** | 0.080 | 0.100 | 0.105 | 0.120 | 0.140 | 0.015 |
| **Total Time** | **0.142** | **0.176** | **0.186** | **0.230** | **0.280** | **0.032** |

### 3\. Failure Analysis

Details on all requests that resulted in an error (connection issues, timeouts, or non-2xx/3xx HTTP codes).

| Failure Type | Count | Percentage of Total |
| :--- | :--- | :--- |
| **HTTP 503 (Service Unavailable)** | 8 | 0.8% |
| **CURLE\_OPERATION\_TIMEDOUT** | 5 | 0.5% |
| **CURLE\_COULDNT\_RESOLVE\_HOST (DNS)** | 2 | 0.2% |
| **TOTAL FAILURES** | **15** | **1.5%** |

-----

## 📜 License

This project is licensed under the **MIT License**. See the `LICENSE.txt` file for details.
