import pygame
import math
import sys

pygame.init()

res = 960
hres = res / 2

screen = pygame.display.set_mode((res * 16 / 9, res))
clock = pygame.time.Clock()

vertex = []

for x in range(10):
    for y in range(10):
        vertex += [[10+x*10, 0, y*10], [x*10, 0, y*10], [10+x*10, 0, 10+y*10], [x*10, 0, 10+y*10],
                      [10+x*10, 10, y*10], [x*10, 10, y*10], [10+x*10, 10, 10+y*10], [x*10, 10, 10+y*10]]

lines = [[0, 1], [0, 2], [2, 3], [1, 3], [4, 5], [4, 6], [6, 7], [5, 7], [0, 4], [1, 5], [2, 6], [3, 7]]

#lines = [[x + y * 20, x + 1 + y * 20] for x in range(19) for y in range(20)
#        ] + [[x * 20 + y, (x + 1) * 20 + y] for x in range(19) for y in range(20)]
     
focall = 7
cam = [20, 10, -20]
croty = 0
crotx = 0
farest = 100

def translate(v3o, v3t):
    return v3o[0] + v3t[0], v3o[1] + v3t[1], v3o[2] + v3t[2]

def negative(v3):
    return -v3[0], -v3[1], -v3[2]

def weak_pers(v3):
    v3 = translate(v3, negative(cam))
    div = focall + v3[2]
    if div <= 0:
        return -1
    return focall * v3[0] / div, focall * v3[1] / div

def rotate_y(v3, angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return v3[0] * c + v3[2] * s, v3[1], -v3[0] * s + v3[2] * c

def rotate_x(v3, angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return v3[0], v3[1] * c - v3[2] * s, v3[1] * s + v3[2] * c

def tos(v2):
    return v2[0] * 100 + hres, hres - v2[1] * 100

def rotate_on_orgin(orgin, v3, angley, anglex):
    v3 = translate(rotate_x(rotate_y(translate(v3, negative(orgin)), angley), anglex), orgin)
    return v3

def distance2v(v2orgin, v2):
    v2 = translate(v2, negative(v2orgin))
    return (v2[0]**2 + v2[1]**2)**0.5

def distance3v(v3orgin, v3):
    v3 = translate(v3, negative(v3orgin))
    return (v3[0]**2 + v3[1]**2 + v3[2]**2)**0.5

def foward(v3, angley, anglex, step):
    direcv3 = rotate_x(rotate_y((0, 0, step), -angley), -anglex)
    return translate(v3, direcv3)

tick = 0
smx = -1
move = 0

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            smx, smy = pygame.mouse.get_pos()
            ocroty = croty
            ocrotx = crotx
        elif e.type == pygame.MOUSEBUTTONUP:
            smx = -1
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                move = 0.1
            elif e.key == pygame.K_LSHIFT:
                move = -0.1
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_SPACE:
                move = 0
            if e.key == pygame.K_LSHIFT:
                move = 0

    if smx != -1:
        mx, my = pygame.mouse.get_pos()
        croty = ocroty + (mx - smx) / hres * math.pi
        crotx = ocrotx + (my - smy) / hres * math.pi

    if move:
        cam = foward(cam, croty, crotx, move)

    screen.fill(0)

    rver2s = []

    for v3 in vertex:
        pv4 = farest - distance3v(cam, v3)
        if pv4 > 0:
            pers = weak_pers(rotate_on_orgin(cam, v3, croty, crotx))
            if pers != -1:
                pers = tos(pers)
                rver2s.append(pers)
                pygame.draw.circle(screen, 0xffffff, pers, 2)
            else:
                rver2s.append(-1)
        else:
            rver2s.append(-1)

    for li in lines:
        v2o = rver2s[li[0]]
        v2t = rver2s[li[1]]
        if v2o != -1 and v2t != -1:
            pygame.draw.line(screen, 0xffffff, v2o, v2t)

    pygame.display.flip()
    clock.tick(60)
    tick += 1
