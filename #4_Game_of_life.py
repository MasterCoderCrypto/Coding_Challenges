import pygame
from farbkonstanten import constants as const
import random
import sys

pygame.init()

width, height = 500, 500

screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

pygame.display.set_caption('Game_of_life')

blocksize = 10

randomize = False

fps = 27

if '-r' in sys.argv:
    randomize = True

if '-fps' in sys.argv:
    fps = int(sys.argv[sys.argv.index('-fps')+1])

pre = True

class Zelle:
    def __init__(self, x, y, alive=False):
        self.x = x
        self.y = y
        self.draw_x = x*blocksize
        self.draw_y = y*blocksize
        self.color = const['GREEN']
        self.alive = (alive if not randomize else random.choice([True, False]))
    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, self.color, (self.draw_x, self.draw_y, blocksize, blocksize))

zellen = {}
besetzte = {}

for g in range(height//blocksize):
    for t in range(width//blocksize):
        zellen[(t, g)] = Zelle(t, g)

def generation():
    counter = 0
    for a, b in zellen:
        for t in range(-1, 2, 1):
            for u in range(-1, 2, 1):
                try:
                    if zellen[(a+t, b+u)].alive:
                        counter += 1
                except:
                    pass
        if zellen[(a, b)].alive:
            counter -= 1
            if counter <= 1 or counter >= 4:
                besetzte[(a, b)] = False
            else:
                besetzte[(a, b)] = True
        else:
            if counter == 3:
                besetzte[(a, b)] = True
            else:
                besetzte[(a, b)] = False
        counter = 0
    for el in besetzte:
        zellen[el].alive = besetzte[el]

def redraw():
    screen.fill((255, 255, 255))
    for el in zellen:
        zellen[el].draw(screen)
    pygame.display.update()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    clock.tick(fps)

    m = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    m_x, m_y = pygame.mouse.get_pos()
    m_xx, m_yy = m_x//blocksize, m_y//blocksize

    if not pre:
        generation()

    if pre:
        if m[0]:
            zellen[(m_xx, m_yy)].alive = True
        if m[2]:
            zellen[(m_xx, m_yy)].alive = False
        if keys[pygame.K_SPACE]:
            pre = False
            besetzte = {(zellen[el].x, zellen[el].y): zellen[el].alive for el in zellen}

    redraw()

pygame.quit()
