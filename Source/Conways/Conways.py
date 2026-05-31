import pygame
import sys
import os
import math
import numpy as np
import random

#------------------------------------------------------------------------------------------------------------------------------------
#world setup
wolrdWidth = 250
worldHeight = 150
drawnCellSize = 3
#------------------------------------------------------------------------------------------------------------------------------------

pygame.init()
screenWidth = wolrdWidth * drawnCellSize
screenHeight = worldHeight * drawnCellSize
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Conways Game of Life')

#remove window icon
transparent_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
transparent_surface.fill((0, 0, 0, 0))
pygame.display.set_icon(transparent_surface)

#------------------------------------------------------------------------------------------------------
def drawWorld():
    #draw squares where there is a 1 in the world array
    for x in range(len(world)):
        for y in range(len(world[x])):

            #draw square with correct scaling size
            if world[x][y] == 1:
                pygame.draw.rect(screen, (255, 255, 255), (x * drawnCellSize, y * drawnCellSize, drawnCellSize, drawnCellSize))

def updateWorld(world):
    #create next world array
    nextWorld = [[0 for _ in range(worldHeight)] for _ in range(wolrdWidth)]

    #go through each cell and check for rules
    for x in range(len(world)):
        for y in range(len(world[x])):

            #get neighbouring cell count
            neighbours = [(-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0)]
            nCount = 0

            for n in neighbours:
                nX = (x + n[0]) % wolrdWidth
                nY = (y + n[1]) % worldHeight
    
                if world[nX][nY] == 1:
                    nCount += 1

            #-------------------------------------------------------RULES
            #if alive
            if world[x][y] == 1:
                
                #if less than 2 cells alive, die
                if nCount < 2:
                    nextWorld[x][y] = 0

                #if 2 or 3 live on
                if nCount >= 2 and nCount <= 3:
                    nextWorld[x][y] = 1

                #when above 3, die
                if nCount > 3:
                    nextWorld[x][y] = 0

            #if dead
            else:

                #if exacly 3 live, live
                if nCount == 3:
                    nextWorld[x][y] = 1
            #-------------------------------------------------------RULES

    #update the world by overriding it with the next world
    world = nextWorld
    return world

#------------------------------------------------------------------------------------------------------

#initialize 2d arrrays
world = [[0 for _ in range(worldHeight)] for _ in range(wolrdWidth)]

#randomly gemnerate world
for i in range(wolrdWidth):
    for j in range(worldHeight):
        rChoice = random.choice([0, 1, 2, 3, 4, 5])
        if rChoice == 0:
            world[i][j] = 1

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill screen
    screen.fill((0, 0, 0))
    
    #update world
    world = updateWorld(world)

    #draw world
    drawWorld()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
