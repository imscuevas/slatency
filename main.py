import pycurl
import certifi
from io import BytesIO

def sendRequest(url: str) -> dict:
    statistics = {}
    buffer = BytesIO()
    request = pycurl.Curl()
    request.setopt(pycurl.URL, url)
    request.setopt(pycurl.WRITEDATA, buffer)
    request.perform()
    statistics["queueTime"] = request.getinfo(pycurl.QUEUE_TIME_T)
    statistics["namelookupTime"] = request.getinfo(pycurl.NAMELOOKUP_TIME_T)
    statistics["connectTime"] = request.getinfo(pycurl.CONNECT_TIME_T)
    statistics["appconnectTime"] = request.getinfo(pycurl.APPCONNECT_TIME_T)
    statistics["pretransferTime"] = request.getinfo(pycurl.PRETRANSFER_TIME_T)
    statistics["postTransferTime"] = request.getinfo(pycurl.POSTTRANSFER_TIME_T)
    statistics["startTransferTime"] = request.getinfo(pycurl.STARTTRANSFER_TIME_T)
    statistics["totalTime"] = request.getinfo(pycurl.TOTAL_TIME_T)
    statistics["redirectTime"] = request.getinfo(pycurl.REDIRECT_TIME_T)
    statistics["localIP"] = request.getinfo(pycurl.LOCAL_IP)
    statistics["localPort"] = request.getinfo(pycurl.LOCAL_PORT)
    statistics["remoteIP"] = request.getinfo(pycurl.PRIMARY_IP)
    statistics["remotePort"] = request.getinfo(pycurl.PRIMARY_PORT)
    request.close()
    return statistics

def main():
    results = sendRequest("https://www.google.com.mx")
    print(f"Time to lookup: {results["namelookupTime"]}")
    print(f"Time to connect: {results["connectTime"] - results["namelookupTime"]}")
    print(f"Time to TLS: {results["appconnectTime"] - results["connectTime"]}")
    print(f"Time to first request byte: {results["pretransferTime"] - results["appconnectTime"]}")
    print(f"Time to last request byte: {results["postTransferTime"] - results["pretransferTime"]}")
    print(f"Time to first response: {results["startTransferTime"] - results["postTransferTime"]}")
    print(f"Total time: {results["totalTime"] - results["startTransferTime"]}")
    print(f"Redirection time: {results["redirectTime"]}")
    print(f"Connection from {results["localIP"]}:{results["localPort"]} -> {results["remoteIP"]}:{results["remotePort"]}")
    
    return

if __name__ == "__main__":
    # This is going to be how to use the function
    main()