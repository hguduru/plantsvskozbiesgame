import pygame, random
from pygame.locals import *
 

def mousePressed(event, data):
    (pressedX, pressedY) = data.mousePos
    if data.phase == "menu":
        (pressedMenuRow, pressedMenuCol) = getMenuRowAndColFromCoords(data, 
                                            pressedX, pressedY)
        dealWithMenuSelection(data, pressedMenuRow, pressedMenuCol)

    elif (data.phase == "rules") or (data.phase == "instructions"):
        dealWithClickedMenuButton(data, pressedX, pressedY)

    elif data.phase == "game":
        dealWithClickedMenuButton(data, pressedX, pressedY)
        collectSuns(data, pressedX, pressedY)
        dealWithGardenSpade(data, pressedX, pressedY)
        (pressedGardenRow,pressedGardenCol) = getGardenRowAndColFromCoords(data, 
                                                pressedX, pressedY)
        (pressedPSRow, pressedPSCol) = getPSRowAndColFromCoords(data,
                                                pressedX, pressedY)
        # If user clicks in garden, and if player has selected a plant from the
        # plant selection, and if selected row and col is valid
        if ((pressedGardenRow != None) and (pressedGardenCol != None) and
            (data.plantSelection != "")):
            if (data.plantSelection != "spade"):
                createPlant(data, data.plantSelection, pressedGardenRow, 
                            pressedGardenCol)
            elif (data.plantSelection == "spade"):
                useSpadeIfSelected(data, pressedGardenRow, pressedGardenCol, 
                                    pressedX, pressedY)
        # Unselects selected plant if next click is not valid
        elif (data.plantSelection != "spade"):
            data.plantSelection = ""
            data.messageType = None
        # If plant is not selected and player clicks in select options, selects
        # respective plant
        selectPlant(data, pressedPSRow, pressedPSCol)



# Function that returns row, col if user mousePresses inside the garden
def getGardenRowAndColFromCoords(data, xcoord, ycoord):
    gardenRow = gardenCol = None
    for row in xrange(data.rows):
        if (data.margin + row * data.cellSize <= ycoord <= 
            data.margin + row * data.cellSize + data.cellSize):
            gardenRow = row
    for col in xrange(data.cols):
        if (data.margin + col * data.cellSize <= xcoord <= 
            data.margin + col * data.cellSize + data.cellSize):
            gardenCol = col
    return (gardenRow, gardenCol)


#Function that returns row (and col) if player presses a plant selection option
def getPSRowAndColFromCoords(data, xcoord, ycoord):
    PSRow = PSCol = None
    margin = data.margin
    cellSize = data.plantSelectionCellSize
    for row in xrange(data.plantSelectionRows):
        if (margin + row*(margin/4 + cellSize) <= ycoord <=
            margin + row*(margin/4 + cellSize) + cellSize):
            PSRow = row
        if (data.screenWidth - (margin - cellSize)/2 - cellSize <= xcoord <=
            data.screenWidth - (margin - cellSize)/2):
            PSCol = True
    return (PSRow, PSCol)


# Function that returns row (and col) if player presses an option in menu screen
def getMenuRowAndColFromCoords(data, xcoord, ycoord):
    menuRow = menuCol = None
    cellWidth = data.menuCellWidth
    cellHeight = data.menuCellHeight
    vertCenteringMargin = data.menuVertCenteringMargin
    horCenteringMargin = data.menuHorCenteringMargin
    verticalMargin = data.menuVerticalMargin
    left = horCenteringMargin 
    for row in xrange(len(data.menuDict)):
        if (vertCenteringMargin + row*(verticalMargin + cellHeight) <= ycoord 
            <= vertCenteringMargin+row*(verticalMargin+cellHeight)+cellHeight):
            menuRow = row
        if (left <= xcoord <= left + cellWidth):
            menuCol = True
    return (menuRow, menuCol)


# Function to deal with actions when menu options are selected
def dealWithMenuSelection(data, pressedMenuRow, pressedMenuCol):
    if (pressedMenuRow != None) and (pressedMenuCol != None):
        if (pressedMenuRow == 0):
            data.phase = "game"
        elif (pressedMenuRow == 1):
            data.phase = "instructions"
        elif (pressedMenuRow == 2):
            data.phase = "rules"
        elif (pressedMenuRow == 3):
            pygame.quit()
            data.mode = "Done"


def keyPressed(event, data):
    if (data.phase == "game"):
        if (event.key == pygame.K_SPACE):
            createZombie(data, "normalZombie")
        if (event.key == pygame.K_p):
            data.mode = "Paused" if data.mode == "Running" else "Running"
    redrawAll(data)
 

def timerFired(data):
    data.mousePos = pygame.mouse.get_pos()
    redrawAll(data)
    data.clock.tick(20)
    if (data.phase == "game") and (data.mode != "Paused"):
        if (data.gameCondition == ""):
            # Counter to periodically fire peas
            data.counter += 1
            updatePeas(data)
            updateZombies(data)
            updateLawnmowers(data)
            dealWithPeaZombieCollisions(data)
            dealWithPlantZombieCollisions(data)
            dealWithLawnmowerZombieCollisions(data)
            #Ensure that first zombie only spawns after 10 seconds, after which 
            #they spawn every 5 seconds
            spawnZombies(data)
            if (data.zombieList != []):
                # Fire a pea every 2 seconds
                if (data.counter % 40 == 0):
                    shootPeaAtZombies(data)
            if (data.counter % 100 == 0):
                spawnSunFromSky(data)
            if (data.counter % 100 == 0):
                spawnSunFromPlant(data)
            updateSuns(data)
        #manually manage the event queue
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            data.mode = "Done"
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            mousePressed(event, data)
        elif (event.type == pygame.KEYDOWN):
            keyPressed(event,data)


def redrawAll(data):
    data.screen.fill(data.blackColor)
    if (data.phase == "menu"):
        drawMenuScreen(data)
    
    elif (data.phase == "instructions"):
        data.screen.blit(data.rulesBackgroundImage, (0,0))
        drawInstructions(data)

    elif (data.phase == "rules"):
        data.screen.blit(data.rulesBackgroundImage, (0,0))
        drawRules(data)

    elif (data.phase == "game"):
        data.screen.blit(data.gameBackgroundImage, (0,0))
        #pygame.draw.rect(data.screen, data.whiteColor, Rect((0, 0), 
            #(data.screenWidth, data.screenHeight)))
        drawGarden(data)
        drawPlantSelection(data)
        drawGardenSpade(data)
        drawProgressBar(data)
        #Draw all the sprites created
        data.spritesList.draw(data.screen)
        if (data.messageType != None):
            displayMsg(data, data.messageType)
        displaySunCurrency(data)
        if (data.gameCondition != ""):
            displayGameCondition(data)
        dealWithPause(data)
        drawMenuButton(data)
    pygame.display.flip()


# Function that calls on drawMenuOptions and creates the whole menu
def drawMenuScreen(data):
    #data.screen.blit(data.menuImage, (0, 0))
    for row in xrange(len(data.menuDict)):
        drawMenuOptions(data, row)


# Function that takes in row and draws a cell with text in it, for the menu
def drawMenuOptions(data, row):
     # Takes care of extended length of the word "instructions"
    cellWidth = data.menuCellWidth*2.5 if row==1 else data.menuCellWidth
    cellHeight = data.menuCellHeight
    vertCenteringMargin = data.menuVertCenteringMargin
    horCenteringMargin = data.menuHorCenteringMargin
    verticalMargin = data.menuVerticalMargin
    left = horCenteringMargin
    top = vertCenteringMargin + row*(verticalMargin + cellHeight)
    #data.screen.blit(data.menuOptionImage, (left, top))
    # Change color if text is hovered over by mouse
    if ((left <= data.mousePos[0] <= left+cellWidth) and 
        (top <= data.mousePos[1] <= top+cellHeight)):
        color = data.lightBlueColor
    else: color = data.whiteColor
    #pygame.draw.rect(data.screen, color, Rect((left, top),
            #(cellWidth, cellHeight)))
    message = data.menuDict[row][0]
    font = pygame.font.SysFont("helvetica", 30, True)
    text = font.render(message, 1, color)
    data.screen.blit(text, (left, top))


# Function that creates a dictionary for the game menu
def createMenuDictionary(data):
    d = dict()
    #d[row] = [menuOption]
    d[0] = ["Play"]
    d[1] = ["Instructions"]
    d[2] = ["Rules"]
    d[3] = ["Quit"]
    data.menuDict = d


# Function that displays the basic instructions on how to play the game
def drawInstructions(data):
    message = (
        """
        Plants vs Kozbies is a zonal defense game where your goal is to prevent
        the Kozbies from reaching your home. You have an arsenal of plants at 
        your disposal, each with their own purposes, to stop this from 
        happening. 

        1. "Sun" is your currency. Collect falling sun to build more plants.

        2. The Kozbies periodically spawn after a certain time. Plant the 
           appropriate plants in the garden to kill the Kozbies.

        3. If a Kozbie happens to surpass your plant defense, you are backed up
           by a lawnmower on each lane, which kills all the zombies in that
           lane. Beware, as this is only a one-time occurrence. 

        4. The game is won once all the Kozbies are killed, as indicated by the
           game progress bar. 

        5. Press "P" to pause and unpause the game whenever necessary.
        """
        )
    textMarginX = data.screenWidth/7
    textMarginY = data.screenHeight/6
    textRect = Rect((textMarginX, textMarginY, data.screenWidth - 2*textMarginX, 
                    data.screenHeight - 1.8*textMarginY))
    textFont = pygame.font.SysFont("helvetica", 20)
    renderedText = render_textrect(message, textFont, textRect,
        (data.whiteColor), (data.greenColor))
    data.screen.blit(renderedText, (textMarginX, textMarginY))
    titleX = data.screenWidth/2.5
    titleY = data.screenHeight/13
    titleText = "Instructions"
    titleFont = pygame.font.SysFont("helvetica", 50, True)
    title = titleFont.render(titleText, 1, data.whiteColor)
    data.screen.blit(title, (titleX, titleY))
    drawMenuButton(data)


# Function that displays the rules of the game
def drawRules(data):
    message = (
        """
        The Kozbies are out to overtake your house, and there is only one thing
        standing between them and their destination - your garden! Use as many
        plants as you can to prevent this calamity. But before you go any 
        further, here are a few things to keep in mind:

        1. Plants do not grow without sunlight. The sun in the skies above 
           generates sufficient sunlight, but if you want more, you could always
           plant some sunflowers.

        2. The Kozbies stop at nothing, and will eat all the plants in their
           way. However, some plants take longer to be eaten than others...

        3. If you're not content with the way you laid out your plants, you can
           always use the "spade" tool to dig out and remove your plants. Be 
           warned - you will not be refunded for any plants you remove!
        """
        )
    marginX = data.screenWidth/7
    marginY = data.screenHeight/6
    textRect = Rect((marginX, marginY, data.screenWidth - 2*marginX, 
                    data.screenHeight - 2.5*marginY))
    font = pygame.font.SysFont("helvetica", 20)
    renderedText = render_textrect(message, font, textRect,
        (data.whiteColor), (data.armyGreenColor))
    data.screen.blit(renderedText, (marginX, marginY))
    data.screen.blit(data.rulesTextImage, 
                ((data.screenWidth-data.rulesWidth)/2,marginY-data.rulesHeight))
    drawMenuButton(data)



# Function that creates text when the game is paused
def dealWithPause(data):
    if (data.mode == "Paused"):
        left = data.screenWidth/2 - data.screenWidth/10
        top = data.screenHeight/2
        message = "Paused"
        font = pygame.font.SysFont("helvetica", 50, True)
        text = font.render(message, 1, data.blackColor)
        data.screen.blit(text, (left, top))


# Function that draws a button that takes the player to the menu screen on 
# the bottom right corner of the screen
def drawMenuButton(data):
    cellWidth = data.menuCellWidth
    cellHeight = data.menuCellHeight
    left = data.screenWidth - (data.screenWidth/10 + cellWidth)
    top = data.screenHeight - (data.screenHeight/9 + cellHeight)
    # Deal with centering text in button
    centeringX = 5
    centeringY = 4
    data.screen.blit(data.menuButtonImage, (left, top))
    #pygame.draw.rect(data.screen, data.redColor, Rect((left, top),
            #(cellWidth, cellHeight)))
    if ((left <= data.mousePos[0] <= left+cellWidth) and 
        (top <= data.mousePos[1] <= top+cellHeight)):
        color = data.blackColor
    else:
        color = data.whiteColor
    message = "Menu"
    font = pygame.font.SysFont("helvetica", 25, True)
    text = font.render(message, 1, color)
    data.screen.blit(text, (left+centeringX, top+centeringY))


# Function that takes the uset to the menu screen when the menu button is 
# clicked
def dealWithClickedMenuButton(data, pressedX, pressedY):
    cellWidth = data.menuCellWidth
    cellHeight = data.menuCellHeight
    left = data.screenWidth - (data.screenWidth/10 + cellWidth)
    top = data.screenHeight - (data.screenHeight/9 + cellHeight)
    if ((left <= pressedX <= left + cellWidth) and 
        (top <= pressedY <= top + cellHeight)):
        init(data)
        data.phase = "menu"



# Function that draws a garden (grid of light and dark green squares)
def drawGarden(data):
    for row in xrange(data.rows):
        for col in xrange(data.cols):
            drawGardenCell(data,row,col)


# Function that takes in row and col and draws a square cell
def drawGardenCell(data, row, col):
    margin = data.margin
    cellSize = data.cellSize
    lightGreen = (124,252,0)
    darkGreen = (50,205,50)
    top = margin + row*cellSize
    left = margin + col*cellSize
    if ((row+col) % 2 == 0):
        data.screen.blit(data.lightGrassImage, (left, top))
    elif((row+col) % 2 == 1):
        data.screen.blit(data.darkGrassImage, (left, top))


# Creates a 2D list representing the garden       
def loadGarden(data):
    data.garden = [([0]*data.cols) for row in xrange(data.rows)]


# Create a class of lawnmowers that inherits pygame's sprite superclass
class Lawnmower(pygame.sprite.Sprite):
    def __init__(self, data, row, velocity):
            pygame.sprite.Sprite.__init__(self)
            self.image = data.lawnmowerImage
            self.rect = self.image.get_rect()
            self.row = row
            self.velocity = velocity
            self.size = data.lawnmowerSize
            self.inMotion = False


# Function that moves lawnmowers
def placeLawnmowers(data):
    col = 0 # place lawnmowers at start of the garden
    margin = data.margin
    cellSize = data.cellSize
    velocity = 10
    for row in xrange(data.rows):
        lawnmower = Lawnmower(data, row, velocity)
        lawnmower.rect.x = margin + col*cellSize - data.lawnmowerSize
        lawnmower.rect.y = margin + row*cellSize
        data.spritesList.add(lawnmower)
        data.lawnmowerList.add(lawnmower)


# Function that updates the position of the lawnmowers based on collision and
# velocity
def updateLawnmowers(data):
    smallestCol = 0
    largestCol = 8
    for lawnmower in data.lawnmowerList:
        for zombie in data.zombieList:
             # zombie crossing left edge of the garden
            if (zombie.rect.x <= data.margin + smallestCol*data.cellSize):
                if (lawnmower.row == zombie.row):
                    lawnmower.inMotion = True
        if (lawnmower.inMotion == True):
            lawnmower.rect.x += lawnmower.velocity
        if (lawnmower.rect.x > data.margin + largestCol*data.cellSize):
            data.lawnmowerList.remove(lawnmower)
            data.spritesList.remove(lawnmower)


# Function that removes zombies hit by the lawnmower
def dealWithLawnmowerZombieCollisions(data):
    for lawnmower in data.lawnmowerList:
        # Add zombies hit by lawnmowers to list "zombiesHit", 
        # but do not kill sprites
        zombiesHit=pygame.sprite.spritecollide(lawnmower,data.zombieList,False)
        for zombie in zombiesHit:
            data.spritesList.remove(zombie)
            data.zombieList.remove(zombie)


# Draw all the plant selection options
def drawPlantSelection(data):
    for row in xrange(data.plantSelectionRows):
        drawPlantSelectionCell(data, row)


# Draw the individual plant selection cell options
def drawPlantSelectionCell(data, row):
    margin = data.margin
    cellSize = data.plantSelectionCellSize
    top =  margin + row*(margin/4 + cellSize)
    bottom = top + cellSize
    left = data.screenWidth - (margin - cellSize)/2 - cellSize
    right = left + cellSize
    # Get image from dictionary based on selection row
    plantImage = data.plantSelectionDict[row][1]
    # Highlighting plant selection
    if (data.plantSelection == data.plantSelectionDict[row][0]):
        pygame.draw.rect(data.screen, data.blueColor, Rect((left, top), 
                (cellSize, cellSize)))
    else:
        pygame.draw.rect(data.screen, data.blackColor, Rect((left, top), 
                (cellSize, cellSize)))
    # Placing corresponding plant image onto cell
    pygame.Surface.blit(data.screen, plantImage, (left, top))
    displayPlantCost(data, row, top, left)


# Function to draw the garden spade for removing plants from the garden
def drawGardenSpade(data):
    cellSize = data.plantSelectionCellSize
    margin = data.margin
    boxMargin = 6 # Margin between enclosing box and spade image
    gardenCol = 7 # X-axis positioning factor (same offset as 8th garden column)
    # Background is red if selected, and black otherwise
    color=data.redColor if (data.plantSelection == "spade") else data.blackColor
    # Enclosing box is just an outline if not selected, else it is a filled 
    # square
    width = 0 if (data.plantSelection == "spade") else 3
    left = margin + gardenCol*data.cellSize
    top = (margin - cellSize)/2
    pygame.draw.rect(data.screen, color, Rect((left-boxMargin, top-boxMargin), 
                        (cellSize+2*boxMargin, cellSize+2*boxMargin)), width)
    data.screen.blit(data.spadeImage, (left, top))


# Function that selects spade if user clicks on the spade icon
def dealWithGardenSpade(data, pressedX, pressedY):
    cellSize = data.plantSelectionCellSize
    margin = data.margin
    gardenCol = 7
    left = margin + gardenCol*data.cellSize
    right = left + cellSize
    top = (margin - cellSize)/2
    bottom = top + cellSize
    if (left <= pressedX <= right) and (top <= pressedY <= bottom):
        data.plantSelection = "spade"
    

# Function that deletes the plant in the garden row and col clicked, if the 
# spade is selected and if the clicked cell contains a plant
def useSpadeIfSelected(data, gardenRow, gardenCol, pressedX, pressedY):
    margin = data.margin
    cols = data.cols
    rows = data.rows
    cellSize = data.cellSize
    if (not (margin <= pressedX <= margin + cols*cellSize) or
        not(margin <= pressedY <= margin + rows*cellSize)):
        data.plantSelection = ""
    if (gardenRow != None) and (gardenCol != None):
        removePlant(data, gardenRow, gardenCol)
        data.plantSelection = ""
    else:
        data.messageType = "emptySpadeSquare"
        data.plantSelection = ""
        


# Function that displays the cost of each plant beneath the plant icons on the
# right of the screen
def displayPlantCost(data, row, top, left):
    message = "Cost:%s" %str(data.plantSelectionDict[row][2])
    msgColor = data.blackColor 
    positionX = left
    positionY = top + data.plantSelectionCellSize
    # Creating the currency display text
    font = pygame.font.SysFont("helvetica", 15, False, True)
    text = font.render(message, 1, msgColor)
    data.screen.blit(text, (positionX, positionY))


# Creates a dictionary for plant selection
def createPlantSelectionDict(data):
    # d[plantSelectionRow] = [plant type, plant image, cost]
    d = dict()
    d[0] = ["greenPeaShooter", data.PSgreenPeaShooterImage, 100]
    d[1] = ["snowPeaShooter", data.PSSnowPeaShooterImage, 150]
    d[2] = ["sunflower", data.PSSunflowerImage, 50]
    d[3] = ["wallnut", data.PSWallnutImage, 75]
    data.plantSelectionDict = d


# Function to activate selection of plant after clicking on that plant in the
# plants select options
def selectPlant(data, pressedPSRow, pressedPSCol):
    if ((pressedPSRow != None) and (pressedPSCol == True) and
        data.plantSelection == ""):
        data.plantSelection = data.plantSelectionDict[pressedPSRow][0]
        data.messageType = None
    


# Function to call shootPea, only on plants in whose row there are zombies in
def shootPeaAtZombies(data):
    for zombie in data.zombieList:
        for plant in data.plantList: 
            # Check every zombie's and plant's row (and col)
            zombieRow = zombie.row
            plantRow = plant.row
            plantCol = plant.col
            plantType = plant.name
            # Compare if in same row: shootPea
            if ((plantRow == zombieRow) and 
                (plant.plantClass == "PeaShooter")):
                shootPea(data, plantType, plantRow, plantCol)


# Create class of peas by inheriting pygame's "sprite" class
class Pea(pygame.sprite.Sprite):
        def __init__(self, data, plantType, peaVelocity):
            pygame.sprite.Sprite.__init__(self)
            if data.plantDict[plantType][1] == "green":
                self.image = data.normalPeaImage
            elif data.plantDict[plantType][1] == "blue":
                self.image = data.frozenPeaImage
            self.rect = self.image.get_rect()
            self.type = plantType
            self.velocity = peaVelocity
            self.width = data.peaSize


# Function that shoots peas by creating an instance of the Pea type
def shootPea(data, plantType, row, col):
    margin = data.margin
    cellSize = data.cellSize
    plantWidth = data.plantWidth
    peaVelocity = 10
    pea = Pea(data, plantType, peaVelocity)
    pea.rect.x = margin + col*cellSize + (cellSize - plantWidth)/2 + plantWidth
    pea.rect.y = margin + row*cellSize + (cellSize - plantWidth)
    data.spritesList.add(pea)
    data.peasList.add(pea)


# Function that updates the position of the pea(s) based on velocity
def updatePeas(data):
    for pea in data.peasList:
        pea.rect.x += pea.velocity
        if (pea.rect.x > data.margin + 8*data.cellSize+data.cellSize-pea.width):
            data.peasList.remove(pea)
            data.spritesList.remove(pea)


# Creates a class of sun currency by inheriting pygame's "sprite" class
class Sun(pygame.sprite.Sprite):
    def __init__(self, data, velocity, startRow, startCol, endRow):
        pygame.sprite.Sprite.__init__(self)
        self.image = data.sunImage
        self.rect = self.image.get_rect()
        self.size = data.sunSize
        self.velocity = velocity
        self.startRow = startRow
        self.startCol = startCol
        self.endRow = endRow
        self.restTime = 0 # fps * time during which sun is at rest


# Function to create a sun with set velocity, startRow, startCol, and endRow 
# (endRow only applicable if sun is falling from sky)
def spawnSun(data, velocity, startRow, startCol, endRow):
    margin = data.margin 
    cellSize = data.cellSize
    sunSize = data.sunSize
    sun = Sun(data, velocity, startRow, startCol, endRow)
    sun.rect.x = margin + startCol*cellSize + (cellSize - sunSize)/2
    sun.rect.y = margin + startRow*cellSize + (cellSize - sunSize)/2
    data.spritesList.add(sun)
    data.sunList.add(sun)


# Function that makes a sun fall from the sky and drop onto a random location
# on the garden
def spawnSunFromSky(data):
    margin = data.margin
    cellSize = data.cellSize
    sunSize = data.sunSize
    rows = data.rows
    cols = data.cols
    velocity = 1
    startRow = 0
    startCol = random.randint(0, cols - 1)
    endRow = random.randint(rows-2, rows-1)
    spawnSun(data, velocity, startRow, startCol, endRow)


# Function that makes sunflowers generate sun 
def spawnSunFromPlant(data):
    margin = data.margin
    cellSize = data.cellSize
    sunSize = data.sunSize
    velocity = 0
    for plant in data.plantList:
        if (plant.spawnSun == True):
            startRow = plant.row
            startCol = plant.col
            endRow = plant.row
            spawnSun(data, velocity, startRow, startCol, endRow)


# Function that updates the current position of the sun based on the sun's 
# velocity
def updateSuns(data):
    margin = data.margin
    cellSize = data.cellSize
    sunSize = data.sunSize
    # For all suns, move by velocity, and stop movement if it reaches endRow
    for sun in data.sunList:
        sun.rect.y += sun.velocity
        if (sun.rect.y == margin + sun.endRow*cellSize + (cellSize-sunSize)/2):
            sun.velocity = 0
            sun.restTime += 1
            if (sun.restTime == 80): # if sun is at rest for 4 seconds, delete
                data.sunList.remove(sun)
                data.spritesList.remove(sun)


# Function called in Mousepressed that allows user to collect generated sun by 
# clicking on it
def collectSuns(data, pressedX, pressedY):
    for sun in data.sunList:
        if ((sun.rect.x <= pressedX <= sun.rect.x + data.sunSize) and
            (sun.rect.y <= pressedY <= sun.rect.y + data.sunSize)):
            data.sunCurrency += 25
            data.spritesList.remove(sun)
            data.sunList.remove(sun)


# Create class of plants by inheriting pygame's "sprite" class
class Plant(pygame.sprite.Sprite):
    def __init__(self, data, plantType, row, col):
        pygame.sprite.Sprite.__init__(self)
        self.name = plantType
        self.image = data.plantDict[plantType][0]
        self.rect = self.image.get_rect()
        self.width = data.plantWidth
        self.height = data.plantHeight
        self.row = row
        self.col = col
        self.gardenNum = data.plantDict[plantType][2]
        self.health = data.plantDict[plantType][5]
        self.shootPea = False
        self.spawnSun = False
        self.plantClass = Plant


# Create sub-class of plants called peashooters who shoot peas at zombies
class PeaShooter(Plant):
    def __init__(self, data, plantType, row, col):
        super(PeaShooter, self).__init__(data, plantType, row, col)
        self.shootPea = True
        self.spawnSun = False
        self.plantClass = "PeaShooter"


# Create sub-class of plants called Sunflowers who generate sun for building 
# more plants
class Sunflower(Plant):
    def __init__(self, data, plantType, row, col):
        super(Sunflower, self).__init__(data, plantType, row, col)
        self.spawnSun = True
        self.shootPea = False
        self.plantClass = "Sunflower"


# Function that creates plants by creating an instance of the Plant type
def createPlant(data, plantType, row, col):
    if (data.garden[row][col] == 0):       
        if (data.sunCurrency >= data.plantDict[plantType][4]):
            margin = data.margin
            cellSize = data.cellSize
            plant = data.plantDict[plantType][3](data, plantType, row, col)
            # Centering plant in cell
            plant.rect.x = margin + col*cellSize+(cellSize - data.plantWidth)/2
            plant.rect.y = margin + row*cellSize+(cellSize -data.plantHeight)/2
            data.garden[row][col] = plant.gardenNum
            # Subtract cost of plant from sun currency
            data.sunCurrency -= data.plantDict[plantType][4]
            # Adding instance to sprites and plants lists
            data.spritesList.add(plant)
            data.plantList.add(plant)
            data.plantSelection = ""
        else:
            data.messageType = "tooCostly"
            data.plantSelection = ""
    else:
        data.messageType = "nonEmptySquare"
        data.plantSelection = ""


# Function that removes plant from the selected row and col in the garden
def removePlant(data, row, col):
    for plant in data.plantList:
        if (plant.row == row) and (plant.col == col):
            data.spritesList.remove(plant)
            data.plantList.remove(plant)
    data.garden[row][col] = 0


# Creates a dictionary mapping different plantTypes to their attributes
def createPlantDictionary(data):
    d = dict()
    #d[plantType] =[plantImage, peaColor, 2DBoardNum, plantClass, cost, health]
    d["greenPeaShooter"] = ([data.greenPeaShooterImage, "green", 
                            1, PeaShooter, 100, 120])
    d["snowPeaShooter"] = ([data.snowPeaShooterImage, "blue", 2, 
                           PeaShooter, 150, 120])
    #
    d["sunflower"] = [data.sunflowerImage, None, 3, Sunflower, 50, 120]
    d["wallnut"] = [data.wallnutImage, None, 4, Plant, 75, 1000]
    data.plantDict = d


# Create class of zombies by inheriting pygame's "sprite" class
class Zombie(pygame.sprite.Sprite):
    def __init__(self, data, zombieType, row, velocity, zombieHealth):
        pygame.sprite.Sprite.__init__(self)
        self.name = zombieType
        self.image = data.zombieDict[zombieType][0]
        self.rect = self.image.get_rect()
        self.width = data.zombieWidth
        self.height = data.zombieHeight
        self.initialVelocity = velocity
        self.currentVelocity = velocity
        self.health = zombieHealth
        self.row = row


# Function that creates zombies by creating an instance of the Zombie type
def createZombie(data, zombieType):
    margin = data.margin
    cellSize = data.cellSize
    # Spawn zombie at a random row, but at the last col in the garden
    row = random.randint(0, data.rows-1)
    col = data.cols-1
    velocity = data.zombieDict[zombieType][2]
    # number of hits needed to kill zombie
    zombieHealth = data.zombieDict[zombieType][1]
    zombie = Zombie(data, zombieType, row, velocity, zombieHealth)
    zombie.rect.x = margin + col*cellSize + (cellSize - zombie.width)/2
    zombie.rect.y = margin+row*cellSize + (cellSize - zombie.height)/2
    data.spritesList.add(zombie)
    data.zombieList.add(zombie)


# Function that calls createZombie to spawn zombies based on the progression
# of the game
def spawnZombies(data):
    periodicSpawnTime = 190
    zombieType = random.choice(data.zombieTypeList)
    # Only start spawning zombies after 10 seconds
    # Spawn only normal zombies every 8 to 11 seconds
    if (data.counter % periodicSpawnTime == 0):
        if (200 < data.counter < 400):
            createZombie(data, "normalZombie")
    # After 20 seconds, start spawning different types of zombies
        elif (400 < data.counter < 600):
            createZombie(data, zombieType)
    # After 35 seconds, spawn a huge wave of 4 zombies (inequality used to 
    # keep text on screen for 3 seconds)
    #if (700 <= data.counter <= 760):
        elif (data.counter == 760):
            createZombie(data, zombieType)
            createZombie(data, zombieType)
            createZombie(data, zombieType)
            createZombie(data, zombieType)
    elif (data.counter == data.winCounter):
        # End game when time exceeds the winCounter and when there are no 
        # zombies left
        data.gameCondition = "win"



def displayHugeWaveText(data):
    textWidth = 100
    textHeight = 20
    message = "A huge wave of zombies is approaching!"
    msgColor = data.redColor
    positionX = data.screenWidth/2 - textWidth/2
    positionY = data.screenHeight/2 - textHeight/2
    # Creating the "huge wave" text
    font = pygame.font.SysFont("helvetica", 30, True)
    text = font.render(message, 1, msgColor)
    data.screen.blit(text, (positionX, positionY))


# Creates a dictionary mapping different zombieTypes to their attributes
def createZombieDictionary(data):
    d = dict()
    # d[zombieType] = [zombieImage, health, velocity]
    d["normalZombie"] = [data.zombieImage, 5, 2]
    d["toughZombie"] = [data.toughZombieImage, 8, 2]
    d["footballZombie"] = [data.footballZombieImage, 7, 3]
    data.zombieDict = d


# Creates a list of different types of zombies, usable when spawning random 
# zombies
def createZombieTypeList(data):
    zombieTypeList = []
    for key in data.zombieDict:
        zombieTypeList.append(key)
    data.zombieTypeList = zombieTypeList


#Function that updates position of zombie(s) based on velocity
def updateZombies(data):
    for zombie in data.zombieList:
        zombie.rect.x -= zombie.currentVelocity
        if (zombie.rect.x < 0):
            data.zombieList.remove(zombie)
            data.spritesList.remove(zombie)
            data.gameCondition = "loss"


# Function that checks for collision between peas and zombies and deletes both
# pea and zombie on collision
def dealWithPeaZombieCollisions(data):
    for pea in data.peasList:
        # Add zombies hit by peas to list "zombiesHit", but do not kill sprites
        zombiesHit = pygame.sprite.spritecollide(pea, data.zombieList, False)
        if (zombiesHit != []):
            data.peasList.remove(pea)
            data.spritesList.remove(pea)
        for zombie in zombiesHit:
            zombie.health -= 1
            if (pea.type == "snowPeaShooter"):
                if (zombie.name == "normalZombie"):
                    zombie.image = data.sZombieImage
                elif (zombie.name == "toughZombie"):
                    zombie.image = data.sToughZombieImage
                elif (zombie.name == "footballZombie"):
                    zombie.image = data.sFootballZombieImage
                zombie.currentVelocity /= 2.0
            if (zombie.health == 0):
                data.spritesList.remove(zombie)
                data.zombieList.remove(zombie)


# Function that checks for collision between plants and zombies - zombies stop,
# eat plant and then continue moving
def dealWithPlantZombieCollisions(data):
    for zombie in data.zombieList:
        plantsHit = pygame.sprite.spritecollide(zombie, data.plantList, False)
        if (plantsHit != []):
            # Zombie stops to eat plant
            zombie.currentVelocity = 0
        for plant in plantsHit:
            # As zombie eats plant, plant's health decreases
            plant.health -= 1
            if (plant.name == "wallnut") and (plant.health <= 400):
                plant.image = data.eatenWallnutImage
            if (plant.health == 0):
                #When plant reaches 0 health, it dies and zombie resumes motion
                data.spritesList.remove(plant)
                data.plantList.remove(plant)
                zombie.currentVelocity = zombie.initialVelocity


# Function that draws a progress bar to display the progress of the game towards
# a win condition
def drawProgressBar(data):
    counter = data.winCounter
    scalingFactor = 7
    left = data.screenWidth/15 + 100 # Positioning bar on the screen
    top = data.screenHeight/10
    height = 20
    outlineLength = counter/scalingFactor
    barLength = data.counter/scalingFactor
    outline = 2
    color = data.blueColor
    pygame.draw.rect(data.screen, data.redColor, Rect((left, top),
                        (barLength, height)))
    pygame.draw.rect(data.screen, color, Rect((left, top), 
                        (outlineLength, height)), outline)
    positionX = left - 100 # positioning text on the screen
    positionY = top
    message = "Progress:"
    font = pygame.font.SysFont("helvetica", 20, True)
    text = font.render(message, 1, data.blackColor)
    data.screen.blit(text, (positionX, positionY))
    


# Function called in redrawAll that displays the current sun currency that
# the player has
def displaySunCurrency(data):
    row = 5 # positioning
    col = 1 # positioning
    currency = data.sunCurrency
    message = "Sun: %d" % currency
    msgColor = data.blackColor if currency > 0 else data.redColor
    positionX = data.margin + col*data.cellSize
    positionY = data.margin + row*data.cellSize + data.margin/3
    # Creating the currency display text
    font = pygame.font.SysFont("helvetica", 30, True)
    text = font.render(message, 1, msgColor)
    data.screen.blit(text, (positionX, positionY))


# Function that displays win or loss screen
def displayGameCondition(data):
    pygame.draw.rect(data.screen, data.greenColor, Rect((0,0),
                (data.screenWidth, data.screenHeight)))
    message = ""
    if (data.gameCondition == "win"):
        message = "You Win!"
        msgColor = data.blackColor
        positionX = data.screenWidth/2 - data.screenWidth/10
        positionY = data.screenHeight/2
        font = pygame.font.SysFont("helvetica", 40, True)
        text = font.render(message, 1, msgColor)
        data.screen.blit(text, (positionX, positionY))
    elif (data.gameCondition == "loss"):
        data.screen.blit(data.gameOverImage, (0,0))


# Function called in redrawAll that takes in a message type and 
# blits corresponding message on the screen
def displayMsg(data, msgType):
    row = 5 # positioning
    col = 5 # positioning
    # Corresponding message retrieved from dictionary of messages
    message = data.msgDict[msgType][0]
    msgColor = data.msgDict[msgType][1]
    positionX = data.margin + col*data.cellSize
    positionY = data.margin + row*data.cellSize + data.margin/3 # ratio
    # Creating error message text
    font = pygame.font.SysFont("helvetica", 20)
    text = font.render(message, 1, msgColor)
    data.screen.blit(text, (positionX, positionY))


# Creates a dictionary of messages
def createMessageDictionary(data):
    # d[message type] = [message, message color]
    d = dict()
    d["nonEmptySquare"]=["Please select an empty square.", data.redColor]
    d["tooCostly"] = ["Not enough Sun!", data.redColor]
    d["emptySpadeSquare"] = ["No plant to dig out!", data.redColor]
    data.msgDict = d


## Code below taken from source (cited below)
class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def render_textrect(string, font, rect, text_color, 
    background_color, justification=0):

    import pygame
    
    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise (TextRectException, "The word " + word + 
                        " is too long to fit in the rect passed.")
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line
                else:
                    final_lines.append(accumulated_line)
                    accumulated_line = word + " "
            final_lines.append(accumulated_line)
        else:
            final_lines.append(requested_line)

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size)
    surface.fill(background_color)

    accumulated_height = 0
    for line in final_lines:
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise (TextRectException, 
        "Once word-wrapped, the text string was too tall to fit in the rect.")
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, (
                (rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, 
                    (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise (TextRectException, "Invalid justification argument: " + 
                    str(justification))
        accumulated_height += font.size(line)[1]

    return surface

## TextRectException and render_textrect taken from 
## http://www.pygame.org/pcr/text_rect/index.php (David Clarke, 05/23/2001)

def init(data):
    loadGarden(data)

    # Plant selection options initializations
    data.plantSelectionCellSize = data.margin/2
    data.plantSelection = ""

    data.menuCellWidth = int(data.screenWidth/14.0)
    data.menuCellHeight = int(data.screenHeight/20.0)
    data.menuVertCenteringMargin = int(data.screenHeight/3.0)
    data.menuHorCenteringMargin = (data.screenWidth-data.menuCellWidth)/2
    data.menuVerticalMargin = int(data.screenHeight/13.0)

    data.rulesWidth = data.screenWidth/3
    data.rulesHeight = data.screenHeight/7

    data.sunCurrency = 50

    # Initializing all the object sizes
    data.plantWidth = int((7.0/9)*data.cellSize)
    data.plantHeight = int((7.0/9)*data.cellSize)
    data.zombieWidth = int((8.0/9)*data.cellSize)
    data.zombieHeight = int((19.0/20)*data.cellSize)
    data.peaSize = int((1.0/7)*data.plantHeight)
    data.sunSize = int((4.0/7)*data.plantHeight)
    data.lawnmowerSize = int((9.0/10)*data.cellSize)

    # Loading all necessary images and scaling them to size
    data.greenPeaShooterImage = pygame.image.load("PeaShooter.png").convert()
    data.greenPeaShooterImage=(pygame.transform.scale(data.greenPeaShooterImage, 
                           (data.plantWidth,data.plantHeight)))
    data.PSgreenPeaShooterImage=(pygame.transform.scale(data.greenPeaShooterImage, 
        (data.plantSelectionCellSize, data.plantSelectionCellSize)))
    data.snowPeaShooterImage = pygame.image.load("FPeaShooter.png").convert()
    data.snowPeaShooterImage = (pygame.transform.scale(data.snowPeaShooterImage, 
                                 (data.plantWidth,data.plantHeight)))
    data.PSSnowPeaShooterImage=(pygame.transform.scale(data.snowPeaShooterImage, 
                    (data.plantSelectionCellSize, data.plantSelectionCellSize)))
    data.sunflowerImage = pygame.image.load("Sunflower.gif").convert()
    data.sunflowerImage = (pygame.transform.scale(data.sunflowerImage,
                           (data.plantWidth, data.plantHeight)))
    data.PSSunflowerImage = (pygame.transform.scale(data.sunflowerImage, 
                    (data.plantSelectionCellSize, data.plantSelectionCellSize)))
    data.zombieImage = pygame.image.load("Kozbie.png").convert()
    data.zombieImage = (pygame.transform.scale(data.zombieImage, 
                        (data.zombieWidth,data.zombieHeight)))
    data.sZombieImage = pygame.image.load("SKozbie.png").convert()
    data.sZombieImage = (pygame.transform.scale(data.sZombieImage, 
                        (data.zombieWidth,data.zombieHeight)))
    data.sunImage = pygame.image.load("Sun.png").convert()
    data.sunImage = (pygame.transform.scale(data.sunImage,
                        (data.sunSize, data.sunSize)))
    data.wallnutImage = pygame.image.load("Wallnut.png").convert()
    data.wallnutImage = (pygame.transform.scale(data.wallnutImage, 
                           (data.plantWidth,data.plantHeight)))
    data.PSWallnutImage = (pygame.transform.scale(data.wallnutImage, 
                    (data.plantSelectionCellSize, data.plantSelectionCellSize)))
    data.eatenWallnutImage = pygame.image.load("EatenWallnut.png").convert()
    data.eatenWallnutImage = (pygame.transform.scale(data.eatenWallnutImage, 
                           (data.plantWidth,data.plantHeight)))
    data.lawnmowerImage = pygame.image.load("Lawnmower.png").convert()
    data.lawnmowerImage = (pygame.transform.scale(data.lawnmowerImage, 
                        (data.lawnmowerSize, data.lawnmowerSize)))
    data.toughZombieImage = pygame.image.load("ToughKozbie.png").convert()
    data.toughZombieImage = (pygame.transform.scale(data.toughZombieImage, 
                        (data.zombieWidth,data.zombieHeight)))
    data.sToughZombieImage = pygame.image.load("SToughKozbie.png").convert()
    data.sToughZombieImage = (pygame.transform.scale(data.sToughZombieImage, 
                        (data.zombieWidth,data.zombieHeight)))
    data.footballZombieImage = pygame.image.load("FootballKozbie.png").convert()
    data.footballZombieImage = (pygame.transform.scale(data.footballZombieImage, 
                        (data.zombieWidth,data.zombieHeight)))
    data.sFootballZombieImage = pygame.image.load("SFootballKozbie.png").convert()
    data.sFootballZombieImage = (pygame.transform.scale(data.sFootballZombieImage, 
                        (data.zombieWidth,data.zombieHeight)))
    data.normalPeaImage = pygame.image.load("NormalPea.gif").convert()
    data.normalPeaImage = (pygame.transform.scale(data.normalPeaImage,
                            (data.peaSize, data.peaSize)))
    data.frozenPeaImage = pygame.image.load("FrozenPea.gif").convert()
    data.frozenPeaImage = (pygame.transform.scale(data.frozenPeaImage,
                            (data.peaSize, data.peaSize)))
    data.menuButtonImage = pygame.image.load("MenuButton.png").convert()
    data.menuButtonImage = (pygame.transform.scale(data.menuButtonImage,
                            (data.menuCellWidth, data.menuCellHeight)))
    data.rulesBackgroundImage=pygame.image.load("RulesBackground.jpg").convert()
    data.rulesBackgroundImage=(pygame.transform.scale(data.rulesBackgroundImage,
                            (data.screenWidth, data.screenHeight)))
    data.rulesTextImage = pygame.image.load("Rules.png").convert()
    data.rulesTextImage = (pygame.transform.scale(data.rulesTextImage,
                            (data.rulesWidth, data.rulesHeight)))
    data.spadeImage = pygame.image.load("Spade.png").convert()
    data.spadeImage = (pygame.transform.scale(data.spadeImage,
                    (data.plantSelectionCellSize, data.plantSelectionCellSize)))
    data.lightGrassImage = pygame.image.load("LightGrass.jpg").convert()
    data.lightGrassImage = (pygame.transform.scale(data.lightGrassImage,
                    (data.cellSize, data.cellSize)))
    data.darkGrassImage = pygame.image.load("DarkGrass.jpg").convert()
    data.darkGrassImage = (pygame.transform.scale(data.darkGrassImage,
                    (data.cellSize, data.cellSize)))
    #data.menuImage = pygame.image.load("MenuBackgroundImage.png").convert()
    #data.menuImage = (pygame.transform.scale(data.menuImage,
                    (data.screenWidth, data.screenHeight)))
    data.gameBackgroundImage = pygame.image.load("gameBackground.jpg").convert()
    data.gameBackgroundImage = (pygame.transform.scale(data.gameBackgroundImage,
                    (data.screenWidth, data.screenHeight)))
    data.gameOverImage = pygame.image.load("GameOverScreen.png").convert()
    data.gameOverImage = (pygame.transform.scale(data.gameOverImage,
                    (data.screenWidth, data.screenHeight)))

    # Initializing all useful RGB colors
    data.whiteColor = (255,255,255)
    data.blackColor = (0,0,0)
    data.greenColor = (34,139,34)
    data.greyColor = (128,128,128)
    data.blueColor = (35,70,240)#?????
    data.redColor = (255,0,0)
    data.lighterBlueColor = (135, 206, 250)
    data.lightBlueColor = (0, 191, 255)
    data.armyGreenColor = (98, 102, 18)

    #Remove all of the specific color in specific image image
    data.greenPeaShooterImage.set_colorkey(data.whiteColor)
    data.PSgreenPeaShooterImage.set_colorkey(data.whiteColor)
    data.snowPeaShooterImage.set_colorkey(data.blackColor)
    data.PSSnowPeaShooterImage.set_colorkey(data.blackColor)
    data.sunflowerImage.set_colorkey(data.whiteColor)
    data.PSSunflowerImage.set_colorkey(data.whiteColor)
    data.zombieImage.set_colorkey(data.blackColor)
    data.sZombieImage.set_colorkey(data.blackColor)
    data.toughZombieImage.set_colorkey(data.blackColor)
    data.sToughZombieImage.set_colorkey(data.blackColor)
    data.footballZombieImage.set_colorkey(data.blackColor)
    data.sFootballZombieImage.set_colorkey(data.blackColor)
    data.sunImage.set_colorkey(data.blackColor)
    data.PSWallnutImage.set_colorkey(data.blackColor)
    data.wallnutImage.set_colorkey(data.blackColor)
    data.eatenWallnutImage.set_colorkey(data.blackColor)
    data.spadeImage.set_colorkey(data.blackColor)
    data.menuButtonImage.set_colorkey(data.blackColor)

    # Initialize and create dictionaries
    data.plantDict = {}
    createPlantDictionary(data)
    data.zombieDict = {}
    createZombieDictionary(data)
    data.zombieTypeList = []
    createZombieTypeList(data)
    data.plantSelectionDict = {}
    createPlantSelectionDict(data)
    data.msgDict = {}
    createMessageDictionary(data)
    data.menuDict = {}
    createMenuDictionary(data)

    data.messageType = None

    data.plantSelectionRows = len(data.plantSelectionDict)

    # Initialize timerFired counters
    data.counter = 0
    
    # Creates lists of sprites
    data.spritesList = pygame.sprite.Group()
    data.plantList = pygame.sprite.Group()
    data.zombieList = pygame.sprite.Group()
    data.peasList = pygame.sprite.Group()
    data.sunList = pygame.sprite.Group()
    data.lawnmowerList = pygame.sprite.Group()

    data.winCounter = 1500

    data.phase = "menu"

    data.gameCondition = ""

    # Initialize all lawnmowers
    placeLawnmowers(data)

    data.mode = "Running"


def run():
    pygame.init()
     
    #not given the Canvas class
    class Struct: pass
    data = Struct()
    data.rows = 5
    data.cols = 9
    data.margin = 130
    data.cellSize = 90
    data.screenWidth = 2*data.margin + data.cols*data.cellSize
    data.screenHeight = 2*data.margin + data.rows*data.cellSize
    #initialize the screen
    data.screenSize = (data.screenWidth,data.screenHeight)
    data.screen = pygame.display.set_mode(data.screenSize)
    pygame.display.set_caption("Plants vs. Kozbies")
     
    #initialize clock
    data.clock = pygame.time.Clock()
    init(data)
    timerFired(data)
    while (data.mode != "Done"):
        timerFired(data)
 
     
     
run()



# NEXT: 
# Delete everything -speed things up
# Win condition!


# QUESTIONS


# TO FIX:
# After wallnut is destroyed, only one zombie moves ahead - rest stay in place
# 1 pea affects multiple overlapped zombies
# Remove permaslow on zombies hit by snowPeaShooter
# Zombie color change when slowed

#LAST MINUTE
# Remove spacebar to create zombie
# Menu botton!
# Change "zombies" to "Kozbies"!!


# TIME LOG
#   3pm to 4 pm, 18 nov (mon): ??? (in interp)
#   7 pm to 9:30 pm, 18 nov (mon): getting plants to fire peas automatically, other things here and there
#   Worked from 12:30 am to 4:30 am, 19 nov (tue): creating dicts of plants, modifying classes, creating plant selections, adding 
# snowPeaShooter to the game