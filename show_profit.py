import peewee
from datetime import datetime, timedelta
import config_init
from wallet_models import Transactions, Names

configuration = config_init.config_init


def detailed_profit(days: int) -> list:
    sell_query = (Transactions
                  .select(
        Transactions.type_id,
        peewee.fn.sum(Transactions.quantity).alias("number_sold"),
        peewee.fn.sum(Transactions.quantity * Transactions.unit_price).alias("product"),
        peewee.fn.AvgSalePrice(Transactions.unit_price, Transactions.quantity).alias("avg_sell"))
                  .where((Transactions.date > datetime.now() - timedelta(days)) & ~ Transactions.is_buy)
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
        Names.name,
        peewee.fn.sum(Transactions.quantity * Transactions.unit_price).alias("product"),
        peewee.fn.AvgBuyPrice(Transactions.unit_price, Transactions.quantity).alias("avg_buy"))
                    .join(sq, on=(Transactions.type_id == sq.c.type_id))
                    .join(Names, on=(sq.c.type_id == Names.id))
                    .where((Transactions.date > datetime.now() - timedelta(days)) & Transactions.is_buy)
                    .group_by(Transactions.type_id)
                    .having(peewee.SQL("product") > float(configuration.get("profit_sum_limit")))
                    .order_by(Transactions.type_id)
                    )
    return profit_query
"""
for i in sell_query:
    print("{:>7}".format(i.type_id), "{:>15,.2f}".format(i.avg_sell), "{:>20,.0f}".format(i.number_sold * i.avg_sell))
print("sell")"""


def profit(ii):
    return (ii.transactions.avg_sell - float(ii.avg_buy)) * ii.transactions.number_sold


def print_profit(days: int):
    profit_query = detailed_profit(days)
    profit_query = sorted(profit_query, key=profit, reverse=True)
    sumary_profit = 0
    for i in profit_query:
        # print("{:>7}".format(i.type_id), "{:>15,.2f}".format(i.avg_buy), "{:>15,.2f}".format(i.transactions.avg_sell),
        #      "{:>20,.0f}".format(i.transactions.number_sold), "{:<20}".format(i.transactions.names.name))

        print("{:<50}".format(i.transactions.names.name), "{:>20,.0f}".format(profit(i)/days),
              "{:>10.2%}".format((i.transactions.avg_sell-float(i.avg_buy))/float(i.avg_buy)))
        sumary_profit += profit(i)
    print()
    print("Summary trade profit for last ", days, " days is ", "{:>10,.0f}".format(sumary_profit))
    print()
    print()


if __name__ == "__main__":
    print_profit(10)
    print_profit(30)
