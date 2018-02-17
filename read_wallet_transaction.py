import oauth_models
import requests
import wallet_models
import typing
import config_init

configuration = config_init.config_init


def read_wallet_transaction(character_id: int, from_id: int = 0) -> list:
    t = oauth_models.Tokens.get(CharacterID=character_id)
    # url = "https://esi.tech.ccp.is/latest/characters/%s/wallet/journal/" % character_id
    # url = "/v1/characters/%s/wallet/transactions/" % character_id
    host = configuration.get("esi_host")
    path = configuration.get("wallet_transaction_url_path").format(character_id=character_id)
    url = host + path
    params = dict()
    params["datasource"] = "tranquility"
    params["token"] = t.access_token
    if from_id:
        params["from_id"] = from_id
    r = requests.get(url, params=params)
    print("read_wallet_transaction response status code ", r.status_code)
    # print("response text: ", r.text)
    if r.status_code == 200:
        return r.json()
    else:
        print(r.text)
        return []


def test_insert(json):
    wallet_models.Transactions.insert_many(json).execute()


for i in oauth_models.Tokens.select():
    transactions = read_wallet_transaction(i.CharacterID)
    while transactions.__len__() > 0:
        print("loaded ", transactions.__len__(), " transactions")
        print("first transaction: ", transactions[0]["transaction_id"],
              transactions[0]["date"])
        print("last transaction: ", transactions[-1]["transaction_id"],
              transactions[-1]["date"])
        transactions = read_wallet_transaction(i.CharacterID, transactions[-1]["transaction_id"]-1)
    """
    temp_id = 0
    for ii in transactions:
        if not temp_id:
            temp_id = ii["transaction_id"]
            continue
        if temp_id <= ii["transaction_id"]:
            print("warning wrong transactions order")
        temp_id = ii["transaction_id"]
    wallet_models.Transactions.insert_json(json=transactions) """
