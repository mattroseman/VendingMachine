import unittest

from vending_machine import VendingMachine
from vending_machine import InvalidArgumentError
from coin import Coin

coin_radiuses = VendingMachine.COIN_RADIUSES
coin_masses = VendingMachine.COIN_MASSES
NICKEL = Coin(coin_radiuses['nickel'], coin_masses['nickel'])
DIME = Coin(coin_radiuses['dime'], coin_masses['dime'])
QUARTER = Coin(coin_radiuses['quarter'], coin_masses['quarter'])


def read_machine_display(vending_machine):
    """
    returns the last line written to the vending machine display
    """
    display = vending_machine.display
    display.seek(0)
    output = display.read()
    output = output.split('\n')
    if len(output) >= 2:
        return output[-2]
    else:
        return ''


def read_return_slot(vending_machine):
    """
    returns the last line written to the vending machine return slot
    """
    slot = vending_machine.return_slot
    slot.seek(0)
    output = slot.read()
    output = output.split('\n')
    if len(output) >= 2:
        return output[-2]
    else:
        return ''


def read_product_slot(vending_machine):
    """
    returns the last line written tot eh vending machine return slot
    """
    slot = vending_machine.product_slot
    slot.seek(0)
    output = slot.read()
    output = output.split('\n')
    if len(output) >= 2:
        return output[-2]
    else:
        return ''


class VendingMachineTestCase(unittest.TestCase):
    def setUp(self):
        self.vm = VendingMachine()


class VendingMachineInsertingCoinsTestCase(VendingMachineTestCase):
    def test_vending_machine_instantiation_starting_amount(self):
        self.assertEqual(self.vm.current_amount, 0)

    def test_insert_coin_and_print_an_amount(self):
        coin = Coin(10, 5)
        self.vm.insert_coin(coin)
        self.assertRegex(read_machine_display(self.vm), '^current amount is \d+\.\d{2}$')

    def test_inserting_noncoin_instance_throws_proper_exception(self):
        self.assertRaises(InvalidArgumentError, self.vm.insert_coin, 'nickel')

    def test_insert_nickel_and_print_correct_amount(self):
        self.vm.insert_coin(NICKEL)
        self.assertEqual(read_machine_display(self.vm), 'current amount is 0.05')

    def test_insert_dime_and_print_correct_amount(self):
        self.vm.insert_coin(DIME)
        self.assertEqual(read_machine_display(self.vm), 'current amount is 0.10')

    def test_insert_quarter_and_print_correct_amount(self):
        self.vm.insert_coin(QUARTER)
        self.assertEqual(read_machine_display(self.vm), 'current amount is 0.25')

    def test_insert_invalid_coin_and_print_zero_amount(self):
        coin = Coin(22, 15)
        self.vm.insert_coin(coin)
        self.assertEqual(read_machine_display(self.vm), 'current amount is 0.00')

    def test_insert_coin_with_mismatched_radius_and_mass_and_print_zero_amount(self):
        for coin_type, radius in coin_radiuses.items():
            for coin_type, mass in coin_masses.items():
                if coin_type == coin_type:
                    break
                self.vm.insert_coin(Coin(radius, mass))
                self.assertEqual(read_machine_display(self.vm), 'current amount is 0.00')

    def test_insert_nickel_and_dime_and_get_correct_amount(self):
        self.vm.insert_coin(NICKEL)
        self.assertEqual(read_machine_display(self.vm), 'current amount is 0.05')

        self.vm.insert_coin(DIME)
        self.assertEqual(read_machine_display(self.vm), 'current amount is 0.15')

    def test_no_coins_inserted_INSERT_COIN_shows(self):
        # recreate the vending machine to reprint the first output
        self.vm = VendingMachine()
        self.assertEqual(read_machine_display(self.vm), 'INSERT COIN')

    def test_invalid_coin_inserted_and_coin_sent_to_return_slot(self):
        coin = Coin(22, 15)
        self.vm.insert_coin(coin)
        self.assertRegex(read_return_slot(self.vm), '^invalid coin \(radius: \d+mm, mass: \d+g\) returned$')

    def test_invalid_coin_inserted_and_correct_coin_sent_to_return_slot(self):
        coin = Coin(22, 15)
        self.vm.insert_coin(coin)
        self.assertEqual(read_return_slot(self.vm), 'invalid coin (radius: 22mm, mass: 15g) returned')
        coin = Coin(1, 1)
        self.vm.insert_coin(coin)
        self.assertEqual(read_return_slot(self.vm), 'invalid coin (radius: 1mm, mass: 1g) returned')


class VendingMachineVendingProductsTestCase(VendingMachineTestCase):
    def test_product_is_dispensed_when_button_pressed(self):
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.press_button('A')
        self.vm.press_button('1')
        self.assertRegex(read_product_slot(self.vm), '^\d+ \w+ products? (has|have) been vended$')

    def test_cola_product_is_dispensed_when_correct_buttons_are_pressed(self):
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.press_button('A')
        self.vm.press_button('1')
        self.assertEqual(read_product_slot(self.vm), '1 cola product has been vended')

    def test_chips_product_is_dispensed_when_correct_buttons_are_pressed(self):
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.press_button('A')
        self.vm.press_button('2')
        self.assertEqual(read_product_slot(self.vm), '1 chips product has been vended')

    def test_candy_product_is_dispensed_when_correct_buttons_are_pressed(self):
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(DIME)
        self.vm.insert_coin(NICKEL)
        self.vm.press_button('A')
        self.vm.press_button('3')
        self.assertEqual(read_product_slot(self.vm), '1 candy product has been vended')

    def test_no_product_is_dispensed_when_incomplete_button_combination_pressed(self):
        self.assertEqual(read_product_slot(self.vm), '')

        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.press_button('A')
        self.assertEqual(read_product_slot(self.vm), '')

    def test_no_product_is_dispensed_when_incorrect_buttons_are_pressed(self):
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.press_button('A')
        self.vm.press_button('4')
        self.assertEqual(read_product_slot(self.vm), '')

    def test_multiple_products_dispensed_consecutively(self):
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.press_button('A')
        self.vm.press_button('1')
        self.assertEqual(read_product_slot(self.vm), '1 cola product has been vended')

        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.press_button('A')
        self.vm.press_button('2')
        self.assertEqual(read_product_slot(self.vm), '1 chips product has been vended')

    def test_product_dispensed_after_incorrect_buttons_are_pressed(self):
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)

        self.vm.press_button('B')
        self.vm.press_button('4')
        self.assertEqual(read_product_slot(self.vm), '')

        self.vm.press_button('A')
        self.vm.press_button('2')
        self.assertEqual(read_product_slot(self.vm), '1 chips product has been vended')

    def test_product_dispensed_after_multiple_incorrect_button_combinations_are_pressed(self):
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)

        self.vm.press_button('B')
        self.vm.press_button('1')
        self.assertEqual(read_product_slot(self.vm), '')

        self.vm.press_button('A')
        self.vm.press_button('5')
        self.assertEqual(read_product_slot(self.vm), '')

        self.vm.press_button('A')
        self.vm.press_button('1')
        self.assertEqual(read_product_slot(self.vm), '1 cola product has been vended')

    def test_product_not_dispensed_if_not_enough_money_inserted(self):
        self.vm.press_button('A')
        self.vm.press_button('2')
        self.assertEqual(read_product_slot(self.vm), '')

    def test_display_shows_current_buttons_pressed_queue(self):
        self.vm.press_button('A')
        self.assertEqual(read_machine_display(self.vm), 'A')

    def test_display_shows_THANK_YOU_when_a_product_is_vended(self):
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.press_button('A')
        self.vm.press_button('1')
        self.assertEqual(read_machine_display(self.vm), 'THANK YOU')

    def test_display_shows_item_price_when_vending_is_attempted_with_not_enough_money(self):
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.press_button('A')
        self.vm.press_button('1')
        self.assertRegex(read_machine_display(self.vm), '^PRICE \d+\.\d{2}$')

    def test_display_shows_correct_item_price_when_vending_is_attempted_with_not_enough_money(self):
        self.vm.press_button('A')
        self.vm.press_button('1')
        self.assertEqual(read_machine_display(self.vm), 'PRICE 1.00')

        self.vm.press_button('A')
        self.vm.press_button('2')
        self.assertEqual(read_machine_display(self.vm), 'PRICE 0.50')

        self.vm.press_button('A')
        self.vm.press_button('3')
        self.assertEqual(read_machine_display(self.vm), 'PRICE 0.65')

    def test_display_shows_current_amount_after_vending_is_attempted_with_not_enough_money(self):
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.press_button('A')
        self.vm.press_button('1')

        self.assertEqual(read_machine_display(self.vm), 'PRICE 1.00')
        self.vm.reset_display()
        self.assertEqual(read_machine_display(self.vm), 'current amount is 0.50')

    def test_display_shows_INSERT_COIN_after_vending_is_attempted_with_not_enough_money(self):
        self.vm.press_button('A')
        self.vm.press_button('1')

        self.assertEqual(read_machine_display(self.vm), 'PRICE 1.00')
        self.vm.reset_display()
        self.assertEqual(read_machine_display(self.vm), 'INSERT COIN')

    def test_display_shows_INSERT_COIN_after_vending_is_successful(self):
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)

        self.vm.press_button('A')
        self.vm.press_button('1')
        self.assertEqual(read_machine_display(self.vm), 'THANK YOU')
        self.vm.reset_display()
        self.assertEqual(read_machine_display(self.vm), 'INSERT COIN')

    def test_display_shows_INSERT_COIN_after_vending_is_successful_and_change_is_left(self):
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)

        self.vm.press_button('A')
        self.vm.press_button('1')
        self.assertEqual(read_machine_display(self.vm), 'THANK YOU')
        self.vm.reset_display()
        self.assertEqual(read_machine_display(self.vm), 'INSERT COIN')

    def test_display_skips_resetting_if_some_other_message_is_printed_before_reset_display_is_called(self):
        # TODO
        pass


class VendingMachineProducingChangeTestCase(VendingMachineTestCase):
    def test_no_change_returned_when_product_value_is_equal_to_current_amount(self):
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)

        self.vm.press_button('A')
        self.vm.press_button('1')
        self.assertEqual(read_return_slot(self.vm), '')

    def test_change_is_produced_when_product_value_is_less_then_current_amount(self):
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)
        self.vm.insert_coin(QUARTER)

        self.vm.press_button('A')
        self.vm.press_button('1')
        self.assertRegex(read_return_slot(self.vm), '^coin \(radius: \d+mm, mass: \d+g\) returned$')


if __name__ == '__main__':
    unittest.main()
