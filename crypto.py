import requests
import time
API_KEY = ""


def getAllAssets():
    url = "http://rest.coinapi.io/v1/assets"

    payload = {}
    headers = {
        'Accept': 'text/plain',
        'X-CoinAPI-Key': API_KEY
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.json())
    data = response.json()
    currencies = []
    for currency in data:
        if currency['type_is_crypto'] == 1:
            currencies.append(
                {"id": currency['asset_id'], "name": currency['name']})
    return currencies


class Currency:
    def __init__(self, id, name, alertValue, sign):
        self.id = id
        self.name = name
        self.values = []
        self.baseValue = self.getExchangeRate(id)
        self.currentValue = self.baseValue
        self.alertValue = float(alertValue)
        self.oldValue = self.baseValue
        self.sign = sign

    def getExchangeRate(self, id, filter='USD'):
        url = "http://rest.coinapi.io/v1/exchangerate/" + \
            id + '?filter_asset_id=' + filter

        payload = {}
        headers = {
            'Accept': 'text/plain',
            'X-CoinAPI-Key': API_KEY
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.json())

        return response.json()['rates'][0]['rate']

    def updateValues(self):
        currentTime = time.time()
        value = self.getExchangeRate(self.id)
        self.values.append({'time': currentTime, 'value': value})
        self.oldValue = self.currentValue
        self.currentValue = value

    def display(self):
        print('---------------------------------------------------------')
        print('history: ')
        for value in self.values:
            print(str(value['time']) + ': ' + str(value['value']))
        print(self.id + ': ' + self.name + ' - ' + str(self.currentValue))
        if self.oldValue > self.currentValue:
            print('↓' * 10)
        elif self.oldValue < self.currentValue:
            print('↑' * 10)
        else:
            print('=' * 10)
        if self.currentValue < self.alertValue:
            print('/!\\' * 10)
            print('ALERT: ' + str(self.currentValue) +
                  ' is below ' + str(self.alertValue))

    def toLine(self):
        return f"[{round(((self.currentValue/self.baseValue)-1)*100, 4)}%] {self.name} {self.sign} {str(self.alertValue)} ({str(self.currentValue)}) {['↓', '↑'][self.oldValue > self.currentValue]}"