# 1 - Import library
import pygame
import os
import sys

# 2= - Import Ai libaries
import gym
import random
import numpy as np


LR = 1e-3
env = gym.make('CartPole-v0')
env.reset()


class Player(pygame.sprite.Sprite):
    '''
    Spawn a player
    '''
    def __init__(self,speed,team):
        pygame.sprite.Sprite.__init__(self)
        self.team = team
        self.x = 0;
        self.y = 0;
        self.frame = 0;
        self.speed = speed;

        self.images = []
        img = pygame.image.load(os.path.join('resources','images','rob4.png')).convert()
        img.convert_alpha()     # optimise alpha
        img.set_colorkey(ALPHA)
        self.images.append(img)
        self.image = self.images[0]
        self.rect  = self.image.get_rect()

    def touchingWall(self,x,y):
        if(self.x+x<0 or self.x+x>6): return True
        if(self.y+y<0 or self.y+y>6): return True

        for t in towers:
            if self.x+x == t.x and self.y+y ==t.y: return True

        return False

    def move(self,x,y):
        '''
        Control player movement
        '''
        if(not self.touchingWall(x,y)):
            self.x += x
            self.y += y
            #print(self.x,self.y)

    def update(self):
        '''
        Update Player Location
        '''
        self.rect.x = self.x * self.speed
        self.rect.y = self.y * self.speed

    def place_ball(self,c):
        for t in towers:
            a = abs(t.x-self.x)
            b = abs(t.y-self.y)
            if (a+b==1):
                t.place_ball(c)
                return

    def descore_ball(self):
        for t in towers:
            a = abs(t.x-self.x)
            b = abs(t.y-self.y)
            if (a+b==1):
                t.descore()
                return

class Tower():
    '''
    Spawn a Tower
    '''
    def __init__(self,x,y):
        self.x = x;
        self.y = y;
        self.balls = ['-','-','-']
    def place_ball(self,team):
        for i,b in enumerate(self.balls):
            if (b == '-'):
                self.balls[i] = team
                print((self.x,self.y),self.balls,team)
                return

    def descore(self):
        self.balls = [self.balls[1],self.balls[2],'-']
        print((self.x,self.y),self.balls)
    def show_balls(self):
        for i,b in enumerate(self.balls):
            x = round((self.x+0.5)*player.speed)
            y = round((self.y+0.5)*player.speed+25-i*25)
            if (b == 'x'): color = (0,50,0)
            if (b == 'o'): color = (0,50,100)

            if (b!='-'): pygame.draw.circle(world, color,(x,y) , 10, 0)


# Set Black to ALPHA

def set_variables():
    ALPHA = (0,0,0)

    # Set Screen Size
    worldx = 630
    worldy = 630

    # Set refresh rates for frams and animations
    fps = 40
    ani = 4
    clock = pygame.time.Clock()
    pygame.init()

    # Draw the world and backdrop
    world    = pygame.display.set_mode([worldx,worldy])
    backdrop = pygame.image.load(os.path.join('resources','images','backdrop.png')).convert()
    backdropbox = world.get_rect()
    player = Player(90,'x')   # spawn player with speed 90
    player.rect.x = 0   # go to x
    player.rect.y = 0   # go to y
    player_list = pygame.sprite.Group()
    player_list.add(player)
    # backdrop = pygame.image.load(os.path.join('images','stage.png').convert())
    # backdropbox = world.get_rect()

    towers = [Tower(0,0), Tower(0,3), Tower(0,6),
              Tower(3,0), Tower(3,3), Tower(3,6),
              Tower(6,0), Tower(6,3), Tower(6,6)]

def render():
    world.blit(backdrop, backdropbox)
    for t in towers:
        t.show_balls()
    player.update()
    player_list.draw(world) # draw player
    pygame.display.flip()
    clock.tick(fps)



set_variables();
main = True
while main == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
            main = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.move(-1,0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.move(1,0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.move(0,-1)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player.move(0,1)
            if event.key == ord(' '):
                player.place_ball('x')
            if pygame.key.name(event.key).upper()=="LEFT SHIFT":
                player.descore_ball()
            if pygame.key.name(event.key).upper()=="RIGHT SHIFT":
                player.place_ball('o')


        if event.type == pygame.KEYUP:
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                main = False

    render()

# put game loop here
