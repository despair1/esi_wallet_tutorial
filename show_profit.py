import peewee
from datetime import datetime, timedelta
import config_init
from wallet_models import Transactions

configuration = config_init.config_init

sell_query = (Transactions
              .select(
    Transactions.type_id,
    peewee.fn.sum(Transactions.quantity).alias("number_sold"),
    peewee.fn.sum(Transactions.quantity * Transactions.unit_price).alias("product"),
    peewee.fn.AvgSalePrice(Transactions.unit_price, Transactions.quantity).alias("avg_sell"))
              .where((Transactions.date > datetime.now() - timedelta(10)) & ~ Transactions.is_buy)
              .group_by(Transactions.type_id)
              .having(peewee.SQL("product") > float(configuration.get("profit_sum_limit")))
              .order_by(Transactions.type_id)
              )
sq = sell_query.alias("sq1")

profit_query = (Transactions
                .select(
    Transactions.type_id,
    sq.c.avg_sell,
    sq.c.number_sold,
    peewee.fn.sum(Transactions.quantity * Transactions.unit_price).alias("product"),
    peewee.fn.AvgBuyPrice(Transactions.unit_price, Transactions.quantity).alias("avg_buy"))
                .join(sq, on=(Transactions.type_id == sq.c.type_id))
                .where((Transactions.date > datetime.now() - timedelta(10)) &  Transactions.is_buy)
                .group_by(Transactions.type_id)
                .having(peewee.SQL("product") > float(configuration.get("profit_sum_limit")))
                .order_by(Transactions.type_id)
                )

for i in sell_query:
    print("{:>7}".format(i.type_id), "{:>15,.2f}".format(i.avg_sell), "{:>20,.0f}".format(i.number_sold * i.avg_sell))
print("sell")
for i in profit_query:
    print("{:>7}".format(i.type_id), "{:>15,.2f}".format(i.avg_buy), "{:>15,.2f}".format(i.transactions.avg_sell),
          "{:>20,.0f}".format(i.transactions.number_sold))
