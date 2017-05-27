import unittest

from vending_machine import VendingMachine
from vending_machine import InvalidArgumentError
from coin import Coin

coin_radiuses = VendingMachine.COIN_RADIUSES
coin_masses = VendingMachine.COIN_MASSES


def read_machine_display(vending_machine):
    """
    returns the last line written to the vending machine display
    """
    display = vending_machine.display
    display.seek(0)
    output = display.read()
    output = output.split('\n')
    return output[-2]


def read_return_slot(vending_machine):
    """
    returns the last line written to the vending machine return slot
    """
    slot = vending_machine.return_slot
    slot.seek(0)
    output = slot.read()
    output = output.split('\n')
    return output[-2]


class VendingMachineTestCase(unittest.TestCase):
    def setUp(self):
        self.vm = VendingMachine()

    def test_vending_machine_instantiation(self):
        self.assertEqual(0, self.vm.current_amount)

    def test_insert_coin_and_print_an_amount(self):
        coin = Coin(10, 5)
        self.vm.insert_coin(coin)
        self.assertEqual('current amount is 0.05', read_machine_display(self.vm))

    def test_inserting_noncoin_object_throws_proper_exception(self):
        self.assertRaises(InvalidArgumentError, self.vm.insert_coin, 'nickel')

    def test_insert_nickel_and_print_correct_amount(self):
        coin = Coin(coin_radiuses['nickel'], coin_masses['nickel'])
        self.vm.insert_coin(coin)
        self.assertEqual('current amount is 0.05', read_machine_display(self.vm))

    def test_insert_dime_and_print_correct_amount(self):
        coin = Coin(coin_radiuses['dime'], coin_masses['dime'])
        self.vm.insert_coin(coin)
        self.assertEqual('current amount is 0.10', read_machine_display(self.vm))

    def test_insert_quarter_and_print_correct_amount(self):
        coin = Coin(coin_radiuses['quarter'], coin_masses['quarter'])
        self.vm.insert_coin(coin)
        self.assertEqual('current amount is 0.25', read_machine_display(self.vm))

    def test_insert_invalid_coin_and_print_zero_amount(self):
        coin = Coin(22, 15)
        self.vm.insert_coin(coin)
        self.assertEqual('current amount is 0.00', read_machine_display(self.vm))

    def test_insert_coin_with_mismatched_radius_and_mass_and_print_zero_amount(self):
        for coin_type, radius in coin_radiuses.items():
            for coin_type, mass in coin_masses.items():
                if coin_type == coin_type:
                    break
                self.vm.insert_coin(Coin(radius, mass))
                self.assertEqual('current amount is 0.00', read_machine_display(self.vm))

    def test_insert_nickel_and_dime_and_get_correct_amount(self):
        nickel = Coin(coin_radiuses['nickel'], coin_masses['nickel'])
        dime = Coin(coin_radiuses['dime'], coin_masses['dime'])

        self.vm.insert_coin(nickel)
        self.assertEqual('current amount is 0.05', read_machine_display(self.vm))

        self.vm.insert_coin(dime)
        self.assertEqual('current amount is 0.15', read_machine_display(self.vm))

    def test_no_coins_inserted_INSERT_COIN_shows(self):
        # recreate the vending machine to reprint the first output
        self.vm = VendingMachine()
        self.assertEqual('INSERT COIN', read_machine_display(self.vm))

    def test_invalid_coin_inserted_sent_to_return_slot(self):
        coin = Coin(22, 15)
        self.vm.insert_coin(coin)
        self.assertEqual('invalid coin returned', read_return_slot(self.vm))


if __name__ == '__main__':
    unittest.main()
