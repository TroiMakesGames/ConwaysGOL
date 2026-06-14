import pygame
import math
import sys

import random

import pyRecorder

pygame.init()
screenWidth = 480
screenHeight = 480
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("SandSimulation")

worldWidth = 120
worldHeight = 120

#pyrecorder
pyrecorder = pyRecorder.Recorder()

#fps display
clock = pygame.time.Clock()
def displayFPS(screen, fontSize):
    font = pygame.font.SysFont(None, fontSize)
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def drawWorld(currArray, inputToggle):
    tileWidth = screenWidth/worldWidth
    tileHeight = screenHeight/worldHeight

    indexColors = [(30, 30, 30), (255, 255, 0), (100, 100, 255), (155, 155, 155), (70, 70, 70), (150, 128, 0), (150, 50, 0), (125, 125, 255), (random.randint(150, 255), random.randint(0, 50), 0)]

    for x in range(worldWidth):
        for y in range(worldHeight):
            if currArray[x][y] == 0:    #air
                pygame.draw.rect(screen, indexColors[0], pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight))
            if currArray[x][y] == 1:    #sand
                pygame.draw.rect(screen, indexColors[1], pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight))
            if currArray[x][y] == 2:    #water
                pygame.draw.rect(screen, indexColors[2], pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight))
            if currArray[x][y] == 3:    #smoke
                pygame.draw.rect(screen, indexColors[3], pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight))
            if currArray[x][y] == 4:    #stone
                pygame.draw.rect(screen, indexColors[4], pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight))
            if currArray[x][y] == 5:    #clay
                pygame.draw.rect(screen, indexColors[5], pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight))
            if currArray[x][y] == 6:    #wood
                pygame.draw.rect(screen, indexColors[6], pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight))
            if currArray[x][y] == 7:    #ice
                pygame.draw.rect(screen, indexColors[7], pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight))
            if currArray[x][y] == 8:    #fire
                pygame.draw.rect(screen, indexColors[8], pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight))

    #draw selected material
    margin = 5
    selectedCellRectSize = 20
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(screenWidth - (selectedCellRectSize + margin), 0, (selectedCellRectSize + margin), (selectedCellRectSize + margin)))
    pygame.draw.rect(screen, indexColors[inputToggle], pygame.Rect(screenWidth - selectedCellRectSize - margin/2, margin / 2, selectedCellRectSize, selectedCellRectSize))


def generateNewArray(currArray):
    newArray = [[0 for i in range(worldWidth)] for j in range(worldHeight)]

    #update stone
    for y in range(worldHeight):
        iter = range(0, worldWidth, 1)
        if y % 2 == 1:
            iter = range(worldWidth-1, -1, -1)
        for x in iter:
            if currArray[x][y] == 4:
                newArray[x][y] = 4

    #update clay
    for y in range(worldHeight):
        iter = range(0, worldWidth, 1)
        if y % 2 == 1:
            iter = range(worldWidth-1, -1, -1)
        for x in iter:
            if currArray[x][y] == 5:
                newArray[x][y] = 5

                #check if should become sand
                neighbourPositions = [
                    (-1, -1),
                    (0, -1),
                    (1, -1),
                    (1, 0),
                    (1, 1),
                    (0, 1),
                    (-1, 1),
                    (-1, 0)
                ]

                for pos in neighbourPositions:
                    if checkTile(currArray, x + pos[0], y + pos[1]) == 8:
                        if random.randint(0, 10) == 1:
                            newArray[x][y] = 1

    #update wood
    for y in range(worldHeight):
        iter = range(0, worldWidth, 1)
        if y % 2 == 1:
            iter = range(worldWidth-1, -1, -1)
        for x in iter:
            if currArray[x][y] == 6:
                newArray[x][y] = 6

                #check if should become fire
                neighbourPositions = [
                    (-1, -1),
                    (0, -1),
                    (1, -1),
                    (1, 0),
                    (1, 1),
                    (0, 1),
                    (-1, 1),
                    (-1, 0)
                ]

                for pos in neighbourPositions:
                    if checkTile(currArray, x + pos[0], y + pos[1]) == 8:
                        if random.randint(0, 10) == 1:
                            newArray[x][y] = 8

    #update ice
    for y in range(worldHeight):
        iter = range(0, worldWidth, 1)
        if y % 2 == 1:
            iter = range(worldWidth-1, -1, -1)
        for x in iter:
            if currArray[x][y] == 7:
                newArray[x][y] = 7
        
                if random.randint(0, 1000) == 1:
                    newArray[x][y] = 2

    #update fire
    for y in range(worldHeight):
        iter = range(0, worldWidth, 1)
        if y % 2 == 1:
            iter = range(worldWidth-1, -1, -1)
        for x in iter:
            if currArray[x][y] == 8:
                newArray[x][y] = 8
                
                #randomly move upwards
                if random.randint(0, 20) == 1:
                    swapableMaterials = [0]

                    priorityLevels = [
                        [(0, -1)],
                    ]
                    
                    validSpot = priorityCheck(currArray, newArray, x, y, priorityLevels, swapableMaterials)

                    newArray[validSpot[0]][validSpot[1]] = 8
                    newArray[x][y] = 0

                    if random.randint(0, 5) == 1:
                        newArray[validSpot[0]][validSpot[1]] = 3

    #update water
    for y in range(worldHeight):
        iter = range(0, worldWidth, 1)
        if y % 2 == 1:
            iter = range(worldWidth-1, -1, -1)
        for x in iter:
            if currArray[x][y] == 2:

                swapableMaterials = [0]

                priorityLevels = [
                    [(0, 1)],
                    [(-1, 1), (1, 1)],
                    [(-1, 0), (1, 0)]
                ]
                
                validSpot = priorityCheck(currArray, newArray, x, y, priorityLevels, swapableMaterials)

                newArray[validSpot[0]][validSpot[1]] = 2

    #update smoke
    for y in range(worldHeight):
        iter = range(0, worldWidth, 1)
        if y % 2 == 1:
            iter = range(worldWidth-1, -1, -1)
        for x in iter:
            if currArray[x][y] == 3:

                #randomly disappear
                if random.randint(0, 1000) == 1:
                    newArray[x][y] = 0
                else:

                    swapableMaterials = [0]

                    priorityLevels = [
                        [(0, -1)],
                        [(-1, -1), (1, -1)],
                        [(-1, 0), (1, 0)]
                    ]
                    
                    validSpot = priorityCheck(currArray, newArray, x, y, priorityLevels, swapableMaterials)

                    newArray[validSpot[0]][validSpot[1]] = 3

    #update sand
    for y in range(worldHeight):
        iter = range(0, worldWidth, 1)
        if y % 2 == 1:
            iter = range(worldWidth-1, -1, -1)
        for x in iter:
            if currArray[x][y] == 1:

                swapableMaterials = [0, 2, 3]

                priorityLevels = [
                    [(0, 1)],
                    [(-1, 1), (1, 1)]
                ]
                
                validSpot = priorityCheck(currArray, newArray, x, y, priorityLevels, swapableMaterials)

                #displace water
                if newArray[validSpot[0]][validSpot[1]] == 2:
                    newArray[x][y] = 2

                #displace mist
                if newArray[validSpot[0]][validSpot[1]] == 3:
                    newArray[x][y] = 3

                newArray[validSpot[0]][validSpot[1]] = 1

                #check if should become clay
                neighbourPositions = [
                    (-1, -1),
                    (0, -1),
                    (1, -1),
                    (1, 0),
                    (1, 1),
                    (0, 1),
                    (-1, 1),
                    (-1, 0)
                ]

                for pos in neighbourPositions:
                    if checkTile(currArray, validSpot[0] + pos[0], validSpot[1] + pos[1]) == 2:
                        newArray[validSpot[0]][validSpot[1]] = 5

    return newArray

def priorityCheck(currArray, newArray, x, y, priorityLevels, swapableMaterials):
    #go through prioirty list until found a valid spot
    for positions in priorityLevels:

        #get possible positions
        possible = []

        for position in positions:
            if checkPosition(currArray, newArray, x + position[0], y + position[1], swapableMaterials):
                possible.append((x + position[0], y + position[1]))
        
        #check if found a valid, otherwise continue
        if len(possible) > 0:
            return possible[random.randint(0, len(possible) - 1)]
    
    #otherwise if not found any valid spot in priority levels, return x,y
    return (x, y)

def checkPosition(currArray, newArray, x, y, swapableMaterials):
    #check if in bounds
    if x > worldWidth-1 or x < 0 or y > worldHeight-1 or y < 0:
        return False
    
    #check if empty
    if currArray[x][y] not in swapableMaterials or newArray[x][y] not in swapableMaterials:
        return False
    
    return True

def checkTile(currArray, x, y):
    if x < 0 or x > worldWidth - 1 or y < 0 or y > worldHeight - 1:
        return -1
    return currArray[x][y]

def spawnOnMouse():
    #spawn sand on mouse pos
    mousePos = pygame.mouse.get_pos()
    tileWidth = screenWidth/worldWidth
    tileHeight = screenHeight/worldHeight
    worldX = int(mousePos[0] // tileWidth)
    worldY = int(mousePos[1] // tileHeight)

    #alltiles that create a shape of mouse spawn
    spawnOffsets = [
        (0, 0),
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0)
    ]

    for spawnOffset in spawnOffsets:
        spawnInputToggleMaterial(worldX + spawnOffset[0], worldY + spawnOffset[1])

def spawnInputToggleMaterial(x, y):
    if x > 0 and x <worldWidth-1 and y > 0 and y < worldHeight-1:
        currArray[x][y] = inputToggle

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

currArray = [[0 for i in range(worldWidth)] for j in range(worldHeight)]

"""for y in range(worldWidth):
    for x in range(len(currArray[y])):
        if y > 40 and x < 119 and y < 60:
            if x%2 == 0:
                if y%2 == 0:
                    currArray[x+1][y] = 4
                else:
                    currArray[x][y] = 4"""

inputToggle = 1
maxInputToggle = 8

t = 0

running = True
while running:
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            #scrollwheel
            if event.button == 4:
                inputToggle -= 1
            elif event.button == 5:
                inputToggle += 1

            #right click
            if pygame.mouse.get_pressed(3)[2]:
                inputToggle += 1
                if inputToggle > maxInputToggle:
                    inputToggle = 0

            if inputToggle > maxInputToggle:
                inputToggle = maxInputToggle
            if inputToggle < 1:
                inputToggle = 1
                
    if pygame.mouse.get_pressed(3)[0]:
        spawnOnMouse()

    screen.fill((20, 20, 20))

    #draw current
    drawWorld(currArray, inputToggle)

    #generate new and apply
    currArray = generateNewArray(currArray)

    #DEBUG: count existing material
    if False:
        count = [0 for i in range(maxInputToggle + 1)]
        for x in range(worldWidth):
            for y in range(worldHeight):
                count[currArray[x][y]] += 1
        print(count)

    displayFPS(screen, 20)
    pygame.display.flip()

    t += 1
    pyrecorder.takeShot(screen, t)

    clock.tick(60)

pyrecorder.compileToVideo(20)

pygame.quit()