import pygame, sys
import button


pygame.init()

xsize = 500
ysize = 500

def playPause():
    game_paused = False
    menu_state = "main"         #"main","option","sound","video","key"


    screen = pygame.display.set_mode((ysize, xsize))

    #title and icon
    pygame.display.set_caption("Asteroids")
    icon = pygame.image.load('images/letter-a.png')
    pygame.display.set_icon(icon)
    player_name = "Nycollas"


    ################## Personagem 01 ####################
    def player():
        playerImg = pygame.image.load('images/letter-a.png')
        playerX = 0
        playerY = 0
        screen.blit(playerImg,(playerX,playerY))
    #####################################################



    ################## TEXTOOOO ####################
    font = pygame.font.SysFont("arialblack", 20)
    Text_Color = ('white')

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img,(x,y))
    #####################################################

    ############################################# Botões ##############################################
    ####################  RESUME  #######################

    resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
    #botao 
    resume_button = button.Button(185,100, resume_img,0.5)
    #####################################################
    ####################   QUIT   #######################

    quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
    #botao 
    quit_button = button.Button(185,150, quit_img,0.5)
    #####################################################
    ####################  OPTION  #######################

    options_img = pygame.image.load("images/button_options.png").convert_alpha()
    #botao 
    options_button = button.Button(185,200, options_img,0.5)
    #####################################################
    ####################   BACK   #######################

    back_img = pygame.image.load("images/button_back.png").convert_alpha()
    #botao 
    back_button = button.Button(185,300, back_img,0.5)
    #####################################################
    ####################   AUDIO   #######################

    audio_img = pygame.image.load("images/button_audio.png").convert_alpha()
    #botao 
    audio_button = button.Button(185,150, audio_img,0.5)
    #####################################################
    ####################   VIDEO   #######################

    video_img = pygame.image.load("images/button_video.png").convert_alpha()
    #botao 
    video_button = button.Button(185,200, video_img,0.5)
    #####################################################
    ####################   KEYS   #######################

    keys_img = pygame.image.load("images/button_keys.png").convert_alpha()
    #botao 
    keys_button = button.Button(185,250, keys_img,0.5)
    #####################################################
    #####################################################################################################


    run = True

    while run :
        # Cor da tela
        screen.fill("black")

        if game_paused == True:
            draw_text(f"{player_name}", font, Text_Color, 185, 10)
            if menu_state == "main":
                if resume_button.draw(screen):
                    game_paused = False
                    pygame.time.delay(100)
                if quit_button.draw(screen):
                    run = False
                    pygame.time.delay(100)
                    print("quit")
                if options_button.draw(screen):
                    menu_state = "options"
                    pygame.time.delay(100)
            if menu_state == "options":
                if back_button.draw(screen):
                    menu_state = "main"
                    pygame.time.delay(100)
                if audio_button.draw(screen):
                    menu_state = "main"
                    pygame.time.delay(100)
                if video_button.draw(screen):
                    menu_state = "main"
                    pygame.time.delay(100)
                if keys_button.draw(screen):
                    menu_state = "main"
                    pygame.time.delay(100)

        else:
            draw_text("press ESC to Pause", font, Text_Color, 145, 10)
            


        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
                    print("Pause")
            if event.type == pygame.QUIT:
                run = False
        
        
        # player()
        pygame.display.update()