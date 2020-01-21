import sys, pygame, dungeon

scale = 10
scale2 = 8
origin = 50
origin2 = 200
size = width, height = 1200, 800
speed = [1, 1]
black = 0, 0, 0
white = 255,255,255
blue = 0,0,255
lightblue = 165, 245, 255
red = 255,0,0

def printminimap(f, pygame, screen):
    left = origin
    top = origin
    for c in f.pixelMap():
        square = pygame.Rect(left, top, scale*(15/10.0), scale*(9/10.0))
        if c == '*':
            pygame.draw.rect(screen,lightblue,square,0)
            left += scale*15/10.0
        if c == 'R':
            pygame.draw.rect(screen,white,square,0)
            left += scale*15/10.0
        if c == ' ':
            pygame.draw.rect(screen,red,square,0)
            left += scale*15/10.0
        if c == 'n':
            left = origin
            top += scale*9/10.0


def printfloormap(f, pygame, screen):
    left = origin
    top = origin2
    for c in f.pixelFloor():
        square = pygame.Rect(left, top, scale2, scale2)
        if c == 'D':
            pygame.draw.rect(screen,blue,square,0)
            left += scale2
        if c == 'X':
            pygame.draw.rect(screen,red,square,0)
            left += scale2
        if c == ' ':
            pygame.draw.rect(screen,white,square,0)
            left += scale2
        if c == 'n':
            left = origin
            top += scale2



def main():
 
    f = dungeon.Floor()
    pygame.init()
    
    screen = pygame.display.set_mode(size)
    printminimap(f, pygame, screen)
    printfloormap(f, pygame, screen)


    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    f = dungeon.Floor()
                    screen = pygame.display.set_mode(size)
                    printminimap(f, pygame, screen)
                    printfloormap(f, pygame, screen)



        pygame.display.flip()


main()