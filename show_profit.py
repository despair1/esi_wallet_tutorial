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
              .where((Transactions.date > datetime.now() - timedelta(3)) & ~ Transactions.is_buy)
              .group_by(Transactions.type_id)
              .having(peewee.SQL("product") > float(configuration.get("profit_sum_limit")))
              .order_by(Transactions.type_id)
              )

profit_query = (Transactions
                .select(
    Transactions.type_id,

    peewee.fn.sum(Transactions.quantity * Transactions.unit_price).alias("product"),
    peewee.fn.AvgBuyPrice(Transactions.unit_price, Transactions.quantity).alias("avg_buy"))
                .where((Transactions.date > datetime.now() - timedelta(3)) & ~ Transactions.is_buy)
                .group_by(Transactions.type_id)
                .having(peewee.SQL("product") > configuration.get("profit_sum_limit"))
                .order_by(Transactions.type_id)
                )

for i in sell_query:
    print("{:>7}".format(i.type_id), "{:>15,.2f}".format(i.avg_sell), "{:>20,.0f}".format(i.number_sold * i.avg_sell))
