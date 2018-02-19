import peewee
from datetime import datetime, timedelta
import config_init
from wallet_models import Transactions

configuration = config_init.config_init

q = (Transactions
     .select(
    Transactions.type_id,
    peewee.fn.sum(Transactions.quantity).alias("sum"),
    peewee.fn.sum(Transactions.quantity * Transactions.unit_price).alias("product"),
    peewee.fn.AvgSalePrice(Transactions.unit_price, Transactions.quantity).alias("avg"))
     .where(Transactions.date > datetime.now() - timedelta(3))
     .group_by(Transactions.type_id)
     .having(peewee.SQL("product") > 100000)
     .order_by(Transactions.type_id)
     )

for i in q:
    print(i.type_id, i.avg, i.sum, i.product)
