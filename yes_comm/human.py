import main
from time import time

#The function that determines if the human wants/has to keep their turn going
def WantToPlay(humanHand, upPiles, downPiles, mustplay, turns):

    #it is determined if the human has a valid card to play
    canGo = main.StopGame(humanHand, upPiles, downPiles)

    #if they do not have a valid card, their turn is ended
    if canGo == 'no':
        print('You have no playable cards, your turn is over.')
        wantToPlay = 'n'
    #if they have a valid card, and they have not played the required number of cards yet, they have to go regardless of if they would like to go.
    elif mustplay > turns:
        print('You have to play another card.')
        wantToPlay = 'y'
    #if they can go, but do not have to, they get to choose if they would like to continue.
    else:
        print('1. Up pile:', upPiles[0])
        print('2. Up pile:', upPiles[1])
        print('3. Down pile:', downPiles[0])
        print('4. Down pile:', downPiles[1])
        print(main.Colors.CBLUE + 'Your hand:' + main.Colors.CEND, humanHand)
        print(main.Colors.CYELLOW + 'Do you want to play another card? Y/N' + main.Colors.CEND)
        opinion = str(input('Answer: '))
        if opinion == 'y' or opinion == 'Y' or opinion == 'yes' or opinion == 'Yes':
            wantToPlay = 'y'
            print('')
        elif opinion == 'n' or opinion == 'N' or opinion == 'no' or opinion == 'No':
            wantToPlay = 'n'
            print('')
        else:
            print(main.Colors.CGREEN + 'Invalid choice, do you want to play another card? Y/N' + main.Colors.CEND)
            wantToPlay = WantToPlay(humanHand, upPiles, downPiles, mustplay, turns)

    return wantToPlay


#This function lets the human decide which player will have the first turn. 
def GoFirst(humanHand):

    print(main.Colors.CBLUE + 'Your hand:' + main.Colors.CEND, humanHand)
    print(main.Colors.CGREEN + 'Would you like to go first? Y/N' + main.Colors.CEND)

    turn = str(input('Answer: '))
    print('does the human want to go first?', turn , file=open('output.txt', 'a'))

    if turn == 'y' or turn == 'Y' or turn == 'yes' or turn == 'Yes':
        turn = 'human'
    elif turn == 'n' or turn == 'N' or turn == 'no' or turn == 'No':
        turn = 'agent'
    else:
        print(main.Colors.CGREEN + 'Invalid choice, would you like to go first? Y/N' + main.Colors.CEND)
        turn = GoFirst(humanHand)
    
    print('')

    return turn

#This function checks if the card the human tried to play is valid, and otherwise asks them to select a new card.
def validPlay(upPiles, downPiles, cardValue, pile, humanHand):

    try:
        cardValue = int(cardValue)
    except ValueError:
        print(main.Colors.CGREEN + 'You tried to play an invalid card. Select a new card:' + main.Colors.CEND)
        cardValue = input('Value of card: ')
        pile = input('Pile number: ')
        valid, cardValue, pile = validPlay(upPiles, downPiles, cardValue, pile, humanHand)

    try:
        pile = int(pile)
    except ValueError:
        print(main.Colors.CGREEN + 'You tried to play an invalid card. Select a new card:' + main.Colors.CEND)
        cardValue = input('Value of card: ')
        pile = input('Pile number: ')
        valid, cardValue, pile = validPlay(upPiles, downPiles, cardValue, pile, humanHand)

    #First it's checked if a card was played that actually is in the humans hand
    for i in range(len(humanHand)):
        if humanHand[i] == cardValue:
            valid = 'no'
            break
        else:
            valid = 'notInHand'

    #Then it is checked if the pile selected was valid
    if (pile == 1 or pile == 2) and (upPiles[pile-1] < cardValue or upPiles[pile -1]-10 == cardValue) and valid != 'notInHand':
        valid = 'yes'
    if (pile == 3 or pile == 4) and (downPiles[pile-3] > cardValue or downPiles[pile-3]+10 == cardValue) and valid != 'notInHand':
        valid = 'yes'

    #If not valid, the player is asked to select a new card to play
    if valid == 'no' or valid == 'notInHand':
        print(main.Colors.CGREEN + 'You tried to play an invalid card. Select a new card:' + main.Colors.CEND)
        cardValue = input('Value of card: ')
        pile = input('Pile number: ')
        valid, cardValue, pile = validPlay(upPiles, downPiles, cardValue, pile, humanHand)

    return valid, cardValue, pile

#This function asks the human to select a card, and plays it if possible
def PlayCard(upPiles, downPiles, humanHand, drawpile):

    start = time()

    print('1. Up pile:', upPiles[0])
    print('2. Up pile:', upPiles[1])
    print('3. Down pile:', downPiles[0])
    print('4. Down pile:', downPiles[1])
    print(main.Colors.CBLUE + 'Your hand:' + main.Colors.CEND, humanHand)
    print(main.Colors.CGREEN + 'What card would you like to play?' + main.Colors.CEND)

    #collects what card the human wants to play
    cardValue = input('Value of card: ')

    print(main.Colors.CGREEN + 'On what pile would you like to play that card?' + main.Colors.CEND)

    #collects on what pile the human wants to play
    pile = input('Pile number: ')

    #check if the card is valid
    valid, cardValue, pile = validPlay(upPiles, downPiles, cardValue, pile, humanHand)

    #play the card if it was valid
    if valid == 'yes' and (pile == 1 or pile == 2):
        upPiles[pile - 1] = cardValue
    if valid == 'yes' and (pile == 3 or pile == 4):
        downPiles[pile - 3] = cardValue

    #prints what the human did to the output files
    reactionTime = time()-start
    print('time it took to play card:', reactionTime , file=open('output.txt', 'a'))
    print('time it took to play card:', reactionTime , file=open('simple_output.txt', 'a'))
    print('played card:', cardValue , file=open('output.txt', 'a'))
    print('played on pile:', pile , file=open('output.txt', 'a'))

    #takes the played card out of the humans hand
    for j in range(len(humanHand)):
        if humanHand[j] == cardValue:
            humanHand.pop(j)
            break

    return upPiles, downPiles, humanHand, drawpile