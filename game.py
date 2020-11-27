# ur code loser
import os.path, random

def init():
    global highscore
    highscore = 0 
    global score
    score = 0
    # take data from persistent.txt

def askName():
    global name
    name = str(input("Enter your name. If you have played before, enter the same name as last time.  "))
    namePath = "gamedata/players/" + name + ".txt"
    if os.path.exists(namePath):
        # import variables like their highscore
        pass
    else:
        while True:
            res = str(input("Creating new file under filename {}. Is this okay? y/n  ".format(name)))
            if res.lower() == 'y':
                createFile = open("gamedata/players/{}.txt".format(name), 'x')
                createFile.write(name)
                createFile.write('\n')
                createFile.write('0')
                createFile.close()
                break
            if res.lower() == 'n':
                print("Aborted.")
                exit()

def formatLocks():
    fl = []
    for i in range(0, 5):
        if locks[i]: #locked
            fl.append("X")
        else:
            fl.append(" ")
    return fl

dice = []
locks = [False, False, False, False, False]
lockKeyBinds = ['Y', 'U', 'I', 'O', 'P']

def rollDice(rollCount):
    if rollCount == 1:
        for i in range(0, 5):
            dice.append(random.randrange(1, 7))
    else:
        for i in range(0, 5):
            if locks[i] == False:
                dice[i] = random.randrange(1, 7)
    return(dice)

def turnScore(dice, cat):
    cat = cat - 1
    if cat == 1:
        return dice.count(1) * 1
    elif cat == 2:
        return dice.count(2) * 2
    elif cat == 3:
        return dice.count(3) * 3
    elif cat == 4:
        return dice.count(4) * 4
    elif cat == 5:
        return dice.count(5) * 5
    elif cat == 6:
        return dice.count(6) * 6
    elif cat == 7:
        dice.sort()
        if (dice[0] == dice[1] == dice[2] and dice[3] == dice[4]) or (dice[0] == dice[1] and dice[2] == dice[3] == dice[4]):
            return 25
        return 0
    elif cat == 8:
        dice.sort()
        dice = list(dict.fromkeys(dice))
        if (dice[0] + 3 == dice[1] + 2 == dice[2] + 1 == dice[3]) or dice[1] + 3 == dice[2] + 2 == dice[3] + 1 == dice[4]:
            return 30
        return 0
    elif cat == 9:
        dice.sort()
        dice = list(dict.fromkeys(dice))
        if (dice[0] + 4 == dice[1] + 3 == dice[2] + 2 == dice[3] + 1 == dice[4]):
            return 40
        return 0
    elif cat == 10:
        return sum(dice)
    elif cat == 11:
        for i in range(1, 6):
            if dice.count(i) >= 3:
                return sum(dice)
        return 0
    elif cat == 12:
        for i in range(1, 6):
            if dice.count(i) >= 4:
                return (sum(dice) + 10)
        return 0
    elif cat == 13:
        for i in range(1, 6):
            if dice.count(i) >= 5:
                return (sum(dice) + 50)
        return 0
    #should be able to return theoretical score of a turn

scoreCategories = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes", "Full House", "Small Straight", "Large Straight", "Free Space", "Three of a Kind", "Four of a Kind", "Five of a Kind"]
scoreArray = ["", "", "", "", "", "", "", "", "", "", "", "", ""]
# scoreStatus = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #could become codes for what to display, subarrays of the scored dice, strs, etc.

def pageSelector():
    printPointer = 0
    printArray = [(0, 6), (7, 10), (10, 13)]
    while True:
        printPointer = printPointer % 3
        print("Page {}/3 \t Type \"n\" to go to next page, a [number] to score your turn, or \"r\" to enter dice mode.".format(printPointer+1))
        i = 0
        for i in range(printArray[printPointer][0], printArray[printPointer][1]):
            pageScorerIdx = 1 + i - printArray[printPointer][0]
            scoreStatus = scoreArray[i] or "Open"
            print("[{}] - {}:\t\t{}".format(pageScorerIdx, scoreCategories[i], scoreStatus))
        print("Current dice: \n {} {} {} {} {}".format(*dice))
        inputChr = ""
        inputChr = input()
        if inputChr.lower() == 'n':
            printPointer += 1
        if inputChr.lower() == 'r':
            # enter dice mode
            pass
        if inputChr.isnumeric():
            inputIdx = int(inputChr) - 1
            inputIdx += printArray[printPointer][0]
            return inputIdx

def checkGameOver():
    if scoreArray.count("") == 0:
        #game over
        pass

def turnLoop():
    global dice, locks
    rollCount = 1
    dice = []
    locks = [False, False, False, False, False]
    if rollCount == 1:
        ordn = "First"
    elif rollCount == 2:
        ordn = "Second"
    elif rollCount == 3:
        ordn = "Last"

    while True:
        dice = rollDice(rollCount)
        def printstatus():
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print("Turn {}.".format(14 - scoreArray.count("")))
            print("{} roll.".format(ordn))
            print(*dice)
            print(*formatLocks())
            print(*lockKeyBinds)
        printstatus()
        while True:
            c = ''
            c = input()
            if c == 'y':
                locks[0] = not(bool(locks[0]))
                printstatus()
            elif c == 'u':
                locks[1] = not(bool(locks[1]))
                printstatus()
            elif c == 'i':
                locks[2] = not(bool(locks[2]))
                printstatus()
            elif c == 'o':
                locks[3] = not(bool(locks[3]))
                printstatus()
            elif c == 'p':
                locks[4] = not(bool(locks[4]))
                printstatus()
            elif c == '':
                break
        rollCount += 1

print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
turnLoop()


# askName()
# dont bother calling that yet