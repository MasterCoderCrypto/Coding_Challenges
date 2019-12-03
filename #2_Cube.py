import pygame
from farbkonstanten import constants as const

pygame.init()

width = height = 500

rotation_speed = 6

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Cube')

class Cube:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.l_1 = False
        self.l_2 = False
        self.l_3 = False
        self.ausgang = True
        self.color = const['WHITE']
        self.nodes = [[self.x, self.y], [self.x+self.size, self.y],
                      [self.x, self.y+self.size], [self.x+self.size, self.y+self.size],
                      [self.x+self.size//4, self.y+self.size//4], [self.x+self.size//4*3, self.y+self.size//4],
                      [self.x+self.size//4, self.y+self.size-self.size//4], [self.x+self.size//4*3, self.y+self.size-self.size//4]]
    def draw(self, screen):
        self.line(screen, 0, 1)
        self.line(screen, 0, 2)
        self.line(screen, 2, 3)
        self.line(screen, 1, 3)
        self.line(screen, 4, 5)
        self.line(screen, 4, 6)
        self.line(screen, 6, 7)
        self.line(screen, 5, 7)
        self.line(screen, 0, 4)
        self.line(screen, 1, 5)
        self.line(screen, 2, 6)
        self.line(screen, 3, 7)

    def move(self, dest):
        if dest == 'l':
            if self.ausgang:
                a, b, c, d, e, f, g, h = 0, 1, 2, 3, 4, 5, 6, 7
            elif self.l_1:
                a, b, c, d, e, f, g, h = 1, 5, 3, 7, 0, 4, 2, 6
            elif self.l_2:
                a, b, c, d, e, f, g, h = 5, 4, 7, 6, 1, 0, 3, 2
            elif self.l_3:
                a, b, c, d, e, f, g, h = 4, 0, 6, 2, 5, 1, 7, 3
            if self.nodes[b][0] > self.x:
                self.nodes[b][0] -= 1
                self.nodes[d][0] -= 1
                self.nodes[a][0] += 0.25
                self.nodes[a][1] += 0.25
                self.nodes[c][0] += 0.25
                self.nodes[c][1] -= 0.25
                self.nodes[g][0] += 0.5
                self.nodes[e][0] += 0.5
                self.nodes[f][0] += 0.25
                self.nodes[f][1] -= 0.25
                self.nodes[h][0] += 0.25
                self.nodes[h][1] += 0.25
            else:
                self.rotate()
    def rotate(self):
        if self.ausgang:
            self.ausgang = False
            self.l_1 = True
        elif self.l_1:
            self.l_1 = False
            self.l_2 = True
        elif self.l_2:
            self.l_2 = False
            self.l_3 = True
        elif self.l_3:
            self.l_3 = False
            self.ausgang = True



    def line(self, screen, n1, n2):
        pygame.draw.line(screen, self.color, (round(self.nodes[n1][0]), round(self.nodes[n1][1])),
        (round(self.nodes[n2][0]), round(self.nodes[n2][1])))

cube = Cube(width//4, height//4, width//2)

def redraw():
    screen.fill(const['BLACK'])
    cube.draw(screen)
    pygame.display.update()

while 1:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    m = pygame.mouse.get_pressed()

    if m[0]:
        for t in range(rotation_speed):
            cube.move('l')


    redraw()

pygame.quit()
