import unittest
import sys
from io import StringIO
from contextlib import contextmanager

from vending_machine import VendingMachine
from vending_machine import InvalidArgumentError
from coin import Coin

coin_radiuses = VendingMachine.COIN_RADIUSES
coin_masses = VendingMachine.COIN_MASSES


class VendingMachineTestCase(unittest.TestCase):
    def setUp(self):
        self.vm = VendingMachine()

    def test_vending_machine_instantiation(self):
        self.assertEqual(0, self.vm.current_amount)

    def test_insert_coin_and_print_an_amount(self):
        coin = Coin(10, 5)
        with capture(self.vm.insert_coin, coin) as output:
            self.assertEqual('current amount is 0.05\n', output)

    def test_inserting_noncoin_object_throws_proper_exception(self):
        self.assertRaises(InvalidArgumentError, self.vm.insert_coin, 'nickel')

    def test_insert_nickel_and_print_correct_amount(self):
        coin = Coin(coin_radiuses['nickel'], coin_masses['nickel'])
        with capture(self.vm.insert_coin, coin) as output:
            self.assertEqual('current amount is 0.05\n', output)

    def test_insert_dime_and_print_correct_amount(self):
        coin = Coin(coin_radiuses['dime'], coin_masses['dime'])
        with capture(self.vm.insert_coin, coin) as output:
            self.assertEqual('current amount is 0.10\n', output)

    def test_insert_quarter_and_print_correct_amount(self):
        coin = Coin(coin_radiuses['quarter'], coin_masses['quarter'])
        with capture(self.vm.insert_coin, coin) as output:
            self.assertEqual('current amount is 0.25\n', output)

    def test_insert_invalid_coin_and_print_zero_amount(self):
        coin = Coin(22, 15)
        with capture(self.vm.insert_coin, coin) as output:
            self.assertEqual('current amount is 0.00\n', output)

    def test_insert_coin_with_mismatched_radius_and_mass_and_print_zero_amount(self):
        for coin_type, radius in coin_radiuses.items():
            for coin_type, mass in coin_masses.items():
                if coin_type == coin_type:
                    break
                coin = Coin(radius, mass)
                with capture(self.vm.insert_coin, coin) as output:
                    self.assertEqual('current amount is 0.00\n', output)

    def test_insert_nickel_and_dime_and_get_correct_amount(self):
        nickel = Coin(coin_radiuses['nickel'], coin_masses['nickel'])
        dime = Coin(coin_radiuses['dime'], coin_masses['dime'])
        with capture(self.vm.insert_coin, nickel) as output:
            self.assertEqual('current amount is 0.05\n', output)
        with capture(self.vm.insert_coin, dime) as output:
            self.assertEqual('current amount is 0.15\n', output)


@contextmanager
def capture(command, *args, **kwargs):
    out, sys.stdout = sys.stdout, StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        yield sys.stdout.read()
    finally:
        sys.stdout = out


if __name__ == '__main__':
    unittest.main()
