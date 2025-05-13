
#Checks to see if the agent is holding a jump of 10 and notes down the indexes of those cards if so
def InternaTenJump(agentHand):

    tenJumpIndex = []
    
    for i in range(len(agentHand)):
        for j in range(len(agentHand)):
            if agentHand[j] - agentHand[i] == 10:
                tenJumpIndex.append([i,j])
            elif agentHand[j] - agentHand[i] > 10:
                break

    return tenJumpIndex

#determines the best card by first checking if there is a card that can go in the 'opposite' direction, and thne checking which card makes the smallest jump
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
            #check optimal card to play onto the up-piles
            if agentHand[j] - upPiles[k] < jump and agentHand[j] - upPiles[k] > 0:
                bestCardIndex = j
                jump = agentHand[j] - upPiles[k]
                up = 1
                down = 0
                whatPile = k
            #check optimal card to play onto the down-piles
            if downPiles[k] - agentHand[j] < jump and downPiles[k] - agentHand[j] > 0:
                bestCardIndex = j
                jump = downPiles[k] - agentHand[j]
                up = 0
                down = 1 
                whatPile = k
        if oppositeDirection == 1:
            break

    return bestCardIndex, jump, oppositeDirection, up, down, whatPile


#This function plays the  best card(s) the agent has
def PlayCard(upPiles, downPiles, agentHand, drawpile):
    
    #Determines the best card the human can play
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

    #plays the best card the agent is holding
    if playInternalTen == 0:
        if up == 1:
            upPiles[whatPile] = agentHand[bestCardIndex]
            agentHand.pop(bestCardIndex)
        elif down == 1:
            downPiles[whatPile] = agentHand[bestCardIndex]
            agentHand.pop(bestCardIndex)

    return upPiles, downPiles, agentHand, drawpile
