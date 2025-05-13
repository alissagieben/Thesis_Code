
startingPileValue = 0
pileAfterAgentTurn = 0
ruinJumpValue = [30]

#learning function for when a ruined pile was announced, so the agent adjusts its future expectations
def ruinLearn(who, pile, upPiles, downPiles):

    global startingPileValue
    global ruinJumpValue
    global pileAfterAgentTurn

    if who == 'agent':
        if pile == 1 or pile == 2:
            startingPileValue = upPiles[pile-1]
        if pile == 3 or pile == 4:
            startingPileValue = downPiles[pile-3]

    if who == 'agent2':
        if pile == 1 or pile == 2:
            pileAfterAgentTurn = upPiles[pile-1]
        if pile == 3 or pile == 4:
            pileAfterAgentTurn = downPiles[pile-3]
    
    if who =='human' :
        if pile == 1 or pile == 2:
            if upPiles[pile-1] == pileAfterAgentTurn:
                ruinJumpValue.append(upPiles[pile-1] - startingPileValue - 10)
            else:
                ruinJumpValue.append(upPiles[pile-1] - startingPileValue)
        if pile == 3 or pile == 4:
            if downPiles[pile-3] == pileAfterAgentTurn:
                ruinJumpValue.append(startingPileValue - downPiles[pile-3] - 10)
            else:
                ruinJumpValue.append(startingPileValue - downPiles[pile-3])

    return


def returnLearn():

    return

#returns the requested value
def getValue():

    global ruinJumpValue

    value = int(sum(ruinJumpValue) / len(ruinJumpValue))

    return value


