__author__ = 'Skyeyes'

import pygame, sys, random
from pygame.locals import *


pygame.init()
pygame.display.set_caption("drawboard")

font1 = pygame.font.Font(None, 20)
font2 = pygame.font.Font(None, 40)
font3 = pygame.font.Font(None, 80)
font4 = pygame.font.Font(None, 100)
white = 255, 255, 255
red = 220, 50, 50
yellow = 230, 230, 50
black = 0, 0, 0

shapestyle = ""
move = True

screen = pygame.display.set_mode((1200, 800))


class Shape:
    def __init__(self, begin_x, begin_y, end_x, end_y, shapestyle):
        self.begin_x = begin_x
        self.begin_y = begin_y
        self.end_x = end_x
        self.end_y = end_y
        self.shapestyle = shapestyle

    def draw(self):
        model().judge_draw_shape(self.begin_x, self.begin_y, self.end_x, self.end_y, self.shapestyle)




class model:
    def draw_block(self, color, pos_x, pos_y, width, height, linewidth=0):
        pygame.draw.rect(screen, color, (pos_x, pos_y, width, height), linewidth)

    def print_text(self, font, x, y, text, color=(255, 255, 255)):
        imgText = font.render(text, True, color)
        screen.blit(imgText, (x, y))

    def judge_draw_shape(self, begin_x, begin_y, end_x, end_y, shapestyle = ""):
        if shapestyle == "rectangle":
            pygame.draw.rect(screen, black, (begin_x, begin_y, (end_x-begin_x), (end_y-begin_y)), 2)
        elif shapestyle == "square":
            width = min(abs(end_x-begin_x), abs(end_y-begin_y))
            pos_x = begin_x if (end_x-begin_x)>0 else begin_x-width
            pos_y = begin_y if (end_y-begin_y)>0 else begin_y-width
            pygame.draw.rect(screen, black, (pos_x, pos_y, width, width), 2)
        elif shapestyle == "circle":
            radius = min(abs((end_x-begin_x)//2), abs((end_y-begin_y)//2))
            pos_x = radius+begin_x if (end_x-begin_x)>0 else begin_x-radius
            pos_y = radius+begin_y if (end_y-begin_y)>0 else begin_y-radius
            if abs(radius) > 4:
                pygame.draw.circle(screen, black, (pos_x, pos_y), abs(radius), 2)
            else:
                pygame.draw.circle(screen, black, (pos_x, pos_y), abs(radius), 0)
        elif shapestyle == "ellipse":
            pos_x = begin_x if (end_x-begin_x)>0 else end_x
            pos_y = begin_y if (end_y-begin_y)>0 else end_y
            if min(abs(end_x-begin_x), abs(end_y-begin_y)) > 4:
                pygame.draw.ellipse(screen, black, (pos_x, pos_y, abs(end_x-begin_x), abs(end_y-begin_y)), 2)
            else:
                pygame.draw.ellipse(screen, black, (pos_x, pos_y, abs(end_x-begin_x), abs(end_y-begin_y)), 0)



def makebutton():
    model().draw_block(yellow, 10, 10, 50, 50)
    model().draw_block(black, 20, 25, 30, 20, 2)
    model().draw_block(yellow, 10, 80, 50, 50)
    model().draw_block(black, 25, 95, 20, 20, 2)
    model().draw_block(yellow, 10, 150, 50, 50)
    pygame.draw.circle(screen, black, (35, 175), 10, 2)
    model().draw_block(yellow, 10, 220, 50, 50)
    pygame.draw.ellipse(screen, black, (20, 235, 30, 20), 2)
    model().draw_block(black, 100, 100, 1000, 600, 2)
    model().draw_block(yellow, 10, 290, 50, 50)
    model().print_text(font1, 17, 306, "move", black)


shapelist = []


def save_shape(begin_x, begin_y, end_x, end_y):
    if shapestyle == "rectangle":
        shapelist.append(Shape(begin_x, begin_y, end_x, end_y, "rectangle"))
    elif shapestyle == "square":
        shapelist.append(Shape(begin_x, begin_y, end_x, end_y, "square"))
    elif shapestyle == "circle":
        shapelist.append(Shape(begin_x, begin_y, end_x, end_y, "circle"))
    elif shapestyle == "ellipse":
        shapelist.append(Shape(begin_x, begin_y, end_x, end_y, "ellipse"))


def judgemoveshape(x, y):
    i = 0
    for each in shapelist:
        if each.begin_x <= x <= each.end_x and each.begin_y <= y <= each.end_y:
            return i
        i += 1


def moveshape(begin_x, begin_y, end_x, end_y, shapeid):
    movex = end_x-begin_x
    if movex >= 0:
        movex = movex if max(shapelist[shapeid].end_x, shapelist[shapeid].begin_x)+movex <= 1100 else 0
    else:
        movex = movex if min(shapelist[shapeid].end_x, shapelist[shapeid].begin_x)+movex >= 100 else 0
    movey = end_y-begin_y
    if movey >= 0:
        movey = movey if max(shapelist[shapeid].end_y, shapelist[shapeid].begin_y)+movey <= 700 else 0
    else:
        movey = movey if min(shapelist[shapeid].end_y, shapelist[shapeid].begin_y)+movey >= 100 else 0
    shapelist[shapeid].end_x += movex
    shapelist[shapeid].begin_x += movex
    shapelist[shapeid].end_y += movey
    shapelist[shapeid].begin_y += movey
    print(str(shapeid))
    print(shapelist[shapeid].shapestyle)



begin_x = begin_y = end_x = end_y = 0
down = up = False
shapechooseid = -1


while True:
    screen.fill(white)
    makebutton()
    pygame.mouse.set_cursor(*pygame.cursors.arrow)

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYUP:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        elif event.type == MOUSEBUTTONUP:
            mouse_up_x, mouse_up_y = event.pos
            if 10 <= mouse_up_x <= 60 and 10 <= mouse_up_y <= 60:
                shapestyle = "rectangle"
                move = False
            elif 10 <= mouse_up_x <= 60 and 80 <= mouse_up_y <= 130:
                shapestyle = "square"
                move = False
            elif 10 <= mouse_up_x <= 60 and 150 <= mouse_up_y <= 200:
                shapestyle = "circle"
                move = False
            elif 10 <= mouse_up_x <= 60 and 220 <= mouse_up_y <= 270:
                shapestyle = "ellipse"
                move = False
            elif 10 <= mouse_up_x <= 60 and 290 <= mouse_up_y <= 340:
                shapestyle = ""
                move = True
            if down == True:
                end_x = max(mouse_up_x, 100) if mouse_up_x < 600 else min(mouse_up_x, 1100)
                end_y = max(mouse_up_y, 100) if mouse_up_y < 400 else min(mouse_up_y, 700)
                down = False
                up = True
                if shapestyle:
                    save_shape(begin_x, begin_y, end_x, end_y)
            begin_x = begin_y = end_x = end_y = 0
        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if 100 < mouse_x < 1100 and 100 < mouse_y < 700:
                if down:
                    end_x = mouse_x
                    end_y = mouse_y
                    draw_realy = False
        elif event.type == MOUSEBUTTONDOWN:
            mouse_down_x, mouse_down_y = event.pos
            if 100 < mouse_down_x < 1100 and 100 < mouse_down_y < 700:
                if shapestyle:
                    down = True
                    up = False
                    begin_x = mouse_down_x
                    begin_y = mouse_down_y
                if move:
                    down = True
                    up = False
                    begin_x = mouse_down_x
                    begin_y = mouse_down_y
                    shapechooseid = judgemoveshape(begin_x, begin_y)
                    if shapechooseid == None:
                        shapechooseid = -1

    if down == True and begin_x >= 100 and begin_y >= 100 and end_x >= 100 and end_y >= 100:
        if shapestyle:
            model().judge_draw_shape(begin_x, begin_y, end_x, end_y, shapestyle)
        elif move and shapechooseid >= 0:
            moveshape(begin_x, begin_y, end_x, end_y, shapechooseid)
            begin_x = end_x
            begin_y = end_y
            print(shapechooseid)


    for each in shapelist:
        each.draw()

    # print(rectangle, square, circle, ellipse)
    pygame.display.update()