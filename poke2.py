import random

# Define the Pokemon class
class Pokemon:
    def __init__(self, name, poke_type, hp, attack, defense, rarity="common"):
        self.name = name
        self.type = poke_type
        self.max_hp = hp
        self.current_hp = hp
        self.attack = attack
        self.defense = defense
        self.rarity = rarity

    def is_alive(self):
        return self.current_hp > 0

    def take_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)

    def heal(self, amount):
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def view_stats(self):
        print(f"Name: {self.name}")
        print(f"Type: {self.type}")
        print(f"HP: {self.current_hp}/{self.max_hp}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"Rarity: {self.rarity}")

# Define the Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.pokemon = []
        self.items = {'Potion': 5, 'Poke Ball': 3}

    def add_pokemon(self, pokemon):
        self.pokemon.append(pokemon)

    def use_item(self, item, pokemon):
        if item == 'Potion' and self.items[item] > 0:
            pokemon.heal(20)
            self.items[item] -= 1
            print(f"Used Potion on {pokemon.name}. {pokemon.name} now has {pokemon.current_hp} HP.")
        elif item == 'Poke Ball' and self.items[item] > 0:
            self.items[item] -= 1
            return self.try_capture(pokemon)
        else:
            print(f"No {item} left!")

    def try_capture(self, wild_pokemon):
        capture_chance = random.random()
        capture_rate = 0.1 if wild_pokemon.rarity == "legendary" else 0.5
        if capture_chance <= capture_rate:
            self.add_pokemon(wild_pokemon)
            print(f"Captured {wild_pokemon.name}!")
            return True
        else:
            print(f"Failed to capture {wild_pokemon.name}.")
            return False

    def choose_pokemon(self):
        print("Choose a Pokemon:")
        for index, pokemon in enumerate(self.pokemon):
            print(f"{index}: {pokemon.name} (HP: {pokemon.current_hp}/{pokemon.max_hp})")
        choice = int(input("Enter the number of the Pokemon: "))
        if 0 <= choice < len(self.pokemon):
            return self.pokemon[choice]
        else:
            print("Invalid choice. Defaulting to first Pokemon.")
            return self.pokemon[0]

# Define the combat function
def combat(player, wild_pokemon):
    active_pokemon = player.choose_pokemon()
    print(f"A wild {wild_pokemon.name} appeared!")
    
    while active_pokemon.is_alive() and wild_pokemon.is_alive():
        print(f"\n{active_pokemon.name} (HP: {active_pokemon.current_hp}) vs {wild_pokemon.name} (HP: {wild_pokemon.current_hp})")
        action = input("Choose action: (A)ttack, (I)tem, (S)wap, (V)iew Stats: ").lower()

        if action == 'a':
            damage = max(1, active_pokemon.attack - wild_pokemon.defense)
            wild_pokemon.take_damage(damage)
            print(f"{active_pokemon.name} attacked {wild_pokemon.name} for {damage} damage.")
        elif action == 'i':
            item = input("Choose item: (P)otion, (B)all: ").lower()
            if item == 'p':
                player.use_item('Potion', active_pokemon)
            elif item == 'b':
                if player.use_item('Poke Ball', wild_pokemon):
                    return
        elif action == 's':
            active_pokemon = player.choose_pokemon()
            print(f"Swapped to {active_pokemon.name}.")
            continue
        elif action == 'v':
            active_pokemon.view_stats()
            continue
        
        if wild_pokemon.is_alive():
            wild_damage = max(1, wild_pokemon.attack - active_pokemon.defense)
            active_pokemon.take_damage(wild_damage)
            print(f"{wild_pokemon.name} attacked {active_pokemon.name} for {wild_damage} damage.")

    if not active_pokemon.is_alive():
        print(f"{active_pokemon.name} fainted!")
    if not wild_pokemon.is_alive():
        print(f"{wild_pokemon.name} fainted! Battle over.")

# Function to create a random encounter
def random_encounter():
    pokemon_list = [
        Pokemon("Charmander", "Fire", 39, 52, 43, "common"),
        Pokemon("Bulbasaur", "Grass", 45, 49, 49, "common"),
        Pokemon("Squirtle", "Water", 44, 48, 65, "common"),
        Pokemon("Mewtwo", "Psychic", 106, 110, 90, "legendary")
    ]
    return random.choice(pokemon_list)

# Example usage
if __name__ == "__main__":
    # Create player and their Pokemon
    player = Player("Ash")
    pikachu = Pokemon("Pikachu", "Electric", 35, 55, 40, "common")
    jigglypuff = Pokemon("Jigglypuff", "Fairy", 35, 55, 40, "common")
    player.add_pokemon(pikachu)
    player.add_pokemon(jigglypuff)
    
    # Start game loop with random encounters
    while True:
        wild_pokemon = random_encounter()
        combat(player, wild_pokemon)
        if input("Continue with another encounter? (y/n): ").lower() != 'y':
            break
