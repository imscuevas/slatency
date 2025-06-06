import pycurl
import certifi
from io import BytesIO
import argparse
import json # Import the json module

# Define a constant for microsecond to millisecond conversion
US_TO_MS_DIVISOR = 1000.0

def sendRequest(url: str, connect_timeout: int, total_timeout: int) -> dict:
    statistics = {}
    buffer = BytesIO()
    request = pycurl.Curl()
    request.setopt(pycurl.URL, url)
    request.setopt(pycurl.WRITEDATA, buffer)
    request.setopt(pycurl.CAINFO, certifi.where())
    
    request.setopt(pycurl.CONNECTTIMEOUT, connect_timeout)
    request.setopt(pycurl.TIMEOUT, total_timeout)

    try:
        request.perform()
        statistics["http_code"] = request.getinfo(pycurl.RESPONSE_CODE)
        # Collect timings and convert to milliseconds
        statistics["queueTime_ms"] = request.getinfo(pycurl.QUEUE_TIME_T) / US_TO_MS_DIVISOR
        statistics["namelookupTime_ms"] = request.getinfo(pycurl.NAMELOOKUP_TIME_T) / US_TO_MS_DIVISOR
        statistics["connectTime_ms"] = request.getinfo(pycurl.CONNECT_TIME_T) / US_TO_MS_DIVISOR
        statistics["appconnectTime_ms"] = request.getinfo(pycurl.APPCONNECT_TIME_T) / US_TO_MS_DIVISOR
        statistics["pretransferTime_ms"] = request.getinfo(pycurl.PRETRANSFER_TIME_T) / US_TO_MS_DIVISOR
        statistics["startTransferTime_ms"] = request.getinfo(pycurl.STARTTRANSFER_TIME_T) / US_TO_MS_DIVISOR
        statistics["totalTime_ms"] = request.getinfo(pycurl.TOTAL_TIME_T) / US_TO_MS_DIVISOR
        statistics["redirectTime_ms"] = request.getinfo(pycurl.REDIRECT_TIME_T) / US_TO_MS_DIVISOR
        
        if statistics["http_code"] >= 200 and statistics["http_code"] < 400:
            statistics["localIP"] = request.getinfo(pycurl.LOCAL_IP)
            statistics["localPort"] = request.getinfo(pycurl.LOCAL_PORT)
            statistics["remoteIP"] = request.getinfo(pycurl.PRIMARY_IP)
            statistics["remotePort"] = request.getinfo(pycurl.PRIMARY_PORT)
        else:
            statistics["error"] = f"HTTP Error: {statistics['http_code']}"
            for key in ["localIP", "localPort", "remoteIP", "remotePort"]:
                statistics.setdefault(key, "N/A")
    except pycurl.error as e:
        statistics["error"] = f"PycURL error: {e.args[0]} - {e.args[1]}"
        statistics["http_code"] = -1 
        for key_ms in ["queueTime_ms", "namelookupTime_ms", "connectTime_ms", "appconnectTime_ms",
                       "pretransferTime_ms", "startTransferTime_ms", "totalTime_ms", "redirectTime_ms"]:
            statistics.setdefault(key_ms, 0.0) # Default to float 0.0 for milliseconds
        for key_ip in ["localIP", "localPort", "remoteIP", "remotePort"]:
            statistics.setdefault(key_ip, "N/A")
    finally:
        request.close()
    return statistics

def main():
    parser = argparse.ArgumentParser(description="Send multiple HTTP requests, print timing statistics, and save to JSON.")
    parser.add_argument("url", type=str, help="The URL to send requests to.")
    parser.add_argument("probes", type=int, help="The number of requests (probes) to send.")
    parser.add_argument("--timeout", type=int, default=60, help="Total timeout for each request in seconds (default: 60).")
    parser.add_argument("--connect-timeout", type=int, default=30, help="Connection timeout for each request in seconds (default: 30).")
    parser.add_argument("--output-file", type=str, default="results.json", help="File path to save the JSON results (default: results.json).")
    
    args = parser.parse_args()

    target_url = args.url
    num_probes = args.probes
    connect_timeout_val = args.connect_timeout
    total_timeout_val = args.timeout
    output_file = args.output_file

    if num_probes <= 0:
        print("Error: Number of probes must be a positive integer.")
        return

    print(f"Sending {num_probes} probes to {target_url}...\n")

    all_results = []

    for i in range(num_probes):
        print(f"--- Request {i+1}/{num_probes} ---")
        results = sendRequest(target_url, connect_timeout_val, total_timeout_val)
        all_results.append(results)

        if "error" in results:
            print(f"Error during request: {results['error']}")
            if results.get("http_code") and results["http_code"] != -1:
                 print(f"HTTP Status Code: {results['http_code']}")
            print("-" * 30)
            # We still append the error result to all_results for completeness in the JSON
            continue 

        print(f"HTTP Status Code: {results.get('http_code', 'N/A')}")

        namelookup_ms = results.get('namelookupTime_ms', 0.0)
        connect_ms = results.get('connectTime_ms', 0.0)
        appconnect_ms = results.get('appconnectTime_ms', 0.0)
        pretransfer_ms = results.get('pretransferTime_ms', 0.0)
        starttransfer_ms = results.get('startTransferTime_ms', 0.0)
        total_ms = results.get('totalTime_ms', 0.0)
        redirect_ms = results.get('redirectTime_ms', 0.0)

        print(f"Time to lookup: {namelookup_ms:.3f}ms")
        if connect_ms > 0 and namelookup_ms >= 0 : 
            print(f"Time to connect: {(connect_ms - namelookup_ms):.3f}ms")
        else:
            print(f"Time to connect: {connect_ms:.3f}ms (namelookup time was zero or invalid)")

        if appconnect_ms > 0 and connect_ms >= 0:
            print(f"Time to TLS (if HTTPS): {(appconnect_ms - connect_ms):.3f}ms")
        elif appconnect_ms == 0 and connect_ms > 0 and "https://" in target_url:
             print(f"Time to TLS (if HTTPS): 0.000ms (appconnect_time was zero, check SSL details)")
        elif appconnect_ms == 0 and "http://" in target_url:
             print(f"Time to TLS (if HTTPS): N/A (HTTP request)")

        ttfb_base_ms = appconnect_ms if appconnect_ms > 0 else connect_ms
        if pretransfer_ms > 0 and ttfb_base_ms >= 0:
            print(f"Time to first request byte (TTFB setup): {(pretransfer_ms - ttfb_base_ms):.3f}ms")
        else:
            print(f"Time to first request byte (TTFB setup): {pretransfer_ms:.3f}ms (base time was zero or invalid)")

        if starttransfer_ms > 0 and pretransfer_ms >= 0:
            print(f"Time for server processing (to first response byte): {(starttransfer_ms - pretransfer_ms):.3f}ms")
        else:
            print(f"Time for server processing (to first response byte): {starttransfer_ms:.3f}ms (pretransfer time was zero or invalid)")

        if total_ms > 0 and starttransfer_ms >= 0:
            print(f"Time to download response: {(total_ms - starttransfer_ms):.3f}ms")
        else:
            print(f"Time to download response: {(total_ms - (starttransfer_ms if starttransfer_ms > 0 else pretransfer_ms)):.3f}ms (starttransfer time was zero or invalid)")


        print(f"Actual Total time: {total_ms:.3f}ms")
        print(f"Redirection time: {redirect_ms:.3f}ms")
        
        print(f"Connection from {results.get('localIP', 'N/A')}:{results.get('localPort', 'N/A')} -> {results.get('remoteIP', 'N/A')}:{results.get('remotePort', 'N/A')}")
        print("-" * 30)
    
    print(f"\nFinished {num_probes} probes.")

    # Save all results to a JSON file
    try:
        with open(output_file, 'w') as f:
            json.dump(all_results, f, indent=4)
        print(f"Results saved to {output_file}")
    except IOError as e:
        print(f"Error saving results to {output_file}: {e}")

    # Example: Calculate average total time for successful requests
    successful_results = [r for r in all_results if "error" not in r and r.get("http_code", 0) >= 200 and r.get("http_code",0) < 400]
    if successful_results:
        avg_total_time_ms = sum(r.get('totalTime_ms', 0.0) for r in successful_results) / len(successful_results)
        print(f"Average total time for successful requests: {avg_total_time_ms:.3f}ms")
    
    return

if __name__ == "__main__":
    main()