import mcpi.minecraft as minecraft
import mcpi.block as block
import time
import random
import math

def distanceBetweenPoints(point1, point2):
    xd = point2.x - point1.x
    yd = point2.y - point1.y
    zd = point2.z - point1.z
    return math.sqrt((xd*xd) + (yd*yd) + (zd*zd))

def createBeacon(currentTarget):
    mc.postToChat("It looks like you need a little help")
    for x in range(1,300):
        mc.setBlock(currentTarget.x, currentTarget.y+x, currentTarget.z, block.WOOL)

def removeBeacon(currentTarget):
    for x in range(1,300):
        mc.setBlock(currentTarget.x, currentTarget.y+x, currentTarget.z, block.AIR)

mc = minecraft.Minecraft.create()

mc.postToChat("Welcome to Minecraft Find the Diamond")
mc.postToChat("The Game will begin in 3 seconds...")

time.sleep(3)

playerPosition = mc.player.getPos()

airBlock = False

while airBlock == False:

    mc.postToChat("Hiding the Diamond...")

    # pick a random block
    randomBlockPos = minecraft.Vec3(int(playerPosition.x), int(playerPosition.y), int(playerPosition.z))
    randomBlockPos.x = random.randrange(randomBlockPos.x - 50, randomBlockPos.x + 50)
    randomBlockPos.y = random.randrange(0, randomBlockPos.y + 100)
    randomBlockPos.z = random.randrange(randomBlockPos.z - 50, randomBlockPos.z + 50)

    # get the type of the random block
    targetBlockType = mc.getBlock(randomBlockPos.x, randomBlockPos.y, randomBlockPos.z)

    if targetBlockType == 0: #AIR
        # bring it down until it is sitting on the ground level
        blockInAir = True
        CurrentYPos = randomBlockPos.y
        while blockInAir == True:
            CurrentYPos = CurrentYPos - 1
            blockType = mc.getBlock(randomBlockPos.x, CurrentYPos, randomBlockPos.z)
            if blockType <> 0:
                randomBlockPos.y = CurrentYPos+1
                blockInAir = False
        airBlock = True

mc.setBlock(randomBlockPos.x, randomBlockPos.y, randomBlockPos.z, block.DIAMOND_BLOCK)
mc.postToChat("A Diamond has been hidden - Find it!")

seeking = True
timeStarted = time.time()
while (seeking == True):

    mc.postToChat("The Diamond is " + str(int(distanceBetweenPoints(randomBlockPos, mc.player.getPos()))) + " Blocks Away!")
    
    distanceFromBlock = int(distanceBetweenPoints(randomBlockPos, mc.player.getPos()))
    if distanceFromBlock < 2:
        seeking = False
    time.sleep(3)

    if time.time() - timeStarted > 30:
        createBeacon(randomBlockPos)


timeTaken = time.time() - timeStarted
mc.postToChat("Well done - " + str(int(timeTaken)) + " seconds to find the Diamond")
time.sleep(5)
mc.postToChat("Good game!")
mc.setBlock(randomBlockPos.x, randomBlockPos.y, randomBlockPos.z, block.AIR)
removeBeacon(randomBlockPos)
