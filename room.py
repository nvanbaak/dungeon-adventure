import random


class Room:
    def __init__(self):
        self.__health_p = True
        self.__vision_p = True
        self.__impassable = False
        self.__pit = False
        self.__entrance = True
        self.__exit = True
        self.__doors = {
            "n": None,
            "w": None,
            "e": None,
            "s": None
        }
        self.__has_player = True
        self.__pillar = False
    # builds 2D Graphical representation of the room
    def __str__(self):
        item_count = 0
        if self.__health_p:
            item_count += 1
        if self.__vision_p:
            item_count += 1
        if item_count > 1:
            return "M"
        north = " " if self.compass_dict['n'] else "-"
        west = " " if self.compass_dict['w'] else "|"
        east = " " if self.compass_dict['e'] else "|"
        south = " " if self.compass_dict['s'] else "-"

        item = None

        if self.__has_player:
            item = "@"
        elif self.__pillar:
            item = self.__pillar
        elif self.__exit:
            item = "O"
        else:
            item = " "

        return f"*{north}*\n{west}{item}{east}\n*{south}*"


    def link(self, room, dir):
        make_link = True
        if dir == "n":
            if room.get_s() is False:
                make_link = False
        if dir == "w":
            if room.get_e() is False:
                make_link = False
        if dir == "e":
            if room.get_w() is False:
                make_link = False
        if dir == "s":
            if room.get_n() is False:
                make_link = False

        if make_link:
            self.compass_dict[dir] = room
        else:
            self.compass_dict[dir] = False

    def set_health(self, add_potion):
        self.__health_p = add_potion

    def can_enter(self):
        return not self.__impassable and not self.__visited

    def is_exit(self):
        return self.__exit

    def set_visited(self, visited):
        self.__visited = visited

    def set_has_player(self, player):
        self.__has_player = player

    def set_pillar(self, pillar):
        pillars = ["A", "E", "I", "P"]
        self.__pillar = pillar

    def clear_room(self):
        self.__health_p = False
        self.__pit = False
        self.__vision_p = False

    def set_as_exit(self):
        self.__exit = True




