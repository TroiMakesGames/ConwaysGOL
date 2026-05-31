import pygame
import sys
import os
import math
import numpy as np
import random

#set seed
random.seed(42)

import time     #fps display

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

#track time for fps display
last_time = time.time()
highestFps = 0

#write graphing data
fps_file = open("fps_log_CGoL.txt", "w")
accum_time = 0
frame_count = 0
write_count = 0

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

    #display fps in the window caption
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    fps = 1 / dt if dt > 0 else 0

    if fps > highestFps:
        highestFps = fps

    pygame.display.set_caption(f"Conway's Game of Life | FPS: {fps:.0f} | highestFPS: {highestFps:.0f}")
    
    #(stuff for graphing data collection)
    frame_count += 1
    accum_time += dt

    """
    if accum_time >= 0.1 and write_count < 550:     #write every 10ms (10/s) for 400 writes (40 seconds)
        fps = frame_count / accum_time

        fps_file.write(f"{fps}\n")
        fps_file.flush()  # ensures it writes immediately

        frame_count = 0
        accum_time = 0
        write_count += 1
    """
    
    #write active cell count each frame
    if frame_count < 1500:
        fps_file.write(f"{wolrdWidth*worldHeight}\n")
        fps_file.flush()  # ensures it writes immediately

    # Update the display
    pygame.display.flip()

fps_file.close()

# Quit Pygame
pygame.quit()
