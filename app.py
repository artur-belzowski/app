from flask import Flask
from flask import render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import session
import requests
import json
from collection import Collection
from get_nft_data import get_nft_data


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'nbiwbfui98523h8we34ty98wt8w#$%@MN$#NBJ^%$#@HBB'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        user = User.query.filter_by(username=username).first()
        if user:
            message = 'Użytkownik o takiej nazwie już istnieje.'
            return render_template('register.html', message=message)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    collections = Collection.get_collections()
    change24 = collections[0].change24
    reward_points = collections[0].reward_points
    floor_price = collections[0].floor_price
    return render_template('index.html', collections=collections, change24=change24, reward_points=reward_points, floor_price=floor_price)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('user_id', None)  # usuwanie sesji
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.session.query(User.id).filter_by(username=username).first()
        if user:
            session['user_id'] = user[0]  # zapisanie ID użytkownika do sesji
            return redirect(url_for('index'))
        else:
            error = 'Nieprawidłowa nazwa użytkownika lub hasło'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


@app.before_request
def before_request():
    if 'user_id' not in session and request.endpoint not in ['login', 'register', 'index', 'collection', 'logout']:
        return redirect(url_for('login'))

@app.route('/wallet')
def wallet():
    return render_template('wallet.html')

@app.route('/ebisus', methods=['POST'])
def ebisus():
    wallet = request.form['wallet']
    session['wallet'] = wallet
    url = requests.get('https://api.ebisusbay.com/walletoverview?pageSize=1000&wallet=' + wallet)
    response = url.json()
    nfts_ebisus = []
    suma = 0
    for erc721 in response['data']['erc721']:
        name = erc721['name']
        address = erc721['address'].strip()
        sztuk = int(erc721['balance'])
        col_url = requests.get(
            'https://api.ebisusbay.com/collectioninfo?pageSize=750&direction=desc&sortBy=totalvolume&search=&page=all')
        col_response = col_url.json()
        fp = None
        for col in (col_response['collections']):
            nazwa = col['address']
            if nazwa == address:
                fp = str(col['stats']['total']['floorPrice'])
                break
        result = sztuk * float(fp) if fp is not None else None
        suma += result if result is not None else 0
        nft_ebisus = {
            'name': name,
            'address': address,
            'sztuk': sztuk,
            'floor_price': fp,
            'result': result
        }
        nfts_ebisus.append(nft_ebisus)
    with open('nft_ebisus.json', 'w') as f:
        json.dump(nfts_ebisus, f)
    return render_template('ebisus.html', wallet=wallet, nfts_ebisus=nfts_ebisus, suma=suma)

@app.route('/minted')
def minted():
    with open('nft_ebisus.json', 'r') as f:
        data = json.load(f)

    suma = 0
    nfts_minted = []

    for nft in data:
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
                result = balance * float(floor_price_minted)
                suma += result
        else:
            floor_price_minted = None

        nft_minted = {
            'name': name,
            'address': address_collection,
            'balance': balance,
            'floor_price': floor_price_minted,
            'result': result if floor_price_minted is not None else None
        }
        nfts_minted.append(nft_minted)
        with open('nft_minted.json', 'w') as f:
            json.dump(nfts_minted, f)
    return render_template('minted.html',  nfts_minted=nfts_minted, suma=suma)

@app.route('/<collection_name>/')
def floor_price(collection_name):
    if collection_name == 'logout':
        return redirect(url_for('logout'))
    elif collection_name == 'ebisus':
        return redirect(url_for('ebisus'))
    else:
        nft_data = get_nft_data(collection_name)
        return render_template('collection.html', collection_name=collection_name, nft_data=nft_data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
