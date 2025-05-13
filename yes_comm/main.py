
import random
import agent
import human
import human_Communication as huCom
import agentCommunication as agCom
import agentLearn as agLer
from time import time

#To color the text in the terminal
class Colors:
    CEND = '\033[0m'
    CRED = '\33[91m'
    CGREEN = '\33[92m'
    CYELLOW = '\33[93m'
    CBLUE = '\33[94m'
    CVIOLET = '\33[95m'

#Initiates the game by crating a draw pile, shuffeling that pile, and dealing seven cards to each player.
def StartGame():
    drawpile = [] 
    agentHand = []
    humanHand = []

    for i in range(98):
        drawpile.append(i+2)
    random.shuffle(drawpile)
    
    agentHand = DealCard(drawpile, agentHand)
    humanHand = DealCard(drawpile, humanHand)

    return drawpile, agentHand, humanHand


#Deals new cards
def DealCard(drawpile, hand):

    while len(hand) != 7:
        if len(drawpile) != 0:
            hand.append(drawpile.pop())
        else:
            print('The drawpile is empty')
            break
    hand.sort()
          
    return hand

#Determines how many cards need to be played
def MustPlay(drawpile):

    if len(drawpile) == 0:
        mustplay = 1
    else: 
        mustplay = 2

    return mustplay

#Players get to determine who goes first themselves. The starting turn is decided and passed on
def DetermineTurn(agentHand, humanHand):
    
    agent.GoFirst(agentHand)
    turn = human.GoFirst(humanHand)

    return turn


#This function checks if the game can still continue by checking if the current player still has any valid moves left to make
def StopGame(hand, upPiles, downPiles):

    canGo = 'no'

    for i in range(len(hand)):
        for j in range(len(upPiles)):
            if hand[i] > upPiles[j] or hand[i] < downPiles[j] or hand[i] == upPiles[j]-10 or hand[i] == downPiles[j]+10:
                canGo = 'yes'
                break

    return canGo

#This function calculates the final score by tallying up how many cards are left over at the end
def calculateFinalScore(drawpile, humanHand, agentHand):
    
    finalScore = len(drawpile) + len(humanHand) + len(agentHand)

    return finalScore


#Plays the game
def PlayGame(upPiles, downPiles, agentHand, humanHand, drawpile):
    turn = DetermineTurn(agentHand, humanHand)
    canGo = 'yes'
    humanCanGo = 'yes'
    agentCanGo = 'yes'
    whatTypeOfSay = 'bla'
    pile = 6
    howToSay = 'bla'

    #The game will loop through turns as long as the players can play
    while canGo != 'no':

        mustplay = MustPlay(drawpile)
        
        canGo = StopGame(agentHand, upPiles, downPiles)
        #The agents turn
        if turn == 'agent':
            print('\nplayer:', turn , file=open('output.txt', 'a'))
            print('player:', turn , file=open('simple_output.txt', 'a'))
            print('Agent hand before playing:', agentHand , file=open('output.txt', 'a'))
            lenHand = len(agentHand)
            turns = 0
            handledRuinedPile = 0
            
            #The agent plays its cards
            while turns < mustplay or jump <= 2 or (len(humanHand) == 0 and len(agentHand) != 0) or humanCanGo == 'no':
                go = StopGame(agentHand, upPiles, downPiles)
                if go == 'no' and turns < mustplay:
                    print(Colors.CRED+ 'The agent did not play enough cards. The game will end.' + Colors.CEND)
                    canGo = 'no'
                    break
                if go == 'no':
                    break
                else:
                    upPiles, downPiles, agentHand, drawpile, handledRuinedPile = agent.PlayCard(upPiles, downPiles, agentHand, drawpile, whatTypeOfSay, pile, howToSay, turns, handledRuinedPile)
                    turns = lenHand - len(agentHand)
                    if whatTypeOfSay == '1':
                        bestCardIndex, jump, oppositeDirection, up, down, whatPile = agent.PlayWithReservedPile(pile, howToSay, upPiles, downPiles, agentHand)
                    else:
                        bestCardIndex, jump, oppositeDirection, up, down, whatPile  = agent.DetermineBestCard(upPiles, downPiles, agentHand)

            #The state of the game after the agent played is written to the output files.
            print(Colors.CVIOLET + 'The agent has played its cards.' + Colors.CEND)
            print('\nAgent hand after playing:', agentHand , file=open('output.txt', 'a'))
            print('number of cards played:', turns, file=open('output.txt', 'a'))
            print('number of cards played:', turns, file=open('simple_output.txt', 'a'))
            print('Up piles after agent played:', upPiles, file=open('output.txt', 'a'))
            print('Down piles after agent played:', downPiles , file=open('output.txt', 'a'))

            turn = 'human'

        #The agent will learn if the human decided to announce a big jump
            agLer.ruinLearn('agent2', pile, upPiles, downPiles)
        
        #he agent is dealt new cards
        agentHand = DealCard(drawpile, agentHand)
        print('\nAgent hand after dealing', agentHand, file=open('output.txt', 'a'))
        
        #The agent can communicate with the human
        agCom.communicate(upPiles, downPiles, agentHand, drawpile)

        #If the agent has no playable cards left, the human is told that their next turn will be the last
        agentCanGo = StopGame(agentHand, upPiles, downPiles)
        if agentCanGo == 'no' and canGo != 'no':
            humanCanGo = StopGame(humanHand, upPiles, downPiles)
            if humanCanGo == 'no':
                canGo = 'no'
            else:
                print(Colors.CRED+ 'The agent cannot play any other cards. This is your final turn.' + Colors.CEND)

        mustplay = MustPlay(drawpile)

        if canGo != 'no':
            canGo = StopGame(humanHand, upPiles, downPiles)
        
        #The human plays their turn
        if turn == 'human' and canGo != 'no':
            print('\nplayer:', turn , file=open('output.txt', 'a'))
            print('player:', turn , file=open('simple_output.txt', 'a'))
            print('Human hand before playing:', humanHand , file=open('output.txt', 'a'))
            wantToPlay = 'y'
            turns = 0
            # the want to play variable is used to enable the human player to be able to play more than the required number of cards.
            while wantToPlay == 'y' or agentCanGo == 'no':
                go = StopGame(humanHand, upPiles, downPiles)    
                if go == 'no':
                    break
                else:
                    upPiles, downPiles, humanHand, drawpile = human.PlayCard(upPiles, downPiles, humanHand, drawpile)
                    turns += 1
                    print('')
                    if agentCanGo != 'no':
                        wantToPlay = human.WantToPlay(humanHand, upPiles, downPiles, mustplay, turns)
            if mustplay > turns:
                canGo = 'no'
                print('You did not play enough cards, the game will now end.')

            #The state of the game after the human played is written to the output files.
            print('\nHuman hand after playing:', humanHand , file=open('output.txt', 'a'))
            print('number of cards played:', turns, file=open('output.txt', 'a'))
            print('number of cards played:', turns, file=open('simple_output.txt', 'a'))
            print('Up piles after human played:', upPiles, file=open('output.txt', 'a'))
            print('Down piles after human played:', downPiles , file=open('output.txt', 'a'))
            turn = 'agent'

        #The agent will learn if the human decided to announce a big jump
        if whatTypeOfSay == '2':
            agLer.ruinLearn('human', pile, upPiles, downPiles)
        
        #The human is dealt new cards
        humanHand = DealCard(drawpile, humanHand)
        
        #The human can communicate with the agent if desired
        agentCanGo = StopGame(agentHand, upPiles, downPiles)
        if agentCanGo == 'yes' and canGo != 'no':
            start = time()
            whatTypeOfSay, pile, howToSay = huCom.Communicate(upPiles, downPiles, humanHand)
            reactionTime = time()-start
            print('time it took to communicate:', reactionTime , file=open('output.txt', 'a'))
            print('time it took to communicate:', reactionTime , file=open('simple_output.txt', 'a'))

        #If and what the communicated is added to the output files
        print('\nHuman hand after dealing', humanHand, file=open('output.txt', 'a'))
        if whatTypeOfSay == 'bla':
            print('No communication', file=open('output.txt', 'a'))
            print('No communication', file=open('simple_output.txt', 'a'))
        if whatTypeOfSay == '1':
            print('reserve,','pile:', pile,',', howToSay, file=open('output.txt', 'a'))
            print('reserve,','pile:', pile,',', howToSay, file=open('simple_output.txt', 'a'))
        if whatTypeOfSay == '2':
            print('ruin,','pile:' ,pile, file=open('output.txt', 'a'))
            print('ruin,','pile:' ,pile, file=open('simple_output.txt', 'a'))

        humanCanGo = StopGame(humanHand, upPiles, downPiles)

        #A check to see if the game should go on.
        if humanCanGo == 'no':
            if agentCanGo == 'no':
                canGo = 'no'

    return upPiles, downPiles, agentHand, humanHand, drawpile

if __name__ == "__main__":

    #The piles, hands, and drawpiles are initialized
    upPiles = [1, 1]
    downPiles = [100, 100]
    drawpile, agentHand, humanHand = StartGame()

    #The starting hands of the human and the agent are recorded
    print('Agent hand:', agentHand, file=open('output.txt', 'a'))
    print('Human hand:', humanHand, file=open('output.txt', 'a'))

    #The PlayGame() function is called, and the game is played
    upPiles, downPiles, agentHand, humanHand, drawpile = PlayGame(upPiles, downPiles, agentHand, humanHand, drawpile)

    #The final score is calculated
    finalScore = calculateFinalScore(drawpile, humanHand, agentHand)
    
    #Print the final scores for the players
    print('The game is over')
    print('Up pile 1:', upPiles[0])
    print('Up pile 2:', upPiles[1])
    print('Down pile 1:', downPiles[0])
    print('Down pile 2:', downPiles[1])
    print('The agents final hand:', agentHand)
    print('The humans final hand:', humanHand)
    print('The final score is: ', finalScore)

    #Add the final hands, piles, and scores to the output files
    print('The game is over', file=open('output.txt', 'a'))
    print('Up pile 1:', upPiles[0], file=open('output.txt', 'a'))
    print('Up pile 2:', upPiles[1], file=open('output.txt', 'a'))
    print('Down pile 1:', downPiles[0], file=open('output.txt', 'a'))
    print('Down pile 2:', downPiles[1], file=open('output.txt', 'a'))
    print('The agents final hand:', agentHand, file=open('output.txt', 'a'))
    print('The humans final hand:', humanHand, file=open('output.txt', 'a'))
    print('The final score is: ', finalScore, file=open('output.txt', 'a'))
    print('The final score is: ', finalScore, file=open('simple_output.txt', 'a'))








