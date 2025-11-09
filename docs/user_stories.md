# User stories

## Must

- **UHM1**: As the user I want to send HTTP(S) request(s) to any endpoint for measuring the statistical latency to that endpoint
	- Given the command when I am in the command line then I should see the progress for each request and at the end the report
- **UHM2**: As the user I want to be able to read the response from a file to be able to share it with anyone
	- Given the file I should be able to read each one of the requests when I open it on a text editor or parse it with jq
- **UHM3**: As the user I want to be able to know if the requests failed from the file so I can measure the error rate
	- Given the file when I open it on a text editor then I should be able to see if the request failed and if it failed, on which phase it failed.
- **UHM4**: As the user for every successful request I want to read the DNS resolution time, TCP establishment time, TLS handshake time, redirection, time to first byte sent, time to last byte sent, time to first byte received, time to last byte received and the total time to be able to do numerical analysis on the provided data.
	- Given the file when I open it on a text editor then I should be able to see the different phases time for a successful request
- **UHM7**: As the user I want to read from the report the minimum, the maximum, the P90, the P95, the P99 latency for each phase and total for all the successful requests to know the latency to the HTTP(S) endpoint
	- Given the command when it finishes then I should be able to read the information in the command line
- **UHM9**: As the user I want to be able to run it from the command line so this can be run from computers without graphical interface
	- Given the URL and the data for the HTTP(S) endpoint when I am in the command line then I should be able to run the command
- **UHM11**: As the user I should be able to provide the method like GET or POST so I can test any kind of endpoint
	- Given the request method when I use the command line tool then I should be able to run it from the command line
- **UHM12**: As the user I should be able to provide the headers so features like authentication or cache can work as expected
	- Given the headers information when I use the command line tool then I should be able to run it from the command line
- **UHM13**: As the developer I should use libcurl and pandas as they are standard libraries so the development time can be reduced to the minimum as they are really good documented
	- Given the 
- **UHM15**: As the user I want a man page or command line documentation with examples to know how to use the tool
	- Given the command line tool when I am in the command line then I should be able to use the `-h` or `--help` flag to see the short help or use the `man` command to view all the options available to run it
- **UHM16**: As a developer I must upload all code to Github to allow other developers to contribute to this open source tool
	- Given the code when I am develping then I should pull and push code from/to Github so other people can contribute to this open source tool
- **UHM17**: As the user I want to provide a custom filename so I can save multiple rounds of tests without losing information
	- Given the command line tool when I am in the command line then I should be able to use the `-o` or `--output` flag to send the requests output to any filename
- **UHM18**: As a developer I should use json as they are common sharing formats so the customers can read the request file in any other application if they want
	- Given the command when I run the tool I should receive a json file with all the requests information as the output that should be opened in any text editor or parsed with jq
- **UHM20**: As the user I want to be able to see in the report the error rate so I can spot any networking issue. This should be reported for all the requests and per phase
	- Given the report when the command finished running then I should be able to see the error rate for all the failed requests and the percentage of errors per phase
- **UHM21**: As a user, for POST and PUT requests I should be able to provide data on the command line or from a file so I can test latency or error rate when I send traffic to the HTTP(S) endpoint
	- Given a request with POST or PUT HTTP when I use the command line tool then I should be able to provide content in the command line as curl

## Should

- **UHS5**: As the user I want to be able to configure the number of requests that I want to send to the endpoint
- **UHS14**: As the user I would like to have the option to autocomplete the commands so it works as other mature command line tools and avoid reading the help page for completing commands
- **UHS19**: As the user I should be able to configure a request timeout so I can control the maximum time for a full test

## Could

- **UHC6**: As the user I want to receive an automatically generated report so I can have all the information needed to probe any latency issue
- **UHC8**: As the user I would like to see the latency metrics using graphs, so the information is not only readable but understandable

## Won't

- **UHW10**: As a user without command line skills I would like to run it from a graphical interface so I don't have any learning curve to use it

## Unclassified user stories