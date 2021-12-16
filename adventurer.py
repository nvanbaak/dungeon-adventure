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

        self.__vision = 0

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
            self.__game.announce(f"Earned a pillar!  You now have {self.__pillars}")

        else:
            raise Exception("The pillar value <" + pillar + "> is neither 'A', 'E', 'I', or 'P'!!!")

    def add_health_potion(self):
        """
        Increments health potion count by 1.
        """
        self.__health_p += 1
        self.__game.announce(
                f"You pick up a health potion.  You now have {self.__health_p} of them.")
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

            self.__game.announce(f"Used a health potion! It heals {heal} HP, bringing you to {self.__hp}.")
            return True

        elif self.__health_p <= 0:
            self.__game.announce("You reach for a health potion and find only disappointment.")
            return False

    def add_vision_potion(self):
        """
        Increments vision potion count by 1.
        """
        self.__vision_p += 1
        self.__game.announce(
                f"You pick up a vision potion.  You now have {self.__vision_p} of them.")
        return self.__vision_p

    def use_vision_potion(self):
        """
        Uses a vision potion if the Adventurer has one.
        :returns: True if potion used, False otherwise.
        """
        if self.__vision_p > 0:
            self.__vision_p -= 1
            self.__vision += 2
            self.__game.announce(f"Your vision has temporarily increased to {self.__vision}!")
            return True

        else:
            self.__game.announce("You look for a vision potion but don't see one.")
            return False

    def get_vision_range(self):
        return self.__vision

    def decay_vision(self):
        if self.__vision > 0:
            self.__vision -= 1

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

    # debug code, only used for unit tests
    def is_pillar_in_inventory(self, pillar):
        return pillar in self.__pillars