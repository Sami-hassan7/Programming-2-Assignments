class Atom:
    def __init__(self, symbol, atomic_number, neutrons):
        self.symbol = symbol
        self.atomic_number = atomic_number
        self.neutrons = neutrons

class Molecule:
    def __init__(self, atom_pairs):
        self.atom_pairs = atom_pairs

    def __str__(self):
        formula = ''
        for atom, count in self.atom_pairs:
            symbol = atom.symbol
            if count > 1:
                formula += f'{symbol}{count}'
            else:
                formula += symbol
        return formula

    def __add__(self, other):
        if not isinstance(other, Molecule):
            raise ValueError('Only Molecule objects can be added together')

        combined_atom_pairs = self.atom_pairs + other.atom_pairs
        return Molecule(combined_atom_pairs)


class Chloroplast:

    '''
    chloroplast class has two attributes: water and co2 which values are initially set to 0.
    '''
    def __init__(self):
        self.water = 0
        self.co2 = 0

    def add_molecule(self, molecule):

        '''
        This function appends a molecule to the chloroplast. 
        It examines the textual representation of the molecule to identify whether it is water or carbon dioxide. 
        If it's water, it increases the water count; if it's carbon dioxide, it increases the CO2 count. 
        When the total water count reaches 12 and the total CO2 count reaches 6, the process of photosynthesis takes place. 
        It deducts 12 from the water count and 6 from the CO2 count, generating two fresh molecules: sugar and oxygen. 
        The function then provides a list of tuples representing the produced molecules.
        '''

        hydrogen = Atom('H', 1, 1)
        carbon = Atom('C', 6, 6)
        oxygen = Atom('O', 8, 8)
        if str(molecule) == 'H2O':
            self.water += 1
        elif str(molecule) == 'CO2':
            self.co2 += 1
        else:
            raise ValueError('Only H2O and CO2 molecules can be added.')

        if self.co2 == 6 and self.water == 12:
            self.co2 -= 6
            self.water -= 12
            sugar = Molecule([(carbon, 6), (hydrogen, 12), (oxygen, 6)])
            oxygen = Molecule([(oxygen, 6)])
            return [(str(sugar), 1), (str(oxygen), 6)]

        return []

    def __str__(self):
        '''
        This function is designed to create a textual representation of the chloroplast, showing the quantities of water and carbon dioxide molecules.
        '''
        return f'Water molecules: {self.water}, CO2 molecules: {self.co2}'


hydrogen = Atom('H', 1, 1)
carbon = Atom('C', 6, 6)
oxygen = Atom('O', 8, 8)

water = Molecule([(hydrogen, 2), (oxygen, 1)])
co2 = Molecule([(carbon, 1), (oxygen, 2)])

demo = Chloroplast()
els = [water, co2]



while True:
    print('\nWhich molecule would you like to add?')
    print('[1] Water')
    print('[2] Carbon dioxide')
    print('[3] Print chloroplast status')
    print('[4] Quit')
    print('Please enter your choice: ', end='')
    try:
        choice = int(input())
        if choice == 1 or choice == 2:
            res = demo.add_molecule(els[choice - 1])
            if len(res) == 0:
                print(demo)
            else:
                print('\n=== Photosynthesis!')
                print(res)
                print(demo)
        elif choice == 3:
            print(demo)
        elif choice == 4:
            break
        else:
            print('\n=== That is not a valid choice.')

    except ValueError:
        print('\n=== That is not a valid choice.')


