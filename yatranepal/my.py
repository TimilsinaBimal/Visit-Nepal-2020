import datetime
import json
import requests
date = datetime.date.today()
year = f"{date.year}"
month = f"{date:%m}"
day = f"{date:%d}"
my_url = f"https://www.nrb.org.np/exportForexJSON.php?YY={year}&MM={month}&DD={day}"
currencies = json.loads(requests.get(my_url).text)
my_list = currencies["Conversion"]["Currency"]
BaseCurrency = [i["BaseCurrency"] for i in my_list]
BaseValue = [i["BaseValue"] for i in my_list]
TargetSell = [i["TargetSell"] for i in my_list]
print(BaseCurrency, BaseValue, TargetSell)
