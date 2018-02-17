import peewee
import config_init
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

    @staticmethod
    def insert_json(json):
        with db.atomic():
            for data_dict in json:
                Transactions.create(**data_dict)
                """
        with db.atomic():
            for idx in range(0, len(json), 100):
                Transactions.insert_many(json[idx:idx + 100]).execute()
"""


db.connect()
db.create_tables([Transactions, ])

