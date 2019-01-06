import pygame
import random
from sklearn.linear_model import RidgeClassifierCV
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

random.seed(0)

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 16)
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('GAME!')
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


class Drop:
    def __init__(self, position=[random.randrange(0, display_width), 600], vel=[0, -(random.randrange(30, 45))],
                 acc=[0, 0]):
        self.position = position
        self.vel = vel
        self.acc = acc
        self.particles = []
        self.g = 3

    def draw(self, particle = False):
        if not particle:
            pygame.draw.rect(gameDisplay, Red, [self.position[0], self.position[1], 20, 20])
        else:
            pygame.draw.rect(gameDisplay, Green, [self.position[0], self.position[1], 5, 5])

    def update(self):
        self.position[0] += self.vel[0]
        self.position[1] += self.vel[1]

        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1] + self.g

    def explode(self):
        for i in range(0, 100):
            temp = Drop(position=self.position, vel=[(random.randrange(-5, 1)), (random.randrange(-5, 1))],
                                       acc=[0, 0])
            # temp = Drop(position=self.position, vel=[(random.randrange(-15, 5)), (random.randrange(-15, 5))],
            #                            acc=[float(random.randrange(-20, 50)) / 10, float(random.randrange(-20, 50)) / 10])
            self.particles.append(temp)


class Particles(Drop):
    def __init__(self, position=[random.randrange(0, display_width), 600], vel=[0, -(random.randrange(30, 45))],
                 acc=[0, 0]):
        self.position = position
        self.vel = vel
        self.acc = acc
        self.particles = []
        self.g = 3

    def draw(self, particle = False):
        if not particle:
            pygame.draw.rect(gameDisplay, Red, [self.position[0], self.position[1], 20, 20])
        else:
            pygame.draw.rect(gameDisplay, Green, [self.position[0], self.position[1], 5, 5])

    def update(self):
        self.position[0] += self.vel[0]
        self.position[1] += self.vel[1]

        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1] + self.g

    def explode(self):
        for i in range(0, 100):
            temp = Drop(position=self.position, vel=[(random.randrange(-5, 1)), (random.randrange(-5, 1))],
                                       acc=[0, 0])
            # temp = Drop(position=self.position, vel=[(random.randrange(-15, 5)), (random.randrange(-15, 5))],
            #                            acc=[float(random.randrange(-20, 50)) / 10, float(random.randrange(-20, 50)) / 10])
            self.particles.append(temp)

class window:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self):
        pygame.draw.rect(gameDisplay, Red, [self.x, self.y, self.w, self.h])

    def clicked(self, pos):
        if self.x <= pos[0] <= self.x + self.w and self.y <= pos[1] <= self.y + self.h:
            return True
        else:
            return False


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


def Classify(Circles, Rects, model_name='RG'):
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
    if model_name == 'RG':
        model = RidgeClassifierCV()
    if model_name == 'LR':
        model = LogisticRegression()
    model.fit(X, y)
    coef = model.coef_
    intercept = model.intercept_
    print(model.score(X, y))
    return draw_classifier_helper([intercept[0], coef[0][0], coef[0][1]])

def Main_Menu():

    intro = True
    Button_1 = window(300, 500, 80, 40)
    Button_2 = window(400, 500, 80, 40)

    while intro:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                intro = False
            if i.type == pygame.MOUSEBUTTONDOWN:
                if Button_1.clicked(i.pos):
                    Classify_Game()

        gameDisplay.fill(White)

        Button_1.draw()
        Button_2.draw()

        pygame.display.update()
        clock.tick(60)


def Classify_Game():
    Cirles = []
    Rects = []
    Dropping_Mode = False
    Shape_to_draw = ''
    Draw_clf_line = False
    draw_particles = False
    event = False
    a = Drop()
    list_of_drops = list()
    list_of_particles = []

    ck = False
    newWindow = window(10, 10, 30, 40)
    model_name = 'RG'

    for x in range(1, 2):
        list_of_drops.append(Drop(position=[random.randrange(0, display_width), 600]))

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
            if i.type == pygame.MOUSEBUTTONDOWN:
                ck = newWindow.clicked(i.pos)
            if i.type == pygame.QUIT:
                event = True
            ####
            # Buttons:
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
                        points = Classify(Cirles, Rects, )
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
                                     [points[i + 1][0], points[i + 1][1]], 3)
        ############################
        # Buttons:
        pygame.draw.rect(gameDisplay, Red, [display_width * 0.46, display_height * 0.93, 35, 35])
        pygame.draw.ellipse(gameDisplay, Blue, [display_width * 0.54, display_height * 0.93, 35, 35])
        pygame.draw.line(gameDisplay, Black, [display_width * 0.44, display_height],
                         [display_width * 0.44, display_height * 0.92], 1)
        pygame.draw.line(gameDisplay, Black, [display_width * 0.60, display_height],
                         [display_width * 0.60, display_height * 0.92], 1)
        pygame.draw.line(gameDisplay, Black, [display_width * 0.44, display_height * 0.92],
                         [display_width * 0.60, display_height * 0.92], 1)
        pygame.draw.line(gameDisplay, Black, [display_width * 0.52, display_height],
                         [display_width * 0.52, display_height * 0.92], 1)
        # Classify
        pygame.draw.rect(gameDisplay, Green, [display_width * 0.50, display_height * 0, 60, 35])
        textsurface = myfont.render('Classify', False, (0, 0, 0))
        gameDisplay.blit(textsurface, (display_width * 0.50, 0))
        ############################

        ##################
        # rain
        # for x in list_of_drops:
        #     if x.position[1] > 600:
        #         x.position[1] = 600
        #         x.vel = [-i * 0.7 for i in x.vel]
        #     x.update()
        #     x.draw()

        newWindow.draw()

        a.update()
        a.draw()

        if not draw_particles:
            if a.vel[1] > 0:
                a.explode()
                list_of_particles = a.particles
                draw_particles = True

        if len(list_of_particles) != 0:
            for i in list_of_particles:
                i.update()
                i.draw(particle=True)

        if ck:
            #print('go')
            #newWindow.x, newWindow.y = random.randint(0, display_width - newWindow.w), random.randint(0, display_height - newWindow.h)
            model_name = 'LR'
            ck = False
        ###########

        pygame.display.update()
        clock.tick(60)


Main_Menu()
#game_loop()
pygame.quit()
quit()