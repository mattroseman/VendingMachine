from numbers import Number


class Coin:
    """
    Represents a physical coin used as currency
    """
    def __init__(self, radius_mm, mass_grams):
        if not isinstance(radius_mm, Number) or not isinstance(mass_grams, Number):
            raise ValueError('radius_mm and mass_grams arguments must be numbers')
        if radius_mm <= 0 or mass_grams <= 0:
            raise ValueError('radius_mm and mass_grams must be positive numbers')
        self.radius = radius_mm
        self.mass = mass_grams
