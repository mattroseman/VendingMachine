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

    PRODUCT_NUMBERS = {
        'A1': 'cola',
        'A2': 'chips',
        'A3': 'candy'
    }
    PRODUCT_AMOUNTS = {
        'cola': 1.00,
        'chips': 0.50,
        'candy': 0.65
    }

    def __init__(self):
        self.current_amount = 0
        self.display = StringIO()
        # NOTE for now varius outputs of the vending machine are represented as StringIO's for testing purposes
        # in reality these would be functions that cause physical mechanisms to trigger
        self.return_slot = StringIO()
        self.product_slot = StringIO()

        self.buttons_pressed = ""

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
        print('invalid coin (radius: {}mm, mass: {}g) returned'.format(coin.radius, coin.mass), file=self.return_slot)

    def press_button(self, button):
        """
        simulates a button being pressed on the vending machine
        @param button: a char representing a button that was pressed [A-Z,0-9]
        @return: nothing
        """
        self.buttons_pressed += button
        print(self.buttons_pressed, file=self.display)
        if len(self.buttons_pressed) == 1:
            return
        if self.buttons_pressed in self.PRODUCT_NUMBERS:
            vended_product = self.PRODUCT_NUMBERS[self.buttons_pressed]
            # if a combination of buttons have been pressed that match a certain product
            # vend it and clear the buttons pressed queue
            product_price = self.PRODUCT_AMOUNTS[vended_product]
            if self.current_amount >= product_price:
                print('1 {} product has been vended'.format(vended_product), file=self.product_slot)
                print('THANK YOU', file=self.display)
            else:
                print('PRICE {0:.2f}'.format(product_price), file=self.display)
        self.buttons_pressed = ""


class InvalidArgumentError(ValueError):
    pass
