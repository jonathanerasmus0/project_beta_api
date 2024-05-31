import requests
from decimal import Decimal

def convert_currency(amount, from_currency, to_currency):
    api_key = 'cur_live_xq6rcxM9mxOAD0TsRifsOiqnbzpR8CsFt4WCtT9G'  
    url = f"https://api.currencyapi.com/v3/latest?apikey={api_key}&base_currency={from_currency}&currencies={to_currency}"
    response = requests.get(url)
    response.raise_for_status()  
    data = response.json()
    conversion_rate = Decimal(data['data'][to_currency]['value'])
    return amount * conversion_rate
