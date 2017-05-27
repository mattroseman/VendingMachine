from io import StringIO
from coin import Coin


class VendingMachine:
    """
    Vending machine can take in certain coins, and increase a users current amount. With this amount a user can buy
    certain items stored in the vending machine
    """

    # This data was gotten from https://en.wikipedia.org/wiki/Coins_of_the_United_States_dollar
    # approximate coin radius (mm):
    # nickel: ~10mm
    # dime: ~9mm
    # quarter: ~12mm

    # approximate coin mass (gr):
    # nickel: ~5g
    # dime: ~2.27g
    # quarter: ~5.67g
    COIN_RADIUSES = {
        'nickel': 10.0,
        'dime': 9.0,
        'quarter': 12.0
    }
    COIN_MASSES = {
        'nickel': 5.0,
        'dime': 2.27,
        'quarter': 5.67
    }
    COIN_AMOUNTS = {
        'nickel': 0.05,
        'dime': 0.10,
        'quarter': 0.25
    }

    def __init__(self):
        self.current_amount = 0
        self.display = StringIO()
        # NOTE for now the return slot is represented as a StringIO, when in reality there is no disply
        self.return_slot = StringIO()
        print('INSERT COIN', file=self.display)

    def insert_coin(self, coin):
        """
        takes the coin and 'inserts' it into the vending machine, and updates the current amount.
        prints the new current amount.
        @param coin: a Coin instance
        @return: nothing
        """
        if not isinstance(coin, Coin):
            raise InvalidArgumentError(('argument coin is of type {}.\nIt must be of type {}').format(type(coin),
                                       type(Coin)))

        coin_amount = self.get_coin_amount(coin)
        if not coin_amount:
            self.send_coin_to_coin_return(coin)
        else:
            self.current_amount += self.get_coin_amount(coin)
        print('current amount is {0:.2f}'.format(self.current_amount), file=self.display)

    def get_coin_amount(self, coin):
        """
        takes in a coin and returns an integer indicating the amount
        @param coin: a Coin instance
        @return: 0.05 for nickel, 0.10 for dime, 0.25 for quarter, and 0 for anything else
        """
        value_from_radius = 0
        value_from_mass = 0

        for coin_type, radius in VendingMachine.COIN_RADIUSES.items():
            if coin.radius == radius:
                value_from_radius = VendingMachine.COIN_AMOUNTS[coin_type]

        for coin_type, mass in VendingMachine.COIN_MASSES.items():
            if coin.mass == mass:
                value_from_mass = VendingMachine.COIN_AMOUNTS[coin_type]

        if value_from_radius == value_from_mass:
            return value_from_radius
        return 0

    def send_coin_to_coin_return(self, coin):
        """
        sends this coin to the coin return
        @param coin: a Coin instance
        @return: nothing
        """
        print('invalid coin (radius: 22mm, mass 15g) returned', file=self.return_slot)


class InvalidArgumentError(ValueError):
    pass
