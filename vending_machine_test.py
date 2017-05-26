import unittest
from vending_machine import VendingMachine


class VendingMachineTestCase(unittest.TestCase):
    def setUp(self):
        self.vm = VendingMachine()

    def test_vending_machine_instantiation(self):
        self.assertEqual(0, self.vm.current_amount)


if __name__ == '__main__':
    unittest.main()
