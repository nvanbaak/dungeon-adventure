import unittest
from adventurer import Adventurer
from mock_game import MockGame as Game

class Adventurer_Test(unittest.TestCase):
    def test_init(self):
        my_adventurer = Adventurer("Jack", Game())

    def test_name(self):
        my_adventurer = Adventurer("Jack", Game())
        self.assertEqual(my_adventurer.get_name(), "Jack")

    def test_name_fail(self):
        try:
            my_adventurer_fail = Adventurer("JackU", Game())
            self.assertEqual(False, True)
        except:
            self.assertEqual(True, True)

    def test_Earn_Pillar(self, pillar):
        pillars = Adventurer("Jack", Game())
        pillar = ["A", "E", "I", "P"]
        self.assertEqual(pillars.earn_pillar(pillar), ["A", "E", "I", "P"])

    def test_Add_Health_Potion(self):
        adventurer_HP = Adventurer("Jack", Game())
        self.assertEqual(adventurer_HP.add_health_potion(), 1)

    def test_Use_One_Health_Potions(self):
        my_adventurer = Adventurer("Jack", Game())
        self.assertEqual(my_adventurer.use_health_potion(), 0)

    def test_Use_One_Health_Potion_Fail(self):
        my_adventurer = Adventurer("Jack", Game())
        try:
            self.assertEqual(my_adventurer.use_health_potion(), 1)
            self.assertEqual(False, True)
        except:
            self.assertEqual(True, True)

    def test_Add_Vision_Potion(self):
        adventurer_VP = Adventurer("Jack", Game())
        self.assertEqual(adventurer_VP.add_vision_potion(), 1)

    def test_Use_One_Vision_Potions(self):
        my_adventurer = Adventurer("Jack", Game())
        self.assertEqual(my_adventurer.use_vision_potion(), 0)

    def test_Use_One_Vision_Potion_Fail(self):
        my_adventurer = Adventurer("Jack", Game())
        try:
            self.assertEqual(my_adventurer.use_vision_potion(), 1)
            self.assertEqual(False, True)
        except:
            self.assertEqual(True, True)

    def test_Take_Damage(self):
        my_adventurer = Adventurer("Jack", Game())
        self.assertEqual(my_adventurer.take_damage(-1000, source=Adventurer), None)

    def test_Exit_Fail(self):
        my_adventurer = Adventurer("Jack", Game())
        self.assertEqual(my_adventurer.exit(), None)

if __name__ == '__main__':
    unittest.main()