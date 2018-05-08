#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
一个游戏循环（也可以称为主循环）就做下面这三件事：
 1) 处理事件
 2) 更新游戏状态
 3) 绘制游戏状态到屏幕上
"""

# 此代码基本能立于不败之地；
import random
#可视化输出
def draw_Board(board):
    print('-----------')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('-----------')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('-----------')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('-----------')
#输入选择符号
def input_Player_Letter():
    letters = ''
    while not (letters == 'X' or letters == 'O'):
        print('Do you want to be X or O?')
        letters = input().upper()
    if letters == 'X':return ['X','O']
    else:return ['O','X']
#谁先？
def who_Goes_First():
    if random.randint(0, 1) == 0:
        return 'computer'
    else: return 'player'
#是否再来一次？
def play_Again():
    print('Do you want to play again?(yes or no?)')
    return input().lower().startswith('y')
#下子
def make_Move(board, letter, move):
    board[move] = letter
#判断是否有获胜者
def is_Winner(bo, le):
    return ((bo[7] == bo[8] == bo[9] == le) or
            (bo[4] == bo[5] == bo[6] == le) or
            (bo[1] == bo[2] == bo[3] == le) or
            (bo[7] == bo[4] == bo[1] == le) or
            (bo[8] == bo[5] == bo[2] == le) or
            (bo[9] == bo[6] == bo[3] == le) or
            (bo[7] == bo[5] == bo[3] == le) or
            (bo[1] == bo[5] == bo[9] == le))
#复制表盘测试
def get_Board_Copy(board):
    dupe_Board = []
    for i in board:
        dupe_Board.append(i)
    return dupe_Board
#判断位置是否为空
def is_Space_Free(board,move):
    return board[move] == ' '
#选手下棋
def get_Player_Move(board):
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not is_Space_Free(board,int(move)):
        print('What is your next move?')
        move = input()
    return int(move)
#随机下棋
def choose_Random_Move_From_List(board, movesList):
    possibleMoves = []
    for i in movesList:
        if is_Space_Free(board, i):
            possibleMoves.append(i)
    if len(possibleMoves ) != 0 :
        return random.choice(possibleMoves)#随机返回
    else:
        return None ##不在此中下棋
#简易AI
def get_Computer_Move(board, computerLetter):
    if computerLetter == 'X':
        playerLetter = 'O'
    else :playerLetter = 'X'
#是否有胜利的一步
    for i in range(1,10):
        copy = get_Board_Copy(board)
        if is_Space_Free(copy, i):
            make_Move(copy, computerLetter, i)
            if is_Winner(copy, computer_Letter):
                return i
#阻止选手胜利
    for i in range(1,10):
        copy = get_Board_Copy(board)
        if is_Space_Free(copy, i):
            make_Move(copy, player_Letter, i)
            if is_Winner(copy, player_Letter):
                return i
#占中间的
    if is_Space_Free(board, 5):
        return 5
#选角落不易输
    move = choose_Random_Move_From_List(board, [1,3,7,9])
    if move != None:
        return move
#别无后路
    return choose_Random_Move_From_List(board, [2, 4, 6, 8])
#判断棋盘是否满
def is_Board_Full(board):
    for i in range(1, 10):
        if is_Space_Free(board, i):
            return False
    return True
####主函数：
print("Welcome to 井字棋:")
while 1:
    the_Board = [" "]*10
    player_Letter, computer_Letter = input_Player_Letter()
    turn = who_Goes_First()
    print('The {} will go first.'.format(turn))
    game_Is_Playing = True
#游戏开始
    while game_Is_Playing:
        if turn == 'player':
            draw_Board(the_Board)
            move = get_Player_Move(the_Board)
            make_Move(the_Board, player_Letter, move)
#判断是否胜利
            if is_Winner(the_Board,player_Letter):
                draw_Board(the_Board)
                print("You have won the game!")
                game_Is_Playing = False
            else:
                if is_Board_Full(the_Board):
                    draw_Board(the_Board)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'computer'  #交换下棋方
        else:
            move = get_Computer_Move(the_Board, computer_Letter)
            make_Move(the_Board, computer_Letter, move)
#判断胜利
            if is_Winner(the_Board,computer_Letter):
                draw_Board(the_Board)
                print("You have lost the game!")
                game_Is_Playing = False
            else:
                if is_Board_Full(the_Board):
                    draw_Board(the_Board)
                    print('The game is axx tie!')
                    break
                else:
                    turn = 'player'   #交换下棋方
    if not play_Again():
        break