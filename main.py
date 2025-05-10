import pycurl
import certifi
from io import BytesIO

def sendRequest(url: str):
    buffer = BytesIO()
    request = pycurl.Curl()
    request.setopt(pycurl.URL, url)
    request.setopt(pycurl.WRITEDATA, buffer)
    request.perform()
    print(request.getinfo(pycurl.RESPONSE_CODE))
    request.close()

def main():
    sendRequest("https://www.google.com.mx")
    return

if __name__ == "__main__":
    # This is going to be how to use the function
    main()