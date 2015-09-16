#from utils import *
from decimal import Decimal
from collections import deque
from itertools import product
from random import shuffle

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
        # uses 'packs' to determine how many standard 52-card packs of cards to
        # use in creating the deck
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        names = [
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '10',
            'Jack',
            'Queen',
            'King',
            'Ace']
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
                score += value
            elif(card.value == 11):
                value = card.value
                score += value
        return score

    def show_cards(self):
        allcards = ''
        for card in self.cards:
            allcards = allcards + ' - {}'.format(card)
        return allcards

# A class to keep track of all of a player's individual stats


class Player:

    def __init__(self, money=0, name='player'):
        self.money = Decimal(money)
        self.start_money = Decimal(0.00)
        self.wins = 0
        self.name = name
        self.games_played = 0
        self.win_percentage = 0.0
        self.bet = Decimal(0.00)

    def win(self, percent=1):
        win = Decimal(self.bet * percent)
        self.money = self.money + win
        self.wins += 1

    def lose(self, percent=1):
        lose = self.bet * percent
        self.money = self.money - lose

    def update_percentage(self):
        self.win_percentage = round((100 * self.wins / self.games_played), 2)
