# Pricing Project #
Find and display differences between a price sheet and prices in an Avoxi cart.

## Setup and Run ##
Install requirements

```
pip install -r requirements.txt
```

Install `chromedriver` : https://sites.google.com/a/chromium.org/chromedriver/home and add it to your system PATH.

To run the program use the following command:
```
python pricing.py
```

Runs on *python 3.7+*. It might run on *3.6*. I don't think I've used *3.7* specific features.

The first run and periodically, Google will open a web page prompt to authenticate using your google account in order to read from the price sheet.

## Features ##
* Connects to a Google Sheet to automatically pull in the Price Sheet.
* Scrapes the Avoxi shopping cart.
* Outputs a list of differences using price sheet as the standard/expected.

## Immediate TODO ##
* Further cleaning of values from price sheer to catch edge cases in diffing
* Improve diffing so it is more accessible outside the module
* Logging
* Tests and typing when api is stabilizing
* Clean and validate values coming from price sheet
* Verify class names used for scraping are consistent

## Future Work ##
Display methods--depending on the needs of the users:
1. periodically execute the script to write diffs back to the price sheet
  this may present some authentication challenges.
2. host a web interface to control the running of the script and view results.

Investigate using a scraper context manager for better teardown of Chrome.

Run in a Docker container.

## Comments ##
I am still exploring the overall api so I have not started writing tests that may prematurely cement [poor] decisions.

Time delays are substantial in the scraping loop so there is room for improvement using `asyncio` to run multiple instances concurrently. Need to be careful not to hit the server too hard with requests though.

## Requirements ##
```
# see requirements.txt

beautifulsoup4==4.7.1
cachetools==3.1.0
certifi==2018.11.29
chardet==3.0.4
google-api-python-client==1.7.8
google-auth==1.6.3
google-auth-httplib2==0.0.3
google-auth-oauthlib==0.2.0
httplib2==0.12.1
idna==2.8
oauthlib==3.0.1
pyasn1==0.4.5
pyasn1-modules==0.2.4
requests==2.21.0
requests-oauthlib==1.2.0
rsa==4.0
selenium==3.141.0
six==1.12.0
soupsieve==1.8
uritemplate==3.0.0
urllib3==1.24.1
```
