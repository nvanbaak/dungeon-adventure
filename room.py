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
        self.__pillar = ["A", "E", "I", "P"]
    # builds 2D Graphical representation of the room
    def __str__(self):
        return f''
    def set_health(self, add_potion):
        self.__health_p = add_potion

    def can_enter(self):
        return not self.__impassable and not self.__visited

    def is_exit(self):
        return self.__exit

    def set_visited(self, visited):
        self.__visited = visited
