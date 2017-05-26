from coin import Coin


class VendingMachine:

    def __init__(self):
        self.current_amount = 0

    def insert_coin(self, coin):
        if not isinstance(coin, Coin):
            raise InvalidArgumentError(('argument coin is of type {}.\nIt must be of type {}').format(type(coin),
                                       type(Coin)))
        print('current amount is {}'.format('0.05'))


class InvalidArgumentError(ValueError):
    pass
