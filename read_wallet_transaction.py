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


def cleanup_sale_yourself(transactions: list) -> list:
    sale_yourself = []
    last = 999999999999
    for ii in transactions:
        if ii["transaction_id"] > last:
            print("warning wrong transaction order ", ii["transaction_id"])
            return []
        if ii["transaction_id"] == last:
            sale_yourself.append(ii)
            sale_yourself.append(lastii)
        last = ii["transaction_id"]
        lastii = ii
        # print(ii["transaction_id"])
    return [x for x in transactions if x not in sale_yourself]


for i in oauth_models.Tokens.select():
    transactions2database = []
    db_max_transaction_id = wallet_models.Transactions.get_max_transaction_id()
    print("database max transaction: ", db_max_transaction_id)
    transactions = read_wallet_transaction(i.CharacterID)
    while transactions.__len__() > 0:
        print("loaded ", transactions.__len__(), " transactions")
        print("first transaction: ", transactions[0]["transaction_id"],
              transactions[0]["date"])
        print("last transaction: ", transactions[-1]["transaction_id"],
              transactions[-1]["date"])
        if db_max_transaction_id < transactions[-1]["transaction_id"]:
            transactions2database.extend(transactions)
            transactions = read_wallet_transaction(i.CharacterID, transactions[-1]["transaction_id"] - 1)
        else:
            for ii in transactions:
                if ii["transaction_id"] > db_max_transaction_id:
                    transactions2database.append(ii)
                else:
                    break
            transactions = []
    transactions2database = cleanup_sale_yourself(transactions2database)
    wallet_models.Transactions.insert_json(transactions2database)



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
