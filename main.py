import pygame
import random
from pygame import mixer

#initialize pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))

# background
background = pygame.image.load('background.jpg')

#background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Nova_Corps")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#score
score_val=0

font = pygame.font.Font('anime_ace_bb/animeace2bb_tt/animeace2_bld.ttf',12)
textX=10
textY=10


def show_score(x,y):
    score = font.render("Score : "+str(score_val),True,(255,255,255))
    screen.blit(score,(x,y))


# Game Over

Game_over =  pygame.font.Font('anime_ace_bb/animeace2bb_tt/animeace2_bld.ttf',32)

def game_over_text():
    game_over = Game_over.render("GAME OVER",True,(255,255,255))
    screen.blit(game_over,(275,250))
    show_score(350,300)

# player
playerImage= pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0


def player(x,y):
    screen.blit(playerImage,(x,y))


# enemy
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyImage = []
num_of_enemies=5

for i in range(num_of_enemies):
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(30)
    enemyImage.append(pygame.image.load('enemy.png'))



def enemy(x,y,i):
    screen.blit(enemyImage[i],(x,y))  


# bullet
bulletImage= pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1 

bullet_state='ready'  #ready - bullet is invisible   fire - bullet is fired


def fire_bullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bulletImage,(x+16,y+10)) 


#collision

def isCollision(enemyX,enemyY,bulletX,bulletY):
    dist = ((bulletX-enemyX)**2+(bulletY-enemyY)**2)**0.5
    
    if dist<27:
        return True 
    else:
        return False


# Game loop
running=True
while running:
    #RGB
    screen.fill((0,0,0))
    #background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        
        #keystroke control   
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-0.3
            if event.key==pygame.K_RIGHT:
                playerX_change=0.3
            if event.key==pygame.K_SPACE:
                bullet_sound=mixer.Sound('laser.wav')
                bullet_sound.play()

                if bullet_state=='ready':
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)    
        
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0            
    

    #player movement
    playerX+=playerX_change
    
    #player boundary check
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736 
    

    for i in range(num_of_enemies):

        if enemyY[i]>440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            mixer.music.pause()
            break    
            
        #enemy movement
        enemyX[i]+=enemyX_change[i]
        
        #enemy boundary check
        if enemyX[i]<=0:
            enemyX_change[i]=0.3
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-0.3     
            enemyY[i]+=enemyY_change[i]
        
        #collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound=mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_state='ready'
            bulletY=480
            score_val+=1
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i],enemyY[i],i)    

    #bullet movement
    if bulletY<=0:
        bulletY=480
        bullet_state='ready'

    if bullet_state=='fire':
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change


    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()