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

    def test_insert_coin_and_print_a_value(self):
        coin = Coin(10, 5)
        with capture(self.vm.insert_coin, coin) as output:
            self.assertEqual('current amount is 0.05\n', output)

    def test_inserting_noncoin_object_throws_proper_exception(self):
        self.assertRaises(InvalidArgumentError, self.vm.insert_coin, 'nickel')


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
