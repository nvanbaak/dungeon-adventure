import unittest
from room import Room
from adventurer import Adventurer
from mock_game import MockGame as Game



class Room_Test(unittest.TestCase):
    def test_init(self):
        try:
            the_room = Room(0, (0, 0))
            self.assertTrue(True)
        except:
            self.assertTrue(False, "Exception raised during init")

    def test_get_id(self):
        new_room = Room(0, (0, 0))
        self.assertEqual(new_room.get_id(), 0)

    def test_get_location(self):
        new_room = Room(0, (0, 0))
        self.assertEqual(new_room.get_location(), (0, 0))

    def test_link(self):
        room_1 = Room(0, (0, 0))
        room_2 = Room(1, (1, 1))
        room_2.wall("s")
        room_1.link(room_2, "n")
        self.assertFalse(room_1.get_dir("n"), "room not properly walled")
        room_1.link(room_2, "s")
        self.assertEqual(room_1.get_dir("s"), room_2)

    def test_set_pillar_A(self):
        """Simple test to set pillar to A"""
        room = Room(0, 1)
        room.set_pillar("A")
        self.assertEqual("A", room.get_pillar(), "pillar not set to A")

    def test_set_pillar_Y(self):
        """Set pillar to Y, which is which is not in pillars so a ValueError should be raised"""
        room = Room("0", "n")
        try:
            room.set_pillar("Y")
            self.assertEqual(True, False, "exception not thrown for pillar Y which isn't in pillars")
        except ValueError as value_error:
            self.assertEqual(True, True)


    def test_set_as_exit(self):
        new_room = Room(0, (0, 0))
        new_room.set_as_exit()
        self.assertTrue(new_room.is_exit())

    def test_leave(self):
        room_1 = Room(0, (0, 0))
        advent_1 = Adventurer("Jack", Game())
        room_1.enter(advent_1)
        self.assertTrue(room_1.get_player())
        room_1.leave()
        self.assertFalse(room_1.get_player())
