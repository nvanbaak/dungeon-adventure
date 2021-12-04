# tests for Dungeon class

import unittest
from dungeon import Dungeon
from mock_adventurer import MockAdventurer as Adv
from mock_game import MockGame as Game
from mock_room import MockRoom as Room

class DungeonTest(unittest.TestCase):
    def test_init(self):
        my_dungeon = Dungeon(1, Game())
        self.assertIs

        self.assertEqual(my_dungeon._Dungeon__difficulty, 1)
        self.assertEqual(my_dungeon._Dungeon__size, 7)
        self.assertEqual(my_dungeon._Dungeon__entrance, None)
        self.assertEqual(my_dungeon._Dungeon__player_location, None)
        self.assertEqual(my_dungeon._Dungeon__room_count, 0)

    def test_generate(self):
        my_game = Game()
        my_dungeon = Dungeon(1, my_game)
        adv = Adv("Test Adventurer", my_game)

        my_dungeon.generate(adv)

        entrance_room : Room = my_dungeon._Dungeon__entrance

        # ensure all doors out of the entrance room are open
        self.assertNotEqual(entrance_room.get_n(), False)
        self.assertNotEqual(entrance_room.get_w(), False)
        self.assertNotEqual(entrance_room.get_e(), False)
        self.assertNotEqual(entrance_room.get_s(), False)

        # ensure adventurer is in the entrance room
        # self.assertTrue(entrance_room._Room__has_player)
        self.assertEqual(my_dungeon._Dungeon__player_location.get_id(), 0)

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

        my_dungeon._Dungeon__entrance = entrance_room
        my_dungeon._Dungeon__player_location = entrance_room

        return my_dungeon, entrance_room, next_room, adv

    def test_movement(self):
        my_dungeon, entrance_room, next_room, adv = self.make_toy_dungeon()



