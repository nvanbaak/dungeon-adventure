# mock Room object for tests

class MockRoom():
    def __init__(self, id, location):
        self.id = id
        self.location = location
        self.compass_dict = {
            "n" : None,
            "w" : None,
            "e" : None,
            "s" : None
        }
        self.exit = False
        self.pillar = False

    def get_n(self):
        return self.compass_dict["n"]
    
    def get_w(self):
        return self.compass_dict["w"]

    def get_e(self):
        return self.compass_dict["e"]

    def get_s(self):
        return self.compass_dict["s"]

    def get_id(self):
        return self.id

    def get_location(self):
        return self.location

    def wall(self, dir):
        self.compass_dict[dir] = False

    def link(self, room, dir):
        make_link = True
        if dir == "n":
            if room.get_s() is False:
                make_link = False
        if dir == "w":
            if room.get_e() is False:
                make_link = False
        if dir == "e":
            if room.get_w() is False:
                make_link = False
        if dir == "s":
            if room.get_n() is False:
                make_link = False

        if make_link: self.compass_dict[dir] = room
        else: self.compass_dict[dir] = False

    def set_pillar(self, pillar):
        self.pillar = pillar

    def set_as_exit(self):
        self.exit = True

    def is_exit(self):
        return self.exit

    def enter(adventurer):
        pass

    def leave():
        pass

    def __str__(self):

        north = " " if self.compass_dict['n'] else "-"
        west = " " if self.compass_dict['w'] else "|"
        east = " " if self.compass_dict['e'] else "|"
        south = " " if self.compass_dict['s'] else "-"

        item = None

        if self.pillar:
            item = self.pillar
        elif self.exit:
            item = "X"
        else:
            item = " "

        return f"*{north}*\n{west}{item}{east}\n*{south}*"