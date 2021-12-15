from tkinter import *
from tkinter import messagebox
import tkinter as tk


def donothing():
    filewin = Toplevel(root)
    button = Button(filewin, text="Do nothing button")
    button.pack()


def input_name():
    def user_input_adventurer_name():
        print("First Name: %s\nLast Name: %s" % (first_name.get(), last_name.get()))
        messagebox.showinfo("Name info", first_name.get() + " " + last_name.get())

    master = tk.Tk()
    tk.Label(master,
             text="First Name").grid(row=0)
    tk.Label(master,
             text="Last Name").grid(row=1)

    first_name = tk.Entry(master)
    last_name = tk.Entry(master)

    first_name.grid(row=0, column=1)
    last_name.grid(row=1, column=1)

    tk.Button(master,
              text='Quit',
              command=master.quit).grid(row=3,
                                        column=0,
                                        sticky=tk.W,
                                        pady=4)
    tk.Button(master,
              text='Show', command=user_input_adventurer_name).grid(row=3,
                                                                    column=1,
                                                                    sticky=tk.W,
                                                                    pady=4)

    tk.mainloop()


def display_instructions():
    instructions = Toplevel(root)
    instructions.title("Instructions")

    button = Button(instructions, font="Verdana 20 bold", text="""Welcome!!! You are about to brave our maze inorder to 
    find the four pillars of OO! Only by collecting these four pillars, will you be able to escape the maze and win the 
    game. In this maze, you will use the 'n' letter to head up, the 'e' letter to go right, the 's' letter to go down 
    and the 'w' letter to go left. Be careful though, for there are pits within the maze that can injure you and if you 
    take to much damage, you will DIE!!! If that happens, the game ends and you'll start over with a new adventurer and 
    a new maze. To help you survive, we have placed some potions within the maze to either restore your HP (health points) 
    or to help you see deeper within the maze.""")
    button.pack()


def quit():
    # end_game = Toplevel(root)
    # button = Button(end_game, text="Game Over!!!")
    # button.pack()
    root.quit()


root = tk.Tk()
root.title("Dungeon Adventure")

tk.Label(root,
         text="Dungeon Adventure",
         fg="light green",
         bg="dark green",
         font="Helvetica 19 bold italic").pack()
tk.Label(root,
         text="by: Kevin Perkins, Fikadu Balcha \n"
              "        & \n"
              "          Nik van Baak",
         fg="yellow",
         bg="black",
         font="Verdana 10 bold").pack()

canvas1 = tk.Canvas(root, width=600, height=400)
canvas1.pack()

# --Buttons
button1 = tk.Button(text='Start')
canvas1.create_window(300, 150, window=button1)
button1.config(command=input_name)

button2 = tk.Button(text='Instruction')
canvas1.create_window(300, 180, window=button2)
button2.config(command=display_instructions)

button3 = tk.Button(text='Quit')
canvas1.create_window(300, 210, window=button3)
button3.config(command=quit)

# --Menu (Help)
menu_bar = Menu(root)
# file_menu = Menu(menu_bar, tearoff=0)


help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Help Index", command=donothing)
help_menu.add_command(label="About...", command=donothing)
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

root.mainloop()