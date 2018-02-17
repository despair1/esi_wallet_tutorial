import oauth_models
import requests
import wallet_models
import config_init
configuration = config_init.config_init


def test_token(character_id):
    t = oauth_models.Tokens.get(CharacterID=character_id)
    url = "https://esi.tech.ccp.is/latest/characters/%s/wallet/journal/" % character_id
    url = "/v1/characters/%s/wallet/transactions/" % character_id
    url = configuration.get("esi_host") + url
    params = dict()
    params["datasource"] = "tranquility"
    params["token"] = t.access_token
    r = requests.get(url, params=params)
    print("response status code ", r.status_code)
    print("response text: ", r.text)
    return r.json()


def test_insert(json):
    wallet_models.Transactions.insert_many(json).execute()

for i in oauth_models.Tokens.select():
    transactions = test_token(i.CharacterID)
    temp_id = 0
    for ii in transactions:
        if not temp_id:
            temp_id = ii["transaction_id"]
            continue
        if temp_id <= ii["transaction_id"]:
            print("warning wrong transactions order")
        temp_id = ii["transaction_id"]
    wallet_models.Transactions.insert_json(json=transactions)


