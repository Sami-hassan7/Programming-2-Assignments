class Molecule:
    '''
    This class denotes a molecule, which is an electrically neutral assembly of two or more atoms.
    '''
    def __init__(self, pairs):
        '''
        The initialization function creates a Molecule object using a list of atom pairs. 
        Each atom pair is comprised of an Atom object and the quantity of atoms of that specific type within the molecule.
        '''
        self.pairs = pairs

    def __str__(self):
        '''
        This function provides a textual portrayal of the molecule. 
        It loops through the atom pairs and builds a chemical formula by combining atom symbols with their corresponding quantities. 
        When the count is 1, the number is excluded from the formula.
        '''
        formula = ""
        for atom, count in self.pairs:
            symbol = atom.symbol
            if count > 1:
                formula += f"{symbol}{count}"
            else:
                formula += symbol
        return formula

    def __add__(self, other):
        '''
         The addition operator method allows combining two Molecule objects by adding their atom pairs. 
         It checks if the other object is an instance of the Molecule class, raises a TypeError otherwise. 
         This method then creates a new list of atom pairs by concatenating the atom pairs of both molecules and returns a new Molecule instance with the combined pairs.
        '''
        if not isinstance(other, Molecule):
            raise TypeError("Can only add two Molecule objects")

        combined_pairs = self.pairs + other.pairs
        return Molecule(combined_pairs)


class Atom:

    """
    The Atom class represents an atom with a symbol, atomic number, and number of neutrons.
    Proton_number and mass_number methods that can return the atomic number and the sum of the atomic number and neutrons, respectively.

    """

    def __init__(self, symbol, atomic_number, neutrons):
        self.symbol = symbol
        self.atomic_number = atomic_number
        self.neutrons = neutrons

    def proton_number(self):
        return self.atomic_number

    def mass_number(self):
        return self.atomic_number + self.neutrons
    

hydrogen = Atom('H', 1, 1)
carbon = Atom('C', 6, 6)
oxygen = Atom('O', 8, 8)

water = Molecule([(hydrogen, 2), (oxygen, 1)])
co2 = Molecule([(carbon, 1), (oxygen, 2)])

print(water)         
print(co2)            
print(water + co2)  

