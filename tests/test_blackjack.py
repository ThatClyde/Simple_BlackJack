import unittest
from decimal import Decimal
from utils import blackjack_test
from models import Player, Hand, Card

class Test_blackjack_test(unittest.TestCase):

    def setup_player_non_blackjack(self):
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

    def setup_player_blackjack(self):
        player = Player()
        player.bet = Decimal(1.00)
        player.money = Decimal(1.00)
        
        card1 = Card('Hearts', 'Jack')
        card2 = Card('Hearts', 'Ace')
        
        dealer_hand = Hand()
        player_hand = Hand()
        player_hand.add_card(card1)
        player_hand.add_card(card2)
        return player, player_hand, dealer_hand

    def setup_dealer_blackjack(self):
        player = Player()
        player.bet = Decimal(1.00)
        player.money = Decimal(1.00)
        
        card1 = Card('Hearts', 'Jack')
        card2 = Card('Hearts', 'Ace')
        dealer_hand = Hand()
        player_hand = Hand()
        dealer_hand.add_card(card1)
        dealer_hand.add_card(card2)

        return player, player_hand, dealer_hand

    def setup_dual_blackjack_scenario(self):
        player = Player()
        player.bet = Decimal(1.00)
        player.money = Decimal(1.00)
        
        card1 = Card('Hearts', 'Jack')
        card2 = Card('Hearts', 'Ace')
        dealer_hand = Hand()
        player_hand = Hand()
        dealer_hand.add_card(card1)
        dealer_hand.add_card(card2)
        player_hand.add_card(card1)
        player_hand.add_card(card2)

        return player, player_hand, dealer_hand

    def test_blackjack_no_blackjack_returns_false(self):
        player, player_hand, dealer_hand = self.setup_player_non_blackjack()
        self.assertFalse(blackjack_test(player, player_hand, dealer_hand))

    def test_blackjack_with_blackjack_return_true(self):
        player, player_hand, dealer_hand = self.setup_player_blackjack()
        self.assertTrue(blackjack_test(player, player_hand, dealer_hand))

    def test_blackjack_with_dual_blackjacks_return_true(self):
        player, player_hand, dealer_hand = self.setup_dual_blackjack_scenario()
        self.assertTrue(blackjack_test(player, player_hand, dealer_hand))
        
    def test_blackjack_with_dual_blackjack_money_lost(self):
        player, player_hand, dealer_hand = self.setup_dual_blackjack_scenario()
        blackjack_test(player, player_hand, dealer_hand)
        self.assertEqual(player.money, Decimal(0))
        
    def test_blackjack_with_blackjack_wins_increment(self):
        player, player_hand, dealer_hand = self.setup_player_blackjack()
        blackjack_test(player, player_hand, dealer_hand)
        self.assertEqual(player.wins, 1)

    def test_blackjack_with_blackjack_money_added(self):
        player, player_hand, dealer_hand = self.setup_player_blackjack()
        blackjack_test(player, player_hand, dealer_hand)
        self.assertEqual(player.money, Decimal(2.5))
        
    def test_blackjack_with_dealer_blackjack_money_lost(self):
        player, player_hand, dealer_hand = self.setup_dealer_blackjack()
        blackjack_test(player, player_hand, dealer_hand)
        self.assertEqual(player.money, Decimal(0))

    def test_blackjack_with_dealer_blackjack_return_true(self):
        player, player_hand, dealer_hand = self.setup_dealer_blackjack()
        self.assertTrue(blackjack_test(player, player_hand, dealer_hand))
