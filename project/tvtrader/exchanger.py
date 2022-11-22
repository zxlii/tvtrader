import ccxt
import math
from command import Command

class Exchanger:
    def __init__(self, robot):
        self.robot = robot
        self.okx = ccxt.okex(robot.config['okx_info'])
        self.okx.proxies = robot.config['proxies']
        self.symbol = robot.config['symbol']
        self.lever = robot.config['lever']
        self.face = robot.config['face']

    def get_balance(self):
        return self.okx.fetch_balance()["free"]["USDT"]

    def get_order(self, order_id):
        return self.okx.fetch_order(order_id, self.symbol)

    def cancel_order(self, order_id):
        self.okx.cancel_order(order_id, self.symbol)

    def create_order_by_command(self, cmd:Command):
        return self.create_order(cmd.side, cmd.cost, cmd.price, cmd.stop, cmd.profit)

    def create_order(self, side, cost, price, stop, profit):

        self.okx.set_leverage(self.lever, self.symbol, {"mgnMode" : "isolated"})

        VAL = self.face     # 面值 合约单张面值
        cost = cost         # 投入的U
        price = price       # 开仓价格
        lever = self.lever       # 杠杆倍数
        amount = 0          # 合约张数

        # 花费计算公式：   cost = VAL * amount * price / lever

        # 先求出理想的浮点张数
        amount = (cost * lever) / (price * VAL)
        # 向下取整为可开张数
        amount = math.floor(amount)
        # 再计算真实花费
        real_cost = VAL * amount * price / lever

        para = {
            'tdMode': 'isolated',
            'slOrdPx': stop,
            'slTriggerPx': stop,
            'tpOrdPx': profit,
            'tpTriggerPx': profit,
            'tpTriggerPxType' : 'last',
            'slTriggerPxType' : 'last'
        }

        order = self.okx.create_limit_order(self.symbol, side, amount, price, para)

        # order = self.okx.create_order(self.symbol, 'LIMIT', side, amount, price, {'tdMode':'isolated'})
        # print(order)

        # inverted_side = 'sell' if side == 'buy' else 'buy'
        #
        # stopLossOrder = self.okx.create_order(self.symbol, 'limit', inverted_side, amount, None, {'tdMode':'isolated','stopLossPrice': stop})
        # print(stopLossOrder)
        #
        # takeProfitOrder = self.okx.create_order(self.symbol, 'limit', inverted_side, amount, None, {'tdMode':'isolated','takeProfitPrice': profit})
        # print(takeProfitOrder)

        print(order)
        print(amount)
        print(real_cost)

        return order