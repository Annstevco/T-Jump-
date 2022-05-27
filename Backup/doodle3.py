import pygame
from pygame.locals import *
import sys
import random
import os 

pygame.font.init()

def loadimg(filename): #used for load image file 
    path = os.path.dirname(os.path.realpath(__file__))
    iconpath = path+f'/{filename}.png'
    skin = pygame.image.load(str(iconpath))
    skin = pygame.transform.scale(skin, (100, 100))
    return skin

font1 = pygame.font.SysFont("Arial", 30)
font2 = pygame.font.SysFont("Arial", 20)
running = True

def drawtext(self, text, font, color, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    self.screen.blit(textobj, textrect)
    #print('Run')

def gameover():
    while running:
        DoodleJump.screen.fill((0,0,0))
        #Score box
        pygame.draw.line(DoodleJump.screen, (222,222,222), (291, 251), (539, 251)) #Horizontal line (Below)
        pygame.draw.line(DoodleJump.screen, (222,222,222), (291, 195), (539, 195)) #Horizontal line (Above)
        pygame.draw.line(DoodleJump.screen, (222,222,222), (291, 251), (291, 195)) #Vertical line (Left side)
        pygame.draw.line(DoodleJump.screen, (222,222,222), (539, 251), (539, 195)) #Vertical line (Right side)
        drawtext('Score = 9999999', font1, (255,255,255), 300, 208) #Text score
        #End Sbox 

        #Question box
        drawtext('Retry ?', font1, (255,255,255), 364, 258)
        drawtext('Yes', font2, (255,255,255), 322, 318)
        drawtext('No', font2, (255,255,255), 472, 318)
        #End Qbox


        mx, my = pygame.mouse.get_pos()
        print (mx, " -- ", my)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


class DoodleJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.player = loadimg("kiri") #player
        self.sekali = loadimg("sekali") #pijakan
        self.jebakan = loadimg("jebakan") #pijakan
        self.asli = loadimg("asli") #pijakan
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 25)
        self.direction = 1
        self.playerx = 400
        self.playery = 400
        self.platforms = [[400, 500, 10, 10]]
        self.cameray = 0
        self.jump = 0
        self.gravity = 0
        self.xmovement = 0

    def updatePlayer(self):
        if not self.jump:
            self.playery += self.gravity
            self.gravity += 0.4
        elif self.jump:
            self.playery -= self.jump
            self.jump -= 1
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.direction == 1:
                self.player = pygame.transform.flip(self.player, True,False) #Mirror the skin    
            if self.xmovement < 10:
                self.xmovement += 1
            self.direction = 0 # 0 -> Right
        elif key[K_LEFT]:
            if self.direction == 0:
                self.player = pygame.transform.flip(self.player, True,False) #Mirror the skin
            if self.xmovement > -10:
                self.xmovement -= 1
            self.direction = 1 # 1 -> Left
        else:
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
        #WRAPPING PLAYER 
        if self.playerx > 760:
            self.playerx = -50
        elif self.playerx < -50:
            self.playerx = 760
        self.playerx += self.xmovement
        if self.playery - self.cameray <= 200:
            self.cameray -= 10

        self.screen.blit(self.player, (self.playerx, self.playery - self.cameray))
    
    def updatePlatforms(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.asli.get_width() -5, self.asli.get_height())
            player = pygame.Rect(self.playerx, self.playery, self.player.get_width() -10, self.player.get_height())
            if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):
                if p[2] != 2:
                    self.jump = 15
                    self.gravity = 0
                else:
                    p[-1] = 1
            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1
    
    def drawPlatforms(self):
        for p in self.platforms:
            check = self.platforms[1][1] - self.cameray
            if check > 600:
                platform = random.randint(0, 1000)
                if platform < 800:
                    platform = 0
                elif platform < 900:
                    platform = 1
                else:
                    platform = 2

                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platform, 0])
                coords = self.platforms[-1]
                check = random.randint(0, 1000)
                self.platforms.pop(0)
                self.score += 100
            if p[2] == 0:
                self.screen.blit(self.asli, (p[0], p[1] - self.cameray))
            elif p[2] == 1:
                self.screen.blit(self.sekali, (p[0], p[1] - self.cameray))
            elif p[2] == 2:
                if not p[3]:
                    self.screen.blit(self.jebakan, (p[0], p[1] - self.cameray))
    
    def generatePlatforms(self):
        on = 600
        while on > -100:
            x = random.randint(0,700)
            platform = random.randint(0, 1000)
            if platform < 800:
                platform = 0
            elif platform < 900:
                platform = 1
            else:
                platform = 2
            self.platforms.append([x, on, platform, 0])
            on -= 50

    def drawGrid(self):
        for x in range(80):
            pygame.draw.line(self.screen, (222,222,222), (x * 12, 0), (x * 12, 600))
            pygame.draw.line(self.screen, (222,222,222), (0, x * 12), (800, x * 12))
    
    def run(self):
        clock = pygame.time.Clock()
        self.generatePlatforms()
        while True:
            self.screen.fill((255,255,255))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            if self.playery - self.cameray > 700:
                """"
                self.cameray = 0
                self.score = 0
                self.platforms = [[400, 500, 0, 0]]
                self.generatePlatforms()
                self.playerx = 400
                self.playery = 400
                """
                self.gameover()
            self.drawGrid()
            self.drawPlatforms()
            self.updatePlayer()
            self.updatePlatforms()
            self.screen.blit(self.font.render(str(self.score), -1, (0, 0, 0)), (25, 25))
            pygame.display.flip()

    def gameover(self):
        click = False
        while running:
            mx, my = pygame.mouse.get_pos()
            self.screen.fill((0,0,0))
            #Score box
            pygame.draw.line(self.screen, (222,222,222), (291, 251), (539, 251)) #Horizontal line (Below)
            pygame.draw.line(self.screen, (222,222,222), (291, 195), (539, 195)) #Horizontal line (Above)
            pygame.draw.line(self.screen, (222,222,222), (291, 251), (291, 195)) #Vertical line (Left side)
            pygame.draw.line(self.screen, (222,222,222), (539, 251), (539, 195)) #Vertical line (Right side)
            self.drawtext('Score = 9999999', font1, (255,255,255), 300, 208) #Text score
            #End Sbox 

            #Question box
            self.drawtext('Retry ?', font1, (255,255,255), 364, 258)
            self.drawtext('Yes', font2, (255,255,255), 322, 318)
            self.drawtext('No', font2, (255,255,255), 472, 318)
            #End Qbox

            #Making a button for collide point (Rectangle)
            #pygame.Rect (x,y, width, height)
            button_1 = pygame.Rect(322, 318, 40, 20)
            button_2 = pygame.Rect(472, 318, 30, 20)
            if button_1.collidepoint((mx, my)):
                self.drawtext('Yes', font2, (155,155,155), 322, 318) #High light button if mouse colliding with text (rect in text)
                if click:
                    print('Button 1 pressed')
                    DoodleJump().run()
            if button_2.collidepoint((mx, my)):
                self.drawtext('No', font2, (155,155,155), 472, 318)
                if click:
                    print('Button 2 pressed')
                    pygame.quit()
                    sys.exit()
            
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

    def drawtext(self, text, font, color, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x,y)
        self.screen.blit(textobj, textrect)

DoodleJump().run()