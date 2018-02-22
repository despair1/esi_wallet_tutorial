import peewee
import config_init
from wallet_models import Transactions, Names
import requests
configuration = config_init.config_init


def get_blank_ids():
    filled_ids = (Transactions
        .select(Transactions.type_id)
        .join(Names, on=(Transactions.type_id == Names.id))
        .group_by(Transactions.type_id)
        .having(
        peewee.fn.sum(Transactions.quantity * Transactions.unit_price) > float(configuration.get("profit_sum_limit"))))
    all_ids = (Transactions
        .select(Transactions.type_id)
        .join(Names, peewee.JOIN.LEFT_OUTER, on=(Transactions.type_id == Names.id))
        .group_by(Transactions.type_id)
        .having(
        peewee.fn.sum(Transactions.quantity * Transactions.unit_price) > float(configuration.get("profit_sum_limit"))))
    blank_ids = all_ids - filled_ids
    return blank_ids


def load_names(ids):
    host = configuration.get("esi_host")
    path = configuration.get("universe_names_url_path")
    url = host + path
    params = dict()
    params["datasource"] = "tranquility"
    params["user_agent"] = configuration.get("user_agent")
    r = requests.post(url, params=params, json=ids)
    print("status", r.status_code)
    print(r.text)
    if r.status_code == 200:
        return r.json()
    else:
        print(r.text)
        return []


def update_database():
    ids = []
    for i in get_blank_ids():
        ids.append(i.type_id)
        print(i.type_id)
    if ids:
        names = load_names(ids)
        Names.insert_json(names)


if __name__ == "__main__":
    update_database()
