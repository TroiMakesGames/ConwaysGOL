import pygame

import math
import random

#initialize pygame window
pygame.init()
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Conway's Game of Life - Graphs")

#fps display
clock = pygame.time.Clock()
def displayFPS(screen, font_size):
    font = pygame.font.SysFont(None, font_size)
    fps = round(clock.get_fps(), 1)
    fps_text = font.render(f"{fps}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

#CLASS DEFINITION -----------------------------------------------------------------------------------------------------------------------------------------

#FUNCTION DEFINITION - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def drawGraph(values, color, connectDots, left, bottom, width, height, highestvalue):
    points = []

    for i in range(len(values)):
        xOffset = ((i+1)/len(values)) * width
        yOffset = (values[i] / highestvalue) * height

        if connectDots == False:
            pygame.draw.circle(screen, color, (left + xOffset, bottom - yOffset), 2)
        else:
            points.append((left + xOffset, bottom - yOffset))

    #draw lines between points if connectDots
    if connectDots:
        for i in range(1, len(points)):
            pygame.draw.line(screen, color, points[i-1], points[i], 2)


#VARIABLE INITIALIZATION -----------------------------------------------------------------------------------------------------------------------------------------

#get initial ticks
prevT = pygame.time.get_ticks()

# RANDOM 400 writes ----------------------------------------------------------------------------------------------

"""
#read data
values_CGoL = []
with open(r"Source/Conways/Graphs/Data/Random_400/fps_log_CGoL.txt", "r") as f:
    values_CGoL = [float(line.strip()) for line in f]

values_ICGoL = []
with open(r"Source/Conways/Graphs/Data//Random_400/fps_log_ICGoL.txt", "r") as f:
    values_ICGoL = [float(line.strip()) for line in f]

values_LICGoL = []
with open(r"Source/Conways/Graphs/Data//Random_400/fps_log_LICGoL.txt", "r") as f:
    values_LICGoL = [float(line.strip()) for line in f]

#get highest framerate
all = values_CGoL + values_ICGoL + values_LICGoL

highestReachedFPS = max(all)
"""

# SET SEED 550 writes ----------------------------------------------------------------------------------------------

"""
#read data
values_CGoL = []
with open(r"Source/Conways/Graphs/Data/SetSeed_550/fps_log_CGoL_setseed.txt", "r") as f:
    values_CGoL = [float(line.strip()) for line in f]

values_ICGoL = []
with open(r"Source/Conways/Graphs/Data//SetSeed_550/fps_log_ICGoL_setseed.txt", "r") as f:
    values_ICGoL = [float(line.strip()) for line in f]

values_LICGoL = []
with open(r"Source/Conways/Graphs/Data//SetSeed_550/fps_log_LICGoL_setseed.txt", "r") as f:
    values_LICGoL = [float(line.strip()) for line in f]

#get highest framerate
all = values_CGoL + values_ICGoL + values_LICGoL

highestReachedFPS = max(all)
"""

# RELEVANT CELL COUNT 1500 writes ----------------------------------------------------------------------------------------------

#read data
values_CGoL = []
with open(r"Source/Conways/Graphs/Data/RelevantCellCount/RelevantCellCount_log_CGoL.txt", "r") as f:
    values_CGoL = [float(line.strip()) for line in f]

values_ICGoL = []
with open(r"Source/Conways/Graphs/Data//RelevantCellCount/RelevantCellCount_log_ICGoL.txt", "r") as f:
    values_ICGoL = [float(line.strip()) for line in f]

values_LICGoL = []
with open(r"Source/Conways/Graphs/Data//RelevantCellCount/RelevantCellCount_log_LICGoL.txt", "r") as f:
    values_LICGoL = [float(line.strip()) for line in f]

#get highest framerate
all = values_CGoL + values_ICGoL + values_LICGoL

highestReachedFPS = max(all)

#WHILE LOOP - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

hasSavedImage = False

running = True
while running:

    #update delta time
    currT = pygame.time.get_ticks()
    dTms = currT - prevT
    dTs = dTms / 1000.0

    #fill screen
    screen.fill((20, 20, 20))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.line(screen, (100, 100, 100), (50, 50), (50, 550), 1)
    pygame.draw.line(screen, (100, 100, 100), (50, 550), (750, 550), 1)

    connectDots = True
    
    drawGraph(values_CGoL, (0, 255, 0), connectDots, 50, 550, 700, 500, highestReachedFPS)
    drawGraph(values_ICGoL, (0, 0, 255), connectDots, 50, 550, 700, 500, highestReachedFPS)
    drawGraph(values_LICGoL, (255, 0, 0), connectDots, 50, 550, 700, 500, highestReachedFPS)

    # Update the display (buffer flip)
    #displayFPS(screen, 25)
    pygame.display.flip()
    clock.tick(60)

    if not hasSavedImage:
        pygame.image.save(screen, "Graph.png")

    #update delta time
    prevT = currT

# Quit Pygame
pygame.quit()
