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
        self.__root = tk.Tk()
        self.__root.title("Dungeon Adventure")
        self.start_menu()

    def __start_game(self, diff):
        self.__dungeon = Dungeon(diff, self, self.__adventurer)

        game_canvas = tk.Canvas(self.__root, width=940, height=675)
        game_canvas.pack(expand=tk.YES, fill=tk.BOTH)

        button_n = tk.Button(text="Move North")
        button_n.config(command=self.__dungeon.move_north)
        button_n.pack()

        text_area = tk.Text(self.__root, width=940, height=600)

        game_canvas.create_window(650, 500)

        self.hypothetical_game_loop(game_canvas, text_area)

    def hypothetical_game_loop(self, game_canvas, text_area):

        # display dungeon using .display() method

        # wait for player input

        # if potion use, use potion

        # if move, attempt move
        pass

    def announce(self, message):
        pass

    def end_game(self):
        pass

    def start_menu(self):
        # self.__root.geometry("940x675")
        # canvas2 = tk.Canvas(self.__root, bg="gray16", height=1000, width=1000)
        # self.title_image = tk.PhotoImage(file="title_screen.png")
        # background_label = Label(self.__root, image=self.title_image, )
        # background_label.place(x=0, y=0, relwidth=1, relheight=1)
        #
        # canvas2.pack(expand=NO, fill=NONE)

        canvas2 = tk.Canvas(self.__root, width=940, height=675)
        canvas2.pack(expand=tk.YES, fill=tk.BOTH)

        self.title_image = tk.PhotoImage(file="title.png")
        canvas2.create_image(0, 0, anchor=NW, image=self.title_image)

        # --Buttons
        button1 = tk.Button(text='Start', font="Verdana 10 bold", width=5)
        canvas2.create_window(650, 500, window=button1)
        button1.config(command=self.input_name)

        button2 = tk.Button(text='Instruction', font="Verdana 10 bold", width=10)
        canvas2.create_window(650, 530, window=button2)
        button2.config(command=self.display_instructions)

        button3 = tk.Button(text='Quit', font="Verdana 10 bold", width=5)
        canvas2.create_window(650, 560, window=button3)
        button3.config(command=quit)

        # --Menu (Help)
        menu_bar = Menu(self.__root)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help request", command=self.donothing)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.__root.config(menu=menu_bar)

    def donothing(self):
        filewin = Toplevel(self.__root)
        button = Button(filewin, text="Help yourself fool!!! \n Read a book or something!!!", font="Verdana 20 bold",
                        width=40)
        button.pack()

    def input_name(self):
        def user_input_adventurer_name():
            print(f"Name: {adv_name.get()}\nDifficulty: {diff.get()}")
            messagebox.showinfo("Name info", adv_name.get())
            self.__adventurer = Adventurer(adv_name.get(), self)
            self.__start_game(int(diff.get()))

        master = tk.Tk()
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

        tk.mainloop()

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