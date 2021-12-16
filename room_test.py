import unittest
from room import Room


class Room_Test(unittest.TestCase):
    def test_init(self):
        the_room = Room("0", "n")

    def test_get_id(self):
        pass
    def test_get_location(self):
        pass
    def test_get_player(self):
        pass
    def test_link(self):
        pass
    def test_get_dir(self):
        pass
    def test_is_exit(self):
        pass
    def test_set_pillar_A(self):
        """Simple test to set pillar to A"""
        room = Room(0, 1)
        room.set_pillar("A")
        self.assertEqual("A", room.set_pillar("A"), "pillar not set to A")

    def test_set_pillar_Y(self):
        """Set pillar to Y, which is which is not in pillars so a ValueError should be raised"""
        room = Room("0", "n")
        try:
            room.set_pillar("Y")
            self.assertEqual(True, False, "exception not thrown for pillar Y which isn't in pillars")
        except ValueError as value_error:
            self.assertEqual(True, True)

    def test_get_pillar(self):

    def test_clear_room(self):
        pass
    def test_set_as_exit(self):
        pass
    def test_leave(self):
        pass
    def test_wall(self):
        pass
    def test_enter(self):
        pass
