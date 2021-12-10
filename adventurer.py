import random


class Adventurer:
    """
    A class the handles information for the Adventurer
    """
    def __init__(self, name, game):
        self.__name = name
        self.__game = game
        self.__pillars = []
        self.__vision_p = 0
        self.__health_p = 0

        self.__hp = random.randrange(75, 100)
        self.__max_hp = self.__hp
        self.__current_hp = self.__hp

        self.__vision = 0

    def get_name(self):
        return str(self.__name)

    def earn_pillar(self, pillar):
        if pillar in self.__pillars:
            raise Exception("Attempted to collect pillar <", pillar, "> a second time.")
        if pillar is "A":
            self.__pillars.append("A")
        elif pillar is "E":
            self.__pillars.append("E")
        elif pillar is "I":
            self.__pillars.append("I")
        elif pillar is "P":
            self.__pillars.append("P")
        else:
            raise Exception("The pillar value <" + pillar + "> is neither 'A', 'E', 'I', or 'P'!!!")

    def add_health_potion(self):
        self.__health_p += 1
        return self.__health_p

    def use_health_potion(self):
        heal = random.randrange(1, 20)

        if self.__health_p > 0:
            self.__health_p -= 1

            self.__current_hp = self.__current_hp + heal
            if self.__current_hp >= self.__max_hp:
                self.__current_hp = self.__max_hp

            print("Amount healed is: " + str(heal))
            return True

        elif self.__health_p <= 0:
            print("You have no Health Potions!!!")
            # Adventurer.announce(self)
            return False

    def add_vision_potion(self):
        self.__vision_p += 1
        return self.__vision_p

    def use_vision_potion(self):
        vision = 0
        if self.__vision_p > 0:
            self.__vision_p -= 1

            vision += 8
            print("Vision has increased be: " + str(vision))

            return True

        else:
            print("You have no Vision Potions!!!")
            return False

    def announce(self):

        adventurer = Adventurer()

        if self.__health_p is 0:
            return print("You have no health potions!!!")

        if self.__vision_p is 0:
            return print("You have no vision potions!!!")

        if self.__hp <= 0:
            print("You Dead")

    def take_damage(self):

        damage = random.randrange(1, 20)
        if self.__current_hp - damage > 0:
            self.__current_hp = self.__current_hp - damage
            print("Oh No!!! You've fallen into a pit")
            print("Damage taken is: " + str(damage))
            print("Current HP is now: " + str(self.__current_hp) + "\n")

        elif self.__current_hp - damage < 0:
            print("Oh No!!! You've fallen into a pit")
            print("Damage taken is: " + str(damage))

            self.__current_hp = 0
            print("Current HP is now: " + str(self.__current_hp) + "\n")
            print("You've Died!!!")
            print("GAME OVER!!!")
            quit()

    def exit(self):
        if len(self.__pillars) == 4:
            print("Congratulations!!! You've discovered all four pillars of OO!!!")
            quit()
            # self.__game.end_game()
            return True
        else:
            print("Warning! You do not have all pillars of OO! You only have " + str(len(self.__pillars)) + " pillars!")
            return False

    def __str__(self):
        return "\nName: " + self.__name + " HP: " + str(self.__current_hp) + " Number of health potions: " + \
               str(self.__health_p) + " Number of vision potions: " + str(self.__vision_p) + " Pillars Found: " + \
               str(self.__pillars)

    def status(self):
        return self.__str__()


adventurer = Adventurer("Jack", "1")

print("\n------------------------print adventurer status ('empty', try using either potion)-------------------------")
adventurer.use_health_potion()
adventurer.use_vision_potion()
print(adventurer.status())

print("\n------------------------print adventurer status (+1 potion)-------------------------")
adventurer.add_health_potion()
print(adventurer.status())

print("\n------------------------print adventurer status (take damage 1st)-------------------------")
adventurer.take_damage()
print(adventurer.status())

print("\n------------------------print adventurer status (take 1st health potion)-------------------------")
adventurer.use_health_potion()
print(adventurer.status())

print("\n------------------------print adventurer status (Add two of each potion)-------------------------")
adventurer.add_health_potion()
adventurer.add_health_potion()
adventurer.add_vision_potion()
adventurer.add_vision_potion()

print(adventurer.status())

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

print(adventurer.status())



# print("\n------------------------print adventurer status (TIME TO DIE!!!)-------------------------")
# print(adventurer.status())
# adventurer.take_damage()
# adventurer.take_damage()
# adventurer.take_damage()
# adventurer.take_damage()
# adventurer.take_damage()
# adventurer.take_damage()
# adventurer.take_damage()
# adventurer.take_damage()
# adventurer.take_damage()
# adventurer.take_damage()
# adventurer.take_damage()
# adventurer.take_damage()
#
# print(adventurer.status())



print("\n------------------------print adventurer exit (doesn't have all Pillars of OO)-------------------------\n")
adventurer.exit()

print(adventurer.status())


print("\n------------------------print adventurer status (Add 'E', 'I', 'P')-------------------------")
adventurer.earn_pillar("P")
adventurer.earn_pillar("I")
adventurer.earn_pillar("E")

print(adventurer.status())

print("\n------------------------print adventurer exit (has all Pillars of OO)-------------------------\n")
adventurer.exit()


