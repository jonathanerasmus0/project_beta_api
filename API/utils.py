import requests
from decimal import Decimal, InvalidOperation
from rest_framework.exceptions import APIException

class CurrencyConversionException(APIException):
    status_code = 400
    default_detail = 'Currency conversion failed.'
    default_code = 'currency_conversion_failed'

def convert_currency(amount, from_currency, to_currency):
    api_key = 'cur_live_xq6rcxM9mxOAD0TsRifsOiqnbzpR8CsFt4WCtT9G'  
    url = f"https://api.currencyapi.com/v3/latest?apikey={api_key}&base_currency={from_currency}&currencies={to_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        # Check if the response structure is as expected
        if 'data' not in data or to_currency not in data['data']:
            raise ValueError(f"Unexpected response structure: {data}")
        
        conversion_rate = Decimal(data['data'][to_currency]['value'])
        return amount * conversion_rate
    except requests.exceptions.RequestException as e:
        raise CurrencyConversionException(detail=f"Request failed: {e}")
    except KeyError as e:
        raise CurrencyConversionException(detail=f"Key error in response data: {e}")
    except InvalidOperation as e:
        raise CurrencyConversionException(detail=f"Decimal conversion error: {e}")
    except ValueError as e:
        raise CurrencyConversionException(detail=f"Value error: {e}")

# Example usage
try:
    result = convert_currency(100, 'USD', 'EUR')
    print(f"Converted amount: {result}")
except Exception as e:
    print(f"An error occurred: {e}")
