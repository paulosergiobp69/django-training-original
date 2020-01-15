import requests
import json

class TestRequest():

    def get_rates(self, basecurrency='USD'):
        url = 'https://api.exchangeratesapi.io/latest?base=%s' % basecurrency
        print(url)
        response = requests.get(url)
        return json.loads(response.text)


if __name__ == '__main__':
    test_request = TestRequest()
    exchange_dict  = test_request.get_rates()
    print(exchange_dict['rates'])
    for rate, value in exchange_dict['rates']:
        print(rate, value)
