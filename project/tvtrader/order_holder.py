from command import Command

# 最多只开1个订单; 已存在订单的情况下：如果是反向订单先平掉才能开新单。如果是通向订单直接跳过什么也不做。

class OrderHolder:

    def __init__(self, robot):
        self.robot = robot
        self.exchange = robot.exchange
        self.command = None
        self.order_id = None

    def on_recieve_command(self, cmd:Command):
        # 如果已有订单，同向：直接返回，反向：就地平掉。
        if self.order_id and self.order_id > 0:
            info = self.exchange.get_order(self.order_id, self.robot.config['symbol'])
            if info['side'] == cmd.side:
                return
            else:
                self.exchange.cancel_order(self.order_id)

        # 如果没有订单，或者反向订单已经平掉，就会走到这里
        order = self.exchange.create_order_by_command(cmd)
        self.order_id = order['id']
        self.command = cmd