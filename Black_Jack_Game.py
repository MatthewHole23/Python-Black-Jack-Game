"""
Black Jack Card Game
[Author: Matthew Hole]

Milestone 2 Project as part of 'Complete Python Bootcamp: Go from zero to hero in Python 3'

Version History:
[06/09/2020] Matthew Hole - Updates made to the comments and remaining implementation notes
"""

import random

class Card():

    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    # method uses the current total of a hand
    def get_val(self, curr_total):
        if self.rank == "Ace" and curr_total >= 11:
            self.value = 1
        return self.value

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck():

    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                if ranks.index(rank) > 8 and ranks.index(rank) <= 11:
                    value = 10
                elif ranks.index(rank) > 11:
                    value = 11
                else:
                    value = ranks.index(rank) + 2
                self.deck.append(Card(suit, rank, value))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        self.single_card = self.deck.pop()
        return self.single_card

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp


class Bankroll():

    def __init__(self):
        self.bankroll = 1000

    def totalBR(self):
        print("Your current Bank Roll is £%s" % self.bankroll)

    def makebet(self):
        while True:
            while True:
                try:
                    self.bet = int(input('Please place your bet:'))

                    if self.bet <= 0:
                        raise ValueError
                    break

                except ValueError:
                    print('Please only bet a positive number that is greater than £0!')
                    continue

                else:
                    break

            if self.bet <= self.bankroll:
                self.bankroll = self.bankroll - self.bet
                print('You have placed a £%s bet!' % self.bet)
                break
            else:
                print("You cannot bet that amount of money, it has to be less than £%s" % self.bankroll)
                continue

    def win(self):
        self.winnings = self.bet * 2
        self.bankroll = self.bankroll + self.winnings
        print('£%s has been added to your Bank Roll. Your updated balance is £%s' % (self.winnings, self.bankroll))

    def __str__(self):
        return "\nCurrent Bank Roll value: £%s\nCurrent Bet value: £%s" % (self.bankroll, self.bet)


class Player():

    def __init__(self, deck):
        self.name = ""
        self.players = []
        self.playertotal = 0
        self.playerhand = []
        self.deck = deck
        self.been_called = False

    # more to game control class once created
    def add_player(self):
        self.name = input("Please type your name:\n")
        self.players.append(self.name)

    # totval is getval from CardValue class
    def updateTot(self, totval):
        self.playertotal += totval
        return self.playertotal

    def playertot(self):
        return self.playertotal

    def updatehand(self, card):
        self.card = card
        self.playerhand.append(self.card)
        return self.card

    def current_cards(self):
        print("Here are the cards in your hand!\n")
        for index, card in enumerate(self.playerhand, 1):
            print(index, card)

    # will be updated to incorporate error handling
    def move(self):
        while True:
            try:
                self.decision = int(input('%s, Will you Hit(1) or Stand(2)?\n' % self.name))

                if self.decision == 1:
                    self.playhit()
                    break

                elif self.decision == 2:
                    self.playstand()
                    break

                else:
                    raise ValueError

            except ValueError:
                print('Please only select option 1 for Hit or 2 for Stand')
                continue


    # player will hit - draws a card
    def playhit(self):
        print(self.name + " has chosen to HIT!\n")
        deal = self.updatehand(self.deck.deal())
        total = self.playertot()
        value = deal.get_val(total)
        self.updateTot(value)

    # player will end turn and stay with the cards they have
    def playstand(self):
        print(self.name + " has decided to STAND!\n")
        self.been_called = True

    def __str__(self):
        return self.name


# Dealer is to inherit methods of Player
class Dealer(Player):

    def __init__(self):
        Player.__init__(self, deck)
        self.has_been_called = False
        self.name = 'The Dealer'

    def showcard(self):
        randchoice = random.choice(self.playerhand)
        print('\nOne of The Dealers cards are :\n' + str(randchoice) + "\n")

    def dealermove(self):
        if self.playertot() <= 16:
            self.playhit()

        if 17 <= self.playertot() <= 21:
            self.playstand()
            self.has_been_called = True


'''

Game control will be used to control the game. This will involve checking win conditions, keeping track of totals
for all players.

Will also contain the key functionality of the game such as Game Initialisation, Game Running, and Game End Criteria

'''

class GameControl():

    def __init__(self):
        self.deck = Deck()
        self.player = Player(self.deck)
        self.bankroll = Bankroll()
        self.dealer = Dealer()
        self.gamewon = False
        self.numplayers = None

    def gameplayers(self):
        # to be implemented as part of game expansion to have more players
        # self.numplayers = int(input("How many players are there excluding the dealer?"))
        # for x in range(self.numplayers):
        #     self.player.add_player()
        #     self.bankroll.totalBR()
        #     self.bankroll.makebet()
        #     print(self.bankroll)
        self.player.add_player()
        self.bankroll.totalBR()
        self.bankroll.makebet()
        print(self.bankroll)

    # this part of the code initialises the game
    # eventually could expand so number of players and names are called from here
    # will deal out the 2 cards to each player and the dealer
    def gamestart(self):
        # gives 2 cards to each user in the game
        # should the dealers hand be done first so that one of his cards are shown??
        self.deck.shuffle()
        for i in range(2):
            deal = self.player.updatehand(self.deck.deal())
            total = self.player.playertot()
            value = deal.get_val(total)
            self.player.updateTot(value)

    # this method is separate for the dealer starting hand
    # will reuse part of gamestart as well as showing of the dealt cards
    def dealerstart(self):
        self.deck.shuffle()
        for item in range(2):
            deal = self.dealer.updatehand(self.deck.deal())
            total = self.dealer.playertot()
            value = deal.get_val(total)
            self.dealer.updateTot(value)

        self.dealer.showcard()

    # method which will be called to run the made code
    # maybe have bool variable which updates when someone has won which stops the loop
    def main(self):
        while not self.gamewon:
            # asks each player for their move before the dealer's turn
            for i in self.player.players:
                self.player.current_cards()
                print("\nYour current total of points are :%s\n" % self.player.playertot())
                self.player.move()
                self.player.current_cards()
                print("\nYour current total of points are :%s\n" % self.player.playertot())

            # code for dealer functionality
            self.dealer.dealermove()
            self.gamefin()

    def wincondition(self):
        if self.player.playertot() <= 21:

            if self.player.playertot() > self.dealer.playertot():
                self.gamewon = True
                print('%s has won the game!' % self.player.name)
                self.bankroll.win()

            elif (self.player.playertot() <= 21) and (self.dealer.playertot() > 21):
                self.gamewon = True
                print('%s has won the game!' % self.player.name)
                self.bankroll.win()

            else:
                print('===== Next Round =====')
        else:
            print("%s has BUST, they have a score of over 21! They have lost!" % self.player.name)
            self.gamewon = True

    # if win condition is met, self.gamewon = True
    def gamefin(self):
        if self.player.been_called == True:
            self.wincondition()

        if self.dealer.has_been_called == False:
            if self.dealer.playertot() > self.player.playertot():
                print("The Dealer has won the game!")
                print("Here is the Dealer's winning hand!: \n%s" % self.dealer.current_cards())
                self.gamewon = True

            else:
                self.wincondition()
        else:
            self.wincondition()

## MAIN CODE ##
if __name__ == "__main__":
    deck = Deck()
    game = GameControl()
    game.gameplayers()
    game.dealerstart()
    game.gamestart()
    game.main()
