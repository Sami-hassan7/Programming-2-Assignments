class Atom:
    def __init__(self, symbol, atomic_number, neutrons):
        self.symbol = symbol
        self.atomic_number = atomic_number
        self.neutrons = neutrons
    
    def proton_number(self):
        return self.atomic_number
    
    def mass_number(self):
        return self.atomic_number + self.neutrons

    def isotope(self, neutrons):
        self.neutrons = neutrons

    def __eq__(self, other):
        if isinstance(other, Atom) and self.symbol == other.symbol:
            return self.mass_number() == other.mass_number()
        raise TypeError("Can only compare isotopes of the same element")

    def __lt__(self, other):
        if isinstance(other, Atom) and self.symbol == other.symbol:
            return self.mass_number() < other.mass_number()
        raise TypeError("Can only compare isotopes of the same element")

    def __le__(self, other):
        if isinstance(other, Atom) and self.symbol == other.symbol:
            return self.mass_number() <= other.mass_number()
        raise TypeError("Can only compare isotopes of the same element")

    def __gt__(self, other):
        if isinstance(other, Atom) and self.symbol == other.symbol:
            return self.mass_number() > other.mass_number()
        raise TypeError("Can only compare isotopes of the same element")

    def __ge__(self, other):
        if isinstance(other, Atom) and self.symbol == other.symbol:
            return self.mass_number() >= other.mass_number()
        raise TypeError("Can only compare isotopes of the same element")

Hydrogen = Atom("H", 1, 0)
protium = Atom('H', 1, 1)
deuterium = Atom('H', 1, 2)
oxygen = Atom('O', 8, 8)
tritium = Atom('H', 1, 2)

tritium.isotope(3)

assert tritium.neutrons == 3
assert tritium.mass_number() == 4
assert protium < deuterium
assert deuterium <= tritium
assert tritium >= protium

try:
    print(oxygen > tritium)
except TypeError as e:
    print(e)

print(f'The symbol of oxygen is: {oxygen.symbol}')
print(f'Atomic number of oxygen is: {oxygen.atomic_number}')
print(f'Number of neutrons for oxygen is: {oxygen.neutrons}')
print(f'Number of protons in deuterium: {deuterium.proton_number()}')
print(f'Sum of protons and neutrons in deuterium: {deuterium.mass_number()}')
