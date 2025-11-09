# Project description

To develop an application for measuring the statistical latency to HTTP and HTTPS endpoints using Python and the pycurl library, and analize the statistical latency using numpy and/or pandas to save the information regarding the requests made to an endpoint.

## The four pilars of development

### 1. Divide and conquer

The application will be divided in multiple stages

#### The happy path

1. Send a specified number of requests to the endpoint to get the latency for the multiple steps of the request (DNS, TCP establishment time, TLS handshake, etc.)
2. Save the information in a standard format that can be logged for debug purposes and saved for later analysis.
3. After reading the requests information we will proceed to measure the statistical latency using pandas to save the information and numpy to get the statistical information that will be displayed to the user

#### Corner cases

Sometimes, requests fail at a specific stage of the request lifecycle, so we need to consider that we should save in a standard format if the request failed and in which stage it failed, for example, if a request failed because of a DNS error we should know from the standard format that it failed in the DNS stage and if possible get more details about the error.

### 2. Recognize patterns

Pandas dataframes are going to be our base tool as they allow to save information without the needing of other filesystems. They allow to manage large chunks of information and they allow to import and export the information to multiple standard formats. In the first version of this application JSON will be used as it is human readable and it allows to format the information so it can be used with numpy for future analysis.

### 3. Abstraction

The main parts of the application are the following

#### Gathering information requests

This is where the pycurl library will help, as it will gather all the information from a request, and the use of pandas will allow to save that information to a pandas dataframe.

#### Analyze the statistical latency using the requests information

This is where numpy library will read the information in the pandas dataframe and will analyze the statistical latency and will generate a report of that information

### 4. Design algorithms

#### Getting the request information

##### Happy path

When contacting an URL, for example https://www.google.com, we should be able to get basic timing information as how much time it spent on the DNS request, the TCP stablishment time, if HTTPS, the TLS handshake time, the time to first byte sent, the time to last byte sent, the first byte received and the last byte received.

##### Edge cases

The request will fail at any stage, so it is needed to consider that we need to capture the error information so it can be saved in the standard format 

#### Define the standard format

#### Functions that will be used to analyze the information

##### General information for all the stages

1. We should find the minimum and the maximum request latency
2. We should display the error rate
3. For the requests that did not failed, we should dump the 50, 90, 95 and 99 percentiles

##### Information for each stage

1. Find the min and max for each stage
2. Find the 50, 90, 95 and 99 percentiles

##### Information between stages

1. Find the difference between stages, for example, we need to know how much time passed between DNS and DNS and TCP, from TCP to TLS, etc.
2. Get statistical information about that time to find where the latency is getting introduced.

#### Display the information to the customer

Generate a report that outputs the information in an easy to read format.