import random
from mock_game import MockGame as Game


class Adventurer:
    """
    A class the handles information for the Adventurer
    """
    def __init__(self, name, game):
        self.__name = name
        self.__game : Game = game
        self.__pillars = []
        self.__vision_p = 0
        self.__health_p = 0

        self.__hp = random.randrange(75, 100)
        self.__max_hp = self.__hp

    def get_name(self):
        """
        Getter for name property.
        """
        return str(self.__name)

    def earn_pillar(self, pillar):
        """
        Called by Room to add pillars to Adventurer's inventory.
        """
        if pillar in self.__pillars:
            raise Exception("Attempted to collect pillar <", pillar, "> a second time.")
        if pillar == "A" or pillar == "E" or pillar == "I" or pillar == "P":
            self.__pillars.append(pillar)
        else:
            raise Exception("The pillar value <" + pillar + "> is neither 'A', 'E', 'I', or 'P'!!!")

    def add_health_potion(self):
        """
        Increments health potion count by 1.
        """
        self.__health_p += 1
        return self.__health_p

    def use_health_potion(self):
        """
        If the Adventurer has any health potions, uses one and increases
        Adventurer's health by a random number.
        :returns: True if potion was used, False otherwise
        """
        heal = random.randrange(5, 15)

        if self.__health_p > 0:
            self.__health_p -= 1

            self.__hp += heal
            if self.__hp >= self.__max_hp:
                self.__hp = self.__max_hp

            self.__game.announce("Amount healed is: " + str(heal))
            return True

        elif self.__health_p <= 0:
            self.__game.announce("You have no Health Potions!!!")
            return False

    def add_vision_potion(self):
        """
        Increments vision potion count by 1.
        """
        self.__vision_p += 1
        return self.__vision_p

    def use_vision_potion(self):
        """
        Uses a vision potion if the Adventurer has one.
        :returns: True if potion used, False otherwise.
        """
        if self.__vision_p > 0:
            self.__vision_p -= 1
            self.__game.announce("Vision has increased!")
            return True

        else:
            self.__game.announce("You have no Vision Potions!!!")
            return False

    def take_damage(self, damage, source):

        self.__hp -= damage
        print(f"Oh no! {self.__name} took {damage} from {source}!  They are now at {self.__hp} hp!")

    def exit(self):
        if len(self.__pillars) == 4:
            self.__game.announce("Congratulations!!! You've discovered all four pillars of OO!!!")
            self.__game.end_game()
            return
        else:
            self.__game.announce("You feel like you could escape from this room if only you knew more about programming.")
            return

    def __str__(self):
        return "\nName: " + self.__name + " HP: " + str(self.__hp) + " Number of health potions: " + \
               str(self.__health_p) + " Number of vision potions: " + str(self.__vision_p) + " Pillars Found: " + \
               str(self.__pillars)


adventurer = Adventurer("Jack", Game())

print("\n------------------------print adventurer status ('empty', try using either potion)-------------------------")
adventurer.use_health_potion()
adventurer.use_vision_potion()
print(adventurer)

print("\n------------------------print adventurer status (+1 potion)-------------------------")
adventurer.add_health_potion()
print(adventurer)

print("\n------------------------print adventurer status (take damage 1st)-------------------------")
adventurer.take_damage(1, "angry gnat")
print(adventurer)

print("\n------------------------print adventurer status (take 1st health potion)-------------------------")
adventurer.use_health_potion()
print(adventurer)

print("\n------------------------print adventurer status (Add two of each potion)-------------------------")
adventurer.add_health_potion()
adventurer.add_health_potion()
adventurer.add_vision_potion()
adventurer.add_vision_potion()
print(adventurer)

print("\n------------------------print adventurer status (Add 'A' to the Pillars + adding an extra 'A' and a false 'z')"
      "-------------------------")
adventurer.earn_pillar("A")
try:
    adventurer.earn_pillar("A")
    print("should have failed.")
except:
    pass

try:
    adventurer.earn_pillar("z")
    print("should have failed.")
except:
    pass

print(adventurer)



print("\n------------------------print adventurer status (TIME TO DIE!!!)-------------------------")
print(adventurer)
adventurer.take_damage(20, "legendary pit")
adventurer.take_damage(20, "legendary pit")
adventurer.take_damage(20, "legendary pit")
adventurer.take_damage(20, "legendary pit")
adventurer.take_damage(20, "legendary pit")
adventurer.take_damage(2000, "extra legendary pit")
print(adventurer)



print("\n------------------------print adventurer exit (doesn't have all Pillars of OO)-------------------------\n")
adventurer.exit()

print(adventurer)


print("\n------------------------print adventurer status (Add 'E', 'I', 'P')-------------------------")
adventurer.earn_pillar("P")
adventurer.earn_pillar("I")
adventurer.earn_pillar("E")

print(adventurer)

print("\n------------------------print adventurer exit (has all Pillars of OO)-------------------------\n")
adventurer.exit()


