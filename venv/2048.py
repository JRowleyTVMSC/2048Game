import pygame, sys, time
from pygame.locals import *
from colorWheel import *
from random import *

POINTS = 0
DEFAULT_SCORE = 2
BOARDSIZE = 4

pygame.init()

DISPLAYSURF = pygame.display.set_mode((400, 500), 0, 32)
pygame.display.set_caption("Issa Game yo")

myfont = pygame.font.SysFont("freesandbold", 25)
scorefont = pygame.font.SysFont("freesandbold", 50)

gBoard = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
undoBoard = []


def main(fromLoaded=False) :
    if not fromLoaded:
        placeRandomTile()
        placeRandomTile()

    printBoard()

    while True:
        for event in pygame.event.get() :
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if checkIfCanGo() == True:
                if event.type == KEYDOWN :
                    if isArrow(event.key) :
                        rotations = getRotations(event.key)

                        addToUndo()

                        for i in range(0, rotations) :
                            clockwiseBoard()

                        if canMove() :
                            moveTiles()
                            mergeTiles()
                            placeRandomTile()

                        for j in range(0, (4 - rotations) % 4) :
                            clockwiseBoard()

                        printBoard()
            else:
                printGameOver()

            if event.type == KEYDOWN:
                global BOARDSIZE

                if event.key == pygame.K_r :
                    reset()

                if 50 < event.key and 56 > event.key :
                    BOARDSIZE = event.key - 48
                    reset()

                if event.key == pygame.K_s :
                    saveGameState()
                elif event.key == pygame.K_l :
                    loadGameState()
                elif event.key == pygame.K_u :
                    undo()

        pygame.display.update()

# deprecation warning on 85 and 91, not sure why, but doesnt seem to mess anything up
def printBoard() :
    DISPLAYSURF.fill(BLACK)

    global BOARDSIZE
    global POINTS

    for i in range(0, BOARDSIZE) :
        for j in range(0, BOARDSIZE):
            pygame.draw.rect(DISPLAYSURF, colorWheel(gBoard[i][j]),
                             (i * (400 / BOARDSIZE), j * (400 / BOARDSIZE) + 100, 400 / BOARDSIZE, 400 / BOARDSIZE))

            label = myfont.render(str(gBoard[i][j]), 1, (255, 255, 255))
            label2 = scorefont.render("Score:" + str(POINTS), 1, (255, 255, 255))

            DISPLAYSURF.blit(label, (i * (400 / BOARDSIZE) + 30, j * (400 / BOARDSIZE) + 130))
            DISPLAYSURF.blit(label2, (10, 20))


def printGameOver() :
    global POINTS

    DISPLAYSURF.fill(BLACK)

    label = scorefont.render("Ya done kid", 1, (255, 255, 255))
    label2 = scorefont.render("Score:" + str(POINTS), 1, (255, 255, 255))
    label3 = myfont.render("R to restart!", 1, (255, 255, 255))

    DISPLAYSURF.blit(label, (50, 100))
    DISPLAYSURF.blit(label2, (50, 200))
    DISPLAYSURF.blit(label3, (50, 300))

# not the most complicated but the most annoying method
# took a few hours to figure out
def placeRandomTile() :
    count = 0
    for i in range(0, BOARDSIZE):
        for j in range(0, BOARDSIZE):
            if gBoard[i][j] == 0:
                count += 1

    k = floor(random() * BOARDSIZE * BOARDSIZE)

    while gBoard[floor(k / BOARDSIZE)][k % BOARDSIZE] != 0:
        k = floor(random() * BOARDSIZE * BOARDSIZE)

    gBoard[floor(k / BOARDSIZE)][k % BOARDSIZE] = 2

# another method that i got from a friend. was running into some issues with the random tile placement
# so this rather simple method is what i went with. it ended up being integrated with one or two other methods too
def floor(n) :
    return int(n - (n % 1))


def moveTiles() :
    # column by column movement
    for i in range(0, BOARDSIZE):  # going from column 1 to the board size (4)
        for j in range(0, BOARDSIZE - 1):
            while gBoard[i][j] == 0 and sum(gBoard[i][j:]) > 0:
                for k in range(j, BOARDSIZE - 1) :
                    gBoard[i][k] = gBoard[i][k + 1]
                gBoard[i][BOARDSIZE - 1] = 0

# merge function. takes one tile, and sees if the one next to it is the same value !=0
# then it adds to the tile in the direction of movement and sets the other one to 0
def mergeTiles() :
    global POINTS

    for i in range(0, BOARDSIZE) :
        for k in range(0, BOARDSIZE - 1):
            if gBoard[i][k] == gBoard[i][k + 1] and gBoard[i][k] != 0 :
                gBoard[i][k] = gBoard[i][k] * 2
                gBoard[i][k + 1] = 0
                POINTS += gBoard[i][k]
                moveTiles()

# checks to see if tiles can move to merge
def checkIfCanGo() :
    for i in range(0, BOARDSIZE ** 2):
        if gBoard[floor(i / BOARDSIZE)][i % BOARDSIZE] == 0:
            return True

    for i in range(0, BOARDSIZE) :
        for j in range(0, BOARDSIZE - 1):
            if gBoard[i][j] == gBoard[i][j + 1] :
                return True
            elif gBoard[j][i] == gBoard[j + 1][i] :
                return True
    return False

# reset function. pretty simple calls
# hotkey is 'r'
def reset() :
    global POINTS
    global gBoard

    POINTS = 0
    DISPLAYSURF.fill(BLACK)

    gBoard = [[0 for i in range(0, BOARDSIZE)] for j in range(0, BOARDSIZE)]

    main()

# just checks if any tile can move. returns false to end game
def canMove() :
    for i in range(0, BOARDSIZE) :
        for j in range(1, BOARDSIZE) :
            if gBoard[i][j - 1] == 0 and gBoard[i][j] > 0 :
                return True
            elif (gBoard[i][j - 1] == gBoard[i][j]) and gBoard[i][j - 1] != 0 :
                return True

    return False

# the brain child of the project. tried working in a savestate because i was playing skyrim and thought it was a neat idea
# The key to create a save state is 's', and to load is 'l'
# not much testing went into this, so it might be buggy
def saveGameState() :
    f = open("savedata", "w")

    line1 = " ".join([str(gBoard[floor(x / BOARDSIZE)][x % BOARDSIZE]) for x in range(0, BOARDSIZE ** 2)])

    f.write(line1 + "\n")
    f.write(str(BOARDSIZE) + "\n")
    f.write(str(POINTS))
    f.close()


def loadGameState() :
    global POINTS
    global BOARDSIZE
    global gBoard

    f = open("savedata", "r")

    mat = (f.readline()).split(' ', BOARDSIZE ** 2)
    BOARDSIZE = int(f.readline())
    POINTS = int(f.readline())

    for i in range(0, BOARDSIZE ** 2) :
        gBoard[floor(i / BOARDSIZE)][i % BOARDSIZE] = int(mat[i])

    f.close()

    main(True)

# the actual movement method. called after main checks the desired direction using the next two methods
def clockwiseBoard() :
    for i in range(0, int(BOARDSIZE / 2)) :
        for k in range(i, BOARDSIZE - i - 1) :
            temp1 = gBoard[i][k]
            temp2 = gBoard[BOARDSIZE - 1 - k][i]
            temp3 = gBoard[BOARDSIZE - 1 - i][BOARDSIZE - 1 - k]
            temp4 = gBoard[k][BOARDSIZE - 1 - i]

            gBoard[BOARDSIZE - 1 - k][i] = temp1
            gBoard[BOARDSIZE - 1 - i][BOARDSIZE - 1 - k] = temp2
            gBoard[k][BOARDSIZE - 1 - i] = temp3
            gBoard[i][k] = temp4

# outsourced method to call in main, used with the next method to get tile movement
def isArrow(k) :
    return (k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)

# works with isArrow to move tiles in the desired direction
def getRotations(k) :
    if k == pygame.K_UP :
        return 0
    elif k == pygame.K_DOWN :
        return 2
    elif k == pygame.K_LEFT :
        return 1
    elif k == pygame.K_RIGHT :
        return 3

# method a friend came up with
# not completely sure what it does to be honest but it works pretty well
def convertToLinearMatrix() :
    mat = []

    for i in range(0, BOARDSIZE ** 2) :
        mat.append(gBoard[floor(i / BOARDSIZE)][i % BOARDSIZE])

    mat.append(POINTS)

    return mat


def addToUndo() :
    undoBoard.append(convertToLinearMatrix())

# undo key is u, can undo all the way back to the beginning of the game using the undoBoard 2d array
def undo() :
    if len(undoBoard) > 0 :
        mat = undoBoard.pop()

        for i in range(0, BOARDSIZE ** 2) :
            gBoard[floor(i / BOARDSIZE)][i % BOARDSIZE] = mat[i]

        global POINTS
        POINTS = mat[BOARDSIZE ** 2]

        printBoard()


main()