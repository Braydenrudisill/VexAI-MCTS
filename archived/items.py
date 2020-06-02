# 1 - Import library
import pygame
import os
import sys

# 2= - Import Ai libaries
import gym
import random
import numpy as np

pspeed = 90
ALPHA = (0,0,0)


class Player(pygame.sprite.Sprite):
    '''
    Spawn a player
    '''
    def __init__(self,team):
        pygame.sprite.Sprite.__init__(self)
        self.team = team
        self.x = 0;
        self.y = 0;
        self.frame = 0;

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
        self.rect.x = self.x * pspeed
        self.rect.y = self.y * pspeed

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
            x = round((self.x+0.5)*pspeed)
            y = round((self.y+0.5)*pspeed+25-i*25)
            if (b == 'x'): color = (0,50,0)
            if (b == 'o'): color = (0,50,100)

            if (b!='-'): pygame.draw.circle(world, color,(x,y) , 10, 0)

towers = [Tower(0,0), Tower(0,3), Tower(0,6),
          Tower(3,0), Tower(3,3), Tower(3,6),
          Tower(6,0), Tower(6,3), Tower(6,6)]
