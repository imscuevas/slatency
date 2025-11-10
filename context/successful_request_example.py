import pycurl
from io import BytesIO

request = pycurl.Curl()
request.setopt(pycurl.URL, 'https://www.example.com')
request.setopt(pycurl.FOLLOWLOCATION, False)
request.setopt(pycurl.CONNECTTIMEOUT, 5)
request.setopt(pycurl.TIMEOUT, 10)
request.setopt(pycurl.WRITEDATA, BytesIO())

request.perform()

print(request.getinfo(pycurl.QUEUE_TIME_T))
print(request.getinfo(pycurl.NAMELOOKUP_TIME_T))
print(request.getinfo(pycurl.CONNECT_TIME_T))
print(request.getinfo(pycurl.APPCONNECT_TIME_T))
print(request.getinfo(pycurl.PRETRANSFER_TIME_T))
print(request.getinfo(pycurl.POSTTRANSFER_TIME_T))
print(request.getinfo(pycurl.STARTTRANSFER_TIME_T))
print(request.getinfo(pycurl.TOTAL_TIME_T))

request.close()