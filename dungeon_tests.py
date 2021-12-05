# tests for Dungeon class

import unittest
from dungeon import Dungeon
from mock_adventurer import MockAdventurer as Adv
from mock_game import MockGame as Game
from mock_room import MockRoom as Room

class DungeonTest(unittest.TestCase):
    def test_init(self):
        my_dungeon = Dungeon(1, Game())

        self.assertEqual(my_dungeon.debug_get_difficulty(), 1)
        self.assertEqual(my_dungeon.debug_get_size(), 7)
        self.assertEqual(my_dungeon.debug_get_entrance(), None)
        self.assertEqual(my_dungeon.debug_get_player_location(), None)
        self.assertEqual(my_dungeon.debug_get_room_count(), 0)

    def test_generate(self):
        my_game = Game()
        my_dungeon = Dungeon(1, my_game)
        adv = Adv("Test Adventurer", my_game)

        my_dungeon.generate(adv)

        entrance_room : Room = my_dungeon.debug_get_entrance()

        # ensure all doors out of the entrance room are open
        self.assertNotEqual(entrance_room.get_n(), False)
        self.assertNotEqual(entrance_room.get_w(), False)
        self.assertNotEqual(entrance_room.get_e(), False)
        self.assertNotEqual(entrance_room.get_s(), False)

        # ensure adventurer is in the entrance room
        # self.assertTrue(entrance_room._Room__has_player)
        self.assertEqual(my_dungeon.debug_get_pl_location().get_id(), 0)

    def test_validation(self):
        my_game = Game()
        my_dungeon = Dungeon(1, my_game)
        adv = Adv("Test Adventurer", my_game)

        my_dungeon.generate(adv)

        dungeon_str = my_dungeon.__str__()

        # dungeon should have one of each pillar and an exit
        self.assertEqual(dungeon_str.count("A"), 1)
        self.assertEqual(dungeon_str.count("E"), 1)
        self.assertEqual(dungeon_str.count("I"), 1)
        self.assertEqual(dungeon_str.count("P"), 1)
        self.assertEqual(dungeon_str.count("O"), 1)

    def make_toy_dungeon(self):
        my_game = Game()
        my_dungeon = Dungeon(1, my_game)
        adv = Adv("Test Adventurer", my_game)

        # manually create a two-room dungeon
        entrance_room = Room(0, (3,3))
        entrance_room.wall("w")
        entrance_room.wall("e")
        entrance_room.wall("s")

        next_room = Room(1, (3,4))

        entrance_room.link(next_room,"n")
        next_room.link(entrance_room, "s")

        next_room.wall("w")
        next_room.wall("n")
        next_room.wall("e")

        entrance_room.enter(adv)

        my_dungeon.debug_set_entrance(entrance_room)
        my_dungeon.debug_set_pl_location(entrance_room)

        return my_dungeon, entrance_room, next_room, adv

    def test_movement_bad_direction_code(self):
        my_dungeon, entrance_room, next_room, adv = self.make_toy_dungeon()

        self.assertRaises(ValueError, my_dungeon.move_player, adv, "f")

    def test_movement_valid_move_dir(self):
        my_dungeon, entrance_room, next_room, adv = self.make_toy_dungeon()

        my_dungeon.move_player(adv, "n")
        self.assertTrue(next_room.get_player())
        self.assertFalse(entrance_room.get_player())
        self.assertTrue(my_dungeon.debug_get_player_location().get_player())
        self.assertFalse(my_dungeon.debug_get_entrance().get_player())

    def test_movement_invalid_move_dir(self):
        my_dungeon, entrance_room, next_room, adv = self.make_toy_dungeon()

        my_dungeon.move_player(adv, "w")
        self.assertFalse(next_room.get_player())
        self.assertTrue(entrance_room.get_player())
        self.assertTrue(my_dungeon.debug_get_player_location().get_player())

    def test_display(self):
        my_game = Game()
        my_dungeon = Dungeon(1, my_game)
        adv = Adv("Test Adventurer", my_game)

        # the following code builds a small dungeon that should look like this:
        #
        #  ******   
        #  *A**I*   
        #  * ** *   
        #  * ** ****
        #  *O  @  P*
        #  **** ****
        #     * *   
        #     *E*   
        #     ***   
        #
        #  display() shouldn't print the 'A' as it's not in line of sight

        entrance_room = Room(0, (3,3))

        my_dungeon.debug_set_entrance(entrance_room)
        my_dungeon.debug_set_pl_location(entrance_room)
        entrance_room.enter(adv)

        north_room = Room(1, (3,2))
        north_room.set_pillar("I")
        north_room.wall("w")
        north_room.wall("n")
        north_room.wall("e")

        north_room.link(entrance_room, "s")
        entrance_room.link(north_room, "n")

        west_room = Room(2, (2,3))
        west_room.set_as_exit()
        west_room.wall("s")
        west_room.wall("w")

        west_corridor = Room(3, (2,2))
        west_corridor.set_pillar("A")
        west_corridor.wall("w")
        west_corridor.wall("n")
        west_corridor.wall("e")

        west_corridor.link(west_room, "s")
        west_room.link(west_corridor, "n")

        west_room.link(entrance_room, "e")
        entrance_room.link(west_room, "w")

        south_room = Room(4, (3,4))
        south_room.set_pillar("E")
        south_room.wall("w")
        south_room.wall("s")
        south_room.wall("e")

        south_room.link(entrance_room, "n")
        entrance_room.link(south_room, "s")

        east_room = Room(5, (4,3))
        east_room.set_pillar("P")
        east_room.wall("n")
        east_room.wall("e")
        east_room.wall("s")

        east_room.link(entrance_room, "w")
        entrance_room.link(east_room, "e")

        room_array = [
            [west_corridor, north_room, None],
            [west_room, entrance_room, east_room],
            [None, south_room, None]
        ]

        my_dungeon.debug_set_room_array(room_array)

        vision_range = 3
        display_str = my_dungeon.display(vision_range)

        self.assertEqual(display_str.count("A"), 0)
        self.assertEqual(display_str.count("P"), 1)
        self.assertEqual(display_str.count("O"), 1)

if __name__ == "__main__":
    unittest.main()