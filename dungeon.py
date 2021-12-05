
from mock_room import MockRoom as Room


class Dungeon():
    """
    An object that manages the Dungeon and the objects inside of it.
    """
    def __init__(self, diff, game) -> None:
        self.__diff = diff
        self.__game = game
        self.__size = 5 + (2 * diff)
        self.__entrance = None
        self.__pl_location = None
        self.__room_count = 0
        self.__room_array = []

        for _ in range(self.__size):
            row = []
            for _ in range(self.__size):
                row.append(None)
            self.__room_array.append(row)

    def move_player(self, adv, dir) -> None:
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

    def __str__(self) -> str:
        """
        Returns a string displaying the dungeon's contents.
        """
        output_str = ""

        for row in self.__room_array:

            line1 = ""
            line2 = ""
            line3 = ""

            for room in row:
                if room is None:
                    line1 += "###"
                    line2 += "###"
                    line3 += "###"
                else:
                    room = room.__str__().split("\n")
                    line1 += room[0]
                    line2 += room[1]
                    line3 += room[2]

            output_str += f"{line1}\n{line2}\n{line3}\n"

        return output_str

    def display(self, range) -> str:
        """
        Returns a string representing only the parts of the dungeon
        the player can see.
        """
        # start by creating a dictionary of room ids
        # for all rooms the player can see
        visible_rooms = {
            self.__pl_location.get_id() : True
        }

        for direction in ["n","w","s","e"]:
            next_room : Room = self.__pl_location.get_dir(direction)
            if next_room:
                visible_rooms[next_room.get_id()] = True
                next_room = next_room.get_dir(direction)

        # Then we follow a similar process to __str__
        output_str = ""

        for row in self.__room_array:

            line1 = ""
            line2 = ""
            line3 = ""

            for room in row:
                if room is None:
                    line1 += "   "
                    line2 += "   "
                    line3 += "   "
                else:
                    if visible_rooms.setdefault(room.get_id(), False):
                        room = room.__str__().split("\n")
                        line1 += room[0]
                        line2 += room[1]
                        line3 += room[2]
                    else:
                        room = room.__str__().split("\n")
                        line1 += "   "
                        line2 += "   "
                        line3 += "   "

            output_str += f"{line1}\n{line2}\n{line3}\n"

        return output_str




    #########
    # Debug code used only for unit tests
    #########

    def debug_set_room_array(self, array):
        self.__room_array = array

    def debug_set_entrance(self, room):
        self.__entrance = room
    
    def debug_get_entrance(self):
        return self.__entrance

    def debug_set_pl_location(self, room):
        self.__pl_location = room

    def debug_get_player_location(self):
        return self.__pl_location

    def debug_get_difficulty(self):
        return self.__diff
    
    def debug_get_size(self):
        return self.__size
    
    def debug_get_room_count(self):
        return self.__room_count
