import unittest
import sys
from io import StringIO
from contextlib import contextmanager

from vending_machine import VendingMachine
from vending_machine import InvalidArgumentError
from coin import Coin


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
        coin = Coin(VendingMachine.coin_radiuses['nickel'], VendingMachine.coin_masses['nickel'])
        with capture(self.vm.insert_coin, coin) as output:
            self.assertEqual('current amount is 0.05\n', output)

    def test_insert_dime_and_print_correct_amount(self):
        coin = Coin(VendingMachine.coin_radiuses['dime'], VendingMachine.coin_masses['dime'])
        with capture(self.vm.insert_coin, coin) as output:
            self.assertEqual('current amount is 0.10\n', output)

    def test_insert_quarter_and_print_correct_amount(self):
        coin = Coin(VendingMachine.coin_radiuses['quarter'], VendingMachine.coin_masses['quarter'])
        with capture(self.vm.insert_coin, coin) as output:
            self.assertEqual('current amount is 0.25\n', output)

    def test_insert_invalid_coin_and_print_zero_amount(self):
        coin = Coin(22, 15)
        with capture(self.vm.insert_coin, coin) as output:
            self.assertEqual('current amount is 0.00\n', output)

    def test_insert_coin_with_mismatched_radius_and_mass_and_print_zero_amount(self):
        for coin_type, radius in VendingMachine.coin_radiuses.items():
            for coin_type, mass in VendingMachine.coin_masses.items():
                if coin_type == coin_type:
                    break
                coin = Coin(radius, mass)
                with capture(self.vm.insert_coin, coin) as output:
                    self.assertEqual('current amount is 0.00\n', output)


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
