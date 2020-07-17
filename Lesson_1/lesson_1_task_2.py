
import requests
from pprint import pprint
import json

client_id = '5cf3e8edd0964349aeebcb627c23859'
client_secret = '**********************'

def create_access_token(client_id, client_secret, region = 'us'):
    data = { 'grant_type': 'client_credentials' }
    response = requests.post('https://us.battle.net/oauth/token', data=data, auth=(client_id, client_secret))
    return response.json()


#token = create_access_token(client_id, client_secret)


main_link = 'https://us.api.blizzard.com/data/wow/achievement-category/index'
add_link = "?namespace=static-us&locale=en_US&access_token=EUteEv4xPSdMffRNavaf53MF5vQ3nmAOTU"
url = main_link+add_link

response = requests.get(url)
data = response.json()

pprint(data)

with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)