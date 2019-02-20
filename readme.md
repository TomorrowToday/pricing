# Pricing Challenge #


## Features ##
* Connects to a Google Sheet to automatically pull in the Price Sheet.
* Utilizes Selenium and BeastifulSoup to read the Avoxi shoppingcart.
* Outputs a list of differences using price sheet as the standard/expected.

## Immediate TODO ##
* further cleaning for values to catch edge cases in comparison
* improve diffing so it is more accessible outside the module
* logging
* tests and typing when api is stabilizing
* clean and validate values coming from price sheet

## Future Work ##
Display preferences, Depending on the needs of the users:
1. periodically execute the script to write diffs back to the price sheet
  this will present some authentication challenges.
2. host a web interface to control the running of the script.

Investigate making the scraper a context manager.

Put in a Dockr container.

## Comments ##
I am still exploring the overall api so I have not started writing tests that may prematurely cement [poor] decisions.

I left the web scraping iterations in their own loop. The time delays are substantial so there is room for improvement using asyncio to run multiple instances trying to handle everything in one loop will make async difficult later on.

This is my first use of selenium so there are definitely lessons for me to learn here.

## setup ##
Runs on python 3.7+

Might run on 3.6. I don't think I used 3.7 specific features.

Make sure chromedriver is installed: https://sites.google.com/a/chromium.org/chromedriver/home and on your system PATH.


### requirements ###
```
# requirements.txt

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
```pip install -r requirements.txt```
