import os.path
import pickle
import requests
import time

from bs4 import BeautifulSoup
from googleapiclient.discovery import build as build_service
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from selenium import webdriver
from selenium.webdriver.support.ui import Select


class PriceSheet():
    def __init__(self, id, range):
        api_scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        credentials = self.build_credentials(api_scopes=api_scopes)
        google_api_service = build_service('sheets', 'v4', credentials=credentials)
        sheet_access = google_api_service.spreadsheets()
        sheet = sheet_access.values().get(spreadsheetId=id, range=range).execute()

        self.raw_values = sheet.get('values', [])

    def build_credentials(self, api_scopes=''):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('google_token.pickle'):
            with open('google_token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'google_credentials.json', api_scopes)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('google_token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return creds


    def to_dict(self):
        pass





def main():

    # get price sheet data
    # price_sheet = PriceSheet(id='1r0NmNwXggOne5J5voI4gLSZ2UBglEo-D3FRv6FI3b_M', range='Sheet1!A2:H').raw_values


    # format price sheet data


    # connect to cart
    driver = webdriver.Chrome()
    driver.get('http://shoppingcart-staging.avoxi.io')
    time.sleep(5)
    country = Select(driver.find_element_by_name('country'))
    forward = Select(driver.find_element_by_name('userCountry'))

    country.select_by_value('Anguilla')
    forward.select_by_value('VoIP/SIP/Softphone')
    
    time.sleep(5)

    # for country in price sheet

        # get cart for country

        # for option in cart

            # format cart option data


    # find differences between price sheet and cart

    # display/report differnces between price sheet and cart

if __name__ == '__main__':
    main()
