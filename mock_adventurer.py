# mock object for Adventurer

class MockAdventurer():
    def __init__(self, name, game) -> None:
        self.name = name

    def get_name(self):
        return self.name