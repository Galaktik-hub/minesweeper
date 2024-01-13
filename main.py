#!/usr/bin/python3
'''
Recreation of the world-famous game of Minesweeper

I know this program is not much of a revolution but I created to learn about GUI such as tkinter

Please enjoy!
'''
##########################################
#           IMPORTING SECTION            #
##########################################

import tkinter as tk
from random import randrange

##########################################
#               GLOBAL VAR               #
##########################################

BOARD_INFO = {
    "easy": (10, 15),
    "medium": (15, 35),
    "hard": (20, 35),
    "nightmare": (30, 45)
}

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

##########################################

#TODO: Create a way to mark a tile as "NOT SAFE" (Flag it)
#TODO: Implement it in a graphical interface
#TODO: Make the first click impossible to get a bomb, then in a given radius, have no bomb (Kind of like the google one)

##########################################

class Minesweeper:

    def __init__(self):
        # Constants and data structures
        self.difficulty = self.choose_difficulty()
        print(self.difficulty)
        self.user_board = self.init_board()     # Board used to know where the bombs are, and display elements once the user revealed them
        self.bomb_board = self.init_board()     # Board used to display the game
        self.game_over_value = False    # Useful ?
        self.window = tk.Tk()   # Creation of the window
        self.start_game()   # We start the game


    def start_game(self):
        '''Function that calls all the functions needed to start the game'''
        self.bombify()      # We put bombs on the board
        self.near_bomb()    # We display the number of bombs near each tile
        self.init_window()

    def init_board(self):
        '''Returns an empty square matrix of the difficulty size'''
        return [['■']*BOARD_INFO[self.difficulty][0] for _ in range(BOARD_INFO[self.difficulty][0])]

    
    def init_window(self):
        '''Function that displays the game window'''

        self.window.title("Minesweeper")
        self.window.resizable(False, False)
        self.window.geometry("500x500")

        for i in range(BOARD_INFO[self.difficulty][0]):  # Creation of all the buttons that represent tiles
            for j in range(BOARD_INFO[self.difficulty][0]):
                self.window.columnconfigure(i, weight=1)
                self.window.rowconfigure(j, weight=1)

                frame = tk.Frame(
                    master=self.window,
                    relief=tk.RAISED,
                    borderwidth=1
                )
                frame.grid(row=j, column=i)
                label = tk.Button(master=frame, text=f"{self.user_board[i][j]}", command=lambda x = (i, j): self.play(x))
                label.pack()

        self.window.mainloop()

    
    def refresh_window(self):
        '''Function that refreshes the window'''


    def bombify(self):
        '''Function that randomly display bomb on the bomb board, following a certain difficulty'''
        nb_bombs = BOARD_INFO[self.difficulty][1]
        
        while nb_bombs != 0:    # To avoid having two bombs having the same coordinate, thus letting us with less bombs wanted
            bomb = (randrange(len(self.bomb_board)), randrange(len(self.bomb_board)))

            if self.bomb_board[bomb[0]][bomb[1]] != 'X':    # If the tile is already a bomb, we don't touch it
                self.bomb_board[bomb[0]][bomb[1]] = 'X'
                nb_bombs -= 1


    def near_bomb(self):
        '''Function that modify the bomb board to display the number of bomb within a 1 tile range'''
        for i in range(len(self.bomb_board)):
            for j in range(len(self.bomb_board)):

                count = 0   # How many bombs near my position ?
                if self.bomb_board[i][j] == 'X':    # If the tile is already a bomb, we can continue
                    continue
                for direction in DIRECTIONS:
                    if i + direction[0] >= 0 and i + direction[0] < len(self.bomb_board) and j + direction[1] >= 0 and j + direction[1] < len(self.bomb_board):
                        if self.bomb_board[i + direction[0]][j + direction[1]] == 'X':
                            count += 1
                if count > 0:
                    self.bomb_board[i][j] = count


    def refresh_board(self, choice, visited = set()):
        '''Function that refreshes the board for the user, showing blank spaces and number of bomb near the tile chosen'''

        if choice not in visited:   # If we didn't already go on that tile
            if self.bomb_board[choice[0]][choice[1]] == '■':    # Check if the tile is empty or not
                self.user_board[choice[0]][choice[1]] = ' '     # We reveal it
                for direction in [(0,1), (1,0), (0,-1), (-1,0)]:    # Recursive call for each direction 
                    if choice[0] + direction[0] >= 0 and choice[0] + direction[0] < len(self.user_board) and choice[1] + direction[1] >= 0 and choice[1] + direction[1] < len(self.user_board): # To avoid index out of range errors
                        visited.add(choice)
                        self.refresh_board((choice[0] + direction[0], choice[1] + direction[1]))
            else:
                self.user_board[choice[0]][choice[1]] = self.bomb_board[choice[0]][choice[1]]   # We show the number of bomb near the tile


    def play(self, choice):
        '''Main function used to play'''
        if self.user_board[choice[0]][choice[1]] == 'X':  # If the tile chosen is a bomb, we launch the game over sequence
            self.game_over()
        else:   # Else, we refresh the board and continue to play 
            self.refresh_board(choice)


    def game_over(self):
        '''Function use to display the game over'''
        print('Sorry, you picked a bomb!')
        self.window.destroy()


    def choose_difficulty(self):
        '''Function used to choose the difficulty'''

        window = tk.Tk()
        window.title("Minesweeper - Choose a difficulty")
        for i in range(4):  # Creation of four buttons to choose difficulty
            window.columnconfigure(i, weight=1, minsize=150)
            window.rowconfigure(0, weight=1, minsize=75)

            frame = tk.Frame(
                master=window,
                relief=tk.RAISED,
                borderwidth=1
            )
            frame.grid(row=0, column=i)
            label = tk.Button(master=frame, text=f"{list(BOARD_INFO)[i]}", command= lambda x=f"{list(BOARD_INFO)[i]}": self.set_difficulty(x, window))
            label.pack()

        window.mainloop()
    
    def set_difficulty(self, difficulty, window):
        '''Function used to set the difficulty'''
        self.difficulty = difficulty
        window.destroy()

if __name__ == '__main__':

    Minesweeper()