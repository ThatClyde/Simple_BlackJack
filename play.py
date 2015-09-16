#!/usr/bin/env python3
# Blackjack.py - by Clyde Miller
from decimal import Decimal
from models import Card, Deck, Hand, Player
from utils import clearscreen, get_bet, win_conditions


# Starting with a nice, clear screen:
clearscreen()

# Getting the player info
player = Player()
player.name = input("What's your name, pardner? ")
money = (
    input(
        "How much money are you bringing to the table, {}? $".format(
            player.name)))
player.money = Decimal(money)
player.start_money = player.money
bet = 0

# Building the Deck with the number of packs of cards specified
while True:
    try:
        packs = int(
            input("How many packs of cards should make up your deck? [1-10] "))
        if packs < 0:
            raise ValueError()
        break
    except ValueError:
        print("{} is not a valid number of packs. They will throw you out of Vegas for that kinda crap".format(packs))
deck = Deck(packs)
deck.shuffle()

# Setting the play variable and the game counter
play_another = 'y'
while play_another != 'n':
    # clear screen between rounds
    clearscreen()

    if (deck.cards_left() < 10):
        print(
            "There were only {} cards left in the deck, so the dealer reshuffled.".format(
                deck.cards_left()))
        deck = Deck(packs)
        deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    # listing the players's stats
    print("{}'s current chipcount: ${} - {}'s starting amount: ${}.".format(player.name,
                                                                            round(player.money, 2), player.name, round(player.start_money, 2)))
    print("{} Hands played. {} Hands won. Win percentage: {}%".format(
        player.games_played, player.wins, player.win_percentage))
    if player.money < 1:
        break
    else:
        # player.bet() = int(input("{}, make your wager:
        # $".format(player.name)))
        bet = get_bet(player)
        if player.bet > player.money:
            print("You don't have that much, so you promise your partner a payment.")
            print("Luckily (maybe) for you, the dealer accepts.")

        # initial deal
        for i in range(2):
            player_hand.add_card(deck.deal())
            x = deck.deal()
            dealer_hand.add_card(x)
            if i == 1:
                print(
                    "There are {} cards left in the deck.".format(
                        deck.cards_left()))
                print("The dealer's face-up card is a {}".format(x))
                print("")

                print(
                    "Your hand consists of:{}".format(
                        player_hand.show_cards()))
    print("Your score is: {}".format(player_hand.score()))

    # handling being dealt a blackjack
    if(player_hand.score() == 21) and (dealer_hand.score() < 21):
        player.win(1.5)
        print(
            "You got a blackjack and just won ${:.2f}!".format(
                player.bet *
                Decimal(1.50)))
    elif(player_hand.score() == 21) and (dealer_hand.score() == 21):
        player.lose(1)
        print("You got a blackjack!")
        print("The dealer's hand is:{}".format(dealer_hand.show_cards()))
        print("...but so did the dealer. So you lose. Bad luck happens.")
    elif(player_hand.score() < 21) and (dealer_hand.score() == 21):
        player.lose(1)
        print(
            "The dealer shows his hand {}: a blackjack. You lose ${}".format(
                dealer_hand.show_cards(),
                player.bet))

    else:
        hit = 'y'

        # the player gets to hit or stay
        while ((hit != 'n') and (player_hand.score() <= 21)):

            hit = (input("Hit? (y/n)").lower())
            if hit != 'n':
                x = deck.deal()
                player_hand.add_card(x)
                print("You were dealt a {}.".format(x))
                print("Your score is: {}".format(player_hand.score()))

        # dealer logic
        print(
            "The dealer shows his hand and has {}".format(
                dealer_hand.show_cards()))
        while((dealer_hand.score() <= 17) and (dealer_hand.score() < player_hand.score()) and (player_hand.score() <= 21)):
            x = deck.deal()
            dealer_hand.add_card(x)
            print("The dealer hits and gets a {}".format(x))
        print("His score is {}.".format(dealer_hand.score()))
        # win/lose conditions
        win_conditions(player, player_hand, dealer_hand)
    player.games_played += 1
    player.update_percentage()
    print("")
    play_another = (input("Are you up for another hand? (y/n)").lower())


# Goodbye message/warning.
clearscreen()

if player.money <= 0:
    print("Sorry friend, you've got to have money to rent a seat. Have a nice one.")
print(
    "Thanks for playing! You're leaving the table win percentage of {}%.".format(
        player.win_percentage))

if player.money >= player.start_money:
    print(
        "You won ${:.2f}.".format(
            round(
                player.money -
                player.start_money),
            2))
else:
    print(
        "You lost ${:.2f}.".format(
            round(
                (player.money - player.start_money) * -1),
            2))
if(player.money < 0):
    print("The dealer has taken your partner. You need to find a way to pay back the casino quickly.")
    print("Unseemly things are happening.")
if(player.win_percentage > 65 and game.games > 20):
    print("It looks like you might've been card counting. Don't make it too obvious or you'll get banned.")
