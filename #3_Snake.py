import pygame
from farbkonstanten import constants as const
import random
pygame.init()

width, height = 500, 500

screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

font = pygame.font.SysFont("Helvetica", 30)

blocksize = 10

enemy_speed = 10

enemy_count = 0
enemy_max = 20

enemy_speed_count = 0
enemy_speed_max = 400
max_speed = 20

eat_max = 20
eat_count = 0

run = True

class Stein:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = const['WHITE']
        self.size = blocksize

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def move(self, x, y):
        self.x += x
        self.y += y

class Snake:
    def __init__(self, start_size=3, max_size=200, eat_to_grow=3):
        self.x = random.randint(0, width//blocksize*blocksize-blocksize*start_size)
        self.y = random.randint(0, height//blocksize*blocksize-blocksize)
        self.steine = []
        self.max_size = max_size
        self.start_size = start_size
        x = self.x
        self.eaten = False
        self.eat_count = 0
        self.eat_to_grow = eat_to_grow
        for k in range(start_size):
            self.steine.append(Stein(x, self.y))
            x += blocksize
        del x
        self.richtung = 'l'

    def draw(self, screen):
        for el in self.steine:
            el.draw(screen)

    def move(self, r):
        self.richtung = r
        x = 0
        y = 0
        func = True
        if r == 'l' and self.steine[0].x > 0:
            x = -blocksize
        elif r == 'r' and self.steine[0].x+blocksize < width:
            x = blocksize
        elif r == 'o' and self.steine[0].y > 0:
            y = -blocksize
        elif r == 'u' and self.steine[0].y+blocksize < height:
            y = blocksize
        else:
            func = False
        if func:
            if self.eaten and len(self.steine) <= self.max_size:
                self.steine.append(Stein(self.steine[-1].x, self.steine[-1].y))
            liste = (self.steine[::-1] if not self.eaten and len(self.steine) <= self.max_size else self.steine[:-1:-1])
            for el in liste:
                if self.steine.index(el) != 0:
                    el.x = self.steine[self.steine.index(el)-1].x
                    el.y = self.steine[self.steine.index(el)-1].y
            self.steine[0].move(x, y)
            self.x = self.steine[0].x
            self.y = self.steine[0].y
        self.eaten = False

    def eat(self):
        self.eat_count += 1
        if self.eat_count >= self.eat_to_grow:
            self.eat_count = 0
            self.eaten = True

class Enemy(Stein):
    def __init__(self, x, y, ch):
        super().__init__(x, y)
        self.ch = ch




essen = []
enemys = []
Schlange = Snake()

def control():
    global eat_count
    global enemy_speed_count
    global enemy_count
    global enemy_speed
    eat_count += 1
    enemy_speed_count += 1
    enemy_count += 1
    if eat_count >= eat_max and len(essen) < 9:
        eat_count = 0
        essen.append(Stein(random.randint(0, width//blocksize*blocksize),
        random.randint(0, height//blocksize*blocksize)))
        essen[-1].color = const['RED']
    if enemy_count >= enemy_max:
        choices =  [1, 2]
        choice = random.choice(choices)
        if choice == 1:
            enemys.append(Enemy(0, random.randint(0, height//blocksize*blocksize), choice))
        else:
            enemys.append(Enemy(random.randint(0, width//blocksize*blocksize), 0, choice))
        enemy_count = 0
        enemys[-1].color = const['BLUE']
    if enemy_speed_count >= enemy_speed_max and enemy_speed < max_speed:
        enemy_speed_count = 0
        enemy_speed += 1



def redraw():
    screen.fill(const['GREY'])
    screen.blit(font.render("Score: "+str(len(Schlange.steine)-Schlange.start_size+1), True, const['WHITE']), (5, 5))
    Schlange.draw(screen)
    for el in essen:
        el.draw(screen)
    for el in enemys:
        el.draw(screen)
    pygame.display.update()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    clock.tick(27)

    x = Schlange.steine[0].x
    y = Schlange.steine[0].y

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        Schlange.move('r')
    if keys[pygame.K_LEFT]:
        Schlange.move('l')
    if keys[pygame.K_DOWN]:
        Schlange.move('u')
    if keys[pygame.K_UP]:
        Schlange.move('o')


    for el in Schlange.steine:
        for es in essen:
            if el.x >= es.x and el.x <= es.x+blocksize and el.y >= es.y and el.y <= es.y + blocksize\
            or el.x+blocksize >= es.x and el.x + blocksize <= es.x+blocksize and el.y >= es.y and el.y <= es.y+blocksize:
                Schlange.eat()
                essen.remove(es)

    for el in enemys:
        if el.ch == 1:
            if el.x <= width:
                el.x += enemy_speed
            else:
                enemys.remove(el)
        else:
            if el.y <= height:
                el.y += enemy_speed
            else:
                enemys.remove(el)

    for el in Schlange.steine:
        for es in enemys:
            if el.x >= es.x and el.x <= es.x+blocksize and el.y >= es.y and el.y <= es.y + blocksize\
            or el.x+blocksize >= es.x and el.x + blocksize <= es.x+blocksize and el.y >= es.y and el.y <= es.y+blocksize:
                run = False
    control()

    redraw()

pygame.quit()
