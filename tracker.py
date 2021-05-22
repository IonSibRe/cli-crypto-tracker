import requests
import locale
import os
from sys import platform
from colorama import Fore, Style, init
from currency_converter import CurrencyConverter
from termcolor import colored
from threading import Timer


init() # Init Colorama
c = CurrencyConverter() # Set Currency Rates
clearCounter = 0

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC,ETH,ADA'
parameters = {
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'ecaaf610-3666-4ed7-aad9-247d3cf65a0e',
}

def displayData():
  global clearCounter
  currencies = requests.get(url, params=parameters, headers=headers).json()["data"]

  # Clear Screen
  if (clearCounter == 5):
    os.system("clear") if (platform == "linux" or platform == "darwin") else os.system("CLS")
    clearCounter = 0

  # Symbol, Name, Price, Percent Change 1h, Percent Change 24h, Market Cap + 2 spaces
  print(f"{'Symbol'} | {'Name'.ljust(15)} | {'Price'.ljust(15)} | {'Price in CZK'.ljust(15)} | {'% CHG 1h'.ljust(10)} | {'% CHG 24h'.ljust(10)} | {'Market Cap'}")
  print("------------------------------------------------------------------------------------------------------------")

  for coin, value in currencies.items():
      locale.setlocale(locale.LC_ALL, "") # Set locale to en-US for currency formatting

      symbol = value['symbol']
      name = value['name']
      price = value['quote']['USD']['price']
      percent_change_1h = value['quote']['USD']['percent_change_1h']
      percent_change_24h = value['quote']['USD']['percent_change_24h']
      market_cap = value['quote']['USD']['market_cap']

      symbol = f"{Fore.CYAN}{symbol}{Style.RESET_ALL}"

      price_cz = f"{Fore.GREEN}{str(locale.currency(round(c.convert(price, 'USD', 'CZK'), 2), grouping=True))}{Style.RESET_ALL}"

      locale.setlocale(locale.LC_ALL, "en-US")
      price = f"{Fore.GREEN}{str(locale.currency((round(price, 2)), grouping=True))}{Style.RESET_ALL}"

      percent_change_1h = str(format(percent_change_1h, '.2f'))
      percent_change_1h = f"{Fore.GREEN}{percent_change_1h} %{Style.RESET_ALL}".rjust(16) if float(percent_change_1h) >= 0 else f"{Fore.RED}{percent_change_1h} %{Style.RESET_ALL}" 

      percent_change_24h = str(format(percent_change_24h, '.2f'))
      percent_change_24h = f"{Fore.GREEN}{percent_change_24h} %{Style.RESET_ALL}".rjust(16) if float(percent_change_24h) >= 0 else f"{Fore.RED}{percent_change_24h} %{Style.RESET_ALL}" 

      market_cap = locale.currency(market_cap, grouping=True)

      # color spacing = 8 spaces + 1 for "|"
      print(f"{symbol.ljust(15)} | {name.ljust(15)} | {price.ljust(24)} | {price_cz.ljust(24)} | {percent_change_1h.ljust(19)} | {percent_change_24h.ljust(19)} | {market_cap}")
      
  print("\n")
  clearCounter += 1

  Timer(2, displayData).start()

Timer(2, displayData).start()