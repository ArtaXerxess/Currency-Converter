import requests, json, dotenv

with open("metadata/CurrencyNames.json",'r',encoding='utf-8') as f:
    curr_names = json.load(fp=f)
    f.close()


class API:

    __KEY = dotenv.dotenv_values(".env")["KEY"]
    """private api key"""

    def __init__(self, base):
        """init method, new api request for every new call"""
        self.base = base
        self.url = f"https://v6.exchangerate-api.com/v6/{self.__KEY}/latest/{self.base}"
        print(
            f"Sending request to ExchangeRate-API to fetch latest exchange rates for {base}"
        )
        self.fetch()

    def fetch(self):
        """Make the API request"""
        response = requests.get(url=self.url)
        self.data = response.json()

    def getRates(self):
        """Return the JSON object"""
        if self.data["result"] == "success":
            return self.data["conversion_rates"]
        else:
            print("Something went wrong...")
            return None
    
    def getUpdateTimeStats(self):
        if self.data['result']=="success":
            return f'Time of Last Update UTC 👉 {self.data['time_last_update_utc']} and Time of next Update UTC will be 👉 {self.data['time_next_update_utc']}'
        else:
            return "something went wrong, can\'t return stats..."

    def show(self):
        """Formatted print of the API response"""
        self.datadump = json.dumps(obj=self.data, indent=4, sort_keys=True)
        print(self.datadump)
    
    def getTable(self):
        """Return a table of currency name and conversion factor"""
        combined = {}
        data = self.getRates()
        for key in curr_names.keys():
            if key in data:
                combined[key] = [f'{curr_names[key]['name']}',float(data[key])]
        return combined


    def download(self):
        """Download/store the exchange rates in .json file"""
        with open(f"downloads/{self.base}ConvRates.json", "w", encoding="utf-8") as f:
            json.dump(obj=self.data, fp=f, indent=4, sort_keys=True)


if __name__ == "__main__":
    api = API(base="USD")



