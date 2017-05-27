import unittest

from coin import Coin


class CoinTestCase(unittest.TestCase):
    def test_create_a_coin(self):
        coin = Coin(22, 15)
        self.assertEqual(coin.radius, 22)
        self.assertEqual(coin.mass, 15)

    def test_using_zero_radius_throws_error(self):
        with self.assertRaises(ValueError):
            Coin(0, 1)

    def test_using_zero_mass_throws_error(self):
        with self.assertRaises(ValueError):
            Coin(1, 0)

    def test_using_negative_radius_throws_error(self):
        with self.assertRaises(ValueError):
            Coin(-1, 1)

    def test_using_negative_mass_throws_error(self):
        with self.assertRaises(ValueError):
            Coin(1, -1)


if __name__ == '__main__':
    unittest.main()
