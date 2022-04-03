#Blackjack is a game of chance, must implement random library
import random

#All aspects of a deck of cards
suits = ('Hearts','Diamonds','Spades','Clubs')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':1}

#Card Class
class Card():

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit

#Deck Class
class Deck():

    def __init__(self):
        self.all_cards = []

        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit,rank))
    
    def shuffle(self):
        random.shuffle(self.all_cards)
    
    def deal_one(self):
        return self.all_cards.pop()

#Hand class
class Hand():
    def __init__(self,isdealor):
        self.hand = []
        self.isdealor = isdealor

    def add_cards(self,new_cards):
        if type(new_cards) == type([]):
            self.hand.extend(new_cards)
        else:
            self.hand.append(new_cards)

    def hit(self, new_cards):
        return self.hand.append(new_cards)

    def check_value(self):
        #checks value of hand
        handValue = sum(card.value for card in self.hand)
        #if hand value < 11 and contains ace, add 10 to handvalue
        if any(card.rank == 'Ace' for card in self.hand) and handValue < 12:
            handValue += 10
        return handValue

    def show_hand(self):
        if(self.isdealor == True):
            print("--------------------------------------------------------")
            print("Dealor's Hand consists of the following: ")
            for i in range(len(self.hand)):
                print(self.hand[i])
            print(f'{self.check_value()} is the total value ')
            print("--------------------------------------------------------")
        else:
            print("--------------------------------------------------------")
            print("Your Hand consists of the following: ")
            for i in range(len(self.hand)):
                print(self.hand[i])
            print(f'{self.check_value()} is the total value ')
            print("--------------------------------------------------------")  

#Wager Class
class Wallet():
    def __init__(self,cash):
        self.cash = cash
        self.bet = 0
    
    def place_bet(self,wager):
        self.bet += wager
        self.cash -= wager
    
    def win_bet(self):
        self.cash += self.bet * 2

    def blackJack(self):
        self.bet *= 4
        self.cash += self.bet
    
    def lose_bet(self):
        self.bet = 0

    def clear_bet(self):
        self.bet = 0

    def tie(self):
        self.cash += self.bet
    
    def __str__(self):
        return f'You have ${self.cash} in total'


#create player wallet
PlayerWallet = Wallet(1000)

#round #
round = 0

game_on = True

while game_on:

    #create player and dealors hand
    player1 = Hand(False)
    dealor = Hand(True)


    if PlayerWallet.cash == 0:
        print("Player is out of money! Unable to continue playing")
        game_on = False
        break

    #round increment
    round += 1

    #Create a round running
    round_running = True

    #shows current Balance for Player's Wallet
    print("===========================================================================================================================================================")
    print(PlayerWallet)

    #Ask player for wager amount
    result = 0
    while True:

        #make sure bet amount is clear before
        PlayerWallet.clear_bet()
        try:
            result = input("How much are you wagering? (To the nearest whole $) (Type Q to Quit): ") 

            #checks if user wants to quit game
            if result == 'Q' or result == 'q':
                print('User has opted to quit game')
                round_running = False
                game_on = False
                break 
            else:
                result = int(result)

        except:
            print("Not a #")
            continue
        else:
            #Player bets more then he has
            if result > PlayerWallet.cash:
                print("Insufficient Funds")
                continue
            elif result == 0:
                print("Cannot bet $0")
                continue
            elif result % 1 != 0:
                print("$ amount not rounded to the nearest whole $")
                continue
            #Player Wages All-In
            elif result == PlayerWallet.cash:
                print("PLAYER HAS GONE ALL-IN")
                PlayerWallet.place_bet(result)
                print(f"A ${result} wager has been placed")
                break
            else:
                PlayerWallet.place_bet(result)
                print(f"A ${result} wager has been placed")
                break

    while round_running: 
        
        print("===========================================================================================================================================================")
        
        #Make a new deck and shuffle
        new_deck = Deck()
        new_deck.shuffle()
    
        #Deals 2 cards to each at the beginning of game
        for i in range(2):
            player1.add_cards(new_deck.deal_one())
            dealor.add_cards(new_deck.deal_one())
        
        #Show player his hand
        player1.show_hand()

        #Show one card from
        print("--------------------------------------------------------")
        print("Dealor's Hand: ")
        print(dealor.hand[0])
        print("**HIDDEN CARD**")
        print("--------------------------------------------------------")


        #Checks for BlackJack out of the box
        #Checks if both have BlackJack
        if(dealor.check_value() == 21 and player1.check_value() == 21):
            print("Both Player and Dealor have BlackJacks! Tie.")
            PlayerWallet.tie()
            round_running = False
            break

        #Checks if player has BlackJack
        elif(player1.check_value() == 21):
            print("Player has a BlackJack, YOU WIN!!!")
            PlayerWallet.blackJack()
            round_running = False
            break

        #Checks if Dealor has BlackJack
        elif(dealor.check_value() == 21):
            print("Dealor has BlackJack, You Lose!")
            PlayerWallet.lose_bet()
            round_running = False
            break
        
        
        #Store variable for user input
        uInput = ""

        #A Look to keep taking whether user will hit or stand
        userinputting = True

        while userinputting:

            try:
                uInput = input("Would you like to Hit or Stand? Type H or S: ").upper()

                #Throws Error if input isnt h or s
                if uInput not in ['H','S']:
                    uInput += 10

            except:
                print("Not a valid input")
                continue

            else:

                #If Hit
                if uInput == 'H':
                    player1.hit(new_deck.deal_one())
                    player1.show_hand()
                    #checks if player busted
                    if(player1.check_value() > 21):
                        print("Player Busted! Dealor Wins!")
                        PlayerWallet.lose_bet()
                        userinputting = False
                        round_running = False
                        break

                #If Stand
                else:
                    userinputting = False
                    break
        
        dealor.show_hand()

        if player1.check_value() > 21:
            round_running = False
            break
        else:

            if(dealor.check_value() == player1.check_value()):
                print("Both Player and Dealor are Tied!")
                PlayerWallet.tie()
                round_running = False
                break
            elif(dealor.check_value() > player1.check_value()):
                print("Dealor Wins!")
                PlayerWallet.lose_bet()
                round_running = False
                break
            else:
                while dealor.check_value() < player1.check_value():
                    #dealor adds card
                    print("Dealor Hits!")
                    dealor.add_cards(new_deck.deal_one())

                    #show Dealors hand
                    dealor.show_hand()

                    #checks if both have same value
                    if(dealor.check_value() == player1.check_value()):
                        print("Both Player and Dealor are Tied!")
                        PlayerWallet.tie()
                        round_running = False
                        break
                    
                    #checks if dealor busts
                    elif dealor.check_value() > 21:
                        print("Dealor Busted! Player Wins!")
                        PlayerWallet.win_bet()
                        round_running = False
                        break

                    elif dealor.check_value() > player1.check_value():
                        print("Dealor Wins!")
                        PlayerWallet.lose_bet()
                        round_running = False
                        break