import pygame
from farbkonstanten import constants as const
import random

pygame.init()

width, height = 500, 500
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("SKY")

beginner_rad = 1

run = True

speed = 1

stars = []

class Stern:
    def __init__(self, x, y, rad):
        self.x = x
        self.y = y
        self.rad = rad
        self.color = const['WHITE']
        self.x_v = self.x - width//2
        self.y_v = self.y - height//2

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.rad)

    def move(self, speed):
        if self.x + self.rad < 0 or self.x+self.rad > width\
            or self.y + self.rad > height\
            or self.y + self.rad < 0\
            or self.rad > 30:
            return False
        else:
            self.rad += speed//5
            self.x += speed//5*self.x_v//20
            self.y += speed//5*self.y_v//20
            return True

def control(speed):
    if len(stars) < 70:
        stars.append(Stern(random.randint(0, width), random.randint(0, height), beginner_rad))
    for el in stars:
        if not el.move(speed):
            stars.remove(el)




def redraw():
    screen.fill(const['BLACK'])
    for el in stars:
        el.draw(screen)
    pygame.display.update()

while run:

    m_keys = pygame.mouse.get_pressed()

    if m_keys[0] and speed < 50:
        speed += 1
    if m_keys[2] and speed > 1:
        speed -= 1

    clock.tick(27)

    for event in pygame.event.get():
        if event == pygame.QUIT:
            run = False

    control(speed)

    redraw()

pygame.quit()
