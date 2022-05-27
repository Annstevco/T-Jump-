import pygame
from pygame.locals import *
import sys
import random
import os 
from abc import ABC, abstractmethod

pygame.font.init()
font1 = pygame.font.SysFont("Arial", 30)
font2 = pygame.font.SysFont("Arial", 20)
running = True
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont("Arial", 25) #global (outside)
pygame.mixer.init()
chg = True
phase = 1
musicvol = 10
sfc = 3

def loadsound(filename): #used for different img when moving left, right, or fallen(game over)
    path = os.path.dirname(os.path.realpath(__file__))
    soundpath = path+f'/sound/{filename}.ogg'
    sound = pygame.mixer.Sound(soundpath)
    return sound
#Sound list
jumps = loadsound('jump')
gos = loadsound('GameOver')
bgs = loadsound('Bg')
kcbs = loadsound('mouserelease1')
cs = loadsound('click_003')
coinhit = loadsound('coinhit')
#End Sound list
#Sound channel volume settings
pygame.mixer.Channel(0).set_volume(1)
pygame.mixer.Channel(1).set_volume(0.3)
pygame.mixer.Channel(2).set_volume(0.3)
#End of sound volume settings

def loadimg(filename, scalex, scaley): #used for load image file 
    path = os.path.dirname(os.path.realpath(__file__))
    iconpath = path+f'/{filename}.png'
    skin = pygame.image.load(str(iconpath))
    skin = pygame.transform.scale(skin, (scalex, scaley))
    return skin

def drawtext(text, font, color, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    screen.blit(textobj, textrect)

def transisi():
    for i in range (1,510):
        a = 255-(i-2+1)
        if a < 0 :
            a = 0
        screen.fill((a,a,a))
        pygame.display.update()

def bgtransisi(x): # ===> used for transition in background change
    global chg 
    screen.blit(x[0], (0,x[1]-Jumper.cameray))
    
    if x[1] >= Jumper.playery+378:
        chg = False

def drawbg(change, bg1, bg2):
    if change == True:
        bgtransisi(bg1)
        bgtransisi(bg2)
    if change == False:
        bg2[1] = Jumper.playery-200
        screen.blit(bg2[0], (0,0))
    
def settings():
    #transisi()
    leftbtn = loadimg('/properties/tombol/kiri', 25, 25)
    rightbtn = loadimg('/properties/tombol/kanan', 25,25)
    cld = False
    cld2 = False
    change = False
    while True:
        global musicvol, sfc
        screen.fill((0,0,0))
        if pygame.mixer.Channel(0).get_busy() == False: #background music
            pygame.mixer.Channel(0).play(bgs)
        mx, my = pygame.mouse.get_pos() #Mouse pointer coordinates (x, y)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                click  = True
        #Music Volume rectangle
        lbtn1 = pygame.Rect(400,200, 20,20)
        rbtn1 = pygame.Rect(500,200, 20,20)
        #Sounf Effect rectangle
        lbtn2 = pygame.Rect(400,250, 20,20)
        rbtn2 = pygame.Rect(500,250, 20,20)
        #back and default rectangle
        bbtn = pygame.Rect(100,370, 55,20)
        dbtn = pygame.Rect(580,370, 92,20)

        #pygame.draw.rect(screen, (255, 0, 0), bbtn)
        #pygame.draw.rect(screen, (255, 0, 0), dbtn)
        drawtext('BACK', font2, (255,255,255), 100, 370)
        drawtext('DEFAULT', font2, (255,255,255), 580, 370)
        drawtext('Music Volume: ', font1, (255,255,255), 100,200)
        drawtext('Sound Effect  :', font1, (255,255,255), 100,250)
        screen.blit(leftbtn, (400,200))
        screen.blit(rightbtn, (500,200))
        screen.blit(leftbtn, (400,250))
        screen.blit(rightbtn, (500,250))
        mv = str(musicvol/10)
        sf = str(sfc/10)
        drawtext(mv, font2, (255,255,255), 450, 205)
        drawtext(sf, font2, (255,255,255), 450, 255)
        
        if rbtn1.collidepoint((mx,my)) == False and rbtn2.collidepoint((mx,my)) == False and lbtn1.collidepoint((mx,my)) == False and lbtn2.collidepoint((mx,my)) == False and bbtn.collidepoint((mx,my)) == False and dbtn.collidepoint((mx,my)) == False:
            cld = False
            cld2 = False
            change = False
        else :
            cld = True
        if lbtn1.collidepoint((mx,my)):
            if click:
                change = True
                if (musicvol-1) < 0:
                    musicvol = 0
                else:
                    musicvol -= 1
                pygame.mixer.Channel(3).play(cs)
            pygame.mixer.Channel(0).set_volume(musicvol/10)
        if rbtn1.collidepoint((mx,my)):
            if click:
                change = True
                if (musicvol + 1) > 10:
                    musicvol = 10
                else:
                    musicvol += 1
                pygame.mixer.Channel(3).play(cs)
            pygame.mixer.Channel(0).set_volume(musicvol/10)
        if lbtn2.collidepoint((mx,my)):
            if click:
                change = True
                if (sfc-1) < 0:
                    sfc = 0
                else:
                    sfc -= 1
                pygame.mixer.Channel(3).play(cs)
            if change == True and cld == True:
                pygame.mixer.Channel(1).set_volume(sfc/10)
                pygame.mixer.Channel(2).set_volume(sfc/10)
                pygame.mixer.Channel(1).play(jumps)
        if rbtn2.collidepoint((mx,my)):
            if click:
                change = True
                if (sfc+1) > 10:
                    sfc = 10
                else:
                    sfc += 1
                pygame.mixer.Channel(3).play(cs)
            if change == True and cld == True:
                pygame.mixer.Channel(1).set_volume(sfc/10)
                pygame.mixer.Channel(2).set_volume(sfc/10)
                pygame.mixer.Channel(1).play(jumps)
        if bbtn.collidepoint((mx,my)):
            drawtext('BACK', font2, (155,155,155), 100, 370)
            if cld2 == False:
                cld2 = True
                pygame.mixer.Channel(4).play(kcbs)
            if click:
                menu()
        if dbtn.collidepoint((mx,my)):
            drawtext('DEFAULT', font2, (155,155,155), 580, 370)
            if cld2 == False:
                cld2 = True
                pygame.mixer.Channel(4).play(kcbs)
            if click:
                musicvol = 10
                sfc = 3
        

        pygame.display.update()
    
def gameover_opening():
    gameoverimg = loadimg('properties/game over/GameOver', 300, 300)
    a = 100
    b, c = a, a
    light = False
    while running:
        mx, my = pygame.mouse.get_pos() #Mouse pointer coordinates (x, y)
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pygame.mixer.Channel(1).play(cs)
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
    click = False
    cld = False
    while running:
        global Jumper, chg, bgimg, bgimg2, bgimg3, scrncolor
        mx, my = pygame.mouse.get_pos() #Mouse pointer coordinates (x, y)
        screen.fill((0,0,0))
        
        pygame.draw.line(screen, (222,222,222), (291, 251), (539, 251)) #Horizontal line (Below)
        pygame.draw.line(screen, (222,222,222), (291, 195), (539, 195)) #Horizontal line (Above)
        pygame.draw.line(screen, (222,222,222), (291, 251), (291, 195)) #Vertical line (Left side)
        pygame.draw.line(screen, (222,222,222), (539, 251), (539, 195)) #Vertical line (Right side)
        drawtext(f'Score = {Jumper.score}', font1, (255,255,255), 300, 208) #Text score

        drawtext('Retry ?', font1, (255,255,255), 364, 258)
        drawtext('Yes', font2, (255,255,255), 322, 318)
        drawtext('No', font2, (255,255,255), 472, 318)

        button_1 = pygame.Rect(322, 318, 40, 20)
        button_2 = pygame.Rect(472, 318, 30, 20)

        if button_1.collidepoint((mx, my)):
            drawtext('Yes', font2, (155,155,155), 322, 318) #High light button if mouse colliding with text (rect in text)
            if cld == False:
                pygame.mixer.Channel(1).play(kcbs)
                cld = True
            if click:
                pygame.mixer.Channel(2).play(cs)
                restart()
        if button_2.collidepoint((mx, my)):
            drawtext('No', font2, (155,155,155), 472, 318)
            if cld == False:
                pygame.mixer.Channel(1).play(kcbs)
                cld = True
            if click:
                pygame.mixer.Channel(2).play(cs)
                restartvar()
                menu()
        if button_1.collidepoint((mx,my)) == False and button_2.collidepoint((mx,my)) == False:
            cld = False

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                click = True
        pygame.display.update()

def menu():
    bg = loadimg('/properties/bg/StartMenu', 800,600)
    playbtnn = loadimg('/properties/tombol/play', 200,200)
    settingbtn = loadimg('/properties/tombol/tombol_setting', 80,80)
    quitbtn = loadimg('/properties/tombol/tombol_exit', 80, 80)
    click = False
    cld = False 
    while True:
        screen.fill((255,255,255))
        mx, my = pygame.mouse.get_pos() #Mouse pointer coordinates (x, y)
        if pygame.mixer.Channel(0).get_busy() == False:
            pygame.mixer.Channel(0).play(bgs)
        screen.blit(bg, (0,0)) #Background
        screen.blit(playbtnn, (300,250)) #Play button
        screen.blit(settingbtn, (690, 500))
        screen.blit(quitbtn, (40,500))
        quitbtnn = pygame.Rect(40,500, 80,80)
        playbtn = pygame.Rect(310,260, 180, 180)
        setbtn = pygame.Rect(690,500, 80,80)
        if playbtn.collidepoint((mx,my)):
            if click == True :
                pygame.mixer.Channel(2).play(cs)
                run()
        if setbtn.collidepoint((mx,my)):
            if click:
                pygame.mixer.Channel(2).play(cs)
                settings()
        if quitbtnn.collidepoint((mx,my)):
            if click:
                pygame.mixer.Channel(2).play(cs)
                pygame.quit()
                sys.exit()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                click = True
        
        
        pygame.display.update()

def restartvar():
    global chg, x, bgimg, bgimg2, bgimg3, scrncolor, Jumper
    chg = True
    Pijakan.platforms = [[400, 500, 0, 10]] #pijakan awal
    coin.coins = []
    Jumper = Player()
    x = Jumper.playery-1000
    bgimg = [loadimg('/properties/bg/bg1', 800, 600), 0]
    bgimg2 = [loadimg('/properties/bg/bg1-1', 800, 600), x, False]
    bgimg3 = []
    scrncolor = 'Notblck'

def restart():
    restartvar()
    run()
"""
"""
def drawcoins():
    for q in coin.coins:
        check = coin.coins[0][1] - Jumper.cameray
        if check > 600:
            coin.coins.pop(0)
        screen.blit(coin.image, (q[0], q[1]-Jumper.cameray))


def drawPlatforms():
        for p in Pijakan.platforms:
            check = Pijakan.platforms[1][1] - Jumper.cameray
            if check > 600:
                platform = random.randint(0, 1000)
                if platform < 800:
                    platform = 0
                elif platform < 900:
                    platform = 1
                else:
                    platform = 2
                x = random.randint(0, 700)
                y = Pijakan.platforms[-1][1] - 50
                Pijakan.platforms.append([x, y, platform, 0])
                c = random.randint(0,100)
                if x  < 50 and platform == 0:
                    coin.coins.append([x+35, y+7])
                coords = Pijakan.platforms[-1]
                check = random.randint(0, 1000)
                Pijakan.platforms.pop(0)
                Jumper.score += 10
            if p[2] == 0:
                screen.blit(PijakanAsli.asli, (p[0], p[1] - Jumper.cameray))
            elif p[2] == 1:
                screen.blit(PijakanSekali.sekali, (p[0], p[1] - Jumper.cameray))
            elif p[2] == 2:
                if not p[3]:
                    screen.blit(PijakanJebakan.Jebakan, (p[0], p[1] - Jumper.cameray))

def updatePlayer():
        if not Jumper.jump:
            Jumper.playery += Jumper.gravity
            Jumper.gravity += 0.4
        elif Jumper.jump:
            Jumper.playery -= Jumper.jump
            Jumper.jump -= 1
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if Jumper.direction == 1:
                Jumper.player = pygame.transform.flip(Jumper.player, True,False) #Mirror the skin    
            if Jumper.xmovement < 3:
                Jumper.xmovement += 1
            Jumper.direction = 0 # 0 -> Right
        elif key[K_LEFT]:
            if Jumper.direction == 0:
                Jumper.player = pygame.transform.flip(Jumper.player, True,False) #Mirror the skin
            if Jumper.xmovement > -3:
                Jumper.xmovement -= 1
            Jumper.direction = 1 # 1 -> Left
        
        # To make player stay still when no button pressed
        else:
            if Jumper.xmovement > 0:
                Jumper.xmovement -= 1
            elif Jumper.xmovement < 0:
                Jumper.xmovement += 1

        #WRAPPING PLAYER 
        if Jumper.playerx > 760:
            Jumper.playerx = -50
        elif Jumper.playerx < -50:
            Jumper.playerx = 760
        Jumper.playerx += Jumper.xmovement
        if Jumper.playery - Jumper.cameray <= 200:
            Jumper.cameray -= 10

        screen.blit(Jumper.player, (Jumper.playerx, Jumper.playery - Jumper.cameray))  

def generatePlatforms():
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
        if random.randint(0,50) > 48 :
            coin.coins.append([x+35, on+7])
        Pijakan.platforms.append([x, on, platform, 0])
        on -= 50

class Player:
    def __init__(self):
        self.player = loadimg("kiri", 100, 100) #player
        self.direction = 1 #player
        self.playerx = 400 #player
        self.playery = 400 #player
        self.cameray = 0
        self.jump = 0
        self.gravity = 0
        self.xmovement = 0
        self.hp = 1 #Not implemented yet
        self.score = 0 #player
        self.coinhit = 0
    def MoveRight(self):
        if self.direction == 1:
            self.player = pygame.transform.flip(self.player, True,False) #Mirror the skin    
        if self.xmovement < 15:
            self.xmovement += 7
        self.direction = 0 # 0 -> Right
        self.checkboundaries()
    def MoveLeft(self):
        if self.direction == 0:
            self.player = pygame.transform.flip(self.player, True,False) #Mirror the skin
        if self.xmovement > -15:
            self.xmovement -= 7
        self.direction = 1 # 1 -> Left
        self.checkboundaries()
    def TakeDamage(self):
        self.hp -= PijakanJebakan.GiveDamage()
    def Jump(self):
        if not self.jump:
            self.playery += self.gravity
            self.gravity += 0.6
        elif self.jump:
            self.playery -= self.jump
            self.jump -= 1
    def checkboundaries(self):
        if self.playerx > 760:
            self.playerx = -50
        elif self.playerx < -50:
            self.playerx = 760
        self.playerx += self.xmovement
        if self.playery - self.cameray <= 200:
            self.cameray -= 10
        screen.blit(self.player, (self.playerx, self.playery - self.cameray))
    def checkcollision(self):
        self.Jump()
        a = 0
        for q in coin.coins:
            rect = pygame.Rect(q[0]+1, q[1]+1, 13, 18)
            player = pygame.Rect(self.playerx+36, self.playery+8, 30, 70)
            if rect.colliderect(player):
                self.score+=10
                self.coinhit+=1
                pygame.mixer.Channel(2).play(coinhit)
                coin.coins.pop(a)
            a+=1
        for p in Pijakan.platforms:
            rect = pygame.Rect(p[0]+5, p[1]+38, 88, 15)
            player = pygame.Rect(self.playerx+43, self.playery+92, 6, 3)
            if rect.colliderect(player) and self.gravity :
                if p[2] != 4:
                    self.jump = 20
                    self.gravity = 0
                    if p[2] != 2:
                        pygame.mixer.Channel(1).play(jumps)
                    self.Jump()
                    if p[2] == 2:
                        self.TakeDamage()

class coin:
    coins = []
    image = loadimg('/properties/point/point game/coin', 25, 25)

class Pijakan(ABC):
    platforms = [[400, 500, 0, 10]] #pijakan awal -> [x,y,?,?]
    def __init__(self, damage):
        self.Damage = damage
    @abstractmethod
    def Move():
        pass
    @abstractmethod
    def GiveDamage(self):
        pass
    @abstractmethod
    def Dissapear(self):
        pass 
class PijakanAsli(Pijakan):
    asli = loadimg("/properties/pijakan/pijakan asli", 100, 100) #pijakan
    def __init__(self, damage=0):
        super().__init__(damage)
    def Move(self):
        pass
    def GiveDamage(self):
        Jumper.hp-=self.Damage
    def Dissapear(self):
        pass 
class PijakanSekali(Pijakan):
    sekali = loadimg("/properties/pijakan/pijakan transparan", 100, 100) #pijakan
    def __init__(self, damage=0):
        super().__init__(damage)
    def Move():
         for p in Pijakan.platforms:
            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1
    def GiveDamage(self):
        pass
    def Dissapear(self):
        pass 
class PijakanJebakan(Pijakan):
    Jebakan = loadimg("/properties/pijakan/pijakan trap", 100, 100) #pijakan
    def __init__(self, damage=0):
        super().__init__(damage)
    def Move():
        pass
    def GiveDamage(self):
        return self.Damage
    def Dissapear(self):
        pass 

Jumper = Player()
PijakanJebakan = PijakanJebakan()
x = Jumper.playery-1000
scrncolor = 'Notblck'
bgimg = [loadimg('/properties/bg/bg1', 800, 600), 0]
bgimg2 = [loadimg('/properties/bg/bg1-1', 800, 600), x, False]
bgimg3 = []
ldimg = True
def bgtransition():
    #bg transition
    x = Jumper.playery-810
    global chg, bgimg3, scrncolor, bgimg, bgimg2
    
    if Jumper.score >=4490:
        if chg == False and bgimg[2] == True:
            chg = True
            bgimg[2] = False
        drawbg(chg, bgimg, bgimg2)
    
    elif Jumper.score >=4350: #transisi
        if Jumper.score == 4480:
            if bgimg2 == []:
                bgimg2 = [loadimg('/properties/bg/bg4', 800,600), x, False]
            bgimg[2] = True 
        else :
            bgimg2=[]
        if chg == False and bgimg3[2] == True:
            chg = True 
            bgimg3[2]= False 
        drawbg(chg, bgimg3,bgimg)

    elif Jumper.score >=3180:
        if Jumper.score == 4340:
            if bgimg == []:
                bgimg = [loadimg('/properties/bg/bg3-2', 800,600), x, False]
            bgimg3[2] = True 
        else :
            bgimg = []
        if chg == False and bgimg2[2] == True:
            chg = True
            bgimg2[2] = False
        drawbg(chg,bgimg2,bgimg3) 

    elif Jumper.score >= 3040: #transisi
        if Jumper.score == 3170:
            scrncolor = 'black'
            if bgimg3 == []:
                bgimg3 = [loadimg('/properties/bg/bg3-1', 800,600), x, False]
            bgimg2[2] = True
        else :
            bgimg3=[]
        if chg == False and bgimg[2] == True:
            chg = True
            bgimg[2] = False 
        drawbg(chg,bgimg,bgimg2) 

    elif Jumper.score >= 2050:
        if Jumper.score == 3030:
            if bgimg2 == []:
                bgimg2 = [loadimg('/properties/bg/bg2-2', 800, 600), x, False]
            bgimg[2] = True
        else :
            bgimg2 = []
        if chg == False and bgimg3[2] == True:
            chg = True
            bgimg3[2] = False
        drawbg(chg,bgimg3, bgimg)

    elif Jumper.score >= 1910: #Transisi
        if Jumper.score == 2040: #130 
            if bgimg == []:
                bgimg = [loadimg('/properties/bg/bg2-1', 800, 600), x, False]
            bgimg3[2] = True
        else :
            bgimg = []
        if chg == False and bgimg2[2] == True:
            chg = True
            bgimg2[2] = False 
        drawbg(chg,bgimg2,bgimg3)
    
    elif Jumper.score >= 0:
        drawbg(chg, bgimg, bgimg2)
        if Jumper.score==1900:
            bgimg2[2] = True 
            if bgimg3 == []:
                bgimg3 = [loadimg('/properties/bg/bg1-2', 800, 600), x, False]
    #end of bg transition
        
def run():
    clock = pygame.time.Clock()
    generatePlatforms()
    while True:
        global scrncolor
        if pygame.mixer.Channel(0).get_busy() == False:
            pygame.mixer.Channel(0).play(bgs)
        screen.fill((255,255,255))
        bgtransition()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Jumper.MoveLeft()
                elif event.key == pygame.K_RIGHT:
                    Jumper.MoveRight()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    Jumper.xmovement = 0
            
        if Jumper.playery - Jumper.cameray > 700 or Jumper.hp == 0:
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).play(gos)
            transisi()
            gameover_opening()
        drawcoins()
        drawPlatforms()

        Jumper.checkcollision()
        Jumper.checkboundaries()
        PijakanSekali.Move()
        if scrncolor == 'Notblck':
            screen.blit(font.render(str(Jumper.score), -1, (0, 0, 0)), (25, 25))
        else :
            screen.blit(font.render(str(Jumper.score), -1, (255, 255, 255)), (25, 25))
        pygame.display.flip()
        

menu()
