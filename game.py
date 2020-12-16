import os.path, random, json, highscoresave

name = ""
highscore = 0
personalHigh = 0
score = 0
rollCount = 1
dice = []
locks = [False, False, False, False, False]

def ws(count=20):
    for i in range(count):
        print("\n")
    return True

def init():
    global highscore, personalHigh, score, rollCount, dice, locks
    highscore = highscoresave.hs
    # personalHigh = getPersonalHigh?
    score = 0
    rollCount = 1
    dice = []
    locks = [False, False, False, False, False]
    return True

def updateScore():
    score = 0
    for i in scoreArray:
        if isinstance(i, int):
            score += i
    return score

def primGameIntro():
    global name
    # need a full version of this once name input is ready!
    print("Dice Matching Game")
    print("High Score: {}".format(highscore))
    name = input("Enter your name:    ")

def askName():
    # not yet implemented
    # THIS SHOULD ALL BE DONE AS JSON!!! dont bother with writing files theyre way too complicated
    # if thats possible idk, ill look into it
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
                scoreStatus = ("Open, worth {} points".format(checkScore(i)))
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
        if scoreArray.count("") == 0:
            input("Press enter to see results.")
            gameOver()
            return True
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
    global rollCount, dice, locks
    while True:

        dice = rollDice()

        def printstatus():
            ws()
            print("Score: {}\n".format(updateScore()))
            print("Turn {}.".format(14 - scoreArray.count("")))
            print("Rolls remaining: {}\n".format(3 - rollCount))
            print(*dice)
            print(*formatLocks())
            print(*lockKeyBinds)

        printstatus()

        while True:
            if rollCount == 3:
                ws()
                dice = sorted(dice)
                print("Out of rolls.")
                print("Dice: {} {} {} {} {}\n".format(*dice))
                input("Press enter to go to the scoring page.")
                pageSelector()
                return True
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
                break
            printstatus()
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

def getResultMessage(val, mode):
    if mode == "score":
        if val > 400:
            return "What an amazing score!"
        elif val > 300:
            return "Awesome game!"
        elif val > 200:
            return "Great job!"
        elif val > 100:
            return "Good job!"
        elif val < 10:
            return "That's a really low score! Impressive!"
        else:
            return ""
    elif mode == "hs":
        if val > 100:
            return "You crushed the high score! Congratulations!"
        elif val > 50:
            return "You beat the high score by quite a bit, wow!"
        elif val > 10:
            return "You beat the high score!"
        elif val > 0:
            return "You just barely beat the high score!"
        elif val > -100:
            return "You were pretty far off the high score... Better luck next time!"
        elif val > -50:
            return "You were close to the high score! Try again!"
        elif val > -10:
            return "You almost beat the high score! One more shot!"
        else:
            return ""
    # elif mode == "phs":
    #   personal highscore mode

def gameOver():
    global score, highscore
    ws()
    print("Game over! All categories have been scored.\n")
    print("Your final score was {}.".format(score))
    print(getResultMessage(score, "score"))
    ws(1)
    print("The high score is {}.".format(highscore))
    print(getResultMessage((score - highscore), "hs"))
    if highscore < score:
        highscoresave.hs = score
    print("Thanks for playing!")
    ws(1)
    exit(score)
    # print("Your high score: {}.".format(personalHigh))
    # if score > personalHigh:
    #     new personal hs
    # else:
    #     you were x points off your hs
    # repeat for global hs

def newGame():
    ws()
    # askName()
    init()
    primGameIntro()
    prepTurnLoop()
 
newGame()

# askName()
# dont bother calling that yet
