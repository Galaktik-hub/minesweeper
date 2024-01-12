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

#TODO: Create a way to mark a tile as "NOT SAFE" or something like that
#TODO: Implement it in a graphical interface
#TODO: Make the first click impossible to get a bomb, then in a given radius, have no bomb (Kind of like the google one)

##########################################

class Minesweeper:

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.user_board = self.init_board()     # Board used to know where the bombs are, and display elements once the user revealed them
        self.bomb_board = self.init_board()     # Board used to display the game
        self.game_over_value = False
        self.window = tk.Tk()


    def init_board(self):
        '''Returns an empty square matrix of the difficulty size'''
        return [['■']*BOARD_INFO[self.difficulty][0] for _ in range(BOARD_INFO[self.difficulty][0])]

    
    def init_window(self):
        '''Function that displays the game window'''
        self.window.title("Minesweeper")
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
                label = tk.Button(master=frame, text=f"{i, j}")
                label.pack()

        self.window.mainloop()


    def display_board(self, board):
        '''Print in the console the board given in argument'''
        print()
        for line in board:
            print('|', end=' ')

            for tile in line:
                print(tile, end = ' | ')

            print()
        print()


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


    def play(self, board):
        '''Main function used to play'''
        choice = (int(input('Choose a row to play: ')), int(input('Choose a column to play: ')))

        if board[choice[0]][choice[1]] == 'X':  # If the tile chosen is a bomb, we launch the game over sequence
            self.game_over()
        else:   # Else, we refresh the board and continue to play 
            self.refresh_board(choice)


    def game_over(self):
        '''Function use to display the game over'''
        print('Sorry, you picked a bomb!')
        self.game_over_value = True


def choose_difficulty():
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
        label = tk.Button(master=frame, text=f"{list(BOARD_INFO)[i]}", command=lambda x=f"{list(BOARD_INFO)[i]}": main(x, window))
        label.pack()

    window.mainloop()

def main(difficulty, window):
    window.destroy()

    game = Minesweeper(difficulty)

    game.bombify()
    game.near_bomb()

    game.display_board(game.bomb_board)

    game.init_window()

    while True:

        if game.game_over_value:
            break

        game.display_board(game.user_board)
        game.play(game.bomb_board)


if __name__ == '__main__':

    difficulty = choose_difficulty()