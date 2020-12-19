import random, time, pygame, sys
from pygame.locals import *


fps= 25
w_width = 1080
w_height = 720
bsize = 20
b_width = 25
b_height = 35
blankspace ='.'

mvsdfrq = 0.30
mvdwnfrq = 0.2

xmarg = int((w_height - b_width * bsize) / 2)
ymarg = w_height - (b_height * bsize) - 5
#             R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

brdrcolor = RED
bgcolor = BLACK
textcolor = WHITE 
txtshwcolor = GRAY
colors      = (     BLUE,      GREEN,      RED,      YELLOW)
lightcolors = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(colors) == len(lightcolors)
t_width = 5
t_height = 5

S_SHAPE_TEMPLATE = [['.....',             
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

pieces = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}


def main():
    global fpsclock,bigfont,gamewindow,normalfont
    pygame.init()
    fpsclock = pygame.time.Clock()
    gamewindow = pygame.display.set_mode((w_width, w_height))
    normalfont = pygame.font.Font('freesansbold.ttf', 18) 
    bigfont = pygame.font.Font('freesansbold.ttf', 40)
    pygame.display.set_caption('Tetris Remastered')
    display_text('Tetris Remastered')
    while True:
        run_game()
        #pygame.mixer.music.stop()
        display_text('Game Over')

def run_game():
    board = displayblankboard()
    lmdt = time.time()
    lmst = time.time()
    lft = time.time()
    md = False # note: there is no movingUp variable
    ml = False
    mr = False
    score = 0
    lvl, fallfreq = lvl_and_fall_frq(score)

    fp = new_piece()
    np = new_piece()

    while True: # game loop
        if fp == None:
            # No falling piece in play, so start a new piece at the top
            fp = np
            np = new_piece()
            lft = time.time() # reset lft

            if not valid_position(board, fp):
                return # can't fit a new piece on the board, so game over

        check_if_end_game()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP:
                if (event.key == K_p):
                    # Pausing the game
                    gamewindow.fill(bgcolor)
                    pygame.mixer.music.stop()
                    display_text('Paused') # pause until a key press
                    pygame.mixer.music.play(-1, 0.0)
                    lft = time.time()
                    lmdt = time.time()
                    lmst = time.time()
                elif (event.key == K_LEFT or event.key == K_a):
                    ml = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    mr = False
                elif (event.key == K_DOWN or event.key == K_s):
                    md = False

            elif event.type == KEYDOWN:
                # moving the piece sideways
                if (event.key == K_LEFT or event.key == K_a) and valid_position(board, fp, adjX=-1):
                    fp['x'] -= 1
                    ml = True
                    mr = False
                    lmst = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and valid_position(board, fp, adjX=1):
                    fp['x'] += 1
                    mr = True
                    ml = False
                    lmst = time.time()

                # rotating the piece (if there is room to rotate)
                elif (event.key == K_UP or event.key == K_w):
                    fp['rotation'] = (fp['rotation'] + 1) % len(pieces[fp['shape']])
                    if not valid_position(board, fp):
                        fp['rotation'] = (fp['rotation'] - 1) % len(pieces[fp['shape']])
                elif (event.key == K_q): # rotate the other direction
                    fp['rotation'] = (fp['rotation'] - 1) % len(pieces[fp['shape']])
                    if not valid_position(board, fp):
                        fp['rotation'] = (fp['rotation'] + 1) % len(pieces[fp['shape']])

                # making the piece fall faster with the down key
                elif (event.key == K_DOWN or event.key == K_s):
                    md = True
                    if valid_position(board, fp, adjY=1):
                        fp['y'] += 1
                    lmdt = time.time()

                # move the current piece all the way down
                elif event.key == K_SPACE:
                    md = False
                    ml = False
                    mr = False
                    for i in range(1, b_height):
                        if not valid_position(board, fp, adjY=i):
                            break
                    fp['y'] += i - 1

        # handle moving the piece because of user input
        if (ml or mr) and time.time() - lmst > mvsdfrq:
            if ml and valid_position(board, fp, adjX=-1):
                fp['x'] -= 1
            elif mr and valid_position(board, fp, adjX=1):
                fp['x'] += 1
            lmst = time.time()

        if md and time.time() - lmdt > mvdwnfrq and valid_position(board, fp, adjY=1):
            fp['y'] += 1
            lmdt = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lft > fallfreq:
            # see if the piece has landed
            if not valid_position(board, fp, adjY=1):
                # falling piece has landed, set it on the board
                display_to_board(board, fp)
                score += remvcomp_line(board)
                lvl, fallfreq = lvl_and_fall_frq(score)
                fp = None
            else:
                # piece did not land, just move the piece down
                fp['y'] += 1
                lft = time.time()

        # drawing everything on the screen
        gamewindow.fill(bgcolor)
        drboard(board)
        drstat(score, lvl)
        drnxtpiece(np)
        if fp != None:
            drpiece(fp)

        pygame.display.update()
        fpsclock.tick(fps)


def end_game():
        pygame.quit()
        sys.exit()


def text_obj(text, font, color):
    dis = font.render(text, True, color)
    return dis,dis.get_rect()
    


def keypress_event_check():
    check_if_end_game()
    for event in pygame.event.get([KEYDOWN,KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def display_text(text):
    #Drawing the text shadow
    titledis, titleRect = text_obj(text, bigfont, txtshwcolor)
    titleRect.center = (int(w_width / 2), int(w_height / 2))
    gamewindow.blit(titledis, titleRect)

    #Drawing the text
    titledis, titleRect = text_obj(text, bigfont, textcolor)
    titleRect.center = (int(w_width / 2) - 3, int(w_height / 2) - 3)
    gamewindow.blit(titledis, titleRect)
    #Draw the additional "press a key to start"
    keypress, keypressRect = text_obj('Press any key to Start.', bigfont, textcolor)
    keypressRect.center = (int(w_width / 2), int(w_height / 2) + 100)
    gamewindow.blit(keypress, keypressRect)
    while keypress_event_check() == None:
        pygame.display.update()
        fpsclock.tick()


def check_if_end_game():
    for event in pygame.event.get(QUIT):
        end_game()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            end_game()
        pygame.event.post(event)


def lvl_and_fall_frq(score):
    lvl = int(score / 10) + 1
    frqforfall = 0.27 - (lvl * 0.02)
    return lvl, frqforfall


def new_piece():
    #func returns a random piece
    shape = random.choice(list(pieces.keys()))
    newpiece = {'shape': shape,
                'rotation': random.randint(0, len(pieces[shape]) - 1),
                'x': int(b_width / 2) - int(t_width / 2),
                'y': -2,
                'color': random.randint(0, len(colors) - 1)}
    return newpiece

    
def display_to_board(board, piece):
    #filling the board based on piece's location, shape, and rotation
    for x in range(t_width):
        for y in range(t_height):
            if pieces[piece['shape']][piece['rotation']][y][x] != blankspace:
                print(x,y)
                board[x + piece['x']][y + piece['y']] = piece['color']
                

def displayblankboard():
    board = []
    for i in range(b_width):
        board.append([blankspace] * b_height)
    return board


def isonboard(x, y):
    return x >= 0 and x < b_width and y < b_height

    
def valid_position(board, piece, adjX = 0, adjY = 0):
    for x in range((t_width)):
        for y in range(t_height):
            isaboveboard = y + piece['y'] + adjY < 0
            if isaboveboard or pieces[piece['shape']][piece['rotation']][y][x] == blankspace:
                continue
            if not isonboard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != blankspace:
                return False
    return True
        




def compl_line(board,y):
    for x in range(b_width):
        if board[x][y]==blankspace:
            return False
    return True
    
def remvcomp_line(board):
    nlremv=0
    y=b_height-1
    while y>=0:
        if compl_line(board,y):
            for pdy in range(y,0,-1):
                for x in range(b_width):
                    board[x][pdy]=board[x][pdy-1]
            for x in range(b_width):
                board[x][0]=blankspace
            nlremv+=1
        else:
            y-=1
    return nlremv
    

def ctpc(bx,by):
    return (xmarg+(bx*bsize)),(ymarg + (by*bsize))

def drbox(bx,by,color,px=None,py=None):
    if color==blankspace:
        return
    if px==None and py==None:
        px,py= ctpc(bx,by)
    pygame.draw.rect(gamewindow,colors[color],(px+1,py+1,bsize-1,bsize-1))
    pygame.draw.rect(gamewindow,lightcolors[color],(px+1,py+1,bsize-4,bsize-4))

def drboard(board):
    pygame.draw.rect(gamewindow,brdrcolor,(xmarg-3,ymarg-7,(b_width*bsize)+8,(b_height*bsize)+8),5)
    pygame.draw.rect(gamewindow,bgcolor,(xmarg,ymarg,bsize*b_width,bsize*b_width))
    for x in range(b_width):
        for y in range(b_height):
            drbox(x,y,board[x][y])



def drstat(score,lvl):
    ssurf=normalfont.render('Score: %s' % score, True, textcolor)
    srect=ssurf.get_rect()
    srect.topleft=(w_width-150,20)
    gamewindow.blit(ssurf,srect)
    lvlsurf=normalfont.render('Score: %s' % lvl, True, textcolor)
    lvlrect=lvlsurf.get_rect()
    lvlrect.topleft=(w_width-150,50)
    gamewindow.blit(lvlsurf,lvlrect)
    

def drpiece(piece,px=None,py=None):
    std=pieces[piece['shape']][piece['rotation']]
    if px==None and py==None:
        px,py=ctpc(piece['x'],piece['y'])
        
    for x in range(t_width):
        for y in range(t_height):
             if std[y][x]!=blankspace:
                drbox(None,None,piece['color'],px+(x*bsize),py+(y*bsize))



def drnxtpiece(piece):
    nxtsurf=normalfont.render('Next',True,textcolor)
    nxtrect=nxtsurf.get_rect()
    nxtrect.topleft=(w_width-120,80)
    gamewindow.blit(nxtsurf,nxtrect)
    drpiece(piece,px=w_width-120,py=100)
    
    
if __name__ == '__main__':
    main()
