# Mars Lander Source Code.
import math
import random

GRAVITY = 100 
# The rate in which the spaceship descents in free fall (in ten seconds)

version = "1.2" # The Version of the program

# various end-of-game messages.
dead = "\nThere were no survivors.\n\n"
crashed = "\nThe Spaceship crashed. Good luck getting back home.\n\n"
success = "\nYou made it! Good job!\n\n"
emptyfuel = "\nThere is no fuel left. You're floating around like Wheatley.\n\n"

def randomheight():
    # start from a random altitude
    max = 20000
    min = 10000
    r = math.floor(random.random() * (max - min)) + min
    return (r % 15000 + 4000)


def gameHeader():
    s = ""
    s = s + "\nMars Lander - Version " + version + "\n"
    s = s + "This is a computer simulation of an Apollo Mars landing capsule.\n"
    s = s + "The on-board computer has failed so you have to land the capsule manually.\n"
    s = s + "Set burn rate of retro rockets to any value between 0 (free fall) and 200\n"
    s = s + "(maximum burn) kilo per second. Set burn rate every 10 seconds.\n" 
    # /* That's why we have to go with 10 second-steps. */
    s = s + "You must land at a speed of 2 or 1. Good Luck!\n\n"
    return s


def getHeader():
    s = ""
    s = s + "\nTime\t"
    s = s + "Speed\t\t"
    s = s + "Fuel\t\t"
    s = s + "Height\t\t"
    s = s + "Burn\n"
    s = s + "----\t"
    s = s + "-----\t\t"
    s = s + "----\t\t"
    s = s + "------\t\t"
    s = s + "----\n"
    return s



def computeDeltaV(vehicle):
    return (vehicle['Speed'] + GRAVITY - vehicle['Burn'])


def checkStatus(vehicle):
    s = ""
    if (vehicle['Height'] <= 0):
        if (vehicle['Speed'] > 10):
            s = dead
        
        if (vehicle['Speed'] < 10 and vehicle['Speed'] > 3):
            s = crashed
        
        if (vehicle['Speed'] < 3):
            s = success
    else:
        if (vehicle['Height'] > 0):
            s = emptyfuel
        
    
    return s


def adjustForBurn(vehicle):
    # save previousHeight
    vehicle['PrevHeight'] = vehicle['Height']
    # compute new velocity
    vehicle['Speed'] = computeDeltaV(vehicle)
    # compute new height of vehicle
    vehicle['Height'] = vehicle['Height'] - vehicle['Speed']
    # subtract fuel used from tank
    vehicle['Fuel'] = vehicle['Fuel'] - vehicle['Burn']


def stillFlying():
    return (vehicle['Height'] > 0)


def outOfFuel(vehicle):
    return (vehicle['Fuel'] <= 0)


def getStatus(vehicle):
    # create a string with the vehicle status on it.
    s = ""
    s = str(vehicle['Tensec']) + "0 \t\t" + str(vehicle['Speed']) \
        + " \t\t" + str(vehicle['Fuel']) + " \t\t" + str(vehicle['Height'])
    return s


def printString(string):
    # print long strings with new lines the them.
    # a = string.split(/\r?\n/)
    #for (i = 0 i < a.length i++):
    #    print(a[i])
    print(string)
    


# this is initial vehicle setup
vehicle = {
    'Height': 8000,
    'Speed': 1000,
    'Fuel': 12000,
    'Tensec': 0,
    'Burn': 0,
    'PrevHeight': 8000,
    'Step': 1,
}


# main game loop
def runGame(burns):
    status = ""

    # Set initial vehicle parameters
    h = randomheight()
    vehicle['Height'] = h
    vehicle['PrevHeight'] = h

    burnIdx = 0

    printString(gameHeader())
    printString(getHeader())

    while (stillFlying() == True):
        status = getStatus(vehicle)
        vehicle['Burn'] = burns[burnIdx]
        printString(status + "\t\t" + str(vehicle['Burn']))
        adjustForBurn(vehicle)
        if (outOfFuel(vehicle) == True):
            break
        
        vehicle['Tensec'] += 1
        burnIdx += 1


    
    status = checkStatus(vehicle)
    printString(status)


# these are the series of burns made each 10 secs by the lander.
# change them to see if you can get the lander to make a soft landing.
# burns are between 0 and 200. This burn array usually crashes.
burnArray = [100, 100, 200, 200, 100, 100, 0, 0, 200, 100, 100, 0, 0, 0, 0]

runGame(burnArray)
