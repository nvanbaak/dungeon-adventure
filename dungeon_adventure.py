import tkinter as tk
from adventurer import Adventurer
from dungeon import Dungeon
# from PIL import ImageTk, Image

from tkinter import *
from tkinter import messagebox


class DungeonAdventure():
    def __init__(self):
        self.__dungeon = None
        self.__adventurer = None
        self.__diff = None
        self.__root = tk.Tk()
        self.__root.title("Dungeon Adventure")

        self.__start_canvas = None
        self.__st_menu_button1 = None
        self.__st_menu_button2 = None
        self.__st_menu_button3 = None

        self.__input_name = None
        self.__in_menu_button1 = None
        self.__in_menu_button2 = None




        self.__name_input_window = None

        self.start_menu()

    def __start_game(self, diff):
        self.__dungeon = Dungeon(diff, self, self.__adventurer)

        text_area = tk.Text(self.__root, width=50, height=50)
        text_area.pack(anchor=NW)

        button_n = tk.Button(text="Move North")
        button_n.config(command=self.__dungeon.move_north)
        button_n.pack()

        self.hypothetical_game_loop(text_area)

    def hypothetical_game_loop(self, text_area : tk.Text):

        # display dungeon using .display() method
        text_area.insert("1.0", self.__dungeon.display(3))

        # wait for player input

        # if potion use, use potion

        # if move, attempt move
        self.__root.after(40, self.hypothetical_game_loop(text_area))
        pass

    def announce(self, message):
        pass

    def end_game(self):
        pass

    def start_menu(self):
        """
        Creates and displays the start menu.
        """

        self.__start_canvas = tk.Canvas(self.__root, width=940, height=675)
        self.__start_canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.title_image = tk.PhotoImage(file="title_screen.png")
        self.__start_canvas.create_image(0, 0, anchor=NW, image=self.title_image)

        # --Buttons
        self.__st_menu_button1 = tk.Button(text='Start', font="Verdana 10 bold", width=5)
        self.__start_canvas.create_window(220, 580, window=self.__st_menu_button1)
        self.__st_menu_button1.config(command=self.input_name)

        self.__st_menu_button2 = tk.Button(text='Instruction', font="Verdana 10 bold", width=10)
        self.__start_canvas.create_window(480, 580, window=self.__st_menu_button2)
        self.__st_menu_button2.config(command=self.display_instructions)

        self.__st_menu_button3 = tk.Button(text='Quit', font="Verdana 10 bold", width=5)
        self.__start_canvas.create_window(740, 580, window=self.__st_menu_button3)
        self.__st_menu_button3.config(command=quit)

        # --Menu (Help)
        menu_bar = Menu(self.__root)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help request", command=self.donothing)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.__root.config(menu=menu_bar)

    def __delete_start_menu(self):
        self.__start_canvas.pack_forget()
        self.__st_menu_button1.pack_forget()
        self.__st_menu_button2.pack_forget()
        self.__st_menu_button3.pack_forget()

    def __delete_input_name(self):
        self.__input_name.pack_forget()
        self.__in_menu_button1.pack_forget()
        self.__in_menu_button2.pack_forget()

    def donothing(self):
        filewin = Toplevel(self.__root)
        button = Button(filewin, text="Help yourself fool!!! \n Read a book or something!!!", font="Verdana 20 bold",
                        width=40)
        button.pack()

    def input_name(self):
        master = tk.Tk()

        def user_input_adventurer_name():
            print(f"Name: {adv_name.get()}\nDifficulty: {diff.get()}")
            self.__adventurer = Adventurer(adv_name.get(), self)
            self.__delete_start_menu()
            self.__start_game(int(diff.get()))
            # master.after(5000, master.destroy)


            # self.__delete_input_name()
            # master.destroy()

            # self.__delete_input_name()


        # master = tk.Tk()
        tk.Label(master,
                 text="First Name").grid(row=0)
        tk.Label(master,
                 text="Difficulty").grid(row=1, rowspan=2)

        adv_name = tk.Entry(master)
        diff = tk.Entry(master)

        # selected_difficulty = 1
        # easy = tk.Radiobutton(master, value=1, variable=selected_difficulty)
        # medium = tk.Radiobutton(master, value=2, variable=selected_difficulty)
        # hard = tk.Radiobutton(master, value=3, variable=selected_difficulty)

        adv_name.grid(row=0, column=1, columnspan=1)
        diff.grid(row=1, column=1)
        # easy.grid(row=1, column=1)
        # medium.grid(row=1, column=2)
        # hard.grid(row=1, column=3)

        tk.Button(master,
                  text='Quit',
                  command=master.destroy).grid(row=4,
                                               column=2,
                                               columnspan=2,
                                               sticky=tk.W,
                                               pady=4)
        tk.Button(master,
                  text='Accept', command=user_input_adventurer_name).grid(row=4,
                                                                          column=0,
                                                                          columnspan=2,
                                                                          sticky=tk.W,
                                                                          pady=4)

        # if user_input_adventurer_name is True:
        #     master.destroy()
        # tk.mainloop()

        master.after(10000, master.destroy)

    def display_instructions(self):
        instructions = Toplevel(self.__root)
        instructions.title("Instructions")

        button = Button(instructions, font="Verdana 19 bold", text="""Welcome!!! You are about to brave our maze inorder to 
        find the four pillars of OO! Only by collecting these four pillars, will you be able to escape the maze and win the 
        game. In this maze, you will use the 'n' letter to head up, the 'e' letter to go right, the 's' letter to go down 
        and the 'w' letter to go left. Be careful though, for there are pits within the maze that can injure you and if you 
        take to much damage, you will DIE!!! If that happens, the game ends and you'll start over with a new adventurer and 
        a new maze. To help you survive, we have placed some potions within the maze to either restore your HP (health points) 
        or to help you see deeper within the maze.""")
        button.pack()

    def start_loop(self):
        self.__root.mainloop()