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
    coin_radiuses = {
        'nickel': 10.0,
        'dime': 9.0,
        'quarter': 12.0
    }
    coin_masses = {
        'nickel': 5.0,
        'dime': 2.27,
        'quarter': 5.67
    }
    coin_amounts = {
        'nickel': 0.05,
        'dime': 0.10,
        'quarter': 0.25
    }

    def __init__(self):
        self.current_amount = 0

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

        print('current amount is {0:.2f}'.format(self.get_coin_amount(coin)))

    def get_coin_amount(self, coin):
        """
        takes in a coin and returns an integer indicating the amount
        @param coin: a Coin instance
        @return: 0.05 for nickel, 0.10 for dime, 0.25 for quarter, and 0 for anything else
        """
        value_from_radius = 0
        value_from_mass = 0

        for coin_type, radius in VendingMachine.coin_radiuses.items():
            if coin.radius == radius:
                value_from_radius = VendingMachine.coin_amounts[coin_type]

        for coin_type, mass in VendingMachine.coin_masses.items():
            if coin.mass == mass:
                value_from_mass = VendingMachine.coin_amounts[coin_type]

        if value_from_radius == value_from_mass:
            return value_from_radius
        return 0


class InvalidArgumentError(ValueError):
    pass
