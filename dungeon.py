
from mock_room import MockRoom as Room


class Dungeon():
    """
    An object that manages the Dungeon and the objects inside of it.
    """
    def __init__(self, diff, game):
        self.__diff = diff
        self.__game = game
        self.__size = 5 + (2 * diff)
        self.__entrance = None
        self.__pl_location = None
        self.__room_count = 0

    def move_player(self, adv, dir):
        """
        Moves the player within the dungeon if there's an open door in the specified direction.
        Raises ValueError if dir isn't "n", "w", "e", or "s"
        params:
        :adv: a reference to the adventurer.
        :dir: the direction to move in.
        :returns: None.
        """

        if not (dir == "n" or dir == "w" or dir == "e" or dir == "s"):
            raise ValueError("Invalid move command!")

        pl_room : Room = self.__pl_location
        target_room : Room = pl_room.get_dir(dir)
        pl_name = adv.get_name()
        dir_names = {
            "n" : "north",
            "w" : "west",
            "e" : "east",
            "s" : "south"
        }

        if target_room:
            target_room.enter(adv)
            self.__pl_location = target_room
            pl_room.leave()

            self.__game.announce(f"{pl_name} opens the {dir_names[dir]} door.")

        else:
            self.__game.announce(f"{pl_name} tries to move {dir_names[dir]} and runs headfirst into the wall.")





    #########
    # Debug code used only for unit tests
    #########

    def debug_set_entrance(self, room):
        self.__entrance = room
    
    def debug_get_entrance(self):
        return self.__entrance

    def debug_set_pl_location(self, room):
        self.__pl_location = room

    def debug_get_pl_location(self):
        return self.__pl_location

    def debug_get_difficulty(self):
        return self.__diff
    
    def debug_get_size(self):
        return self.__size
    
    def debug_get_room_count(self):
        return self.__room_count
