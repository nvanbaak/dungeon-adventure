import tkinter as tk
from adventurer import Adventurer
from dungeon import Dungeon
import PIL
from PIL import ImageTk, Image

from tkinter import *
from tkinter import messagebox

import re

class DungeonAdventure:
    def __init__(self):
        self.__dungeon = None
        self.__adventurer = None
        self.__diff = 1
        self.__root = tk.Tk()
        self.__root.title("Dungeon Adventure")

        self.__start_canvas = None
        self.__game_canvas = None

        self.__dungeon_display = None
        self.__message_log = None
        self.__dungeon_legend = None

        self.__omniscience = False

        self.__game_over = False

        self.start_menu()

    def __start_game(self):
        self.__delete_start_canvas()

        self.__game_canvas = tk.Canvas(self.__root, width=940, height=675)
        self.__game_canvas.pack(fill=tk.BOTH)

        self.__game_bg = tk.PhotoImage(file="background.png")
        self.__game_canvas.create_image(0, 0, anchor=NW, image=self.__game_bg)

        self.__dungeon = Dungeon(self.__diff, self, self.__adventurer)
        textbox_size = self.__dungeon.get_size() * 3

        self.__dungeon_display = tk.Text(self.__game_canvas, width=textbox_size, height=textbox_size+4)
        self.__dungeon_display.pack(anchor=CENTER, padx=140, pady=30, ipadx=20)

        self.__message_log = tk.Text(self.__game_canvas, width=100, height=10)
        self.__message_log.pack(pady=20)
        self.__message_log.config(state="disabled")

        self.draw_map()
        self.announce(self.__adventurer.__str__())

        self.__root.bind("<w>", self.move_player)
        self.__root.bind("<a>", self.move_player)
        self.__root.bind("<s>", self.move_player)
        self.__root.bind("<d>", self.move_player)

        self.__root.bind("<h>", self.use_health_potion)
        self.__root.bind("<j>", self.use_vision_potion)
        self.__root.bind("<q>", self.adventurer_status)

        self.__root.bind("<5>", self.cheat_codes)
        self.__root.bind("<6>", self.cheat_codes)
        self.__root.bind("<7>", self.cheat_codes)
        self.__root.bind("<8>", self.cheat_codes)
        self.__root.bind("<9>", self.cheat_codes)
        self.__root.bind("<0>", self.cheat_codes)

    def move_player(self, keypress):
        """
        Passes keyboard input to dungeon to move the player
        """
        if not self.__game_over:
            dir_dict = {
                "w": "n",
                "a": "w",
                "s": "s",
                "d": "e"
            }
            self.__dungeon.move_player(self.__adventurer, dir_dict[keypress.char])
            self.__adventurer.decay_vision()

            self.draw_map()

            if self.__adventurer.is_dead():
                self.announce(f"{self.__adventurer.get_name()} has tragically expired.")
                self.end_game()

            if self.__game_over:
                self.draw_whole_map()

    def adventurer_status(self, keypress):
        if not self.__game_over:
            self.announce(f"{self.__adventurer.__str__()}")

    def use_health_potion(self, keypress):
        if not self.__game_over:
            self.__adventurer.use_health_potion()

    def use_vision_potion(self, keypress):
        if not self.__game_over:
            self.__adventurer.use_vision_potion()
            self.draw_map()

    def cheat_codes(self, keypress):
        """
        Number keys are cheats
        """
        if not self.__game_over:
            key = keypress.char
            if key == "5":
                self.__omniscience = True
                self.draw_whole_map()
            elif key == "6":
                self.__adventurer.earn_pillar("A")
                self.__adventurer.earn_pillar("I")
                self.__adventurer.earn_pillar("E")
                self.__adventurer.earn_pillar("P")
            elif key == "7":
                self.draw_whole_map()
            elif key == "8":
                for _ in range(0, 50):
                    self.__adventurer.add_vision_potion()
            elif key == "9":
                for _ in range(0, 50):
                    self.__adventurer.add_health_potion()
            elif key == "0":
                self.__adventurer.take_damage(1000, "the developers")
                self.end_game()

    def draw_map(self):
        """
        Gets the dungeon string from Dungeon and displays it in window
        """
        if not self.__omniscience:
            self.__dungeon_display.config(state="normal")
            self.__dungeon_display.delete("1.0", "end")
            self.__dungeon_display.tag_configure("center", justify="center")
            self.__dungeon_display.insert("1.0", "\n\n" + self.__dungeon.display(3,
                    self.__adventurer.get_vision_range()))
            self.__dungeon_display.tag_add("center", "1.0", "end")
            self.__dungeon_display.config(state="disabled")
        else:
            self.draw_whole_map()

    def draw_whole_map(self):
        """
        Prints the entire dungeon to the game window
        """
        self.__dungeon_display.config(state="normal")
        self.__dungeon_display.delete("1.0", "end")
        self.__dungeon_display.insert("1.0", "\n\n" + self.__dungeon.__str__(), "center")
        self.__dungeon_display.config(state="disabled")

    def announce(self, message):

        log_text = self.__message_log.get("1.0", "end")
        log_text += message
        log_text = log_text.split("\n")

        if len(log_text) > 9:
            log_text = log_text[-9:]

        log_text = "\n".join(log_text)

        self.__message_log.config(state="normal")
        self.__message_log.delete("1.0", "end")
        self.__message_log.insert("end", log_text)
        self.__message_log.config(state="disabled")

    def end_game(self):
        self.__game_over = True
        if self.__adventurer.is_dead():
            self.announce("You lose!  Better luck next time!")
        else:
            self.announce("Victory is yours!  You have mastered the four pillars of object-oriented progamming!")
            self.announce("Without them, the dungeon crumbles behind you.")

    def start_menu(self):
        """
        Creates and displays the start menu.
        """
        self.__root.geometry("950x675+50+50")

        self.__start_canvas = tk.Canvas(self.__root, width=940, height=675)
        self.__start_canvas.pack(fill=tk.BOTH)

        self.__title_image = tk.PhotoImage(file="title.png")
        self.__start_canvas.create_image(0, 0, anchor=NW, image=self.__title_image)

        # --Buttons
        st_menu_button1 = tk.Button(text='Start', font="Verdana 10 bold", width=5)
        self.__start_canvas.create_window(220, 580, window=st_menu_button1)
        st_menu_button1.config(command=self.input_name)

        st_menu_button2 = tk.Button(text='Instruction', font="Verdana 10 bold", width=10)
        self.__start_canvas.create_window(480, 580, window=st_menu_button2)
        st_menu_button2.config(command=self.display_instructions)

        st_menu_button3 = tk.Button(text='Quit', font="Verdana 10 bold", width=5)
        self.__start_canvas.create_window(740, 580, window=st_menu_button3)
        st_menu_button3.config(command=quit)

        # --Menu (Help)
        menu_bar = Menu(self.__root)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Cheats", command=self.cheats)
        help_menu.add_command(label="Dungeon Key", command=self.dungeon_key_images)
        help_menu.add_command(label="Help request", command=self.donothing)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.__root.config(menu=menu_bar)

    def __delete_start_canvas(self):
        self.__start_canvas.destroy()

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

            numbers_only = re.compile("[0-9]*")
            attempt_difficulty = diff.get()
            if numbers_only.fullmatch(attempt_difficulty):
                self.__diff = int(diff.get())
            else:
                print("Use numbers ya goof")
                return

            if 4 > int(self.__diff) and int(self.__diff) > 0:
                print(f"Name: {adv_name.get()}\nDifficulty: {diff.get()}")
                self.__adventurer = Adventurer(adv_name.get(), self)
                self.__delete_start_canvas()
                self.__start_game()
                return
            else:
                print("Please enter a difficulty between 1 and 3.")

        tk.Label(self.__start_canvas,
                 text="Player Name").place(x=30, y=610)
        tk.Label(self.__start_canvas,
                 text="Difficulty").place(x=250, y=610)

        adv_name = tk.Entry(self.__start_canvas)
        diff = tk.Entry(self.__start_canvas)

        adv_name.place(x=110, y=610)
        diff.place(x=310, y=610)

        tk.Button(self.__start_canvas,
                  text='Quit',
                  command=self.__root.destroy).place(x=250, y=640)

        tk.Button(self.__start_canvas,
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
        self.__root.mainloop()