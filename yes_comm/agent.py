import main
import agentLearn as agLer


#This function says something about the starting hand of the agent and if they are holding good cards to start with
def GoFirst(agentHand):

    #For the smallest jump we only have to look at the two highest and lowest cards the agent is holding in three configurations, since one of those three
    #options will always be the optimal cards to play at the start.
    smallestJump = (agentHand[0]-1) + (100 - agentHand[6])
    if smallestJump > (agentHand[1]-1):
        smallestJump = agentHand[1]-1
    if smallestJump > (100-agentHand[5]):
        smallestJump = 100-agentHand[5]

    if smallestJump < 15:
        print(main.Colors.CRED + 'AGENT: I have good cards to start with' + main.Colors.CEND)
        print('AGENT: I have good cards to start with', file=open('output.txt', 'a'))
    if 15 < smallestJump < 25:
        print(main.Colors.CRED + 'AGENT: I have mediocre cards to start with' + main.Colors.CEND)
        print('AGENT: I have mediocre cards to start with', file=open('output.txt', 'a'))
    if smallestJump > 25:
        print(main.Colors.CRED + 'AGENT: I have bad cards to start with' + main.Colors.CEND)
        print('AGENT: I have bad cards to start with', file=open('output.txt', 'a'))

    return

#Checks to see if the agent is holding an jump of 10 within its own hand and notes down the indexes of applicable cards
def InternaTenJump(agentHand):

    tenJumpIndex = []

    for i in range(len(agentHand)):
        for j in range(len(agentHand)):
            if agentHand[j] - agentHand[i] == 10:
                tenJumpIndex.append([i,j])
            elif agentHand[j] - agentHand[i] > 10:
                break

    return tenJumpIndex


#determines the best card by first checking if there is a card that can go in the 'opposite' direction, and then checking which card makes the smallest jump
def DetermineBestCard(upPiles, downPiles, agentHand):
    bestCardIndex = 0
    jump = 100
    oppositeDirection = 0
    up = 0
    down = 0
    whatPile = 0

    #loop through all cards in hand
    for j in range(len(agentHand)):
        #loop through the up/down piles
        for k in range(len(upPiles)):
            #check if a card in the opposite direction can be played onto an up-pile
            if upPiles[k] - 10 == agentHand[j]:
                bestCardIndex = j
                oppositeDirection = 1
                up = 1
                down = 0
                whatPile = k
                jump = 0
                break
            #check if a card in the opposite direction can be played onto a down-pile
            if downPiles[k] + 10 == agentHand[j]:
                bestCardIndex = j
                oppositeDirection = 1
                down = 1
                up = 0
                whatPile = k
                jump = 0
                break
            #check optimal card to play on up-piles
            if agentHand[j] - upPiles[k] < jump and agentHand[j] - upPiles[k] > 0:
                bestCardIndex = j
                jump = agentHand[j] - upPiles[k]
                up = 1
                down = 0
                whatPile = k
            #check optimal card to play on down-piles
            if downPiles[k] - agentHand[j] < jump and downPiles[k] - agentHand[j] > 0:
                bestCardIndex = j
                jump = downPiles[k] - agentHand[j]
                up = 0
                down = 1
                whatPile = k
        if oppositeDirection == 1:
            break

    return bestCardIndex, jump, oppositeDirection, up, down, whatPile

#This function determines what card the agent will play if the human reserved a pile
def PlayWithReservedPile(pile, howToSay, upPiles, downPiles, agentHand):

    up = 0
    down = 0
    bestCardIndex = 0
    whatPileToPlay = 0
    normal = 0

    #First it looks at the best card the agent is holding in general
    normalBestCardIndex, normalJump, normalOppositeDirection, normalUp, normalDown, normalWhatPileToPlay  = DetermineBestCard(upPiles, downPiles, agentHand)

    #It checks if that card gets played into the opposite direction. If it does not, the pile that the human reserved is made unavailable
    if normalOppositeDirection != 1:
        if (pile == 1 or pile == 2):
            whatPile = pile - 1
            reservedPileValue = upPiles[whatPile]
            upPiles[whatPile] = 1000
        if (pile == 3 or pile == 4):
            whatPile = pile - 3
            reservedPileValue = downPiles[whatPile]
            downPiles[whatPile] = -100

        #check to see if the agent can still play without the reserved pile
        canGo = main.StopGame(agentHand, upPiles, downPiles)

        #The best card the agent can play onto a non-reserved pile is determined
        if canGo == 'yes':
            bestCardIndex, jump, oppositeDirection, up, down, whatPileToPlay  = DetermineBestCard(upPiles, downPiles, agentHand)

        if (pile == 1 or pile == 2):
                upPiles[whatPile] = reservedPileValue
        if (pile == 3 or pile == 4):
                downPiles[whatPile] = reservedPileValue

        #If the agent has to play onto the reserved pile, it will do so
        if canGo == 'no':
            bestCardIndex, jump, oppositeDirection, up, down, whatPileToPlay  = DetermineBestCard(upPiles, downPiles, agentHand)

        #Depending on what statement the human made, the agent decides here to honor the reserved pile or play their card there anyways.
        if howToSay == '1':
            if jump - normalJump >= 10:
                normal = 1
        if howToSay == '2':
            if jump - normalJump >= 20:
                normal = 1
        if howToSay == '3':
            if jump - normalJump >= 30:
                normal = 1

    #This sets in stone what card will actually be played
    if normal == 1 or normalOppositeDirection == 1:
        bestCardIndex = normalBestCardIndex
        jump = normalJump
        oppositeDirection = normalOppositeDirection
        up = normalUp
        down = normalDown
        whatPileToPlay = normalWhatPileToPlay

    return bestCardIndex, jump, oppositeDirection, up, down, whatPileToPlay


#if the human announced a big jump, this handles that
def PlayWithRuinPile(startingPileValue, agentHand, upPiles, downPiles, whatPile, up, down):

    maxJumpValue = agLer.getValue()

    for i in range(len(agentHand)):
        if up == 1 and (upPiles[whatPile] - agentHand[i] == 10 or 0 < agentHand[i] - startingPileValue < maxJumpValue or startingPileValue > agentHand[i] > upPiles[whatPile]):
            upPiles[whatPile] = agentHand[i]
            agentHand.pop(i)
            agentHand, upPiles, downPiles = PlayWithRuinPile(startingPileValue, agentHand, upPiles, downPiles, whatPile, up, down)
            break
        if down == 1 and (agentHand[len(agentHand) - i - 1] - downPiles[whatPile] == 10 or 0 < startingPileValue - agentHand[len(agentHand) - i - 1] < maxJumpValue or startingPileValue < agentHand[len(agentHand)-i-1] < downPiles[whatPile]):
            downPiles[whatPile] = agentHand[len(agentHand) - i - 1]
            agentHand.pop(len(agentHand) - i - 1)
            agentHand, upPiles, downPiles = PlayWithRuinPile(startingPileValue, agentHand, upPiles, downPiles, whatPile, up, down)
            break

    return agentHand, upPiles, downPiles


#This function plays the  best card(s) the agent has
def PlayCard(upPiles, downPiles, agentHand, drawpile, whatTypeOfSay, pile, howToSay, turns, handledRuinedPile):

    lenHand = len(agentHand)

    #if human annouced they will ruin a pile
    if whatTypeOfSay == '2' and turns == 0 and handledRuinedPile == 0:
        up = 0
        down = 0
        handledRuinedPile = 1
        if whatTypeOfSay == '2':
            if (pile == 1 or pile == 2):
                up = 1
                whatPile = pile - 1
                startingPileValue = upPiles[whatPile]
            if (pile == 3 or pile == 4):
                down = 1
                whatPile = pile - 3
                startingPileValue = downPiles[whatPile]

        agLer.ruinLearn('agent', pile, upPiles, downPiles)
        agentHand, upPiles, downPiles = PlayWithRuinPile(startingPileValue, agentHand, upPiles, downPiles, whatPile, up, down)

    #if the human reserved a pile
    elif lenHand == len(agentHand):
        if whatTypeOfSay == '1':
            bestCardIndex, jump, oppositeDirection, up, down, whatPile = PlayWithReservedPile(pile, howToSay, upPiles, downPiles, agentHand)
        else:
            bestCardIndex, jump, oppositeDirection, up, down, whatPile  = DetermineBestCard(upPiles, downPiles, agentHand)

        #if the human holds an internal 10 jump
        tenJumpIndex = InternaTenJump(agentHand)
        playInternalTen = 0
        jumpIndex = [bestCardIndex]

        for i in range(len(tenJumpIndex)):
            if up == 1 and (bestCardIndex == tenJumpIndex[i][0] or jumpIndex == tenJumpIndex[i][0]):
                playInternalTen = 1
                jumpIndex = tenJumpIndex[i][1]
            if down == 1 and (bestCardIndex == tenJumpIndex[(len(tenJumpIndex) - i - 1)][1] or jumpIndex == tenJumpIndex[(len(tenJumpIndex) - i) -1][1]):
                playInternalTen = 1
                jumpIndex = tenJumpIndex[(len(tenJumpIndex) - i - 1)][0]

        if playInternalTen == 1 and up == 1:
            cardsToPlay = jumpIndex - bestCardIndex + 1
            upPiles[whatPile] = agentHand[bestCardIndex]
            for i in range(cardsToPlay):
                agentHand.pop(bestCardIndex)

        if playInternalTen == 1 and down == 1:
            cardsToPlay = bestCardIndex - jumpIndex + 1
            downPiles[whatPile] = agentHand[bestCardIndex]
            for i in range(cardsToPlay):
                agentHand.pop(jumpIndex)

        #otherwise just plays the best card the agent is holding
        if playInternalTen == 0:
            if up == 1:
                upPiles[whatPile] = agentHand[bestCardIndex]
                agentHand.pop(bestCardIndex)
            elif down == 1:
                downPiles[whatPile] = agentHand[bestCardIndex]
                agentHand.pop(bestCardIndex)

    return upPiles, downPiles, agentHand, drawpile, handledRuinedPile
