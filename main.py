#!/usr/bin/python3
'''
This program lets you create freely a README file for your GitHub profile or your projects.

Throught a graphical interface, you can type in your text and the way you want to formate it.

Once you're done creating your README file, you can press the 'Finished!' button and it will create the file in your current directory.

In the commentary of the README, there will always be a credit to this program, I do not restreint you to remove it, though crediting someone for their work is always good!
'''
##########################################
#           IMPORTING SECTION            #
##########################################
#import PySimpleGUI as sg
#import pygame as pg
import tkinter as tk
from random import randrange
##########################################
#               GLOBAL VAR               #
##########################################
BOARD_INFO = {
    "easy": (10, 15),
    "medium": (15, 25),
    "hard": (20, 35),
    "nightmare": (30, 45)
}

BOMB_BOARD = None
USER_BOARD = None

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

GAME_OVER = False
##########################################

#TODO: Create a function to play (Pick a tile on the board)
#TODO: After the tile was picked, refresh the board
#TODO: Create a way to mark a tile as "NOT SAFE" or something like that
#TODO: Implement it in a graphical interface



def init_board(size):
    '''Returns an empty square matrix of the size given in argument'''
    return [['■']*size for _ in range(size)]


def display_board(board):
    '''Print in the console the board given in argument'''
    print()
    for line in board:
        print('|', end=' ')

        for tile in line:
            print(tile, end = ' | ')

        print()
    print()


def bombify(board, difficulty):
    '''Function that randomly display bomb on the board given in argument, following a certain difficulty'''
    nb_bombs = BOARD_INFO[difficulty][1]
    
    while nb_bombs != 0:

        bomb = (randrange(len(board)), randrange(len(board)))

        if board[bomb[0]][bomb[1]] != 'X':
            board[bomb[0]][bomb[1]] = 'X'
            nb_bombs -= 1


def near_bomb(board):
    '''Function that modify the board give in argument to display the number of bomb within a 1 tile range'''
    for i in range(len(board)):
        for j in range(len(board)):

            count = 0
            if board[i][j] == 'X':
                continue
            for direction in DIRECTIONS:
                if i + direction[0] >= 0 and i + direction[0] < len(board) and j + direction[1] >= 0 and j + direction[1] < len(board):
                    if board[i + direction[0]][j + direction[1]] == 'X':
                        count += 1
            if count > 0:
                board[i][j] = count


def refresh_board(choice):
    '''Function that refreshes the board for the user, showing blank spaces and number of bomb near tile'''
    if BOMB_BOARD[choice[0]][choice[1]] == '■':
        USER_BOARD[choice[0]][choice[1]] = ' '
        for direction in DIRECTIONS:
                if choice[0] + direction[0] >= 0 and choice[0] + direction[0] < len(USER_BOARD) and choice[1] + direction[1] >= 0 and choice[1] + direction[1] < len(USER_BOARD):
                    refresh_board(choice)
    else:
        USER_BOARD[choice[0]][choice[1]] = BOMB_BOARD[choice[0]][choice[1]]



def play(board):
    '''Main function used to play'''
    choice = (int(input('Choose a row to play: ')), int(input('Choose a column to play: ')))

    if board[choice[0]][choice[1]] == 'X':
        game_over()
    else:
        refresh_board(choice)


def game_over():
    '''Function use to display the game over'''
    global GAME_OVER

    print('Sorry, you picked a bomb!')
    GAME_OVER = True


if __name__ == '__main__':

    BOMB_BOARD = init_board(BOARD_INFO['easy'][0])
    USER_BOARD = init_board(BOARD_INFO['easy'][0])

    bombify(BOMB_BOARD, 'easy')
    near_bomb(BOMB_BOARD)

    display_board(BOMB_BOARD)

    while True:

        if GAME_OVER:
            break

        display_board(USER_BOARD)
        play(BOMB_BOARD)