import main
import agent
import agentLearn as agLer

#to easily convert between the two different ways that piles are often referred to
def pileConverter(up, down, whatPile):

    pile = 0

    if up == 1:
        pile = whatPile + 1
    if down == 1:
        pile = whatPile + 3

    return pile

#Decides if the agent wants to reserve a pile, and then does so
def reservePileAnnouncement(upPiles, downPiles, agentHand, drawpile):

    offLimitsPile = 0
    numberOfPlayableCards = 0
    goodPlayableCards = 0
    counted = 0
    goodUpCards = []
    goodDownCards = []
    appendedUp = 0
    appendedDown = 0

    #determines how many playable cards, and how many good cards the agent is holding
    for i in range(len(agentHand)):
        counted = 0
        appendedUp = 0
        appendedDown = 0
        for j in range(len(upPiles)):
            if (agentHand[i] > upPiles[j] or agentHand[i] < downPiles[j] or agentHand[i] == upPiles[j]-10 or agentHand[i] == downPiles[j]+10) and counted == 0:
                numberOfPlayableCards += 1
                counted = 1

            if ((agentHand[i] > upPiles[j] and 0 <= agentHand[i] - upPiles[j] <= 10)  or agentHand[i] == upPiles[j]-10) and appendedUp ==0:
                goodUpCards.append(agentHand[i])
                appendedUp = 1

            if ((agentHand[len(agentHand) - i - 1] < downPiles[j] and 0 <= downPiles[j] - agentHand[len(agentHand) - i - 1] <= 10) or agentHand[len(agentHand) - i - 1] == downPiles[j]+10) and appendedDown == 0:
                goodDownCards.append(agentHand[len(agentHand) - i - 1])
                appendedDown = 1

            if appendedUp == 1 and appendedDown == 1:
                break

    result= list(set(goodUpCards) | set(goodDownCards))
    result.sort()
    goodPlayableCards = len(result)
    
    bestCardIndex, jump, oppositeDirection, up, down, whatPile  = agent.DetermineBestCard(upPiles, downPiles, agentHand)
    offLimitsPile = pileConverter(up, down, whatPile)

    #the reserve pile announement is made
    if (oppositeDirection == 1 and goodPlayableCards >= 5) or (numberOfPlayableCards <= 5 and goodPlayableCards == 4):
        print(main.Colors.CRED +'AGENT: It would be nice if you could leave pile', offLimitsPile, 'alone' + main.Colors.CEND)
        print('AGENT: It would be nice if you could leave pile', offLimitsPile, 'alone', file=open('output.txt', 'a'))
        print('AGENT: It would be nice if you could leave pile', offLimitsPile, 'alone', file=open('simple_output.txt', 'a'))

    if (oppositeDirection == 1 and (goodPlayableCards == 3 or goodPlayableCards == 4)) or (numberOfPlayableCards <= 4 and goodPlayableCards == 3):
        print(main.Colors.CRED + 'AGENT: Please do not play on pile', offLimitsPile, '' + main.Colors.CEND)
        print('AGENT: Please do not play on pile', offLimitsPile, '', file=open('output.txt', 'a'))
        print('AGENT: Please do not play on pile', offLimitsPile, '', file=open('simple_output.txt', 'a'))

    if (oppositeDirection == 1 and goodPlayableCards <= 2) or (numberOfPlayableCards <= 3 and goodPlayableCards == 2):
        print(main.Colors.CRED + 'AGENT: You really should not play on pile', offLimitsPile, '' + main.Colors.CEND)
        print('AGENT: You really should not play on pile', offLimitsPile, '',  file=open('output.txt', 'a'))
        print('AGENT: You really should not play on pile', offLimitsPile, '',  file=open('simple_output.txt', 'a'))
    
    if (numberOfPlayableCards <= 2 and goodPlayableCards <= 1):
        print(main.Colors.CRED + 'AGENT: If you play on pile', offLimitsPile, 'everything will go really wrong' + main.Colors.CEND)
        print('AGENT: If you play on pile', offLimitsPile, 'everything will go really wrong', file=open('output.txt', 'a'))
        print('AGENT: If you play on pile', offLimitsPile, 'everything will go really wrong', file=open('simple_output.txt', 'a'))

    return numberOfPlayableCards


#Decides if the agent wants to announce a big jump, and then does so
def ruinPileAnnouncement(upPiles, downPiles, agentHand, drawpile):
    
    mustplay = main.MustPlay(drawpile)
    cardInfo = []
    cardValue = []
    previousPilevalue = []

    #checks if any of the cards the agent has to play in their next turn would cause a big jump
    for i in range(mustplay):
        bestCardIndex, jump, oppositeDirection, up, down, whatPile  = agent.DetermineBestCard(upPiles, downPiles, agentHand)
        if up == 1:
            pile = whatPile + 1
            previousPilevalue.append(upPiles[whatPile])
            upPiles[whatPile] = agentHand[bestCardIndex]
        if down == 1:
            pile = whatPile + 3
            previousPilevalue.append(downPiles[whatPile])
            downPiles[whatPile] = agentHand[bestCardIndex]
        cardInfo.append([jump, pile])
        cardValue.append(agentHand.pop(bestCardIndex))

    maxJumpValue = agLer.getValue()

    #actually announces a big jump if applicable
    if mustplay == 2:
        if cardInfo[0][1] == cardInfo[1][1]:
            if cardInfo[0][0] >= maxJumpValue:
                print(main.Colors.CRED + 'AGENT: There will be a big jump on pile:', str(cardInfo[0][1]) + main.Colors.CEND)
                print('AGENT: There will be a big jump on pile:', str(cardInfo[0][1]), file=open('output.txt', 'a'))
                print('AGENT: There will be a big jump on pile:', str(cardInfo[0][1]), file=open('simple_output.txt', 'a'))
        else:
            for i in range(mustplay):
                if cardInfo[i][0] >= maxJumpValue:
                    print(main.Colors.CRED + 'AGENT: There will be a big jump on pile:', str(cardInfo[i][1]) + main.Colors.CEND)
                    print('AGENT: There will be a big jump on pile:', str(cardInfo[0][1]), file=open('output.txt', 'a'))
                    print('AGENT: There will be a big jump on pile:', str(cardInfo[0][1]), file=open('simple_output.txt', 'a'))
    else:
        if cardInfo[0][0] >= maxJumpValue:
            print(main.Colors.CRED + 'AGENT: There will be a big jump on pile:', str(cardInfo[0][1]) + main.Colors.CEND)
            print('AGENT: There will be a big jump on pile:', str(cardInfo[0][1]), file=open('output.txt', 'a'))  
            print('AGENT: There will be a big jump on pile:', str(cardInfo[0][1]), file=open('simple_output.txt', 'a'))   

    #returns the agents hand to normal
    for i in range(mustplay):
        agentHand.append(cardValue.pop())
        if cardInfo[mustplay - i - 1][1] == 1 or cardInfo[mustplay - i - 1][1] == 2:
            upPiles[cardInfo[mustplay - i - 1][1] - 1] = previousPilevalue[mustplay - i - 1]
        if cardInfo[mustplay - i - 1][1] == 3 or cardInfo[mustplay - i- 1][1] == 4:
            downPiles[cardInfo[mustplay - i - 1][1] - 3] = previousPilevalue[mustplay - i - 1]
    agentHand.sort()

    return

#initiates all communication from the agent
def communicate(upPiles, downPiles, agentHand, drawpile):

    canGo = main.StopGame(agentHand, upPiles, downPiles)
    mustplay = main.MustPlay(drawpile)

    if canGo == 'yes':
        numberOfPlayableCards = reservePileAnnouncement(upPiles, downPiles, agentHand, drawpile)
        if numberOfPlayableCards >= mustplay:
            ruinPileAnnouncement(upPiles, downPiles, agentHand, drawpile)

    return


