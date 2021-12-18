import tkinter as tk
from adventurer import Adventurer
from dungeon import Dungeon

from tkinter import *

import re

class DungeonAdventure:
    def __init__(self):
        self.__dungeon = None
        self.__adventurer = None
        self.__diff = 1
        self.__root = tk.Tk()
        self.__window_size = (1150, 875)
        self.__root.geometry(f"{self.__window_size[0]}x{self.__window_size[1]}+250+100")
        self.__root.title("Dungeon Adventure")

        self.__intro_slide = 0

        self.__start_canvas = None

        self.__dungeon_display = None
        self.__message_log = None
        self.__legend = None

        self.__omniscience = False
        self.__game_over = False

        self.__make_help_menu()
        self.__initialize_intro()

    def start_loop(self):
        """
        Begins the main loop
        """
        self.__root.mainloop()

    ##################################
    #          GUI methods
    ##################################

    def __initialize_intro(self):
        """
        Sets up canvas for intro slides, then calls the intro method.
        """

        self.__start_canvas = tk.Canvas(self.__root, width=self.__window_size[0], height=self.__window_size[1])
        self.__start_canvas.configure(bg="#FFBF90")

        self.__start_canvas.pack(expand=True)

        self.__root.bind("<Button-1>", self.__advance_intro)

        self.__advance_intro(None)

    def __advance_intro(self, keypress):
        """
        Each time the method is called, changes the image to create a pseudo-slideshow.
        When the last slide is reached, calls the start menu.
        """
        if self.__intro_slide == 0:
            self.__title_image = tk.PhotoImage(file="assets/intro_1.png")
            self.__start_canvas.create_image(
                    self.__window_size[0]//2, self.__window_size[1]//2, anchor=CENTER, image=self.__title_image)
            self.__intro_slide += 1
        elif self.__intro_slide == 1:
            self.__title_image = tk.PhotoImage(file="assets/intro_2.png")
            self.__start_canvas.create_image(
                    self.__window_size[0]//2, self.__window_size[1]//2, anchor=CENTER, image=self.__title_image)
            self.__intro_slide += 1
        elif self.__intro_slide == 2:
            self.__title_image = tk.PhotoImage(file="assets/intro_3.png")
            self.__start_canvas.create_image(
                    self.__window_size[0]//2, self.__window_size[1]//2, anchor=CENTER, image=self.__title_image)
            self.__intro_slide += 1
        elif self.__intro_slide == 3:
            self.__title_image = tk.PhotoImage(file="assets/controls.png")
            self.__start_canvas.create_image(
                    self.__window_size[0]//2, self.__window_size[1]//2, anchor=CENTER, image=self.__title_image)
            self.__intro_slide += 1
        elif self.__intro_slide == 4:
            self.__title_image = tk.PhotoImage(file="assets/objectives.png")
            self.__start_canvas.create_image(
                    self.__window_size[0]//2, self.__window_size[1]//2, anchor=CENTER, image=self.__title_image)
            self.__intro_slide += 1
        elif self.__intro_slide == 5:
            self.__start_canvas.destroy()
            self.__root.unbind("<Button-1>")
            self.__start_menu()

    def __start_game(self):
        """
        Sets up the main game interface and binds the controls to enable play.
        """
        self.__reset_start_canvas(None)

        # Setup dungeon & get size
        self.__dungeon = Dungeon(self.__diff, self, self.__adventurer)
        textbox_size = self.__dungeon.get_size() * 3
        tb_y = self.__window_size[1]//2

        # build legend textbox
        self.__legend = tk.Text(self.__start_canvas, width=38, height=textbox_size)
        self.__legend.place(x=0, y=tb_y, anchor="w")

        spacer = "\n" * ((textbox_size - 10) // 2)
        self.__legend.insert("end", 
                spacer + "           *****LEGEND***** \n\n    @ = The Adventurer\n    A = pillar of Abstraction\n    E = Pillar of Encapsulation\n    I = Pillar of Inheritance\n    P = Pillar of Polymorphism\n    0 = Exit\n    X = Pit (watch out!)\n    H = Health Potion\n    V = Vision Potion\n    M = Both Potions\n    | = Wall")
        self.__legend.config(state="disabled")

        # build dungeon display
        self.__dungeon_display = tk.Text(self.__start_canvas, width=textbox_size, height=textbox_size)
        self.__dungeon_display.place(x=self.__window_size[0]//2, y=tb_y, anchor=CENTER)

        # build message box
        self.__message_log = tk.Text(self.__start_canvas, width=40, height=textbox_size)
        self.__message_log.place(x=self.__window_size[0], y=tb_y, anchor="e")
        self.__message_log.config(state="disabled")

        self.__draw_map()
        self.announce(self.__adventurer.__str__())

        # keybinds
        self.__root.bind("<w>", self.__move_player)
        self.__root.bind("<a>", self.__move_player)
        self.__root.bind("<s>", self.__move_player)
        self.__root.bind("<d>", self.__move_player)

        self.__root.bind("<h>", self.__use_health_potion)
        self.__root.bind("<j>", self.__use_vision_potion)
        self.__root.bind("<q>", self.__adventurer_status)

        self.__root.bind("<p>", self.__cheat_codes)
        self.__root.bind("<6>", self.__cheat_codes)
        self.__root.bind("<7>", self.__cheat_codes)
        self.__root.bind("<8>", self.__cheat_codes)
        self.__root.bind("<9>", self.__cheat_codes)
        self.__root.bind("<0>", self.__cheat_codes)

    def __start_menu(self):
        """
        Creates and displays the start menu.
        """
        if not self.__start_canvas:
            self.__start_canvas = tk.Canvas(self.__root, width=self.__window_size[0], height=self.__window_size[1])
            self.__start_canvas.pack(expand=True)

            self.__title_image = tk.PhotoImage(file="title.png")
            self.__start_canvas.create_image(self.__window_size[0]//2, self.__window_size[1]//2, anchor=CENTER, image=self.__title_image)
        else:
            self.__reset_start_canvas("assets/title.png")

        # --Buttons
        button_y = self.__window_size[1]//2 + 240
        button_x = self.__window_size[0]//2 - 40

        st_menu_button1 = tk.Button(text='Start', font="Verdana 10 bold", width=5)
        self.__start_canvas.create_window(button_x-260, button_y, window=st_menu_button1)
        st_menu_button1.config(command=self.__input_name)

        st_menu_button2 = tk.Button(text='Instruction', font="Verdana 10 bold", width=10)
        self.__start_canvas.create_window(button_x, button_y, window=st_menu_button2)
        st_menu_button2.config(command=self.__display_instructions)

        st_menu_button3 = tk.Button(text='Quit', font="Verdana 10 bold", width=5)
        self.__start_canvas.create_window(button_x+260, button_y, window=st_menu_button3)
        st_menu_button3.config(command=quit)

    def __reset_start_canvas(self, file_str):
        """
        Resets the canvas by deleting it and making a fresh one.
        """
        self.__start_canvas.destroy()
        self.__start_canvas = tk.Canvas(self.__root, width=self.__window_size[0], height=self.__window_size[1])
        self.__start_canvas.configure(bg="#FFBF90")
        self.__start_canvas.pack(expand=True)

        if file_str:
            self.__title_image = tk.PhotoImage(file=file_str)
            self.__start_canvas.create_image(self.__window_size[0]//2, self.__window_size[1]//2, anchor=CENTER, image=self.__title_image)

    ##################################
    #         Menu Methods
    ##################################

    def __make_help_menu(self):
        """
        Creates the help menu and addes it to application menu.
        """
        # --Menu (Help)
        menu_bar = Menu(self.__root)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Cheats", command=self.__display_cheats)
        help_menu.add_command(label="Dungeon Key", command=self.__dungeon_key_images)
        help_menu.add_command(label="Help request", command=self.__donothing)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.__root.config(menu=menu_bar)

    def __donothing(self):
        """
        Taunts the player for daring to ask for help.
        """
        filewin = Toplevel(self.__root)
        button = Button(filewin, text="Help yourself fool!!! \n Read a book or something!!!", font="Verdana 20 bold",
                        width=40)
        button.pack()

    def __display_cheats(self):
        """
        Menu option explaining the cheats.
        """
        codes = Toplevel(self.__root)
        button = Button(codes, text="""There are currently five codes that you can use by typing them on your keyboard (while you are in the maze.) 
        6 = Draw whole map (the whole maze is displayed permanently. (Recommended for people who hate fun)) 
        7 = See the whole map (note, this ends as soon as you move) 
        8 = Increases your health & vision potion count by 50!!! 
        9 = Gives the adventurer all four pillars of OO
        0 = developers hate the player, - 1000 HP. Your Dead
        p = Reset the map""", font="Verdana 15 bold",
                        width=90)
        button.pack()

    def __input_name(self):
        """
        Replaces start menu with entry fields for player name and difficulty.
        """
        def __user_input_adventurer_name():

            numbers_only = re.compile("[0-9]*")
            attempt_difficulty = diff.get()
            if numbers_only.fullmatch(attempt_difficulty):
                self.__diff = int(diff.get())
            else:
                print("Use numbers ya goof")
                return

            if 4 > int(self.__diff) and int(self.__diff) > 0:
                self.__adventurer = Adventurer(adv_name.get(), self)
                self.__reset_start_canvas("assets/background.png")
                self.__start_game()
                return
            else:
                print("Please enter a difficulty between 1 and 3.")

        self.__reset_start_canvas("assets/title.png")

        button_y = self.__window_size[1]//2 + 240
        button_x = self.__window_size[0]//2 - 100

        tk.Label(self.__start_canvas,
                 text="Player Name").place(x=button_x-110, y=button_y-40)
        tk.Label(self.__start_canvas,
                 text="Difficulty (1-3):").place(x=button_x-110, y=button_y)

        adv_name = tk.Entry(self.__start_canvas)
        diff = tk.Entry(self.__start_canvas)

        adv_name.place(x=button_x, y=button_y-40)
        diff.place(x=button_x, y=button_y)

        tk.Button(self.__start_canvas,
                  text='Quit',
                  command=self.__root.destroy).place(x=button_x+200, y=button_y)

        tk.Button(self.__start_canvas,
                  text='Accept', command=__user_input_adventurer_name).place(x=button_x+200, y=button_y-40)

    def __display_instructions(self):
        """
        Gives the player a briefing on how to play the game.
        """
        instructions = Toplevel(self.__root)
        instructions.title("Instructions")

        button = Button(instructions, font="Verdana 19 bold", text="""Welcome!!! You are about to brave our maze 
        inorder to find the four pillars of OO! Only by collecting these four pillars, will you be able to escape the 
        maze and win the game. In this maze, you will use the 'w' letter to head up, the 'd' letter to go right, 
        the 's' letter to go down and the 'a' letter to go left. Be careful though, for there are pits within the 
        maze that can injure you and if you take to much damage, you will DIE!!! If that happens, the game ends and 
        you'll start over with a new adventurer and a new maze. To help you survive, we have placed some potions 
        within the maze to either restore your HP (health points) by pressing the 'h' button. Or, to help you see 
        deeper within the maze, press the 'j' button. If You wish to check your adventurers stats, press the 'q' button.
        Once you've found all four pillars of OO, find the room with the 0 mark in the maze and enter it to complete the
        maze. Important to note, if the edges have holes, you can walk through them and it'll warp you to the other 
        side of the maze!!!""")
        button.pack()

    def __dungeon_key_images(self):
        """
        Displays a legend for the dungeon screen.
        """
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


    ##################################
    #      User Keyboard Actions
    ##################################

    def __move_player(self, keypress):
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

            self.__draw_map()

            if self.__adventurer.is_dead():
                self.announce(f"{self.__adventurer.get_name()} has tragically expired.")
                self.end_game()

            if self.__game_over:
                self.__draw_whole_map()

    def __adventurer_status(self, keypress):
        """
        Prints adventurer status to announcements.
        """
        if not self.__game_over:
            self.announce(f"{self.__adventurer.__str__()}")

    def __use_health_potion(self, keypress):
        """
        Has the adventurer drink a health potion.
        """
        if not self.__game_over:
            self.__adventurer.use_health_potion()

    def __use_vision_potion(self, keypress):
        """
        Has the adventurer drink a vision potion.
        """
        if not self.__game_over:
            self.__adventurer.use_vision_potion()
            self.__draw_map()

    def __cheat_codes(self, keypress):
        """
        Enables various cheats when number keys are pressed.
        """
        if not self.__game_over:
            key = keypress.char
            if key == "p":
                self.__start_game()
            if key == "6":
                self.__draw_whole_map()
            elif key == "7":
                self.__omniscience = True
                self.__draw_whole_map()
            elif key == "8":
                for _ in range(0, 50):
                    self.__adventurer.add_vision_potion()
                    self.__adventurer.add_health_potion()
            elif key == "9":
                self.__adventurer.earn_pillar("A")
                self.__adventurer.earn_pillar("I")
                self.__adventurer.earn_pillar("E")
                self.__adventurer.earn_pillar("P")
            elif key == "0":
                self.__adventurer.take_damage(1000, "the developers")
                self.__draw_whole_map()
                self.end_game()

    ##################################
    #      Game Functionality
    ##################################

    def __draw_map(self):
        """
        Gets the dungeon string from Dungeon and displays it in window
        """
        if not self.__omniscience:
            self.__dungeon_display.config(state="normal")
            self.__dungeon_display.delete("1.0", "end")
            self.__dungeon_display.tag_configure("center", justify="center")
            self.__dungeon_display.insert("1.0", self.__dungeon.display(3,
                    self.__adventurer.get_vision_range()))
            self.__dungeon_display.tag_add("center", "1.0", "end")
            self.__dungeon_display.config(state="disabled")
        else:
            self.__draw_whole_map()

    def __draw_whole_map(self):
        """
        Prints the entire dungeon to the game window
        """
        self.__dungeon_display.config(state="normal")
        self.__dungeon_display.delete("1.0", "end")
        self.__dungeon_display.insert("1.0", self.__dungeon.__str__(), "center")
        self.__dungeon_display.config(state="disabled")

    def announce(self, message):
        """
        Given a string, prints it to the message log
        """

        log_text = self.__message_log.get("1.0", "end")
        log_text += message
        log_text = log_text.split("\n")

        log_length = self.__dungeon.get_size() * 3 - 5

        if len(log_text) > log_length:
            log_text = log_text[-log_length:]

        log_text = "\n".join(log_text)

        self.__message_log.config(state="normal")
        self.__message_log.delete("1.0", "end")
        self.__message_log.insert("end", log_text)
        self.__message_log.config(state="disabled")

    def end_game(self):
        """
        Ends the game and makes the appropriate announcements.
        """
        self.__game_over = True
        self.announce(self.__adventurer.__str__())
        if self.__adventurer.is_dead():
            self.announce("You lose!  Better luck next time!")
        else:
            self.announce("Victory is yours!\nYou have taken the four pillars of object-oriented \nprogamming!")
            self.announce("Without them, the dungeon crumbles behind you.  Whoops!")
