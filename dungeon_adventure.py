import tkinter as tk
from adventurer import Adventurer
from dungeon import Dungeon
import PIL
from PIL import ImageTk, Image

from tkinter import *
from tkinter import messagebox


class DungeonAdventure:
    def __init__(self):
        self.__dungeon = None
        self.__adventurer = None
        self.__diff = 1
        self.__root = tk.Tk()
        self.__root.title("Dungeon Adventure")

        self.__start_canvas = None
        self.__st_menu_button1 = None
        self.__st_menu_button2 = None
        self.__st_menu_button3 = None

        self.__input_name = None
        self.__in_menu_button1 = None
        self.__in_menu_button2 = None

        self.__text_area = None

        self.start_menu()

    def __start_game(self):
        self.__adventurer = Adventurer("Test Adventurer", self)
        self.__delete_start_menu()

        self.__dungeon = Dungeon(self.__diff, self, self.__adventurer)
        self.__dungeon.generate()

        self.__text_area = tk.Text(self.__root, width=200, height=45)
        self.__text_area.pack(anchor=NW)

        self.__text_area.insert("1.0", self.__dungeon.display(3, 0))
        self.__text_area.config(state="disabled")

        self.__root.bind("<w>", self.move_player)
        self.__root.bind("<a>", self.move_player)
        self.__root.bind("<s>", self.move_player)
        self.__root.bind("<d>", self.move_player)

        self.__root.bind("<h>", self.use_health_potion)
        self.__root.bind("<j>", self.use_vision_potion)
        self.__root.bind("<q>", self.adventurer_status)

        self.__root.bind("<7>", self.cheat_codes)
        self.__root.bind("<8>", self.cheat_codes)
        self.__root.bind("<9>", self.cheat_codes)

    def move_player(self, keypress):
        """
        Passes keyboard input to dungeon to move the player
        """
        dir_dict = {
            "w": "n",
            "a": "w",
            "s": "s",
            "d": "e"
        }
        self.__dungeon.move_player(self.__adventurer, dir_dict[keypress.char])
        self.__adventurer.decay_vision()

        self.draw_map()

    def adventurer_status(self, keypress):
        self.announce(f"{self.__adventurer.__str__()}")

    def use_health_potion(self, keypress):
        self.__adventurer.use_health_potion()

    def use_vision_potion(self, keypress):
        self.__adventurer.use_vision_potion()
        self.draw_map()

    def cheat_codes(self, keypress):
        """
        Number keys are cheats
        """
        key = keypress.char
        if key == "7":
            self.draw_whole_map()
        elif key == "8":
            self.__adventurer.add_vision_potion()
        elif key == "9":
            self.__adventurer.add_health_potion()

    def draw_map(self):
        self.__text_area.config(state="normal")
        self.__text_area.delete("1.0", "end")
        self.__text_area.insert("1.0", self.__dungeon.display(3,
                                                              self.__adventurer.get_vision_range()))
        self.__text_area.config(state="disabled")

    def draw_whole_map(self):
        """
        Prints the entire dungeon to the game window
        """
        self.__text_area.config(state="normal")
        self.__text_area.delete("1.0", "end")
        self.__text_area.insert("1.0", self.__dungeon.__str__())
        self.__text_area.config(state="disabled")

    def announce(self, message):
        print(message)

    def end_game(self):
        pass

    def start_menu(self):
        """
        Creates and displays the start menu.
        """

        self.__start_canvas = tk.Canvas(self.__root, width=940, height=675)
        self.__start_canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.title_image = tk.PhotoImage(file="title.png")
        self.__start_canvas.create_image(0, 0, anchor=NW, image=self.title_image)

        # --Buttons
        self.__st_menu_button1 = tk.Button(text='Start', font="Verdana 10 bold", width=5)
        self.__start_canvas.create_window(220, 580, window=self.__st_menu_button1)
        self.__st_menu_button1.config(command=lambda: [self.input_name(), self.__delete_start_menu_buttons()])

        self.__st_menu_button2 = tk.Button(text='Instruction', font="Verdana 10 bold", width=10)
        self.__start_canvas.create_window(480, 580, window=self.__st_menu_button2)
        self.__st_menu_button2.config(command=self.display_instructions)

        self.__st_menu_button3 = tk.Button(text='Quit', font="Verdana 10 bold", width=5)
        self.__start_canvas.create_window(740, 580, window=self.__st_menu_button3)
        self.__st_menu_button3.config(command=quit)

        # --Menu (Help)
        menu_bar = Menu(self.__root)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Cheats", command=self.cheats)
        help_menu.add_command(label="Dungeon Key", command=self.dungeon_key_images)
        help_menu.add_command(label="Help request", command=self.donothing)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.__root.config(menu=menu_bar)

    def __delete_start_menu(self):
        self.__start_canvas.pack_forget()
        self.__st_menu_button1.pack_forget()
        self.__st_menu_button2.pack_forget()
        self.__st_menu_button3.pack_forget()

    def __delete_start_menu_buttons(self):
        self.__st_menu_button1.pack_forget()
        self.__st_menu_button2.pack_forget()
        self.__st_menu_button3.pack_forget()

    def resizer(self, e):

        global bg, resized_bg, new_bg
        # Open image
        bg = PIL.Image.open("title.png")

        # resize image
        resize_bg = bg.resize((e.width, e.height), PIL.Image.ANTIALIAS)

        # define image
        new_bg = PIL.ImageTk.PhotoImage(resize_bg)

        # Add back to Canvas
        self.__start_canvas.create_image(0, 0, anchor=NW, image=new_bg)

    def donothing(self):
        filewin = Toplevel(self.__root)
        button = Button(filewin, text="Help yourself fool!!! \n Read a book or something!!!", font="Verdana 20 bold",
                        width=40)
        button.pack()

    def cheats(self):
        codes = Toplevel(self.__root)
        button = Button(codes, text="""There are currently three codes that you can use by typing them on your keyboard (while you are in the maze.) 
        7 = See the whole map (note, this ends as soon as you move) \n8 = Increases your vision potion count by 1 
        9 = Increases your health potions by 1""", font="Verdana 15 bold",
                        width=90)
        button.pack()

    def input_name(self):
        def user_input_adventurer_name():
            try:
                # if 1 <= int(diff.get()) >= 3 or int(diff.get()) != int:
                if diff.get() == "1" or diff.get() == "2" or diff.get() == "3":

                    print(f"Name: {adv_name.get()}\nDifficulty: {int(diff.get())}")
                    self.__adventurer = Adventurer(adv_name.get(), self)
                    # self.__delete_start_menu_buttons()
                    self.__delete_start_menu()
                    self.__start_game()
                    # self.__delete_start_menu_buttons()
                    # self.__root.after(1000,  self.__root.destroy())
                    return True
            except ValueError:
                print("Error!!! Please input a values 1, 2 or 3 for difficulty please.")

        self.__delete_start_menu_buttons()

        tk.Label(self.__root,
                 text="Player Name").place(x=30, y=610)
        tk.Label(self.__root,
                 text="Difficulty").place(x=250, y=610)

        adv_name = tk.Entry(self.__root)
        diff = tk.Entry(self.__root)

        adv_name.place(x=110, y=610)
        diff.place(x=310, y=610)

        tk.Button(self.__root,
                  text='Quit',
                  command=self.__root.destroy).place(x=250, y=640)

        tk.Button(self.__root,
                  text='Accept', command=user_input_adventurer_name).place(x=30, y=640)

    def display_instructions(self):
        instructions = Toplevel(self.__root)
        instructions.title("Instructions")

        button = Button(instructions, font="Verdana 19 bold", text="""Welcome!!! You are about to brave our maze 
        inorder to find the four pillars of OO! Only by collecting these four pillars, will you be able to escape the 
        maze and win the game. In this maze, you will use the 'w' letter to head up, the 'd' letter to go right, 
        the 's' letter to go down and the 'a' letter to go left. Be careful though, for there are pits within the 
        maze that can injure you and if you take to much damage, you will DIE!!! If that happens, the game ends and 
        you'll start over with a new adventurer and a new maze. To help you survive, we have placed some potions 
        within the maze to either restore your HP (health points) by pressing the 'h' button. Or, to help you see 
        deeper within the maze, press the 'j' button. Once you've found all four pillars of OO, find the room with 
        the 0 mark in the maze and enter it to complete the maze.""")
        button.pack()

    def dungeon_key_images(self):
        dungeon_key = Toplevel(self.__root)
        dungeon_key.title("Dungeon Key")

        button = Button(dungeon_key, text="""Here is the key for images you will find within the dungeon's maze: \n
        @ = The Adventurer
        A = pillar of Abstraction
        E = Pillar of Encapsulation
        I = Pillar of Inheritance
        P = Pillar of Polymorphism
        0 = Exit (Remember that it won't activate until you get all four pillars)
        X = A Pit (removes some HP on enter)
        H = Health Potion (is added into your inventory and removed from room on enter)
        V = Vision Potion (is added into your inventory and removed from room on enter)
        M = Both Potions (is added into your inventory and removed from room on enter)
        " " = Blank Room (nothing to see here move along)
        | = Wall (can't move through this)""", font="Verdana 13 bold", )
        button.pack()

    def start_loop(self):
        self.__root.bind('<Configure>', self.resizer)
        self.__root.mainloop()