from socket import getnameinfo
import pygame, sys
import pandas as pd
from pygame import mixer
import pygame
import math
from math import atan2, degrees, radians
import random
import time
from addons import button
from addons import functions as func
import DataBase as db

#######################################################################################


import pygame
import math
from math import atan2, degrees, radians
import random
import time

xsize = 900
ysize = 900

win = pygame.display.set_mode((xsize,ysize))

x = xsize/2
y = ysize/2
enemy_x = xsize/1.75
enemy_y = ysize/1.75
enemy_x_spd = 0
enemy_y_spd = 0
radius = ysize/60
angle = 180
rotspd = 120
xvel = 0
yvel = 0  
accel = 3
speedlimit = 15
enemyspd = 7
decell = 7
bltspd = 20
edgepenetration = 18
start = 1 
ast_speedlimit = 6
score = 0
l_size = ysize/18
m_size = ysize/30
s_size = ysize/60
lives = 3
ticker = 0
ticks = 0
secs = 0
global_pulse = 0
old_res = 480


s_ast = []
m_ast = []
l_ast = []

hist = []

level = 0

enemy_spawn = 0

bullets = []

def game():

    global run

    pygame.init()

    pygame.display.set_caption("Asteroids")

    
    fonte = pygame.freetype.Font("fonte.ttf", 100)
    livesf = pygame.freetype.Font("fonte.ttf", 50)

    global x,y,ticker,ticks,radius,angle,rotspd,xsize,ysize,lives,secs,global_pulse,score,start,enemy_spawn,keys,xvel,yvel,player_nickname,resolution,old_res,win



    run = True
    while run:

        if old_res != resolution:
            if resolution == 480:
                xsize = 854
                ysize = 480
            elif resolution == 720:
                xsize = 1280
                ysize = 720
            elif resolution == 1080:
                xsize = 1920
                ysize = 1080
            win = pygame.display.set_mode((xsize,ysize))
        
        old_res = resolution



        if (level >=1) and (secs == 10):
            enemy_spawn = 1
        if (level >=3) and (math.floor(secs/13)%2==0) and (math.floor(secs/13)*13 == secs) and (math.floor(secs/13) != 0):
            enemy_spawn = 1

        if ticks == 60:
            secs += 1
            ticks = 0
            global_pulse = 1
        else:
            ticks += 1
            global_pulse = 0

        pygame.time.delay(16)

        win.fill((0,0,0))
        fonte.render_to(win, (50, 50), str(score) , (255, 255, 255))
        livesf.render_to(win, (55, 100), str(lives) , (255, 255, 255))

        if ticker != 0:
            ticker -= 1

        if start == 1:
            if enemy_spawn == 1:
                pass
            x = xsize/2
            y = ysize/2
            xvel = 0
            yvel = 0
            func.spawn_asts(level)
            start = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
                

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and ticker < 120:
                    incx = ((math.sin(math.radians(angle)))*bltspd)
                    incy = ((math.cos(math.radians(angle)))*bltspd)
                    bullets.append([x, y, incx, incy, 0, 0])
                    shooterFx.play()

                if event.key == pygame.K_DOWN:
                    newpos = func.teleport()
                    ticker = 60
                    x = newpos[0]
                    y = newpos[1]

                if event.key == pygame.K_ESCAPE:
                    player_nickname = player_nickname[:-1]
                    playPause()

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            angle += rotspd/20
            
        if keys[pygame.K_RIGHT]:
            angle -= rotspd/20
        
        if keys[pygame.K_UP]:
            if ticker < 120:
                if abs(yvel) < speedlimit:
                    yvel += (math.cos(math.radians(angle)))*accel/20
                elif yvel > 0 and (math.cos(math.radians(angle)))*accel/20 < 0:
                    yvel += (math.cos(math.radians(angle)))*accel/20
                elif yvel < 0 and (math.cos(math.radians(angle)))*accel/20 > 0:
                    yvel += (math.cos(math.radians(angle)))*accel/20
                
                if abs(xvel) < speedlimit:
                    thrustFx.play()
                    xvel += (math.sin(math.radians(angle)))*accel/20
                elif xvel > 0 and (math.sin(math.radians(angle)))*accel/20 < 0:
                    xvel += (math.sin(math.radians(angle)))*accel/20
                elif xvel < 0 and (math.sin(math.radians(angle)))*accel/20 > 0:
                    xvel += (math.sin(math.radians(angle)))*accel/20

        else:
            yvel = yvel/(1+(decell/1000))
            xvel = xvel/(1+(decell/1000))
        
        if angle < 0:
            angle += 360
        elif angle >= 360:
            angle -= 360
            
        x = x + xvel
        y = y + yvel

        if x > xsize:
            x = x - xsize
        if y > ysize:
            y = y - ysize
        if x < 0:
            x = xsize - x
        if y < 0:
            y = ysize - y

        if not run:
            break

        if ticker < 120:
            rounded = math.floor(ticker/10)
            if rounded % 2 == 0:
                func.draw_ship()
        
        if ticker == 0:
            func.ship_collision(x, y)
            func.bullet_collision()
            
        if enemy_spawn == 1:
            func.enemy_logic()

        func.updatebullets()  
        func.updateasts()
        func.leveluptest()

        if lives <= 0:
            gameOver()
        
        pygame.display.update()
    pygame.quit()




#######################################################################################




#lendo arquivo csv
scoreArc = pd.read_csv("points/points.csv")
scoreArc = scoreArc.sort_values(by='Score',ascending=False).reset_index()
# print(scoreArc)

resolution = 480
pygame.init()
clock = pygame.time.Clock()
xsize = 854                        # LARGURA DA TELA 
ysize = 480                         # ALTURA DA TELA



screen = pygame.display.set_mode((xsize, ysize))

#title and icon
pygame.display.set_caption("Asteroids")
icon = pygame.image.load('images/letter-a.png')
pygame.display.set_icon(icon)

running = True
################## TEXTOOOO ####################
tam_font = 30
base_font = pygame.font.Font(None, tam_font)
hyper_font = pygame.font.Font("fonts/HyperspaceBold-GM0g.ttf", tam_font)
font = pygame.font.SysFont("arialblack", 20)
Text_Color = ('white')

background_music = mixer.music.load('songs/Master_of_Puppets.wav')
mixer.music.play(-1)


volume = 1 
shooterFx = mixer.Sound("songs/fire.wav")
thrustFx = mixer.Sound("songs/thrust.wav")
breakFx = mixer.Sound("songs/breaking.wav")

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img,(x,y))
################################################
player_nickname = ''                # NICKNAME DO PLAYER
score = 0

def mainPage(run):
    
    ####################   QUIT BUTTON  #######################
    global player_nickname 
    global xsize
    global ysize
    quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
    #botao 
    quit_button = button.Button(0,0, quit_img,0.5)
    ###########################################################
    tam_background = 0.5
    background_img = pygame.image.load("images/backgroung.jpg").convert_alpha()
    back_button = button.Button(0,0,background_img,tam_background)



    ###### medidas retangulo texto #####
    xrect = 200         #tamanho de x (Largura)
    yrect = 28          #tamanho de y (altura)
    xrect_pos = (xsize/2)-(xrect/2)   # posição x
    yrect_pos = (100)-(yrect/2)   # posição y 
    input_rect = pygame.Rect(xrect_pos,yrect_pos,xrect,yrect)        # Medidas retangulo texto player_nickname
    active_box = False
    colorBox = pygame.Color('white')

    ##### Retangulo best's score's #####
    def points_rect():
        x = 300
        y = 250
        xBestRecord_pos = xsize/2 - x/2
        yBestRecord_pos = ysize/2 - y/4
        draw_text("Best Records",base_font,Text_Color,xsize/2-65,yBestRecord_pos-20)     #a frase tem 130 de tamanho 
        BestRecord_rect = pygame.Rect(xBestRecord_pos,yBestRecord_pos,x,y)
        color = pygame.Color('white')
        pygame.draw.rect(screen,color,BestRecord_rect,3)
        def divisions(xPos,yPos,multiply,xTam,yTam):
            x1 = xTam
            y1 = yTam/5
            xPos = xPos
            yPos = yPos+(y1*multiply)
            divisionRecord = pygame.Rect(xPos,yPos,x1,y1)
            primeiro = scoreArc['Nickname'][multiply]
            Score = scoreArc['Score'][multiply]
            draw_text(f'{primeiro}', base_font, color, xPos+x1*0.05, yPos+y1*0.33)
            draw_text(f"{Score}", base_font, color, xPos+x1*0.75, yPos+y1*0.33)
            pygame.draw.rect(screen,color,divisionRecord,1)
        divisions(xBestRecord_pos,yBestRecord_pos,0,x,y)
        divisions(xBestRecord_pos,yBestRecord_pos,1,x,y)
        divisions(xBestRecord_pos,yBestRecord_pos,2,x,y)
        divisions(xBestRecord_pos,yBestRecord_pos,3,x,y)
        divisions(xBestRecord_pos,yBestRecord_pos,4,x,y)
        
    ###############################################################
    while run:
        if resolution == 480:
            xsize = 854
            ysize = 480
        elif resolution == 720:
            xsize = 1280
            ysize = 720
        elif resolution == 1080:
            xsize = 1920
            ysize = 1080
        xrect = 200         #tamanho de x (Largura)
        yrect = 28          #tamanho de y (altura)
        xrect_pos = (xsize/2)-(xrect/2)   # posição x
        yrect_pos = (100)-(yrect/2)   # posição y 
        input_rect = pygame.Rect(xrect_pos,yrect_pos,xrect,yrect)        # Medidas retangulo texto player_nickname
        colorBox = pygame.Color('white')
        screen = pygame.display.set_mode((xsize, ysize))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active_box = True
            
            if active_box == True:
                if len(player_nickname) < 17:
                    if event.type == pygame.KEYDOWN:                #Configuração de texto Nickname 
                        if event.key == pygame.K_BACKSPACE:
                            player_nickname = player_nickname[:-1]
                        else:
                            player_nickname += event.unicode
                if event.type == pygame.KEYDOWN:                #Configuração de texto Nickname 
                    if event.key == pygame.K_BACKSPACE:
                        player_nickname = player_nickname[:-1]

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game()

            if event.type == pygame.KEYDOWN:                #Configuração esc 
                if event.key == pygame.K_ESCAPE:
                    player_nickname = player_nickname[:-1]
                    playPause()
                # if event.key == pygame.K_RETURN:
                #     player_nickname = player_nickname[:-1]
                #     playPause()
        # screen.fill('black')

        # if back_button.draw(screen):
        #     pass

        if quit_button.draw(screen):            #Botão quit na tela 
            run = False
            pygame.time.delay(50)

        if active_box:
            colorBox = ((100, 100, 255))
        else:
            colorBox = ('white')

        pygame.draw.rect(screen,colorBox,input_rect,3)                 # Caixa de texto onde o player insere o nome

        draw_text("Nickname:",base_font,Text_Color,xrect_pos+47,yrect_pos-25)
        text_nick = base_font.render(player_nickname,True,'white')
        screen.blit(text_nick,((xrect_pos+5),(yrect_pos + (tam_font/2) - (yrect/4))))                # Texto onde o player insere o nickname 

        points_rect()
      
        clock.tick(60)

        pygame.display.update()
        






def playPause():
    global run, player_nickname, addLinha, scoreArc
    run = True
    global resolution, player_nickname
    game_paused = False
    menu_state = "main"         #"main","option","sound","video","key"


    screen = pygame.display.set_mode((xsize, ysize))

    #title and icon
    pygame.display.set_caption("Asteroids")
    icon = pygame.image.load('images/letter-a.png')
    pygame.display.set_icon(icon)


    #####################################################   Botões   #####################################################
    ####################  RESUME  #######################   142 x 38
    keys_tam = 0.5
    resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
    #botao 
    resume_button = button.Button((xsize/2) - 65, ysize/2-100, resume_img,keys_tam)
    #####################################################
    ####################   QUIT   #######################       285 x 75

    quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
    #botao 
    quit_button = button.Button((xsize/2) - 65, ysize/2, quit_img,keys_tam)
    #####################################################
    ####################  OPTION  #######################       285 x 75

    options_img = pygame.image.load("images/button_options.png").convert_alpha()
    #botao 
    options_button = button.Button((xsize/2) - 65,ysize/2-50, options_img,keys_tam)
    ##################################################### SEGUNDA TELA ##################################################### 
    ####################   BACK   #######################       285 x 75

    back_img = pygame.image.load("images/button_back.png").convert_alpha()
    #botao 
    back_button = button.Button((xsize/2) - 65,ysize/2+50, back_img,keys_tam)
    #####################################################
    ####################   AUDIO   #######################       285 x 75

    audio_img = pygame.image.load("images/button_audio.png").convert_alpha()
    #botao 
    audio_button = button.Button((xsize/2) - 65,ysize/2-100, audio_img,keys_tam)
    #####################################################
    ####################   VIDEO   #######################       285 x 75

    video_img = pygame.image.load("images/button_video.png").convert_alpha()
    #botao 
    video_button = button.Button((xsize/2) - 65,ysize/2-50, video_img,keys_tam)
    #####################################################
    ####################   KEYS   #######################       285 x 75
    keys_img = pygame.image.load("images/button_keys.png").convert_alpha()
    #botao 
    keys_button = button.Button((xsize/2) - 65,ysize/2, keys_img,keys_tam)

    xKeys_pos = xsize/4
    yKeys_pos = ysize/3
    

    key_top = pygame.image.load("images/top.png").convert_alpha()
    top_button = button.Button(xKeys_pos,yKeys_pos-85*2*keys_tam,key_top,keys_tam)
    key_left = pygame.image.load("images/left.png").convert_alpha()
    left_button = button.Button(xKeys_pos-50*keys_tam, yKeys_pos-85*keys_tam,key_left,keys_tam)
    key_right = pygame.image.load("images/right.png").convert_alpha()
    right_button = button.Button(xKeys_pos+50*keys_tam, yKeys_pos-85*keys_tam,key_right,keys_tam)
    key_down = pygame.image.load("images/down.png").convert_alpha()
    down_button = button.Button(xKeys_pos, yKeys_pos,key_down,keys_tam)

    key_space = pygame.image.load("images/space.png").convert_alpha()
    space_button = button.Button(xKeys_pos, yKeys_pos+191*keys_tam,key_space,keys_tam)
    key_teleport = pygame.image.load("images/space.png").convert_alpha()

    #####################################################################################################

    tam_playerName = (len(player_nickname)/2)* 20
    volume = 100

    paused = True

    while paused :
        # Cor da tela
        screen.fill("black")
        game_paused = True
        if game_paused == True:
            if menu_state == "main":
                global running
                draw_text(f"{player_nickname}", font, Text_Color, (xsize/2)-tam_playerName, 25)
                if resume_button.draw(screen):
                    paused = False
                    pygame.time.delay(100)
                if quit_button.draw(screen):
                    running = False
                    run = False
                    pygame.quit()
                    pygame.time.delay(100)
                    print("quit")
                if options_button.draw(screen):
                    menu_state = "options"
                    pygame.time.delay(250)
            elif menu_state == "options":
                back_button = button.Button((xsize/2) - 65,ysize/2+50, back_img,keys_tam)
                if back_button.draw(screen):
                    menu_state = "main"
                    pygame.time.delay(100)
                elif audio_button.draw(screen):
                    menu_state = "audio"
                    pygame.time.delay(100)
                elif video_button.draw(screen):
                    menu_state = "video"
                    pygame.time.delay(100)
                elif keys_button.draw(screen):
                    menu_state = "keys"
                    pygame.time.delay(100)
            elif menu_state == "keys":
                top_button.draw(screen)
                left_button.draw(screen)
                right_button.draw(screen)
                down_button.draw(screen)
                space_button.draw(screen) 
                draw_text("Move",base_font,'white',(xKeys_pos*2)+(100*keys_tam),yKeys_pos-85+(95*keys_tam)*0.25)
                draw_text("Direction",base_font,'white',(xKeys_pos*2)+(100*keys_tam),yKeys_pos-42+(95*keys_tam)*0.25)
                draw_text("Teleport",base_font,'white',(xKeys_pos*2)+(100*keys_tam),yKeys_pos+(95*keys_tam)*0.25)
                draw_text("Shoot",base_font,'white',(xKeys_pos*2)+(100*keys_tam),yKeys_pos+(191*keys_tam)+(95*keys_tam)*0.25)
                # draw_text("Teleport",base_font,'white',(xKeys_pos*2)+(100*keys_tam),yKeys_pos+(191*2*keys_tam)+(95*keys_tam)*0.25)
                back_button = button.Button(xsize - 65*2,ysize-50*2, back_img,keys_tam)
                if back_button.draw(screen):
                    menu_state = "options"
                    pygame.time.delay(100)    
                if event.type == pygame.KEYDOWN:                #Configuração esc 
                    if event.key == pygame.K_ESCAPE:
                        menu_state = "options"
            elif menu_state == "video":
                #################### Video Settings ######################
                qhd = pygame.image.load('images/480.png').convert_alpha()
                qhd_button = button.Button((xsize/2) - 65*3,ysize/3,qhd,keys_tam)
                hd = pygame.image.load('images/720.png').convert_alpha()
                hd_button = button.Button((xsize/2) - 65,ysize/3,hd,keys_tam)
                fullhd = pygame.image.load('images/1080.png').convert_alpha()
                fullhd_button = button.Button((xsize/2) + 65,ysize/3,fullhd,keys_tam)

                if back_button.draw(screen):
                    menu_state = "options"
                    back_button = button.Button((xsize/2) - 65,ysize/2+50, back_img,keys_tam)
                    pygame.time.delay(100)
                if qhd_button.draw(screen):
                    resolution = 480
                if hd_button.draw(screen):
                    resolution = 720
                if fullhd_button.draw(screen):
                    resolution = 1080
                if event.type == pygame.KEYDOWN:                #Configuração esc 
                    if event.key == pygame.K_ESCAPE:
                        menu_state = "options"
            elif menu_state == "audio":
                draw_text(f"Music", font, Text_Color, xsize/5 + 10, ysize/8)
                mute = pygame.image.load("images/mute.png")
                mute_button = button.Button((xsize/3) - 65,ysize/3,mute,keys_tam)
                unmute = pygame.image.load("images/unmute.png")
                unmute_button = button.Button((xsize/3) - 65,ysize/4,unmute,keys_tam)
                volMax = pygame.image.load("images/vol_max.png")
                volMax_button = button.Button((xsize/4) - 65*1.5,ysize/4,volMax,keys_tam)
                volMin = pygame.image.load("images/vol_min.png")
                volMin_button = button.Button((xsize/4) - 65*1.5,ysize/3,volMin,keys_tam)
                

                draw_text(f"FX", font, Text_Color, (xsize/8)*5 + 50, ysize/8)
                FXmute = pygame.image.load("images/mute.png")
                FXmute_button = button.Button((xsize/6)*4 - 65,ysize/3,FXmute,keys_tam)
                FXunmute = pygame.image.load("images/unmute.png")
                FXunmute_button = button.Button((xsize/6)*4 - 65,ysize/4,FXunmute,keys_tam)
                FXvolMax = pygame.image.load("images/vol_max.png")
                FXvolMax_button = button.Button((xsize/6)*5 - 65*1.5,ysize/4,FXvolMax,keys_tam)
                FXvolMin = pygame.image.load("images/vol_min.png")
                FXvolMin_button = button.Button((xsize/6)*5 - 65*1.5,ysize/3,FXvolMin,keys_tam)
                
                volume = mixer.Sound.get_volume(shooterFx)   #visualiza o volume atual da musica
                if volMin_button.draw(screen):
                    mixer.music.set_volume(volume - 0.01)
                if volMax_button.draw(screen):
                    mixer.music.set_volume(volume + 0.01)
                if mute_button.draw(screen):
                    mixer.music.set_volume(0)
                if unmute_button.draw(screen):
                    mixer.music.set_volume(0.5)
                

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_CAPSLOCK:
                        shooterFx.play()
                        # print('tiro')

                #sound effects
                volFx = shooterFx.get_volume()
                if FXvolMin_button.draw(screen):
                    shooterFx.set_volume(volFx - 0.01)
                if FXvolMax_button.draw(screen):
                    shooterFx.set_volume(volFx + 0.01)
                if FXmute_button.draw(screen):
                    shooterFx.set_volume(0)
                if FXunmute_button.draw(screen):
                    shooterFx.set_volume(1)
                
                if back_button.draw(screen):
                    menu_state = "options"
                    back_button = button.Button((xsize/2) - 65,ysize/2+50, back_img,keys_tam)
                    pygame.time.delay(100)
                if event.type == pygame.KEYDOWN:                #Configuração esc 
                    if event.key == pygame.K_ESCAPE:
                        menu_state = "options"
                
            


        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
                    print("Pause")
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()

def gameOver():
    global run, player_nickname,scoreArc,addLinha
    screen = pygame.display.set_mode((xsize, ysize))

    #title and icon
    pygame.display.set_caption("Asteroids")
    icon = pygame.image.load('images/letter-a.png')
    pygame.display.set_icon(icon)

    GO_tam = 1
    xISize = 422    # Largura da imagem
    yISize = 182    # Altura da imagem
    GO_img = pygame.image.load("images/game_over.png").convert_alpha()
    GO_button = button.Button((xsize/2) - xISize/2, (ysize/2) - yISize/2 -50, GO_img,GO_tam)
    quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
    quit_button = button.Button((xsize/2) - 65, ysize/2 + (ysize/5), quit_img,0.5)
    
    #inserindo pontuação no banco de dados
    if(db.FindData(player_nickname)):
        db.UpdateData(player_nickname,score,1)
    else:    
        db.InsertData(player_nickname,1,score)

    addLinha = pd.DataFrame({'Nickname':player_nickname,'Score':score},index=[len(scoreArc['Nickname'])+1])
    scoreArc = pd.concat([addLinha,scoreArc])
    scoreArc.to_csv('points/points.csv',columns = ['Nickname','Score'],index=False)

    run = True
    while run:
        # screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if GO_button.draw(screen):
                pass
            elif quit_button.draw(screen):
                run = False
                break
            #implementar                    #####################################################################################
        pygame.display.update()



mainPage(running)

# salva score no CSV
# print("amo ")
# addLinha = pd.DataFrame({'Nickname':player_nickname,'Score':score},index=[len(scoreArc['Nickname'])+1])
# scoreArc = pd.concat([addLinha,scoreArc])
# scoreArc.to_csv('points/points.csv',columns = ['Nickname','Score'],index=False)

