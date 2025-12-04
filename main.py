import random
import json
import os

# -----------------------------
# Player Class
# -----------------------------
class Player:
    def __init__(self, name, pclass):
        self.name = name
        self.pclass = pclass
        self.level = 1
        self.xp = 0
        self.gold = 50
        self.max_hp = 100
        self.hp = self.max_hp
        self.attack = 10
        self.defense = 5
        self.inventory = {"Potion": 3}
        self.skills = self.init_skills()
        self.location = "Town"

    def init_skills(self):
        if self.pclass == "Warrior":
            return {"Slash": 15, "Power Strike": 25}
        elif self.pclass == "Mage":
            return {"Fireball": 20, "Ice Spike": 25}
        elif self.pclass == "Rogue":
            return {"Backstab": 25, "Poison Dart": 15}
        else:
            return {"Punch": 10}

    def level_up(self):
        while self.xp >= self.level * 50:
            self.xp -= self.level * 50
            self.level += 1
            self.max_hp += 20
            self.hp = self.max_hp
            self.attack += 5
            self.defense += 2
            print(f"\n*** {self.name} leveled up to {self.level}! ***\n")

    def use_item(self, item_name):
        if item_name in self.inventory and self.inventory[item_name] > 0:
            if item_name == "Potion":
                heal = random.randint(20, 40)
                self.hp = min(self.max_hp, self.hp + heal)
                print(f"{self.name} used a Potion and healed {heal} HP!")
            self.inventory[item_name] -= 1
        else:
            print(f"No {item_name} left!")

# -----------------------------
# Enemy Class
# -----------------------------
class Enemy:
    def __init__(self, name, hp, attack, xp_reward, gold_reward):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward

# -----------------------------
# Combat System
# -----------------------------
def battle(player, enemy):
    print(f"\nA wild {enemy.name} appears!")
    while enemy.hp > 0 and player.hp > 0:
        print(f"\n{player.name} HP: {player.hp}/{player.max_hp} | {enemy.name} HP: {enemy.hp}")
        action = input("Choose action: (A)ttack, (S)kill, (I)tem, (R)un: ").lower()
        
        if action == "a":
            damage = max(0, random.randint(player.attack-5, player.attack+5) - random.randint(0, enemy.attack//3))
            enemy.hp -= damage
            print(f"You attacked {enemy.name} for {damage} damage!")
        
        elif action == "s":
            print("Skills:")
            for i, skill in enumerate(player.skills, 1):
                print(f"{i}. {skill} ({player.skills[skill]} dmg)")
            choice = input("Choose skill number: ")
            try:
                skill_name = list(player.skills.keys())[int(choice)-1]
                damage = player.skills[skill_name] + random.randint(-3,3)
                enemy.hp -= damage
                print(f"You used {skill_name} and dealt {damage} damage!")
            except:
                print("Invalid skill!")

        elif action == "i":
            print("Inventory:", player.inventory)
            item_choice = input("Choose item to use: ")
            player.use_item(item_choice)
        
        elif action == "r":
            if random.random() < 0.5:
                print("You successfully ran away!")
                return False
            else:
                print("Failed to escape!")

        else:
            print("Invalid action!")

        # Enemy attacks if alive
        if enemy.hp > 0:
            enemy_damage = max(0, random.randint(enemy.attack-3, enemy.attack+3) - player.defense//2)
            player.hp -= enemy_damage
            print(f"{enemy.name} attacks you for {enemy_damage} damage!")

    if player.hp > 0:
        print(f"\nYou defeated {enemy.name}!")
        player.xp += enemy.xp_reward
        player.gold += enemy.gold_reward
        print(f"Gained {enemy.xp_reward} XP and {enemy.gold_reward} gold.")
        player.level_up()
        return True
    else:
        print("\nYou have been defeated...")
        return False

# -----------------------------
# Area / Exploration System
# -----------------------------
areas = {
    "Town": ["Forest", "Dungeon"],
    "Forest": ["Town", "Cave"],
    "Dungeon": ["Town", "Cave"],
    "Cave": ["Forest", "Dungeon"]
}

enemies = {
    "Forest": [Enemy("Goblin", 30, 8, 20, 10), Enemy("Wolf", 25, 10, 25, 15)],
    "Dungeon": [Enemy("Skeleton", 40, 12, 40, 20), Enemy("Orc", 50, 15, 50, 25)],
    "Cave": [Enemy("Bat", 20, 5, 15, 5), Enemy("Spider", 35, 10, 30, 10)]
}

def explore(player):
    print("\nWhere do you want to go?")
    for i, loc in enumerate(areas[player.location],1):
        print(f"{i}. {loc}")
    choice = input("Enter number: ")
    try:
        new_location = areas[player.location][int(choice)-1]
        player.location = new_location
        print(f"\nYou travel to {new_location}...")
        # Random encounter
        if random.random() < 0.7:
            enemy = random.choice(enemies[new_location])
            battle(player, enemy)
    except:
        print("Invalid choice!")

# -----------------------------
# Save / Load System
# -----------------------------
def save_game(player, filename="savegame.json"):
    with open(filename, "w") as f:
        json.dump(player.__dict__, f)
    print("Game saved!")

def load_game(filename="savegame.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            player = Player(data["name"], data["pclass"])
            player.__dict__.update(data)
            return player
    else:
        return None

# -----------------------------
# Main Game Loop
# -----------------------------
def main():
    print("=== Welcome to Expert-Expert Text RPG ===")
    player = load_game()
    if not player:
        name = input("Enter your character name: ")
        pclass = input("Choose class (Warrior/Mage/Rogue): ")
        player = Player(name, pclass)
    
    while True:
        print(f"\nCurrent Location: {player.location} | HP: {player.hp}/{player.max_hp} | Gold: {player.gold} | Level: {player.level}")
        print("1. Explore\n2. Inventory\n3. Save Game\n4. Quit")
        choice = input("Choose action: ")
        if choice == "1":
            explore(player)
        elif choice == "2":
            print(player.inventory)
        elif choice == "3":
            save_game(player)
        elif choice == "4":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
