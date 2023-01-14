import pygame
from sys import exit
import math

pygame.init()

#Make Screen
screen = pygame.display.set_mode((800,500))
img = pygame.image.load('fun\Pygame Breakout\Graphics\Images\MinecraftBreakout_Icon.png').convert()
pygame.display.set_icon(img)
pygame.display.set_caption("Minecraft Breakout")
clock = pygame.time.Clock()

#Font
minecraft_font = pygame.font.Font('fun\Pygame Breakout\Graphics\Font\Minecraft_Bold.otf', 24)

#Player
player_xpos, player_dx = 400, 0
player_surface = pygame.image.load('fun\Pygame Breakout\Graphics\Images\Red_Bed.png').convert_alpha()

#Ball/Dragon and Aim
ball_xpos, ball_ypos, ball_dx, ball_dy = 400, 460, 0, 0
ball_surface = pygame.image.load('fun\Pygame Breakout\Graphics\Images\Dragon.png').convert_alpha()
aim_surface = pygame.image.load('fun\Pygame Breakout\Graphics\Images\Aim.png').convert_alpha()
aim_x, aim_y = 400, 400

#Background
background2_xpos, background_base_xpos, background2_dx, background_base_dx = 400, 400, 0, 0
background2_surface = pygame.image.load('fun\Pygame Breakout\Graphics\Images\Background_2.png').convert_alpha()
background_base = pygame.image.load('fun\Pygame Breakout\Graphics\Images\Background_Base.png').convert_alpha()

#Time
time, text1_xpos, text1_ypos = 0, 0, 0
text2_xpos, text2_ypos = 0, 0
text_surface1 = minecraft_font.render('', False, 'White')
text_surface2 = minecraft_font.render('', False, 'White')

gamestate = 0 #[0 = menu, 1 = game, 2 = end, 3 = pausemenu]

#Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    keys_down = pygame.key.get_pressed()
    if gamestate == 0:
        if keys_down[pygame.K_LEFT]:
            aim_x += -1
        if keys_down[pygame.K_RIGHT]:
            aim_x += 1
        text1_xpos, text1_ypos = 400, 40
        text2_xpos, text2_ypos = 400, 80
        text1_surface = minecraft_font.render('Press Space to start', False, 'White')
        text2_surface = minecraft_font.render('Arrow Keys to aim', False, 'White')
        if aim_x > 450: aim_x = 450
        if aim_x < 350: aim_x = 350
        aim_y = 460 - math.sqrt(3600 - math.pow((aim_x-400), 2))

        #Aiming Ball
        if keys_down[pygame.K_SPACE]:
            if aim_x > player_xpos: 
                ball_dx = 2.5*(math.cos(math.atan((460 - aim_y)/(400 - aim_x))))
                ball_dy = 2*(math.sin(math.atan((460 - aim_y)/(400 - aim_x))))
            if aim_x < player_xpos: 
                ball_dx = -2.5*(math.cos(math.atan((460 - aim_y)/(400 - aim_x))))
                ball_dy = -2*(math.sin(math.atan((460 - aim_y)/(400 - aim_x))))
            if aim_x == player_xpos: ball_dy = -2.25
            gamestate = 1
    
    if gamestate == 1:
            #Check for inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_dx = -2.5
                background2_dx = -0.5
                background_base_dx = -0.25
            if event.key == pygame.K_RIGHT:
                player_dx = 2.5
                background2_dx = 0.5
                background_base_dx = 0.25
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_dx = 0
                background2_dx = 0
                background_base_dx = 0
            if event.key == pygame.K_RIGHT:
                player_dx = 0
                background2_dx = 0
                background_base_dx = 0
        
        #Update velocities
        player_xpos += player_dx
        background2_xpos += background2_dx
        background_base_xpos += background_base_dx
        ball_ypos += ball_dy
        ball_xpos += ball_dx
        
        #Time
        time += 0.005
        time_surface = minecraft_font.render('Time(s): '+ str(round(time, 2)), False, 'White')

        #Detecting borders
        if player_xpos < 64: player_xpos = 64
        if player_xpos > 736: player_xpos = 736
        if background_base_xpos < 358: background_base_xpos = 358
        if background_base_xpos > 442: background_base_xpos = 442
        if background2_xpos < 316: background2_xpos = 316
        if background2_xpos > 494: background2_xpos = 494
        if ball_xpos > 788: ball_dx *= -1
        if ball_xpos < 12: ball_dx *= -1
        if ball_ypos < 20: ball_dy *= -1

        #Collision of Ball with Bed
        if ball_ypos > 460 and ball_ypos < 480:
            if ball_xpos < player_xpos+76 and ball_xpos > player_xpos-76: 
                aim_x = ball_xpos
                if aim_x > player_xpos + 50: aim_x = player_xpos + 50
                if aim_x < player_xpos - 50: aim_x = player_xpos - 50
                aim_y = 460 - math.sqrt(3600 - math.pow((aim_x-player_xpos), 2))
                if aim_x > player_xpos: 
                    ball_dx = 2.5*(math.cos(math.atan((460 - aim_y)/(player_xpos - aim_x))))
                    ball_dy = 2*(math.sin(math.atan((460 - aim_y)/(player_xpos - aim_x))))
                if aim_x < player_xpos: 
                    ball_dx = -2.5*(math.cos(math.atan((460 - aim_y)/(player_xpos - aim_x))))
                    ball_dy = -2*(math.sin(math.atan((460 - aim_y)/(player_xpos - aim_x))))
                if aim_x == player_xpos: ball_dy = -2.25
        
        #Detecting End/Pause
        if ball_ypos > 500: gamestate = 2
        if keys_down[pygame.K_ESCAPE]: gamestate = 3

    #end
    if gamestate == 2:
        minutes = int(time)/60
        seconds = time - (int(minutes)*60)
        text1_surface = minecraft_font.render('The End', False, 'White')
        text1_ypos = 250
        text2_surface = minecraft_font.render('Press R to play again', False, 'White')
        text2_ypos = 290
        if seconds>=10:
            time_surface = minecraft_font.render('Final Time '+ str(int(minutes)) +':'+ str(round(seconds, 2)), False, 'White')
        else:
            time_surface = minecraft_font.render('Final Time '+ str(int(minutes)) +':0'+ str(round(seconds, 2)), False, 'White')

        #Reset
        if keys_down[pygame.K_r]: 
            gamestate = 0
            ball_xpos, ball_ypos, ball_dx, ball_dy = 400, 460, 0, 0
            player_xpos, player_dx = 400, 0
            background2_xpos, background_base_xpos, background2_dx, background_base_dx = 400, 400, 0, 0
            time, text1_xpos, text1_ypos = 0, 0, 0
            text2_xpos, text2_ypos = 0, 0
            aim_x, aim_y = 400, 400
    
    if gamestate == 3:
        text1_surface = minecraft_font.render('Game Paused', False, 'White')
        text2_surface = minecraft_font.render('Press Space to resume', False, 'White')
        if keys_down[pygame.K_SPACE]: gamestate = 1

    #Get rectangles
    player_rect = player_surface.get_rect(midbottom = (player_xpos, 500))
    ball_rect = ball_surface.get_rect(midbottom = (ball_xpos, ball_ypos))
    background2_rect = background2_surface.get_rect(midbottom = (background2_xpos, 516))
    background_base_rect = background_base.get_rect(midbottom = (background_base_xpos, 500))
    text1_rect = text1_surface.get_rect(midbottom = (text1_xpos, text1_ypos))
    text2_rect = text2_surface.get_rect(midbottom = (text2_xpos, text2_ypos))
    aim_rect = aim_surface.get_rect(center = (aim_x, aim_y))
    
    #Blitting to screen
    screen.blit(background_base, background_base_rect)     #Background Base
    screen.blit(background2_surface, background2_rect)     #Background layer 1
    screen.blit(player_surface, player_rect)
    if gamestate!=1: 
        screen.blit(text1_surface, text1_rect)
        screen.blit(text2_surface, text2_rect)
    else: screen.blit(time_surface, (10, 5))
    if gamestate == 2: screen.blit(time_surface, (10, 5))  #Time(s)
    if gamestate == 0: screen.blit(aim_surface, aim_rect)  #Aim Box
    screen.blit(ball_surface, ball_rect)                   #Dragon
    
    pygame.display.update()
    clock.tick(200)