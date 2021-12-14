import tkinter as tk
from adventurer import Adventurer
from dungeon import Dungeon

from tkinter import *
from tkinter import messagebox

class DungeonAdventure():
    def __init__(self):
        self.dungeon = None
        self.adventurer = None
        self.root = tk.Tk()
        self.root.title("Dungeon Adventure")
        self.start_menu()


    def start_game(self):
        pass

    def announce(self, message):
        pass

    def end_game(self):
        pass


    def start_menu(self):
        tk.Label(self.root,
            text="Dungeon Adventure",
            fg="light green",
            bg="dark green",
            font="Helvetica 19 bold italic").pack()
        tk.Label(self.root,
            text="by: Kevin Perkins, Fikadu Balcha \n"
                "        & \n"
                "          Nik van Baak",
            fg="yellow",
            bg="black",
            font="Verdana 10 bold").pack()

        canvas1 = tk.Canvas(self.root, width=600, height=400)
        canvas1.pack()

        # --Buttons
        button1 = tk.Button(text='Start')
        canvas1.create_window(300, 150, window=button1)
        button1.config(command=self.input_name)

        button2 = tk.Button(text='Instruction')
        canvas1.create_window(300, 180, window=button2)
        button2.config(command=self.display_instructions)

        button3 = tk.Button(text='Quit')
        canvas1.create_window(300, 210, window=button3)
        button3.config(command=quit)

        # --Menu (Help)
        menu_bar = Menu(self.root)
        # file_menu = Menu(menu_bar, tearoff=0)


        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help Index", command=self.donothing)
        help_menu.add_command(label="About...", command=self.donothing)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)


    def donothing(self):
        filewin = Toplevel(self.root)
        button = Button(filewin, text="Do nothing button")
        button.pack()


    def input_name(self):
        def user_input_adventurer_name():
            print(f"Name: {adv_name.get()}\nDifficulty: {selected_difficulty}")
            messagebox.showinfo("Name info", adv_name.get())
            self.adventurer = Adventurer(adv_name.get(), self)

        master = tk.Tk()
        tk.Label(master,
                text="First Name").grid(row=0)
        tk.Label(master,
                text="Difficulty").grid(row=1, rowspan=2)

        adv_name = tk.Entry(master)

        selected_difficulty = 1
        easy = tk.Radiobutton(master, value=1, variable=selected_difficulty)
        medium = tk.Radiobutton(master, value=2, variable=selected_difficulty)
        hard = tk.Radiobutton(master, value=3, variable=selected_difficulty)

        adv_name.grid(row=0, column=1, columnspan=3)
        easy.grid(row=1, column=1)
        medium.grid(row=1, column=2)
        hard.grid(row=1, column=3)

        tk.Button(master,
                text='Quit',
                command=master.quit).grid(row=4,
                                            column=2,
                                            columnspan=2,
                                            sticky=tk.W,
                                            pady=4)
        tk.Button(master,
                text='Show', command=user_input_adventurer_name).grid(row=4,
                                                                        column=0,
                                                                        columnspan=2,
                                                                        sticky=tk.W,
                                                                        pady=4)

        tk.mainloop()


    def display_instructions(self):
        instructions = Toplevel(self.root)
        instructions.title("Instructions")

        button = Button(instructions, font="Verdana 20 bold", text="""Welcome!!! You are about to brave our maze inorder to 
        find the four pillars of OO! Only by collecting these four pillars, will you be able to escape the maze and win the 
        game. In this maze, you will use the 'n' letter to head up, the 'e' letter to go right, the 's' letter to go down 
        and the 'w' letter to go left. Be careful though, for there are pits within the maze that can injure you and if you 
        take to much damage, you will DIE!!! If that happens, the game ends and you'll start over with a new adventurer and 
        a new maze. To help you survive, we have placed some potions within the maze to either restore your HP (health points) 
        or to help you see deeper within the maze.""")
        button.pack()


    # def quit(self):
    #     # end_game = Toplevel(root)
    #     # button = Button(end_game, text="Game Over!!!")
    #     # button.pack()
    #     self.root.quit()

    def start_loop(self):
        self.root.mainloop()

