

#Idea I got from the parsing work we've done in class, and after talking to a friend of mine about how to streamline the main file a bit


BLACK = (0, 0, 0)
RED = (244, 67, 54)
PINK = (234, 30, 90)
PURPLE = (156, 39, 176)
DPURPLE = (103, 58, 183)
BLUE = (33, 150, 243)
TEAL = (0, 150, 136)
GREEN = (60, 175, 80)
LGREEN = (139, 195, 74)
ORANGE = (255, 152, 0)
DORANGE = (255, 87, 34)
BROWN = (121, 85, 72)

bookOfColors = {0:BLACK, 2:RED, 4:PINK, 8:PURPLE, 16:DPURPLE, 32:BLUE, 64:TEAL, 128:LGREEN, 256:GREEN, 512:ORANGE, 1024:DORANGE, 2048:BROWN}

def colorWheel(c) :
    return bookOfColors[c]