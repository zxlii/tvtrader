import math

import requests

import okx.Account_api as Account
import okx.Funding_api as Funding
import okx.Market_api as Market
import okx.Public_api as Public
import okx.Trade_api as Trade
import okx.status_api as Status
import okx.subAccount_api as SubAccount
import okx.TradingData_api as TradingData
import okx.Broker_api as Broker
import okx.Convert_api as Convert
import okx.FDBroker_api as FDBroker
import okx.Rfq_api as Rfq
import okx.TradingBot_api as TradingBot
import okx.Finance_api as Finance

from command import Command


class ExchangeOKX:
    def __init__(self, robot):
        self.robot = robot
        self.accountAPI = None
        self.fundingAPI = None
        self.convertAPI = None
        self.marketAPI = None
        self.publicAPI = None
        self.tradingDataAPI = None
        self.tradeAPI = None
        self.subAccountAPI = None
        self.BrokerAPI = None
        self.FDBrokerAPI = None

        self.symbol = robot.config['symbol']
        self.lever = robot.config['lever']
        self.face = robot.config['face']

        self.init()

    def init(self):
        requests.proxies = self.robot.config['proxies']
        api_key = self.robot.config['apiKey']
        secret_key = self.robot.config['secret']
        passphrase = self.robot.config['password']

        flag = '0'  # 0实盘 1模拟盘

        self.accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
        self.fundingAPI = Funding.FundingAPI(api_key, secret_key, passphrase, False, flag)
        self.convertAPI = Convert.ConvertAPI(api_key, secret_key, passphrase, False, flag)
        self.marketAPI = Market.MarketAPI(api_key, secret_key, passphrase, True, flag)
        self.publicAPI = Public.PublicAPI(api_key, secret_key, passphrase, False, flag)
        self.tradingDataAPI = TradingData.TradingDataAPI(api_key, secret_key, passphrase, False, flag)
        self.tradeAPI = Trade.TradeAPI(api_key, secret_key, passphrase, False, flag)
        self.subAccountAPI = SubAccount.SubAccountAPI(api_key, secret_key, passphrase, False, flag)
        self.BrokerAPI = Broker.BrokerAPI(api_key, secret_key, passphrase, False, flag)
        self.FDBrokerAPI = FDBroker.FDBrokerAPI(api_key, secret_key, passphrase, False, flag)

        # result = self.accountAPI.get_position_risk('SWAP')
        # print(result)

        # result = self.accountAPI.get_account('BTC')

        # result = self.publicAPI.get_interest_loan()
        # print(result)

    # result = publicAPI.get_funding_rate('BTC-USD-SWAP')

    def get_balance(self):
        r = self.accountAPI.get_account('USDT')
        return r['data'][0]['details'][0]['availEq']

    def get_order(self, order_id):
        return self.tradeAPI.get_orders(self.symbol, order_id)[0]

    def cancel_order(self, order_id):
        self.tradeAPI.close_positions(self.symbol, 'isolated')

    def create_order_by_command(self, cmd: Command):
        self.create_order(cmd.side, cmd.cost, cmd.price, cmd.stop, cmd.profit)

    def create_order(self, side, cost, price, stop, profit):

        self.accountAPI.set_leverage(instId=self.symbol, lever=str(self.lever), mgnMode='isolated')

        # self.okx.set_leverage(self.lever, self.symbol, {"mgnMode": "isolated"})

        VAL = self.face  # 面值 合约单张面值
        cost = cost  # 投入的U
        price = price  # 开仓价格
        lever = self.lever  # 杠杆倍数
        amount = 0  # 合约张数

        # 花费计算公式：   cost = VAL * amount * price / lever

        # 先求出理想的浮点张数
        amount = (cost * lever) / (price * VAL)
        # 向下取整为可开张数
        amount = math.floor(amount)
        # 再计算真实花费
        real_cost = VAL * amount * price / lever

        posSide = "long" if side == "buy" else "short"

        self.tradeAPI.place_algo_order(
            instId = self.symbol,
            tdMode = 'isolated',
            side = side,
            sz = str(amount),
            posSide = posSide,
            ordType = 'conditional',
            triggerPx = str(price),
            orderPx = str(price),
            slTriggerPx = str(stop),
            slOrdPx = str(stop),
            tpTriggerPx = str(profit),
            tpOrdPx = str(profit)
        )

        result = self.tradeAPI.place_multiple_orders([
            {
                'instId': self.symbol,
                'tdMode': 'isolated',
                'side': side,
                'ordType': 'limit',
                'sz': str(amount),
                'px': str(price),
                'posSide': posSide,
                'clOrdId': '',
                'tag': '',
                'tgtCcy':''
            },
            {
                'instId': self.symbol,
                'tdMode': 'isolated',
                'side': side,
                'ordType': 'limit',
                'sz': str(amount),
                'px': str(price),
                'posSide': posSide,
                'clOrdId': '',
                'tag': '',
                'tgtCcy':''
            }
        ])



