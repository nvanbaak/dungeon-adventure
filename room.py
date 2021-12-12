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
        return f''

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




