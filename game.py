import pygame
import random
from sklearn.linear_model import LogisticRegression
import numpy as np
import cx_Freeze
display_width = 800
display_height = 600

Red = (255, 15, 10)
Blue = (10, 10, 255)
Green = (50, 150, 80)
White = (255, 255, 255)
Grey = (210, 210, 210)
Black = (0, 0, 0)

Shape_rect = 'rect'
Shape_circle = 'circle'


pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 16)
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('balls')
clock = pygame.time.Clock()

# image1 = pygame.image.load('clipart11701.png')
# image1 = pygame.transform.scale(image1, (120, 100))
#
# image2 = pygame.image.load('Corruption_and_Energy.png')
# image2 = pygame.transform.scale(image2, (120, 100))

image_width = 120

to_draw_pos = (100, 260)

def the_object(image, x, y):
    gameDisplay.blit(image, (x, y))

def things(thing_x, thing_y, thing_w, thing_h, thing_color):
    pygame.draw.rect(gameDisplay, Red, [thing_x, thing_y, thing_w, thing_h])

class Circle:
    def __init__(self, position):
        self.position = position
    def draw(self, position):
        pygame.draw.ellipse(gameDisplay, Blue, [position[0], position[1], 20, 20])
class Rect:
    def __init__(self, position):
        self.position = position
    def draw(self, position):
        pygame.draw.rect(gameDisplay, Red, [position[0], position[1], 20, 20])

def draw_the_thing(thing):
    thing.draw(thing)

def draw_classifier_helper(weights):
    points = []
    # (-w[0] - w[1] * X_1) / w[2]
    plot_helper = [i for i in range(-800, 600, 20)]
    X_2_values = [(-weights[0] - weights[1] * i) / weights[2] for i in plot_helper]
    for i in range(len(plot_helper)):
        points.append((plot_helper[i] + 400, X_2_values[i] + 300))
    return points

def Classify(Circles, Rects):
    X = []
    y = []
    for i in Circles:
        X.append(i.position)
        y.append(0)
    for i in Rects:
        X.append(i.position)
        y.append(1)
    X = np.array(X)
    y = np.array(y)

    for i in X:
        i[0] -= 400
        i[1] -= 300

    model = LogisticRegression()
    model.fit(X, y)
    coef = model.coef_
    intercept = model.intercept_
    print(model.score(X, y))
    return draw_classifier_helper([intercept[0], coef[0][0], coef[0][1]])

def game_loop():

    Cirles = []
    Rects = []
    Dropping_Mode = False
    Shape_to_draw = ''
    Draw_clf_line = False

    event = False

    while not event:
        for i in pygame.event.get():
            #####
            if i.type == pygame.MOUSEBUTTONDOWN and Dropping_Mode and Shape_to_draw == 'circle':
                to_draw_pos = i.pos
                shape_to_be_drawn = Circle(position=to_draw_pos)
                Cirles.append(shape_to_be_drawn)
            if i.type == pygame.MOUSEBUTTONDOWN and Dropping_Mode and Shape_to_draw == 'rect':
                to_draw_pos = i.pos
                shape_to_be_drawn = Rect(position=to_draw_pos)
                Rects.append(shape_to_be_drawn)
            #####
            if i.type == pygame.QUIT:
                event = True
            ####
            #Buttons:
            if i.type == pygame.MOUSEBUTTONDOWN:
                # left
                if i.pos[0] < display_width * 0.52 and i.pos[1] > display_height * 0.92:
                    if i.pos[0] > display_width * 0.44 and i.pos[1] < display_height:
                        if Dropping_Mode and Shape_to_draw == 'circle':
                            if len(Cirles) != 0:
                                Cirles.pop()
                            # Dropping_Mode = False
                        if Dropping_Mode and Shape_to_draw == 'rect':
                            if len(Rects) != 0:
                                Rects.pop()
                            # Dropping_Mode = False
                        Shape_to_draw = 'rect'
                        Dropping_Mode = True
                # right
                if i.pos[0] > display_width * 0.52 and i.pos[1] > display_height * 0.92:
                    if i.pos[0] < display_width * 0.60 and i.pos[1] < display_height:
                        if Dropping_Mode and Shape_to_draw == 'rect':
                            if len(Rects) != 0:
                                Rects.pop()
                            # Dropping_Mode = False
                        if Dropping_Mode and Shape_to_draw == 'circle':
                            if len(Cirles) != 0:
                                Cirles.pop()
                            # Dropping_Mode = False
                        Dropping_Mode = True
                        Shape_to_draw = 'circle'
                # Classify:
                if i.pos[0] > display_width * 0.5 and i.pos[1] < display_height * 0 + 35:
                    if Dropping_Mode and Shape_to_draw == 'rect':
                        if len(Rects) != 0:
                            Rects.pop()
                        # Dropping_Mode = False
                    if Dropping_Mode and Shape_to_draw == 'circle':
                        if len(Cirles) != 0:
                            Cirles.pop()
                    if i.pos[0] < display_width * 0.5 + 60:
                        points = Classify(Cirles, Rects)
                        Dropping_Mode = False
                        Draw_clf_line = True

            #####

        gameDisplay.fill(Grey)

        if len(Cirles) is not 0:
            for i in Cirles:
                i.draw(i.position)
        if len(Rects) is not 0:
            for i in Rects:
                i.draw(i.position)
        if Draw_clf_line:
            for i in range(len(points)):
                if i < len(points) - 1:
                    pygame.draw.line(gameDisplay, Black, [points[i][0], points[i][1]],
                                     [points[i+1][0], points[i+1][1]], 3)
        ############################
        # Buttons:
        pygame.draw.rect(gameDisplay, Red, [display_width*0.46, display_height*0.93, 35, 35])
        pygame.draw.ellipse(gameDisplay, Blue, [display_width*0.54, display_height*0.93, 35, 35])
        pygame.draw.line(gameDisplay, Black, [display_width * 0.44, display_height],
                         [display_width * 0.44, display_height*0.92], 1)
        pygame.draw.line(gameDisplay, Black, [display_width * 0.60, display_height],
                         [display_width * 0.60, display_height * 0.92], 1)
        pygame.draw.line(gameDisplay, Black, [display_width * 0.44, display_height*0.92],
                         [display_width * 0.60, display_height * 0.92], 1)
        pygame.draw.line(gameDisplay, Black, [display_width * 0.52, display_height],
                         [display_width * 0.52, display_height * 0.92], 1)
        # Classify
        pygame.draw.rect(gameDisplay, Green, [display_width*0.50, display_height*0, 60, 35])
        textsurface = myfont.render('Classify', False, (0, 0, 0))
        gameDisplay.blit(textsurface, (display_width*0.50, 0))
        ############################

        pygame.display.update()
        clock.tick(30)
game_loop()
pygame.quit()
quit()