from models import *
import os


def clearscreen():
    if(os.name == "posix"):
        os.system('clear')
    else:
        os.system('cls')

# gets the player's bet and does a simple error check


def get_bet(player):
    while True:
        try:
            player.bet = int(
                input(
                    "{}, make your wager: $".format(
                        player.name)))
            if player.bet < 0:
                raise ValueError()
            break
        except ValueError:
            print(
                "That is not a valid bet. They will throw you out of Vegas for that kinda crap")

# all of the ifs that determine if the player won/lost


def win_conditions(player, player_hand, dealer_hand):
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
        print("Your score of {} is higher than the dealer's {}. You win ${}.".format(
            player_hand.score(), dealer_hand.score(), player.bet))
    else:
        print("Well, shit. There's a corner case you don't have the logic for or this is broken. What the hell happened?")
