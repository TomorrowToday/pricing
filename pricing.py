import os.path
import pickle
import string
import time

from bs4 import BeautifulSoup
from googleapiclient.discovery import build as build_service
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

CART_URL = 'http://shoppingcart-staging.avoxi.io'
PRICE_SHEET_ID = '1zNV1vOgodBGCa7-vJTNwWILFDRBTT01Osr-CdO5Ct_Y'
SHEET_RANGE = 'ITFS Packages!A2:H'

class PriceSheet():
    def __init__(self, id, range):
        api_scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        credentials = self.build_credentials(api_scopes=api_scopes)
        google_api_service = build_service(
            'sheets', 'v4', credentials=credentials)
        sheet_access = google_api_service.spreadsheets()
        sheet = sheet_access.values().get(spreadsheetId=id, range=range).execute()

        self._values = {}
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
        if self._values:
            return self._values

        self._values = {}
        for row in self.raw_values:
            code, country, number_type, plan, mrc, included_minutes, added_minutes, _ = row
            country = string.capwords(country)
            if country not in self._values:
                self._values[country] = {}
            self._values[country][plan.split()[1].lower()] = {
                'mrc': mrc,
                'included_minutes': included_minutes,
                'added_minutes': added_minutes
            }
        return self._values


class CartScraper():
    '''
    Web scraping just for an avoxi cart.
    '''

    def __init__(self, url):
        '''

        '''
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self._driver = webdriver.Chrome(chrome_options=chrome_options)
        self._driver.get(url)

        time.sleep(2)  # wait for form to load

        self.country_options = Select(self._driver.find_element_by_name('country'))
        self.forward_options = Select(self._driver.find_element_by_name('userCountry'))
        self.type_options = Select(self._driver.find_element_by_name('numberType'))

    def scrape_country_plans(
            self,
            country,
            forward='VoIP/SIP/Softphone',
            number_type_index=0):
        '''
        Scrape the cart plans by first setting the country and forwarding
        '''
        self.country_options.select_by_value(country)
        self.type_options.select_by_index(number_type_index)
        self.forward_options.select_by_value(forward)

        time.sleep(2)  # wait for new prices to load

        page = self._driver.execute_script(
            "return document.documentElement.outerHTML")
        soup = BeautifulSoup(page, features='html.parser')
        price_options = soup.find_all('div', {'class': 'a4jPqxiquQKU7Gps8sGb'})

        plans = {}
        for option in price_options[:6]:
            plan = option.find('div',
                               {'class': '_2tWbNTe38p5RG2fxbXUY-Y'}).text
            mrc = option.find('div', {'class': 'dLIpmj8etT1Qi6XOPThm6'}).text
            included_minutes = option.find(
                'div', {'class': 'VWds6YAFGXmeGTAXTEB8b'}).text
            added_minutes = option.find(
                'div', {'class': '_2lqwLdOto5DKzOnceK9XXJ'}).text

            if not plan or not added_minutes or not included_minutes or not mrc:
                print(f"{plan}, {mrc}, {included_minutes}, {added_minutes}")
                raise AttributeError('A cart value was not scraped')

            # format cart option data
            plans[plan.lower()] = {
                'mrc': mrc.split()[0][1:],
                'included_minutes': included_minutes,
                'added_minutes': added_minutes.split()[0][1:],
            }

        return plans

    def close(self):

        self._driver.quit()


def diff_plans(standard, testing):
    for plan, values in standard.items():
        if plan not in testing:
            yield f"{plan} is missing"

        for metric, value in values.items():
            if testing[plan][metric] != value:
                yield (f"There's a mismatch on {plan}, {metric}. "
                       f"Expected: {value}, read {testing[plan][metric]}")


def main():
    price_sheet = PriceSheet(id=PRICE_SHEET_ID, range=SHEET_RANGE).to_dict()
    scraper = CartScraper(CART_URL)

    diffs = []
    for country, sheet_plans in price_sheet.items():
        cart_plans = scraper.scrape_country_plans(country)
        diff_items = list(diff_plans(sheet_plans, cart_plans))
        if diff_items:
            diffs.append((country, diff_items))

    scraper.close()

    # display/report differences between price sheet and cart
    if not diffs:
        print('No diffs between price sheet and carts')
    else:
        print('The following differences were found:')
        for country, diff in diffs:
            print(f'{country}:')
            for item in diff:
                print(f'\t{item}')

            print('\n')


if __name__ == '__main__':
    main()
