# --coding:utf-8--
from sys import exit  # 用exit来退出程序

import easy_pc
import gloval
import judgewin
import menu
import windows as wd

gloval.init()


def main():
    wd.Image_PreProcessing()
    wd.windows()
    mainloop()


if __name__ == '__main__':
    while 1:
        main()


def mainloop():
    # 设置默认光标样式
    pg.mouse.set_cursor(*pg.cursors.arrow)
    gloval.setval('restart', 0)
    global restart

    restart = gloval.getval('restart')
    gloval.setval('press_intro', 0)
    gloval.setval('press_regret', 0)
    global gamestate
    gamestate = 1
    gloval.setval('gamestate', 1)
    global press, button
    press = (0, 0, 0)
    button = (132, 71, 34)  # 字体颜色
    global screen
    screen = gloval.getval('screen')
    global imBackground
    imBackground = gloval.getval('imBackground')
    global imChessboard
    imChessboard = gloval.getval('imChessboard')
    global imBlackPiece
    imBlackPiece = gloval.getval('imBlackPiece')
    global imWhitePiece
    imWhitePiece = gloval.getval('imWhitePiece')
    global whiteround  # 回合，黑子先走，whiteround为-1
    whiteround = [-1]
    global chess_array  # 储存双方落子信息，0246先手，1357后手
    chess_array = []
    global chess_num
    chess_num = 0
    global piece_x, piece_y, piece
    FPS = 60
    piece_x = []
    piece_y = []
    piece = []

    while restart == 0:
        # 刷新gamestate
        gamestate = gloval.getval('gamestate')
        # 画背景，左上角是坐标
        drawbg()
        # 画菜单
        drawmenu()
        # 鼠标事件按键情况
        drawpress()
        # 画鼠标移动的相关效果
        drawmove()
        # 判断是否赢棋
        judgewin.check_win(chess_array)
        # 刷新画面
        pg.display.update()
        # 调整游戏帧数
        FPSClock = pg.time.Clock()
        FPSClock.tick(FPS)
        restart = gloval.getval('restart')


def drawbg():
    ##画背景
    screen.blit(imBackground, (0, 0))
    global chessboard_start_x
    global chessboard_start_y
    chessboard_start_x = 50  # (1024-(1024-540))/2
    chessboard_start_y = (768 - 540) / 2
    screen.blit(imChessboard, (chessboard_start_x, chessboard_start_y))


def drawmenu():
    ##画菜单
    if gamestate == 1:
        menu.menu1()  # 画’开始游戏‘，‘游戏说明’，’结束游戏‘按钮
    elif gamestate == 2:
        menu.menu2()  # 画 ‘人机对战’，‘双人对战’，'返回上级菜单',‘结束游戏’
    elif gamestate == 3:
        menu.menu3()  # 画 ‘玩家先手’，‘电脑先手’，'返回上级菜单',‘结束游戏’
    elif gamestate == 4 or gamestate == 5 or gamestate == 6:
        menu.menu4()  # 画‘悔棋’，‘重新开始’，‘结束游戏’按钮
    elif gamestate == 7:
        menu.menu7()  # 画‘重新开始’，‘结束游戏’按钮


##画鼠标移动的相关效果
def drawmove():
    gloval.setval('mouse_x', pg.mouse.get_pos()[0])  # 鼠标的坐标
    gloval.setval('mouse_y', pg.mouse.get_pos()[1])
    mouse_x, mouse_y = pg.mouse.get_pos()  # 棋子跟随鼠标移动
    if chessboard_start_x < mouse_x < chessboard_start_x + 540 and chessboard_start_y < mouse_y < chessboard_start_y + 540 and (
            gamestate == 4 or gamestate == 5 or gamestate == 6):
        if whiteround[chess_num] == 1:
            screen.blit(imWhitePiece, (mouse_x - 16, mouse_y - 16))
        else:
            screen.blit(imBlackPiece, (mouse_x - 16, mouse_y - 16))
    elif gamestate == 1:
        menu.movemenu1()
    elif gamestate == 2:
        menu.movemenu2()
    elif gamestate == 3:
        menu.movemenu3()
    elif gamestate == 4 or gamestate == 5 or gamestate == 6:
        menu.movemenu4()
    elif gamestate == 7:
        menu.movemenu7()


def drawpress():
    global whiteround
    global chess_array
    global d
    global chess_num
    global piece_x, piece_y, piece
    press_intro = gloval.getval('press_intro')
    press_regret = gloval.getval('press_regret')
    d = (518 - 22) / 14  # (1，1)的实际坐标为(22，22)，(15，15)的实际坐标为(518，518),有14个间隔
    for event in pg.event.get():  # 获取鼠标点击事件
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            gloval.setval('pressed_x', event.pos[0])
            gloval.setval('pressed_y', event.pos[1])
            pressed_x, pressed_y = event.pos[0], event.pos[1]
            # 第一种情况，人人对战
            if chessboard_start_x < pressed_x < chessboard_start_x + 540 and chessboard_start_y < pressed_y < chessboard_start_y + 540 and gamestate == 4:
                player_pos_chess(pressed_x, pressed_y)
            # 第二种情况，玩家先手
            elif chessboard_start_x < pressed_x < chessboard_start_x + 540 and chessboard_start_y < pressed_y < chessboard_start_y + 540 and gamestate == 5:
                ifem = player_pos_chess(pressed_x, pressed_y)  # 玩家下棋
                if ifem != False:
                    pc_pos_chess()  # 电脑下棋
            # 第三种情况，电脑先手
            elif chessboard_start_x < pressed_x < chessboard_start_x + 540 and chessboard_start_y < pressed_y < chessboard_start_y + 540 and gamestate == 6:
                ifem = player_pos_chess(pressed_x, pressed_y)  # 玩家下棋
                if ifem != False:
                    pc_pos_chess()  # 电脑下棋
            # 第四种情况，点击菜单

            else:
                if gamestate == 1:
                    menu.pressmenu1()
                elif gamestate == 2:
                    menu.pressmenu2()
                elif gamestate == 3:
                    if 6 == menu.pressmenu3():
                        pc_pos_chess()
                elif gamestate == 4 or gamestate == 5 or gamestate == 6:
                    menu.pressmenu4()
                elif gamestate == 7:
                    menu.pressmenu7()
    restart = gloval.getval('restart')  # 是否重启游戏
    if chess_array:  # 画棋子和棋子上面的数字不为空，有落子
        draw_chess(chess_num, whiteround)  # 画棋子和上面的数字
    if press_intro == 1:  # 游戏简介信息
        draw_intro_text()
    if press_regret == 1:  # 悔棋
        regret()
    draw_chesscross(chess_num)  # 画最后一个落子位置


def draw_intro_text():
    my_font = pg.font.Font('mufont.ttf', 25)
    text1 = my_font.render("双方分别使用黑白两色的棋子，", True, button)
    text2 = my_font.render("下在棋盘直线与横线的交叉点上，", True, button)
    text3 = my_font.render("先形成五子连线者获胜。", True, button)
    screen.blit(text1, (640, 100))
    screen.blit(text2, (640, 140))
    screen.blit(text3, (640, 180))


def regret():
    global chess_num, chess_array, piece_y, piece_x, piece, whiteround
    if chess_num != 0:  # 删除所有储存的数组
        if gamestate == 4:
            del chess_array[-1]
            del piece_x[-1]
            del piece_y[-1]
            del piece[-1]
            del whiteround[-1]
            chess_num = chess_num - 1
        if gamestate == 5 or gamestate == 6:
            del chess_array[-1]
            del chess_array[-1]
            del piece_x[-1]
            del piece_y[-1]
            del piece_x[-1]


##二维坐标值转一维索引
def array2index(array):
    return (array[0] - 1) * 15 + array[1]


##一维索引值转二维坐标
def index2array(index):
    i, j = int((index - index % 15) / 15 + 1), int(index % 15)
    if j == 0:
        i -= 1
        j = 15
    return i, j


##判断是否为空
def if_isempty(i, j):
    if [i, j] not in piece:
        return True
    else:
        return False
    ##判断是否为空


def if_isempty(i, j):
    if [i, j] not in piece:
        return True
    else:
        return False

    def player_pos_chess(pressed_x, pressed_y):

        global whiteround
    global chess_array
    global chess_num
    global piece_x, piece_y, piece
    chess_array.append(list(getpos(pressed_x, pressed_y)))  # 记录位置，黑棋白棋数组交替
    piece_i, piece_j = getrealpos(chess_array[chess_num])  # 已处理的位置
    isempty = if_isempty(piece_i, piece_j)

    if isempty == True:  # 如果这个地方没有棋子
        whiteround.append(-whiteround[chess_num])
        piece_x.append(piece_i)
        piece_y.append(piece_j)
        piece.append([piece_i, piece_j])
        chess_num += 1
        gloval.setval("chess_array", chess_array)
        return 1
    else:  # 如果这个地方有棋子
        del chess_array[chess_num]  # 删除那个重复的数组
        return 0


def pc_pos_chess():
    global whiteround
    global chess_array
    global chess_num
    global piece_x, piece_y, piece
    pc_pressed = easy_pc.find_maxscore(chess_array, whiteround[-1])
    chess_array.append(pc_pressed)  # 记录电脑下棋位置
    piece_i, piece_j = getrealpos(chess_array[chess_num])  # 已处理的位置
    isempty = if_isempty(piece_i, piece_j)
    print(isempty)
    if isempty == True:  # 如果这个地方没有棋子
        whiteround.append(-whiteround[chess_num])
        piece_x.append(piece_i)
        piece_y.append(piece_j)
        piece.append([piece_i, piece_j])
        chess_num += 1
        gloval.setval("chess_array", chess_array)
    else:  # 如果这个地方有棋子
        del chess_array[chess_num]  # 删除那个重复的数组


# --coding:utf-8--
from PIL import Image
import pygame as pg
from sys import *  # 用exit来退出程序
import gloval

gloval.init()


def Image_PreProcessing():
    # 图片存储路径
    im = Image.open('background.jpeg')
    # Resize图片大小，入口参数为一个tuple，为新的图片大小
    imBackground = im.resize((424, 300))
    imBackground.save('1111.jpg', 'JPEG')

    im = Image.open('chessboard.jpeg')
    # Resize图片大小，入口参数为一个tuple，为新的图片大小
    imBackground = im.resize((540, 540))
    imBackground.save('new_chessboard.jpg', 'JPEG')

    im = Image.open('chessblack.png')
    # Resize图片大小，入口参数为一个tuple，为新的图片大小
    imBackground = im.resize((32, 32))
    imBackground.save('new_chessblack.png', 'PNG')

    im = Image.open('chesswhite.png')
    # Resize图片大小，入口参数为一个tuple，为新的图片大小
    imBackground = im.resize((32, 32))
    imBackground.save('new_chesswhite.png', 'PNG')


def windows():
    pg.init()  # 初始化pygame,为使用硬件做准备
    #	screen=pg.display.set_mode((1024,768),0,32)#分辨率，标志位，色深
    # 加载背景和光标图片
    gloval.setval('screen', pg.display.set_mode((1024, 768), 0, 32))
    gloval.setval('imBackground', pg.image.load('new_background.jpg').convert())
    gloval.setval('imChessboard', pg.image.load('new_chessboard.jpg').convert())
    gloval.setval('imBlackPiece', pg.image.load('new_chessblack.png').convert_alpha())
    gloval.setval('imWhitePiece', pg.image.load('new_chesswhite.png').convert_alpha())

    pg.display.set_caption('五子棋      by Ace Cheney')  # 设置窗口标题

    def init():

        global glodic
    glodic = {}


def setval(name, val):
    glodic[name] = val


def getval(name, defva=None):
    return glodic[name]
