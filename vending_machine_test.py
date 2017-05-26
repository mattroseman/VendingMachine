import unittest
import sys
from io import StringIO
from contextlib import contextmanager

from vending_machine import VendingMachine
from vending_machine import InvalidArgumentError
from coin import Coin

coin_radiuses = VendingMachine.COIN_RADIUSES
coin_masses = VendingMachine.COIN_MASSES


def read_stdout():
    """
    returns the last line written to stdout
    """
    sys.stdout.seek(0)
    output = sys.stdout.read()
    output = output.split('\n')
    return output[-2]


class VendingMachineTestCase(unittest.TestCase):
    def setUp(self):
        self.out, sys.stdout = sys.stdout, StringIO()
        self.vm = VendingMachine()

    def tearDown(self):
        sys.stdout = self.out

    def test_vending_machine_instantiation(self):
        self.assertEqual(0, self.vm.current_amount)

    def test_insert_coin_and_print_an_amount(self):
        coin = Coin(10, 5)
        self.vm.insert_coin(coin)
        self.assertEqual('current amount is 0.05', read_stdout())

    def test_inserting_noncoin_object_throws_proper_exception(self):
        self.assertRaises(InvalidArgumentError, self.vm.insert_coin, 'nickel')

    def test_insert_nickel_and_print_correct_amount(self):
        coin = Coin(coin_radiuses['nickel'], coin_masses['nickel'])
        self.vm.insert_coin(coin)
        self.assertEqual('current amount is 0.05', read_stdout())

    def test_insert_dime_and_print_correct_amount(self):
        coin = Coin(coin_radiuses['dime'], coin_masses['dime'])
        self.vm.insert_coin(coin)
        self.assertEqual('current amount is 0.10', read_stdout())

    def test_insert_quarter_and_print_correct_amount(self):
        coin = Coin(coin_radiuses['quarter'], coin_masses['quarter'])
        self.vm.insert_coin(coin)
        self.assertEqual('current amount is 0.25', read_stdout())

    def test_insert_invalid_coin_and_print_zero_amount(self):
        coin = Coin(22, 15)
        self.vm.insert_coin(coin)
        self.assertEqual('current amount is 0.00', read_stdout())

    def test_insert_coin_with_mismatched_radius_and_mass_and_print_zero_amount(self):
        for coin_type, radius in coin_radiuses.items():
            for coin_type, mass in coin_masses.items():
                if coin_type == coin_type:
                    break
                self.vm.insert_coin(Coin(radius, mass))
                self.assertEqual('current amount is 0.00', read_stdout())

    def test_insert_nickel_and_dime_and_get_correct_amount(self):
        nickel = Coin(coin_radiuses['nickel'], coin_masses['nickel'])
        dime = Coin(coin_radiuses['dime'], coin_masses['dime'])

        self.vm.insert_coin(nickel)
        self.assertEqual('current amount is 0.05', read_stdout())

        self.vm.insert_coin(dime)
        self.assertEqual('current amount is 0.15', read_stdout())

    def test_no_coins_inserted_show_INSERT_COIN_shows(self):
        # recreate the vending machine to reprint the first output
        self.vm = VendingMachine()
        self.assertEqual('INSERT COIN', read_stdout())


if __name__ == '__main__':
    unittest.main()
