import unittest
from decimal import Decimal
from utils import win_conditions
from models import Player, Hand, Card

class TestWinConditions(unittest.TestCase):

    def setup_win_scenario(self):
        player = Player()
        player.bet = Decimal(1.00)
        player.money = Decimal(1.00)
        
        card1 = Card('Hearts', 'Jack')
        card2 = Card('Hearts', 'King')
        
        player_hand = Hand()
        player_hand.add_card(card1)
        player_hand.add_card(card2)
        
        dealer_hand = Hand()
        return player, player_hand, dealer_hand

    def setup_lose_scenario(self):
        player = Player()
        player.bet = Decimal(1.00)
        player.money = Decimal(1.00)
        
        card1 = Card('Hearts', 'Jack')
        card2 = Card('Hearts', 'King')
        
        dealer_hand = Hand()
        player_hand = Hand()
        dealer_hand.add_card(card1)
        dealer_hand.add_card(card2)
        return player, player_hand, dealer_hand

    def setup_bust_scenario(self):
        player = Player()
        player.bet = Decimal(1.00)
        player.money = Decimal(1.00)
        
        card1 = Card('Hearts', 'Jack')
        card2 = Card('Hearts', 'King')
        
        player_hand = Hand()
        player_hand.add_card(card1)
        player_hand.add_card(card2)
        player_hand.add_card(card2)
        
        dealer_hand = Hand()

        return player, player_hand, dealer_hand

    def setup_dealer_bust_scenario(self):
        player = Player()
        player.bet = Decimal(1.00)
        player.money = Decimal(1.00)
        
        card1 = Card('Hearts', 'Jack')
        card2 = Card('Hearts', 'King')
        dealer_hand = Hand()
        player_hand = Hand()
        dealer_hand.add_card(card1)
        dealer_hand.add_card(card2)
        dealer_hand.add_card(card2)

        return player, player_hand, dealer_hand

    def setup_dealer_tie_scenario(self):
        player = Player()
        player.bet = Decimal(1.00)
        player.money = Decimal(1.00)
        
        card1 = Card('Hearts', 'Jack')
        card2 = Card('Hearts', 'King')
        dealer_hand = Hand()
        player_hand = Hand()
        dealer_hand.add_card(card1)
        player_hand.add_card(card2)

        return player, player_hand, dealer_hand
        
    def test_win_conditions_win(self):
        player, player_hand, dealer_hand = self.setup_win_scenario()
        win_conditions(player, player_hand, dealer_hand)
        self.assertEqual(player.money, Decimal(2.00))

    def test_win_conditions_win_causes_player_win_counter_to_go_up(self):
        player, player_hand, dealer_hand = self.setup_win_scenario()
        win_conditions(player, player_hand, dealer_hand)
        self.assertEqual(player.wins, 1)

    def test_win_conditions_dealer_busts(self):
        player, player_hand, dealer_hand = self.setup_dealer_bust_scenario()
        win_conditions(player, player_hand, dealer_hand)
        self.assertEqual(player.money, Decimal(2.00))

    def test_win_conditions_lose(self):
        player, player_hand, dealer_hand = self.setup_lose_scenario()
        win_conditions(player, player_hand, dealer_hand)
        self.assertEqual(player.money, Decimal(0.00))

    def test_win_conditions_lose_by_tie(self):
        player, player_hand, dealer_hand = self.setup_dealer_tie_scenario()
        win_conditions(player, player_hand, dealer_hand)
        self.assertEqual(player.money, Decimal(0.00))

    def test_win_conditions_lose_by_busting(self):
        player, player_hand, dealer_hand = self.setup_bust_scenario()
        win_conditions(player, player_hand, dealer_hand)
        self.assertEqual(player.money, Decimal(0.00))
