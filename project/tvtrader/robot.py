from command import Command
from exchanger import Exchanger
from order_holder import OrderHolder

class Robot:
    def __init__(self, config):
        self.config = config
        self.exchange = Exchanger(self)
        self.holder = OrderHolder(self)
        self.cmd = Command()

    def on_recieve_command(self, side, item):
        self.cmd.side = side
        self.cmd.cost = self.exchange.get_balance() * 0.5
        self.cmd.price = float(item.price)
        self.cmd.stop = float(item.stop)

        if side == "buy":
            self.cmd.profit = self.cmd.price + (self.cmd.price - self.cmd.stop) * self.config['win_ratio']
        else:
            self.cmd.profit = self.cmd.price - (self.cmd.stop - self.cmd.price) * self.config['win_ratio']

        self.holder.on_recieve_command(self.cmd)

    def on_close_all(self):
        self.holder.on_close_all()

    def on_recieve_command_test(self, side, price, stop):
        self.cmd.side = side
        self.cmd.cost = self.exchange.get_balance() * 0.5
        self.cmd.price = price
        self.cmd.stop = stop

        if side == "buy":
            self.cmd.profit = self.cmd.price + (self.cmd.price - self.cmd.stop) * self.config['win_ratio']
        else:
            self.cmd.profit = self.cmd.price - (self.cmd.stop - self.cmd.price) * self.config['win_ratio']

        self.holder.on_recieve_command(self.cmd)