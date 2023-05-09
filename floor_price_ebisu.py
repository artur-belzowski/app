import requests

def get_floor_price_ebisu(address):
    url = requests.get('https://api.ebisusbay.com/collectioninfo?pageSize=750&direction=desc&sortBy=totalvolume&search=&page=all')
    response = url.json()
    for col in (response['collections']):
        nazwa = col['address']
        if nazwa == address:
            floor_price_ebisu = str(col['stats']['total']['floorPrice'])
            return floor_price_ebisu
