import unittest
from decimal import Decimal
from utils import blackjack_test
from models import Player, Hand, Deck, Card

class Test_models_Card(unittest.TestCase):

    def test_card_number(self):
        card1 = Card('Diamond', '4')
        self.assertTrue(card1.value, 4)

    def test_card_face(self):
        card1 = Card('Diamond', 'King')
        self.assertTrue(card1.value, 10)

    def test_card_ace(self):
        card1 = Card('Diamond', 'Ace')
        self.assertTrue(card1.value, 11)
        
class Test_models_Deck(unittest.TestCase):

    def test_deck_size_with_multiple_packs(self):
        pack = 10
        deck = Deck(pack)
        self.assertTrue(deck.cards_left, 520)
        
    def cards_are_unique(self):
        deck = Deck(1)
        card1 = deck.deal
        card2 = deck.deal
        self.assertFalse(card1, card2)
        
class Test_models_Hand(unittest.TestCase):

    def test_hand_scoring(self):
        hand = Hand()
        hand.add_card(Card('Heart','4'))
        hand.add_card(Card('Diamond','7'))
        self.assertTrue(hand.score, '11')
        
    def test_hand_scoring_with_multiple_aces(self):
        hand = Hand()
        hand.add_card(Card('Heart','Ace'))
        hand.add_card(Card('Diamond','Ace'))
        self.assertTrue(hand.score, '12')
        
    def test_show_cards_returns_string(self):
        hand = Hand()
        hand.add_card(Card('Heart','4'))
        hand.add_card(Card('Diamond','Ace'))
        self.assertTrue(hand.show_cards, 'a string, any string')
        
class Test_models_Player(unittest.TestCase):
    
    def setup_player_scaffolding(self):
        player = Player()
        player.bet = Decimal(1.00)
        player.money = Decimal(1.00)
        player.games_played = 4
        player.wins = 1
        player.win_percentage = 0.0
        return player
        
    def test_player_win(self):
        player = self.setup_player_scaffolding()
        player.win
        self.assertTrue(player.money, Decimal(2))

    def test_player_win_increments(self):
        player = self.setup_player_scaffolding()
        player.win
        self.assertTrue(player.wins, 2)

    def test_player_lose(self):
        player = self.setup_player_scaffolding()
        player.win
        self.assertTrue(player.money, Decimal(0))    

    def test_player_win_percentage_updating(self):
        player = self.setup_player_scaffolding()
        player.update_percentage()
        self.assertTrue(player.win_percentage, 25)            