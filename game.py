import os.path, random

rollCount = 1
dice = []
locks = [False, False, False, False, False]

def ws(count=20):
    for i in range(count):
        print("\n")

def init():
    global highscore, score, rollCount, dice, locks
    highscore = 0
    # take from persistent.txt
    global score
    score = 0
    rollCount = 1
    dice = []
    locks = [False, False, False, False, False]

def updateScore():
    score = 0
    for i in scoreArray:
        if isinstance(i, int):
            score += i
    return score

def askName():
    # not yet implemented
    global name
    name = str(input("Enter your name. If you have played before, enter the same name as last time.  "))
    namePath = "gamedata/players/" + name + ".txt"
    if os.path.exists(namePath):
        # import variables like their highscore
        pass
    elif name != "playerdata":
        while True:
            res = str(input("Creating new file under filename {}. Is this okay? y/n  ".format(name)))
            if res.lower() == 'y':
                createFile = open("gamedata/players/{}.txt".format(name), 'x')
                createFile.write("{}\n0")
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

scoreCategories = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes", "Full House", "Small Straight", "Large Straight", "Free Space", "Three of a Kind", "Four of a Kind", "Five of a Kind"]
scoreArray = ["", "", "", "", "", "", "", "", "", "", "", "", ""]

def pageSelector():
    global dice
    ws()
    printPointer = 0
    printArray = [(0, 6), (6, 10), (10, 13)]
    while True:
        printPointer = printPointer % 3
        ws()
        print("Current score: {}".format(updateScore()))
        print("Page {}/3 \t Press enter to go to the next page, or a [number] to score your turn.".format(printPointer+1))
        i = 0
        for i in range(printArray[printPointer][0], printArray[printPointer][1]):
            pageScorerIdx = 1 + i - printArray[printPointer][0]
            if isinstance(scoreArray[i], int):
                scoreStatus = ("Scored {} points".format(scoreArray[i]))
            else:
                scoreStatus = ("Open, worth {} points".format(checkScore(i+1)))
            print("[{}] - {}:\t\t{}".format(pageScorerIdx, scoreCategories[i], scoreStatus))
        print("Current dice: \n {} {} {} {} {}".format(*dice))
        inputChr = ''
        inputChr = input()
        if inputChr.lower() == '':
            printPointer += 1
        if inputChr.lower() == 'd':
            turnLoop()
            return True
        if inputChr.isnumeric():
            inputIdx = printArray[printPointer][0] + int(inputChr) - 1
            if procScore(inputIdx):
                return True
        else:
            print("")

def procScore(cat):
    if scoreArray[cat] != '':
        ws()
        print("Category already scored. Press enter to continue.")
        input()
        return False
    else:
        scoreArray[cat] = checkScore(cat)
        ws()
        print("Scored {} points.".format(scoreArray[cat]))
        input("Press enter to begin next turn.")
        prepTurnLoop()
        return True

def prepTurnLoop():
    global rollCount, dice, locks
    rollCount = 1
    dice = []
    locks = [False, False, False, False, False]
    turnLoop()
    return True

def turnLoop():
    if scoreArray.count("") == 0:
        gameOver()
        return True
    global rollCount, dice, locks
    while True:
        if rollCount == 1:
            ordn = "First"
        elif rollCount == 2:
            ordn = "Second"
        elif rollCount == 3:
            ordn = "Last"

        dice = rollDice()

        def printstatus():
            ws()
            print("Score: {}\n".format(updateScore()))
            print("Turn {}.".format(14 - scoreArray.count("")))
            print("{} roll.\n".format(ordn))
            print(*dice)
            print(*formatLocks())
            print(*lockKeyBinds)

        printstatus()

        while True:
            c = ''
            c = input().upper()
            if c == lockKeyBinds[0]:
                locks[0] = not(bool(locks[0]))
            elif c == lockKeyBinds[1]:
                locks[1] = not(bool(locks[1]))
            elif c == lockKeyBinds[2]:
                locks[2] = not(bool(locks[2]))
            elif c == lockKeyBinds[3]:
                locks[3] = not(bool(locks[3]))
            elif c == lockKeyBinds[4]:
                locks[4] = not(bool(locks[4]))
            elif c == '':
                break
            elif c == 'S':
                pageSelector()
                return True
            printstatus()
        if rollCount == 3:
            ws()
            dice = sorted(dice)
            print("Out of rolls.")
            print("Dice: {} {} {} {} {}\n".format(*dice))
            input("Press enter to go to the scoring page.")
            pageSelector()
            return True
        rollCount += 1

def rollDice():
    global rollCount
    if rollCount == 1:
        for i in range(0, 5):
            dice.append(random.randrange(1, 7))
    else:
        for i in range(0, 5):
            if locks[i] == False:
                dice[i] = random.randrange(1, 7)
    return dice

def checkScore(cat):
    global dice
    cat += 1 # not good practice but keeps cats 1~6 equal to target number
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
        diceCopy1 = dice
        if (diceCopy1[0] == diceCopy1[1] == diceCopy1[2] and diceCopy1[3] == diceCopy1[4]) or (diceCopy1[0] == diceCopy1[1] and diceCopy1[2] == diceCopy1[3] == diceCopy1[4]):
            return 25
        return 0
    elif cat == 8:
        diceCopy2 = list(dict.fromkeys(dice))
        if len(diceCopy2) >= 4:
            if (diceCopy2[0] + 3 == diceCopy2[1] + 2 == diceCopy2[2] + 1 == diceCopy2[3]) or diceCopy2[1] + 3 == diceCopy2[2] + 2 == diceCopy2[3] + 1 == diceCopy2[4]:
                return 30
        return 0
    elif cat == 9:
        diceCopy3 = list(dict.fromkeys(dice))
        if len(diceCopy3) >= 5:
            if (diceCopy3[0] + 4 == diceCopy3[1] + 3 == diceCopy3[2] + 2 == diceCopy3[3] + 1 == diceCopy3[4]):
                return 40
        return 0
    elif cat == 10:
        return sum(dice)
    elif cat == 11:
        for i in range(1, 7):
            if dice.count(i) >= 3:
                return sum(dice)
        return 0
    elif cat == 12:
        for i in range(1, 7):
            if dice.count(i) >= 4:
                return (sum(dice) + 10)
        return 0
    elif cat == 13:
        for i in range(1, 7):
            if dice.count(i) >= 5:
                return (sum(dice) + 50)
        return 0

def gameOver():
    global score, highscore
    ws()
    print("Game over! All categories have been scored.")
    print("Your final score was {}.".format(score))
    print("Your high score: {}.".format(highscore))
    # if score > personalHigh:
    #     new personal hs
    # else:
    #     you were x points off your hs
    # repeat for global hs

def newGame():
    # askName()
    init()
    prepTurnLoop()

ws()
prepTurnLoop()

# askName()
# dont bother calling that yet
