import peewee
import config_init
import sys

configuration = config_init.config_init
db = peewee.SqliteDatabase(configuration.get("wallet_database_path"))


class Transactions(peewee.Model):
    transaction_id = peewee.BigIntegerField(unique=True)
    date = peewee.DateTimeField()
    location_id = peewee.IntegerField()
    type_id = peewee.IntegerField()
    unit_price = peewee.DecimalField()
    quantity = peewee.IntegerField()
    client_id = peewee.BigIntegerField()
    is_buy = peewee.BooleanField()
    is_personal = peewee.BooleanField()
    journal_ref_id = peewee.BigIntegerField()

    class Meta:
        database = db

    @db.aggregate()
    class AvgSalePrice(object):
        def __init__(self):
            self.product = 0
            self.quantity = 0
            pass

        def step(self, unit_price, quantity):
            self.product += unit_price * quantity
            self.quantity += quantity

        def finalize(self):
            # print(self.quantity)
            # print(configuration.get("sales_tax"))
            # print(configuration.get("sell_broker_fee"))
            r = self.product / self.quantity * (
                    1.0 - float(configuration.get("sales_tax")) * (1.0 - float(configuration.get("sell_broker_fee"))))
            # print(r)
            r1 = 1.0 - float(configuration.get("sales_tax"))
            # print(r1)
            return r
            # return 1.0
            try:
                return self.product / self.quantity * (
                        1 - configuration.get("sales_tax") * (1 - configuration.get("sell_broker_fee")))

            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

    @staticmethod
    def insert_json(json: list) -> object:
        with db.atomic():
            for data_dict in json:
                Transactions.create(**data_dict)

    @staticmethod
    def get_max_transaction_id() -> int:
        max_transaction_id = 0
        for i in Transactions.select(peewee.fn.MAX(Transactions.transaction_id).alias("max1")):
            max_transaction_id = i.max1
        if max_transaction_id is None:
            max_transaction_id = 0
        return max_transaction_id


"""
        with db.atomic():
            for idx in range(0, len(json), 100):
                Transactions.insert_many(json[idx:idx + 100]).execute()
"""

db.connect()
db.create_tables([Transactions, ])
