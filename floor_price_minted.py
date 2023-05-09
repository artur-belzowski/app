import requests
import json

def get_floor_price_minted():
    with open('nft_ebisu.json', 'r') as f:
        data = json.load(f)

    suma = 0
    nfts = []

    for nft in data:
        # print(nft['address'])
        body3 = {
            "operationName": "getCollectionAssets",
            "variables": {
                "address": nft['address'],
                "chain": "CRONOS",
                "first": 1,
                "filter": {
                    "chain": "CRONOS",
                    "listingType": None,
                    "priceRange": None,
                    "attributes": None,
                    "rarityRange": None,
                    "nameOrTokenId": None
                },
                "sort": "LOWEST_PRICE"
            },
            "query": "query getCollectionAssets($address: EvmAddress!, $chain: Blockchain!, $first: Int!, $sort: AssetSort!, $after: String, $filter: AssetFilterInput) {\n  collection(address: $address, chain: $chain) {\n    ...CollectionIdentifyFields\n    assets(first: $first, after: $after, filter: $filter, sort: $sort) {\n      totalCount\n      edges {\n        node {\n          ...AssetDetailFields\n          bids(first: 1) {\n            edges {\n              node {\n                ...OrderFields\n                __typename\n              }\n              cursor\n              __typename\n            }\n            pageInfo {\n              ...PageInfoFields\n              __typename\n            }\n            totalCount\n            __typename\n          }\n          __typename\n        }\n        cursor\n        __typename\n      }\n      pageInfo {\n        ...PageInfoFields\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CollectionIdentifyFields on AssetCollection {\n  address\n  name\n  chain {\n    name\n    __typename\n  }\n  status\n  __typename\n}\n\nfragment AssetDetailFields on Asset {\n  name\n  tokenId\n  image {\n    url\n    __typename\n  }\n  animatedImage {\n    url\n    __typename\n  }\n  owner {\n    ...UserFields\n    __typename\n  }\n  ask {\n    ...OrderFields\n    __typename\n  }\n  collection {\n    ...CollectionIdentifyFields\n    __typename\n  }\n  rarityRank\n  __typename\n}\n\nfragment UserFields on UserAccount {\n  evmAddress\n  name\n  avatar {\n    url\n    __typename\n  }\n  nonce\n  __typename\n}\n\nfragment OrderFields on MakerOrder {\n  hash\n  chain\n  isOrderAsk\n  collection\n  tokenId\n  currency\n  strategy\n  startTime\n  endTime\n  minPercentageToAsk\n  nonce\n  price\n  amount\n  status\n  signer\n  encodedParams\n  paramTypes\n  signature\n  __typename\n}\n\nfragment PageInfoFields on PageInfo {\n  hasPreviousPage\n  hasNextPage\n  startCursor\n  endCursor\n  __typename\n}"
        }

        resp = requests.post(url="https://api.minted.network/graphql", json=body3)
        lin = resp.json()
        ask = lin['data']['collection']['assets']['edges'][0]['node']['ask']
        address_collection = ask['collection'] if ask else None
        name = nft['name']
        balance = nft['sztuk']

        if ask:
            if address_collection == nft['address']:
                floor_price_minted = int(ask['price']) / 1000000000000000000
                result = balance * int(floor_price_minted)
                suma += result
        else:
            floor_price_minted = None
        # print(floor_price_minted)

        nft = {
            'name': name,
            'address': address_collection,
            'balance': balance,
            'floor_price': floor_price_minted,
            'result': result if floor_price_minted is not None else None
        }
        nfts.append(nft)
        # print(suma)
        with open('nft_minted.json', 'w') as f:
            json.dump(nfts, f)
