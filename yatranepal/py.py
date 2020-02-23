from geolite2 import geolite2
import requests
my_ip = requests.get('https://api.ipify.org').text
reader = geolite2.reader()
location = reader.get(my_ip)


print(location)
print(my_ip)
