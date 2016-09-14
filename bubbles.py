import pygame, math, os, random
from pygame.locals import *
from time import sleep
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 255, 0)
DARKBLUE = (0, 0, 150)
CELLWIDTH = 50
currentplayer = 1
explodingcells = []
screen = pygame.display.set_mode((600, 600),HWSURFACE|DOUBLEBUF|RESIZABLE)
pygame.display.set_caption('Bubbles')
fps = pygame.time.Clock()


class cell():
    def __init__(self, bubbles, player):
        self.bubbles = bubbles
        self.player = player


def load_image(name):
    fullname = os.path.join('resources', name)
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = pygame.transform.smoothscale(image, (CELLWIDTH, CELLWIDTH))
    return image
           

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('resources', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound

def getboardsize():
    while True:
        screen.fill(BLACK)
        (x, y) = pygame.mouse.get_pos()
        (boardwidth, boardheight) = (int(math.ceil(x / 20.0)), int(math.ceil(y / 20.0)))
        screen.fill(DARKBLUE, (0, 0, 20 * boardwidth, 20 * boardheight))
        for a in range(30):
            pygame.draw.line(screen, WHITE, (20 * a, 0), (20 * a, 600))
        for b in range(30):
            pygame.draw.line(screen, WHITE, (0, 20 * b), (600, 20 * b))
        pygame.draw.line(screen, WHITE, (200, 0), (200, 120), 3)
        pygame.draw.line(screen, WHITE, (0, 120), (200, 120), 3)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                return (boardwidth, boardheight)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() 
    
def drawboard():
    screen.fill(BLACK)
    for x in range(boardwidth):
        for y in range(boardheight):
            screen.blit(FRAME, (x * CELLWIDTH, y * CELLWIDTH))
            if cells[x][y].player == 1 and cells[x][y].bubbles == 1:
                screen.blit(ONE_RED_BUBBLE, (x * CELLWIDTH, y * CELLWIDTH))
            if cells[x][y].player == 1 and cells[x][y].bubbles == 2:
                screen.blit(TWO_RED_BUBBLES, (x * CELLWIDTH, y * CELLWIDTH))
            if cells[x][y].player == 1 and cells[x][y].bubbles == 3:
                screen.blit(THREE_RED_BUBBLES, (x * CELLWIDTH, y * CELLWIDTH))
            if cells[x][y].player == 2 and cells[x][y].bubbles == 1:
                screen.blit(ONE_GREEN_BUBBLE, (x * CELLWIDTH, y * CELLWIDTH))
            if cells[x][y].player == 2 and cells[x][y].bubbles == 2:
                screen.blit(TWO_GREEN_BUBBLES, (x * CELLWIDTH, y * CELLWIDTH))
            if cells[x][y].player == 2 and cells[x][y].bubbles == 3:
                screen.blit(THREE_GREEN_BUBBLES, (x * CELLWIDTH, y * CELLWIDTH))

def explosions():
    while len(explodingcells) != 0:
        explode()

def checkexplode(x, y):
    if x == 0 and y == 0 or \
       x == (boardwidth - 1) and y == 0 or \
       x == 0 and y == (boardheight - 1)or \
       x == (boardwidth - 1) and y == (boardheight - 1):
        if cells[x][y].bubbles == 2:
            explodingcells.append((x, y, 3))
    elif x == 0 or \
         x == (boardwidth - 1) or \
         y == 0 or \
         y == (boardheight - 1):
        if cells[x][y].bubbles == 3:
            explodingcells.append((x, y, 2))
    else:
        if cells[x][y].bubbles == 4:
            explodingcells.append((x, y, 1))

def explode():
    global explodingcells, currentplayer
    blip_sound = getRandomSound()
    blip_sound.play()
    for x, y, explosiontype in explodingcells:
        if explosiontype == 1:
            cells[x][y].bubbles -= 4
        if explosiontype == 2:
            cells[x][y].bubbles -= 3
        if explosiontype == 3:
            cells[x][y].bubbles -= 2
    for step in range(10, CELLWIDTH, 2):
        drawboard()
        for x, y, explosiontype in explodingcells:
            if cells[x][y].player == 1:
                if x + 1 < boardwidth: 
                    screen.blit(ONE_RED_BUBBLE, (x * CELLWIDTH + step, y * CELLWIDTH))
                if x - 1 >= 0:
                    screen.blit(ONE_RED_BUBBLE, (x * CELLWIDTH - step, y * CELLWIDTH))
                if y + 1 < boardheight:
                    screen.blit(ONE_RED_BUBBLE, (x * CELLWIDTH, y * CELLWIDTH + step))
                if y - 1 >= 0:
                    screen.blit(ONE_RED_BUBBLE, (x * CELLWIDTH, y * CELLWIDTH - step))
            if cells[x][y].player == 2:
                if x + 1 < boardwidth: 
                    screen.blit(ONE_GREEN_BUBBLE, (x * CELLWIDTH + step, y * CELLWIDTH))
                if x - 1 >= 0:
                    screen.blit(ONE_GREEN_BUBBLE, (x * CELLWIDTH - step, y * CELLWIDTH))
                if y + 1 < boardheight:
                    screen.blit(ONE_GREEN_BUBBLE, (x * CELLWIDTH, y * CELLWIDTH + step))
                if y - 1 >= 0:   
                    screen.blit(ONE_GREEN_BUBBLE, (x * CELLWIDTH, y * CELLWIDTH - step))
        fps.tick(70)
        pygame.display.flip()
    done = explodingcells
    explodingcells = []
    for x, y, explosiontype in done:
        if cells[x][y].bubbles == 0:
            cells[x][y].player = 0
        if x + 1 < boardwidth: 
            cells[x + 1][y].bubbles += 1
            cells[x + 1][y].player = currentplayer
            checkexplode(x + 1, y)
        if x - 1 >= 0:
            cells[x - 1][y].bubbles += 1
            cells[x - 1][y].player = currentplayer
            checkexplode(x - 1, y)
        if y + 1 < boardheight:
            cells[x][y + 1].bubbles += 1
            cells[x][y + 1].player = currentplayer
            checkexplode(x, y + 1)
        if y - 1 >= 0:
            cells[x][y - 1].bubbles += 1
            cells[x][y - 1].player = currentplayer
            checkexplode(x, y - 1)
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            return (boardwidth, boardheight)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit() 
    #checkwin()

def checkwin():
    reds = 0
    greens = 0
    for x in range(boardwidth):
        for y in range(boardheight):
            if cells[x][y].player == 1:
                reds += 1
            if cells[x][y].player == 2:
                greens += 1
    if reds == 0 and greens > 1:
        win(2)
    if greens == 0 and reds > 1:
        win(1)

def getRandomSound():
    rand = random.randint(1,4)
    if rand == 1:
        return BLIP_SOUND1
    elif rand == 2:
        return BLIP_SOUND2
    elif rand == 3:
        return BLIP_SOUND3
    elif rand == 4:
        return BLIP_SOUND4
    else:
        return None


def win(player):
    WIN_FONT = pygame.font.Font('freesansbold.ttf', boardwidth * 8)
    REMATCH_FONT = pygame.font.Font('freesansbold.ttf', boardwidth * 3)
    if player == 1:
        wintext = WIN_FONT.render('Red Wins!', True, RED)
        rematchtext = REMATCH_FONT.render('Play Again?', True, RED)
    if player == 2:
        wintext = WIN_FONT.render('Green Wins!', True, GREEN)
        rematchtext = REMATCH_FONT.render('Play Again?', True, GREEN)
    screen.blit(wintext, wintext.get_rect(center = (boardwidth*CELLWIDTH/2, boardheight*CELLWIDTH/2)))
    screen.blit(rematchtext, rematchtext.get_rect(center = (boardwidth*CELLWIDTH/2, boardheight*CELLWIDTH/2 + boardwidth*6)))
    pygame.display.flip()
    replay(rematchtext)

def replay(rematchtext):
    global explodingcells
    button = rematchtext.get_rect(center = (boardwidth*CELLWIDTH/2, boardheight*CELLWIDTH/2 + boardwidth*6))
    clicked = False
    explodingcells = []
    while clicked == False:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                (x, y) = event.pos
                mouse = pygame.Rect(x, y, 0, 0)
                if mouse.colliderect(button):
                    clicked = True
                    for x in range(boardwidth):
                        for y in range(boardheight):
                            cells[x][y].player = 0
                            cells[x][y].bubbles = 0
                    drawboard()
                    pygame.display.flip()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  

def pause(seconds):
    for interval in range(0, seconds*10):
        sleep(.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

FRAME = load_image('frame.png')

ONE_RED_BUBBLE = load_image('1redball.png')
TWO_RED_BUBBLES = load_image('2redballs.png')
THREE_RED_BUBBLES = load_image('3redballs.png')

ONE_GREEN_BUBBLE = load_image('1greenball.png')
TWO_GREEN_BUBBLES = load_image('2greenballs.png')
THREE_GREEN_BUBBLES = load_image('3greenballs.png')

BLIP_SOUND1 = load_sound('pop1.ogg')
BLIP_SOUND2 = load_sound('pop2.ogg')
BLIP_SOUND3 = load_sound('pop3.ogg')
BLIP_SOUND4 = load_sound('pop4.ogg')

pygame.display.set_icon(THREE_RED_BUBBLES)
(boardwidth, boardheight) = getboardsize()
screen = pygame.display.set_mode(((boardwidth * CELLWIDTH), boardheight * CELLWIDTH),HWSURFACE|DOUBLEBUF|RESIZABLE)
cells = [[0 for y in range(boardheight)] for x in range(boardwidth)]
for x in range(boardwidth):
    for y in range(boardheight):
        cells[x][y] = cell(0,0)
drawboard()
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            x = int(math.floor(x / CELLWIDTH))
            y = int(math.floor(y / CELLWIDTH))
            if cells[x][y].player == currentplayer or cells[x][y].player == 0:
                cells[x][y].bubbles += 1
                cells[x][y].player = currentplayer
                checkexplode(x, y)
                explosions()
                if currentplayer == 1:
                    currentplayer = 2
                else:
                    currentplayer = 1
            drawboard()
            pygame.display.flip()
            checkwin()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

boardwidth = int(input('Enter number of columns '))
boardheight = int(input('Enter number of rows '))
    



