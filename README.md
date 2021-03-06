## asyncio_dnac_client
Python script for a DNA-Center REST API Client implemented using asyncio python using aiohttp module

* Technology stack: Primary programming language Python3.7. The code is intended to be used as a standalone script with the modules used defined in requirements.txt
* Status:  Beta

## Use Case Description

DNA-Center REST APIs are used to programmatically configure and gather network infrastructure resources managed by the controller. Since the REST APIs are I/O intensive, a REST API client built using simple requests/session module tends to get slower as multiple REST API calls are made simultaneously. Asyncio DNA-Center REST API client on the other hand handles each REST API call as a task. Therefore the asyncio implementation provides huge run-time performance gain since the REST API calls are handled concurrently.

## Installation

* Python version: Python3 (Preferably Python3.7)
* Install the packages mentioned in requirements.txt using 'pip install -r requirements.txt'

## Usage

* The DNA-Center controller details should be provided in the config.ini file
* The DnacHttpSession class is instantiated in asyncio_dnac_client.py file
* The REST API call details are entered as a list of tuples to the create_rest_api_tasks method of DnacHttpSession object in asyncio_dnac_client.py file
* Run 'python asyncio_dnac_client.py' to execute the code

## Getting help

If you have questions, concerns, bug reports, etc., please create an issue against this repository.

## Getting involved

If you want to extend the scripts beyond feature templates, please push the changes to this repository in a new branch and create a Pull Request. Changes will be reviewed and then merged to develop branch
