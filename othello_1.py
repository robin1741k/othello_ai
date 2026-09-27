# othelloを作る.

import numpy as np
import random
import re

def first_turn():
    if random.randint(0,1) == 1:
        print("あなたは白(後手)です")
        return False
    else:
        print("あなたは黒(先手)です")
        return True

def move_check(board, x, y, color):
    if board[x,y] != 0:
        return False
    if color:
        stone_m = black
        stone_e = white
    else:
        stone_m = white
        stone_e = black
    for dx, dy in direction: # 方向別にひっくり返せるかを判定.
        is_stone_e = False
        for i in range(1,8):
            nx = x + dx * i
            ny = y + dy * i
            if not (0 <= nx < 8 and 0 <= ny < 8):
                break
            elif board[nx,ny] == 0:
                break
            if board[nx,ny] == stone_e: # 相手の石を保存.
                is_stone_e = True
            elif board[nx,ny] == stone_m:
                if is_stone_e:
                    return True
                break
    return False

def reversi(board, x, y, color):
    can_reversi = []
    if color:
        stone_m = black
        stone_e = white
    else:
        stone_m = white
        stone_e = black

    for dx, dy in direction: # 方向別にひっくり返せるかを判定.
        temp = []
        for i in range(1,8):
            nx = x + dx * i
            ny = y + dy * i
            if not (0 <= nx < 8 and 0 <= ny < 8):
                break
            elif board[nx,ny] == 0:
                break
            if board[nx,ny] == stone_e: # 相手の石を保存.
                temp.append((nx,ny))
            elif board[nx,ny] == stone_m: # 途切れて自分の石になったタイミングで結合.
                if len(temp) > 0:
                    can_reversi.extend(temp)
                break
    for x_a,y_a in can_reversi:
        board[x_a,y_a] = stone_m

def put_cpu(board, color):
    empty_x, empty_y = np.where(board == 0)
    option = []
    check = True
    if color:
        stone_m = black
        stone_e = white
    else:
        stone_m = white
        stone_e = black
    for i,j in zip(empty_x,empty_y):
        option.append((i,j))
    while check:
        if not option:
            break
        cpu_x, cpu_y = random.choice(option)
        if move_check(board, cpu_x, cpu_y, color):
            check = False
        else:
            option.remove((cpu_x,cpu_y))
    board[cpu_x,cpu_y] = stone_m
    reversi(board, cpu_x, cpu_y, color)
    print(f"あいては{cpu_x},{cpu_y}に石を置きました")

def judge(board,game):
    count_black = count_white = count_empty = 0
    for i in range(8):
        for j in range(8):
            if board[i,j] == black:
                count_black += 1
            elif board[i,j] == white:
                count_white += 1
            else:
                count_empty += 1
    if count_black == 0:
        print("後手の勝ちです")
        game = False
    elif count_white == 0:
        print("先手の勝ちです")
        game = False
    elif count_empty == 0:
        if count_black > count_white:
            print("先手の勝ちです")
        elif count_black < count_white:
            print("後手の勝ちです")
        else:
            print("引き分けです")
        game = False
    return game

game = True
color = first_turn() # first_turn()のTFと黒白が一致.
if color:
    turn = True # 初手黒のとき.
else:
    turn = False # 初手白のとき.
board = np.zeros((8,8), dtype= int)
white = -1
black = 1
board[3,4] = board[4,3] = white # これで同時に初期値代入できる.
board[3,3] = board[4,4] = black
direction = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
current_color = black

# ここからスタート.
print(board)
while game:
    if turn:
        print("あなたの番です")
        print("どこに石を置きますか？ ( , )で入力してください")
        if color:
            stone_m = black
            stone_e = white
        else:
            stone_m = white
            stone_e = black
        sub = input()
        x_player, y_player = map(int, re.split(r"[,._/ ]",sub))
        if move_check(board, x_player, y_player, color): # 石が置いてあるかだけを判定し、そうならT.
            board[x_player,y_player] = stone_m
            reversi(board, x_player, y_player, color) # 間の石をひっくり返す.
            print(f"{(x_player,y_player)}に石を置きました")
        else:
            print("そこには置けません")
            continue
        turn = False
    else:
        print("あいての番です")
        put_cpu(board, not color)
        turn = True
    game = judge(board,game) # もし勝敗がついたらここでループから脱出.
    print(board)