import pygame
from pygame.locals import *
import sys      
import os


pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32) #Screen resolution
running = True
score = 0
font1 = pygame.font.SysFont("Arial", 30)
font2 = pygame.font.SysFont("Arial", 20)
click = False
pygame.mixer.init()


def loadimg(filename): #used for different img when moving left, right, or fallen(game over)
    path = os.path.dirname(os.path.realpath(__file__))
    iconpath = path+f'/{filename}.png'
    skin = pygame.image.load(str(iconpath))
    skin = pygame.transform.scale(skin, (100, 100))
    return skin
def loadimg2(filename): #used for different img when moving left, right, or fallen(game over)
    path = os.path.dirname(os.path.realpath(__file__))
    iconpath = path+f'/{filename}.png'
    skin = pygame.image.load(str(iconpath))
    skin = pygame.transform.scale(skin, (25, 25))
    return skin

def loadsound(filename): #used for different img when moving left, right, or fallen(game over)
    path = os.path.dirname(os.path.realpath(__file__))
    soundpath = path+f'/sound/{filename}.ogg'
    sound = pygame.mixer.Sound(soundpath)
    return sound

def drawtext(text, font, color, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    screen.blit(textobj, textrect)
    #print('Run')

def transisi():
    for i in range (1,510):
        a = 255-(i-2+1)
        if a < 0 :
            a = 0
        screen.fill((a,a,a))
        pygame.display.update()
    gameover_opening()

def gameover_opening():
    gameoverimg = loadimg('properties/game over/GameOver')
    #gameoverimg = gameoverimg.transform.scale(gameoverimg, (300,300))
    a = 100
    b, c = a, a
    light = False
    while running:
        mx, my = pygame.mouse.get_pos() #Mouse pointer coordinates (x, y)
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                gameover()
        screen.blit(gameoverimg, (250, 100))
        
        #Blinking text 
        
        if a == 255:
            light = True
        elif a == 100:
            light = False
        if light == True:
            a -= 1
            if a < 100:
                a = 100
        else :
            a += 1
            if a > 255:
                a = 255
        #End of Blinking text

        b, c = a, a #Green and Blue color value initiation
        drawtext('CLICK ANYWHERE TO CONTINUE', font2, (a,b,c), 243, 350)
        
        
        pygame.display.update()

def gameover():
    #pygame.mixer.music.load(sound('jump'))
    jumps = loadsound('jump')
    kcbs = loadsound('click_005')
    cs = loadsound('click_003')
    cld = False
    arr = [0,1,2]
    while running:
        mx, my = pygame.mouse.get_pos() #Mouse pointer coordinates (x, y)
        screen.fill((0,0,0))
        #Score box
        pygame.draw.line(screen, (222,222,222), (291, 251), (539, 251)) #Horizontal line (Below)
        pygame.draw.line(screen, (222,222,222), (291, 195), (539, 195)) #Horizontal line (Above)
        pygame.draw.line(screen, (222,222,222), (291, 251), (291, 195)) #Vertical line (Left side)
        pygame.draw.line(screen, (222,222,222), (539, 251), (539, 195)) #Vertical line (Right side)
        drawtext('Score = 9999999', font1, (255,255,255), 300, 208) #Text score
        #End Sbox 

        #Question box
        drawtext('Retry ?', font1, (255,255,255), 364, 258)
        drawtext('Yes', font2, (255,255,255), 322, 318)
        drawtext('No', font2, (255,255,255), 472, 318)
        #End Qbox

        #Making a button for collide point (Rectangle)
        # rumus => pygame.Rect (x, y, width, height)
        button_1 = pygame.Rect(322, 318, 40, 20)
        button_2 = pygame.Rect(472, 318, 30, 20)
        #End of button

        #Collide detection
        if button_1.collidepoint((mx, my)):
            drawtext('Yes', font2, (155,155,155), 322, 318) #High light button if mouse colliding with text (rect in text)
            if cld == False:
                cld = True 
                pygame.mixer.Channel(1).play(kcbs)
            if click:
                print('Button 1 pressed')
                #pygame.mixer.music.play()
                pygame.mixer.Channel(0).play(cs)
        if button_2.collidepoint((mx, my)):
            drawtext('No', font2, (155,155,155), 472, 318)
            if cld == False :
                cld = True
                pygame.mixer.Channel(1).play(kcbs)
            if click:
                print('Button 2 pressed')
                pygame.mixer.Channel(0).play(cs)
        if button_1.collidepoint((mx, my)) == False and button_2.collidepoint((mx, my)) == False:
            cld = False
        #End of collide detection

        #Delete "#" to see the rectangle
        #pygame.draw.rect(screen, (255, 0, 0), button_1)
        #pygame.draw.rect(screen, (255, 0, 0), button_2)

        click = False
        #print (mx, " -- ", my) #Printing coordinates x and y
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                click = True
        pygame.display.update()
def test():
    jumper=loadimg('kiri')
    pijakan=loadimg('/properties/pijakan/pijakan asli')
    coin = loadimg2('/properties/point/point game/coin')
    while running:
        mx, my = pygame.mouse.get_pos() #Mouse pointer coordinates (x, y)
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(236, 208, 30,70)) # (+36, +08, 30, 70) #Badan Jumper
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(541, 211, 13,18)) # (+36, +08, 30, 70) #Badan Jumper
        screen.blit(jumper, (200, 200))
        screen.blit(pijakan, (500, 200))
        screen.blit(coin, (535, 207))
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(505, 239, 88,15)) # (+10, +39, 84, 10) #pijakan
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(243,292, 8,3)) # (+43, +92, 6, 3) #tapak jumper
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                print(mx,my)
        pygame.display.update()
test()