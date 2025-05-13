import main

#Function to check if the human wants to say anything at all
def WantToSay(upPiles, downPiles, humanHand):

    print('1. Up pile:', upPiles[0])
    print('2. Up pile:', upPiles[1])
    print('3. Down pile:', downPiles[0])
    print('4. Down pile:', downPiles[1])
    print(main.Colors.CBLUE + 'Your hand:' + main.Colors.CEND, humanHand)
    print(main.Colors.CYELLOW + 'Would you like to say something to the agent? Y/N'+ main.Colors.CEND)

    wantToSay = input()

    if wantToSay == 'y' or wantToSay == 'Y' or wantToSay == 'yes' or wantToSay == 'Yes':
        wantToSay = 'y'
    elif wantToSay == 'n' or wantToSay == 'N' or wantToSay == 'no' or wantToSay == 'No':
        wantToSay = 'n'
    else:
        print(main.Colors.CGREEN + 'Invalid choice.'+ main.Colors.CEND)
        wantToSay = WantToSay(upPiles, downPiles, humanHand)

    return wantToSay

#The human chooses what they want to say
def WhatToSay():

    print(main.Colors.CYELLOW + 'What would you like to say to the agent?'+ main.Colors.CEND)
    print('1. I want to reserve a pile.')
    print('2. I want to announce a big jump.')
    print('3. Nevermind')

    whatTypeOfSay = input()

    if whatTypeOfSay != '1' and whatTypeOfSay != '2' and whatTypeOfSay != '3':
        print(main.Colors.CYELLOW + 'Invalid choice.'+ main.Colors.CEND)
        whatTypeOfSay = WhatToSay()
            
    return whatTypeOfSay

#When the human reserves a pile, this function has them choose what pile
def OffLimitsPile(upPiles, downPiles):

    print(main.Colors.CYELLOW + 'What pile should the agent not touch?'+ main.Colors.CEND)
    print('1. Up pile:', upPiles[0])
    print('2. Up pile:', upPiles[1])
    print('3. Down pile:', downPiles[0])
    print('4. Down pile:', downPiles[1])
    print('5. Nevermind')

    offLimitsPile = input()

    if offLimitsPile != '1' and offLimitsPile != '2' and offLimitsPile != '3' and offLimitsPile != '4' and offLimitsPile != '5':
        print(main.Colors.CYELLOW + 'Invalid choice'+ main.Colors.CEND)
        offLimitsPile = OffLimitsPile(upPiles, downPiles)
    else:
        offLimitsPile = int(offLimitsPile)
    
    return offLimitsPile

#This function let's the human choose between different statements to reserve a pile
def ReservePile(offLimitsPile):

    print(main.Colors.CYELLOW + 'How would you like to say that?'+ main.Colors.CEND)
    print('1. It would be nice if you could leave pile', offLimitsPile, 'alone')
    print('2. Please do not play on pile', offLimitsPile, '')
    print('3. You really should not play on pile', offLimitsPile)
    print('4. If you play on pile', offLimitsPile, 'everything will go really wrong')
    print('5. Nevermind')

    howToSay = input()

    if howToSay != '1' and howToSay != '2' and howToSay != '3' and howToSay != '4' and howToSay != '5':
        print(main.Colors.CYELLOW + 'Invalid choice'+ main.Colors.CEND)
        howToSay = ReservePile(offLimitsPile)

    return howToSay

#Function it have the human announce where a big jump will take place
def RuinPile(upPiles, downPiles):
        
    print(main.Colors.CYELLOW + 'On what pile will the big jump happen?'+ main.Colors.CEND)
    print('1. Up pile:', upPiles[0])
    print('2. Up pile:', upPiles[1])
    print('3. Down pile:', downPiles[0])
    print('4. Down pile:', downPiles[1])
    print('5. Nevermind')

    pileToRuin = input()

    if pileToRuin != '1' and pileToRuin != '2' and pileToRuin != '3' and pileToRuin != '4' and pileToRuin != '5':
        print(main.Colors.CYELLOW + 'Invalid choice'+ main.Colors.CEND)
        pileToRuin = RuinPile(upPiles, downPiles)
    else:
        pileToRuin = int(pileToRuin)

    return pileToRuin

#Function that initiates and handles all of the humans communication
def Communicate(upPiles, downPiles, humanHand):

    #check to see if the human wants to say something at all
    wantToSay = WantToSay(upPiles, downPiles, humanHand)

    whatTypeOfSay = 'bla'
    pile = 6
    howToSay = 'bla'

    #check what statement that human wants to make
    if wantToSay == 'y':
        whatTypeOfSay = WhatToSay()

    #have the human reserve a pile
    if wantToSay == 'y' and whatTypeOfSay == '1':
        pile = OffLimitsPile(upPiles, downPiles)
        if pile != 5:
            howToSay = ReservePile(pile)
    
    #have the human announce a big jump
    if wantToSay == 'y' and whatTypeOfSay == '2':
        pile = RuinPile(upPiles, downPiles)
        howToSay = 'irrelevant'
    
    #In case the human backs out of talking
    if whatTypeOfSay == '3' or howToSay == '5' or pile == 5:
        whatTypeOfSay, pile, howToSay = Communicate(upPiles, downPiles, humanHand)

    print('')
    
    return whatTypeOfSay, pile, howToSay

