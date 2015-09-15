# Blackjack.py - by Clyde Miller
from random import shuffle
from collections import deque
from itertools import product
import os
from decimal import Decimal
import re

def clearscreen():
    if(os.name == "posix"):
        os.system('clear')
    else:
        os.system('cls')
    
def get_bet():
    while True:
        try:
            player.bet = int(input("{}, make your wager: $".format(player.name)))
            if player.bet < 0:
                raise ValueError()
            break
        except ValueError:
            print("That is not a valid bet. They will throw you out of Vegas for that kinda crap")

def win_conditions(player):
    if player_hand.score() > 21:
        player.lose()
        print("Sorry, friend. You busted and lost ${}.".format(player.bet))
    
    elif(player_hand.score() <= dealer_hand.score() <= 21):
        player.lose()
        print("Dealer wins. You lost ${}.".format(player.bet))
    elif(dealer_hand.score() > 21):
        player.win()
        print("Dealer busts! You win ${}".format(player.bet))
    elif(21 >= player_hand.score() > dealer_hand.score()):
        player.win()
        print("Your score of {} is higher than the dealer's {}. You win ${}.".format(player_hand.score(),dealer_hand.score(),player.bet))
    else:
        print("Well, shit. There's a corner case you don't have the logic for or this is broken. What the hell happened?")


# Establishing the info each card represents
class Card:
    def __init__(self, suit, name):
        if name in ('Jack', 'Queen', 'King'):
            value = 10
        elif name == 'Ace':
            value = 11
        else:
            value = int(name)
        self.suit = suit
        self.name = name
        self.value = value

    def __str__(self):
        return '{self.name} of {self.suit}'.format(self=self)
    

# building a deck of cards
class Deck:
    def __init__(self, packs=1):
        self.cards = deque()
        self.packs = packs
        # uses 'packs' to determine how many standard 52-card packs of cards to use in creating the deck
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        names = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        for i in range(self.packs):
            for suit, name in product(suits, names):
                    self.cards.append(Card(suit, name))
    
    # shuffles the deck
    def shuffle(self):
        shuffle(self.cards)
    
    # deals a card from the top of the deck
    def deal(self):
        top_card = self.cards.pop()
        return top_card
    
    # determines the number of cards left in the deck
    def cards_left(self):
        return len(self.cards)

# The class that determines the cards in the player or dealer's hand
class Hand:
    
    def __init__(self):
        self.cards = deque()

    def add_card(self, card):
        self.cards.append(card)
    
    def score(self):
        score = 0
        for card in self.cards:
            if (card.value != 11):
                value = card.value        
                score += value
        for card in self.cards:
            if((score > 10) and (card.value == 11)):
                value = 1
                score +=value
            elif(card.value == 11):
                value = card.value
                score +=value
        return score

    def show_cards(self):
        allcards = ''
        for card in self.cards:
            allcards = allcards + ' - {}'.format(card)
        return allcards
            
# A class to keep track of the global number of games played so that we con do win ratios
class Game:
    def __init__(self):
        self.games = 0

# A class to keep track of all of a player's individual stats        
class Player:
    def __init__(self, money = 0, name = 'player'):
        self.money = Decimal(money)
        self.start_money = Decimal(0.00)
        self.wins = 0
        self.name = name
        self.games_played = 0
        self.win_percentage = 0.0
        self.bet = Decimal(0.00)

    def win(self, percent = 1):
        win = Decimal(self.bet * percent)
        self.money = self.money + win
        self.wins += 1
        
    def lose(self, percent = 1):
        lose = self.bet * percent
        self.money = self.money - lose

    def update_percentage(self):
        self.win_percentage = round((100 * self.wins / self.games_played),2)


#Starting with a nice, clear screen:
clearscreen()

# Getting the player info        
player = Player()

player.name = input("What's your name, pardner? ")
money = (input("How much money are you bringing to the table, {}? $".format(player.name)))
player.money = Decimal(money)
player.start_money = player.money
bet = 0

# Building the Deck
while True:
    try:
        packs = 1
        packs = int(input("How many packs of cards should make up your deck? [1-10] "))
        if packs < 0:
            raise ValueError()
        break
    except ValueError:
        print("{} is not a valid number of packs. They will throw you out of Vegas for that kinda crap".format(packs))

deck = Deck(packs)
deck.shuffle()

#Setting the play variable and the game counter
play_another = 'y'
game = Game()
while play_another != 'n':
    # clear screen between rounds
    clearscreen()

    if (deck.cards_left() < 10):
        print("There were only {} cards left in the deck, so the dealer reshuffled.".format(deck.cards_left()))
        deck=Deck(packs)
        deck.shuffle()

    player_hand = Hand()
    dealer_hand = Hand()
    #listing the players's stats
    print("{}'s current chipcount: ${} - {}'s starting amount: ${}.".format(player.name, round(player.money,2), player.name,round(player.start_money,2)))
    print("{} Hands played. {} Hands won. Win percentage: {}%".format(player.games_played, player.wins, player.win_percentage))
    if player.money < 1:
        break
    else:
        # player.bet() = int(input("{}, make your wager: $".format(player.name)))
        bet = get_bet()
        if player.bet > player.money:
            print("You don't have that much, so you promise your partner as a sex slave.") 
            print("Luckily (maybe) for you, the dealer accepts.")

        #initial deal
        for i in range(2):
            player_hand.add_card(deck.deal())
            x = deck.deal()
            dealer_hand.add_card(x)
            if i == 1:
                print("There are {} cards left in the deck.".format(deck.cards_left()))
                print("The dealer's face-up card is a {}".format(x))
                print("")

                print("Your hand consists of:{}".format(player_hand.show_cards()))
    print("Your score is: {}".format(player_hand.score()))
    
    #handling being dealt a blackjack
    if(player_hand.score() == 21) and (dealer_hand.score() < 21):
        player.win(1.5)
        print("You got a blackjack and just won ${:.2f}!".format(player.bet * Decimal(1.50)))
    elif(player_hand.score() == 21) and (dealer_hand.score() == 21):
        player.lose(1)
        print("You got a blackjack!")
        print("The dealer's hand is:{}".format(dealer_hand.show_cards()))
        print("...but so did the dealer. So you lose. Bad luck happens.")
    elif(player_hand.score() < 21) and (dealer_hand.score() == 21):
        player.lose(1)
        print("The dealer shows his hand {}: a blackjack. You lose ${}".format(dealer_hand.show_cards(), player.bet))
    
    else:
        hit = 'y'
        
        #the player gets to hit or stay
        while ((hit != 'n') and (player_hand.score() <= 21)):
        
            hit = (input("Hit? (y/n)").lower())
            if hit != 'n':
                x = deck.deal()
                player_hand.add_card(x)
                print("You were dealt a {}.".format(x))
                print("Your score is: {}".format(player_hand.score()))
        
        #dealer logic
        print("The dealer shows his hand and has {}".format(dealer_hand.show_cards()))
        while((dealer_hand.score() <= 17) and (dealer_hand.score() < player_hand.score()) and (player_hand.score() <= 21)):
            x = deck.deal()
            dealer_hand.add_card(x)
            print("The dealer hits and gets a {}".format(x))
        print("His score is {}.".format(dealer_hand.score()))
        #win/lose conditions
        win_conditions(player)
    player.games_played += 1
    player.update_percentage()
    print("")
    play_another = (input("Are you up for another hand? (y/n)").lower())


# Goodbye message/warning.
clearscreen()

if player.money <= 0:
    print("Sorry friend, you've got to have money to rent a seat. Have a nice one.")
print("Thanks for playing! You're leaving the table win percentage of {}%.".format(player.win_percentage))

if player.money >= player.start_money:
    print("You won ${:.2f}.".format(round(player.money - player.start_money),2))
else:
    print("You lost ${:.2f}.".format(round((player.money - player.start_money)*-1),2))
if(player.money < 0):
    print("The dealer has taken your partner. You need to find a way to pay back the casino quickly.") 
    print("Unseemly things are happening.")
if(player.win_percentage > 65 and game.games > 20):
    print("It looks like you might've been card counting. Don't make it too obvious or you'll get banned.")
