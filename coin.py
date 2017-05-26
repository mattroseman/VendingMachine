class Coin:
    """
    This data was gotten from https://en.wikipedia.org/wiki/Coins_of_the_United_States_dollar
    approximate coin radius (mm):
    nickel: ~10mm
    dime: ~9mm
    quarter: ~12mm

    approximate coin mass (gr):
    nickel: ~5g
    dime: ~2.27g
    quarter: ~5.67g
    """

    coin_radiuses = {
        'nickel': 10.0,
        'dime': 9.0,
        'quarter': 12.0
    }
    coin_masses = {
        'nickel': 5.0,
        'dime': 2.27,
        'quarter': 5.67
    }

    def __init__(self, radius_mm, mass_grams):
        self.radius = radius_mm
        self.mass = mass_grams
