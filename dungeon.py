import random
from adventurer import Adventurer
from room import Room
from mock_game import MockGame as Game


class Dungeon():
    """
    An object that manages the Dungeon and the objects inside of it.
    """
    def __init__(self, diff, game : Game, adv : Adventurer) -> None:
        self.__diff = diff
        self.__game = game
        self.__adv = adv
        self.__size = 7 + (3 * diff)
        self.__entrance = None
        self.__pl_location = None
        self.__room_count = 0
        self.__room_array = []

        for _ in range(self.__size):
            row = []
            for _ in range(self.__size):
                row.append(None)
            self.__room_array.append(row)

        self.generate()

    def generate(self) -> None:
        """
        Builds out the dungeon and places objects inside.
        """
        # setup entrance and surrounding rooms
        rooms_to_build = self.__create_entrance(self.__adv)

        # we have 4 pillars and an exit to place
        pillars = ["E", "I", "A", "P"]
        exit_room = 30 + self.__diff * 10

        # next, continue adding and linking rooms
        while rooms_to_build:
            new_room : Room = rooms_to_build.pop(0)
            (x, y) = new_room.get_location()

            # use id to place exit and pillars
            if new_room.get_id() == exit_room:
                new_room.set_as_exit()
            elif pillars and new_room.get_id() > (16 * self.__diff):
                pillar_threshold = {
                    1 : 0.10,
                    2 : 0.5,
                    3 : 0.02
                }
                if random.random() < pillar_threshold[self.__diff]:
                    new_room.clear_room()
                    new_room.set_pillar(pillars.pop())

            # populate the dungeon in each direction
            target_location = {
                "n" : (x, y-1),
                "w" : (x-1, y),
                "e" : (x+1, y),
                "s" : (x, y+1)
            }

            for dir in ["n", "w", "e", "s"]:
                try:
                    # None means this dir isn't built yet
                    if new_room.get_dir(dir) is None:

                        # random chance to make wall or corridor
                        chance_to_wall = .525
                        if random.random() < chance_to_wall:
                            new_room.wall(dir)
                        else:
                            # get a reference to the room to corridor to
                            target_room = self.__get_room_at(target_location[dir])

                            # make the room if it's not there
                            if target_room is None:
                                target_room = self.__make_new_room(target_location[dir])
                                rooms_to_build.append(target_room)

                            # finally, link the rooms
                            self.__double_link(new_room, target_room, dir)

                except IndexError: # if we exceed the array bounds, wall
                    # Note that going to index [-1] causes wraparound
                    # and will not trigger this exception.  We consider
                    # this a feature, not a bug.
                    new_room.wall(dir)

        # check that sufficient rooms were generated
        room_cutoff = self.__size * self.__size * .85
        if self.__room_count < room_cutoff:
            # print("Maze too small!  Regenerating...")
            self.__clear_dungeon()
            self.generate()
            return

        # check that all pillars and exit were placed
        if not self.__validate_maze():
            # print("Objective placement failed!  Regenerating...")
            self.__clear_dungeon()
            self.generate()
            return

        # print(self.display(3))
        # print(self)

    def __validate_maze(self):
        """
        Uses breadth-first search to ensure all objectives are in the maze.
        Returns True if all objectives are present, False otherwise.
        """
        # define flags for objectives
        pillar_flags = {
            "A" : False,
            "E" : False,
            "I" : False,
            "P" : False
        }
        exit_flag = False

        # Set up beginning of traversal
        room_dict = {
            self.__entrance : 0
        }
        rooms_to_check = []

        # We do the first loop manually to set up rooms_to_check
        for dir in ["n", "w", "e", "s"]:
            target_room = self.__entrance.get_dir(dir)
            room_dict[target_room] = 1
            rooms_to_check.append(target_room)

        # now loop through everything else
        while rooms_to_check:
            this_room : Room = rooms_to_check.pop(0)
            this_id = this_room.get_id()

            if this_room.get_pillar():
                pillar_flags[this_room.get_pillar()] = True
            if this_room.is_exit():
                exit_flag = True

            # add adjacent rooms to queue
            for dir in ["n", "w", "e", "s"]:
                target_room : Room = this_room.get_dir(dir)
                if target_room:
                    target_id = target_room.get_id()
                    if this_id < target_id: # prevents backtracking
                        rooms_to_check.append(target_room)

        # check flags now that loop is done
        for pillar in pillar_flags:
            if not pillar_flags[pillar]:
                return False

        # reaching this point means all pillars are present,
        # so the exit flag is what makes or breaks things
        return exit_flag

    def __create_entrance(self, adv) -> list[Room]:
        """
        Helper function that adds an entrance and four connected rooms
        params:
        :adv: a reference to the adventurer
        :returns: a list of rooms connected to the entrance
        """
        rooms_to_build = []

        # build our starting room at a random non-edge location
        x = random.choice(range(1,self.__size-1))
        y = random.choice(range(1,self.__size-1))

        entrance_room : Room = self.__make_new_room((x, y))
        entrance_room.clear_room()
        self.__entrance = entrance_room
        entrance_room.enter(adv)
        self.__pl_location = entrance_room

        # We do this manually to make sure all rooms surrounding
        # the entrance are linked to the entrance (ie not walls)
        north_room = self.__make_new_room((x, y-1))
        self.__double_link(entrance_room, north_room, "n")
        rooms_to_build.append(north_room)

        west_room = self.__make_new_room((x-1, y))
        self.__double_link(entrance_room, west_room, "w")
        rooms_to_build.append(west_room)

        south_room = self.__make_new_room((x, y+1))
        self.__double_link(entrance_room, south_room, "s")
        rooms_to_build.append(south_room)

        east_room = self.__make_new_room((x+1, y))
        self.__double_link(entrance_room, east_room, "e")
        rooms_to_build.append(east_room)

        return rooms_to_build

    def __make_new_room(self, location) -> Room:
        """
        Helper method that automatically creates a new Room obj at the coords.
        Automatically increments room_count.
        params:
        x: x position in the Dungeon's room_array
        y: y position in the Dungeon's room_array
        returns: the Room object.
        """
        new_room = Room(self.__room_count, location)
        self.__room_count += 1
        # due to how room_array is stored, y is first
        self.__room_array[location[1]][location[0]] = new_room
        return new_room

    def __double_link(self, room1 : Room, room2 : Room, dir) -> None:
        """
        Helper method that links room1 to room2 and vice versa.
        dir expects "n", "w", "e", or "s"
        params:
        :room1: First room
        :room2: Second room
        :dir: Used in the room1.link() call and inverted for room2.link()
        """
        compliment = {
            "n" : "s",
            "w" : "e",
            "e" : "w",
            "s" : "n",
        }
        room1.link(room2, dir)
        # only link back if there's not a wall there
        if room2.get_dir(compliment[dir]) is not False:
            room2.link(room1, compliment[dir])
        return

    def __get_room_at(self, location) -> Room:
        """
        Helper method that takes a tuple with x/y coordinates
        and returns the object at that location in room_array
        """
        return self.__room_array[location[1]][location[0]]

    def __clear_dungeon(self):
        """
        Helper method to reset the dungeon.
        """
        self.__entrance = None
        self.__pl_location = None
        self.__room_count = 0
        self.__room_array = []

        for _ in range(self.__size):
            row = []
            for _ in range(self.__size):
                row.append(None)
            self.__room_array.append(row)

    def move_player(self, adv : Adventurer, dir) -> None:
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
            self.__game.announce(f"{pl_name} opens the {dir_names[dir]} door.")

            target_room.enter(adv)
            self.__pl_location = target_room
            pl_room.leave()
        else:
            self.__game.announce(f"{pl_name} tries to move {dir_names[dir]} and runs\nheadfirst into the wall.")

    def get_size(self):
        return self.__size

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
                    line1 += "///"
                    line2 += "///"
                    line3 += "///"
                else:
                    room = room.__str__().split("\n")
                    line1 += str(room[0])
                    line2 += str(room[1])
                    line3 += str(room[2])

            output_str += f"{line1}\n{line2}\n{line3}\n"

        return output_str

    def display(self, vis_range, potion_range) -> str:
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
            for _ in range(0, vis_range):
                if next_room:
                    visible_rooms[next_room.get_id()] = True
                    next_room = next_room.get_dir(direction)
                    if not next_room:
                        break

        # check if vision potion active
        if potion_range > 0:
            (pl_x, pl_y) = self.__pl_location.get_location()
            for row in range(pl_x-potion_range, pl_x+potion_range+1):
                for col in range(pl_y-potion_range, pl_y+potion_range+1):
                    try:
                        if col >= self.__size:
                            col -= self.__size
                        if row >= self.__size:
                            row -= self.__size
                        target_room : Room = self.__room_array[col][row]
                        if target_room:
                            visible_rooms[target_room.get_id()] = True
                    except IndexError:
                        print("display() attempted to access room out of bounds!")
                    

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

    def debug_get_room_count(self):
        return self.__room_count

    def debug_clear_dungeon(self):
        self.__clear_dungeon()