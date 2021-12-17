import random


class Room:
    def __init__(self, room_id, location):
        self.__health_p = False
        if random.random() < 0.1:
            self.__health_p = True
        self.__vision_p = False
        if random.random() < 0.1:
            self.__vision_p = True
        self.__pit = False
        if random.random() < 0.1:
            self.__pit = random.randrange(1, 20)
        self.__exit = False
        self.__doors = {
            "n": None,
            "w": None,
            "e": None,
            "s": None
        }
        self.__has_player = False
        self.__pillar = False
        self.__room_id = room_id
        self.__location = location

    def get_id(self):
        return self.__room_id
    
    def get_location(self):
        return self.__location

    def __str__(self):
        """
        Builds 2D Graphical representation of the room
        """
        north = " " if self.__doors['n'] else "-"
        west = " " if self.__doors['w'] else "|"
        east = " " if self.__doors['e'] else "|"
        south = " " if self.__doors['s'] else "-"

        item = None

        if self.__has_player:
            item = "@"
        elif self.__pillar:
            item = self.__pillar
        elif self.__exit:
            item = "O"
        elif self.__health_p and self.__vision_p:
            item = "M"
        elif self.__pit:
            item = "X"
        elif self.__health_p:
            item = "H"
        elif self.__vision_p:
            item = "V"
        else:
            item = " "

        return f"*{north}*\n{west}{item}{east}\n*{south}*"

    def get_player(self):
        return self.__has_player

    def link(self, room, dir):
        compliment = {
            "n": "s",
            "w": "e",
            "e": "w",
            "s": "n",
        }
        make_link = True
        if room.get_dir(compliment[dir]) is False:
            make_link = False
        if make_link:
            self.__doors[dir] = room
        else:
            self.__doors[dir] = False

    def get_dir(self, dir):
        return self.__doors[dir]

    def is_exit(self):
        return self.__exit

    def set_pillar(self, pillar):
        pillars = ["A", "E", "I", "P"]
        if pillar in pillars:
            self.__pillar = pillar

    def get_pillar(self):
        return self.__pillar

    def clear_room(self):
        self.__health_p = False
        self.__pit = False
        self.__vision_p = False

    def set_as_exit(self):
        self.clear_room()
        self.__exit = True

    def leave(self):
        self.__has_player = False

    def wall(self, dir):
        self.__doors[dir] = False

    def enter(self, adv):
        if self.__exit:
            adv.exit()
            self.__has_player = True
            return
        if self.__pillar:
            adv.earn_pillar(self.__pillar)
            self.__pillar = False
        if self.__vision_p:
            adv.add_vision_potion()
            self.__vision_p = False
        if self.__health_p:
            adv.add_health_potion()
            self.__health_p = False
        if self.__pit:
            adv.take_damage(self.__pit, "pit trap")

        self.__has_player = True






