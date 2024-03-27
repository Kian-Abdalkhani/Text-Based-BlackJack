import unittest
from blackjack import Card, Deck, Hand, Wallet

class TestCard(unittest.TestCase):
    def test_card_creation(self):
        card = Card('Hearts', 'Ace')
        self.assertEqual(card.suit, 'Hearts')
        self.assertEqual(card.rank, 'Ace')

    def test_card_string_representation(self):
        card = Card('Spades', 'King')
        self.assertEqual(str(card), 'King of Spades')

class TestDeck(unittest.TestCase):
    def test_deck_creation(self):
        deck = Deck()
        self.assertEqual(len(deck.all_cards), 52)

    def test_deck_shuffle(self):
        deck = Deck()
        original_order = deck.all_cards[:]
        deck.shuffle()
        self.assertNotEqual(deck.all_cards, original_order)

    def test_deck_deal_one(self):
        deck = Deck()
        card = deck.deal_one()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck.all_cards), 51)

class TestHand(unittest.TestCase):
    def test_hand_creation(self):
        hand = Hand(isdealor=False)
        self.assertEqual(hand.isdealor, False)
        self.assertEqual(len(hand.hand), 0)

    def test_hand_add_cards_multiple(self):
        hand = Hand(isdealor=False)
        card1 = Card('Hearts', 'Ace')
        card2 = Card('Spades', 'King')
        hand.add_cards([card1, card2])
        self.assertEqual(len(hand.hand), 2)
    
    def test_hand_add_cards_one(self):
        hand = Hand(isdealor=False)
        card1 = Card('Hearts', 'Ace')
        hand.add_cards(card1)
        self.assertEqual(len(hand.hand), 1)

    def test_hand_hit(self):
        deck = Deck()
        hand = Hand(isdealor=False)
        hand.hit(deck.deal_one())
        self.assertEqual(len(hand.hand), 1)

    def test_hand_check_value(self):
        hand = Hand(isdealor=False)
        card1 = Card('Hearts', 'Ace')
        card2 = Card('Spades', 'King')
        hand.add_cards([card1, card2])
        self.assertEqual(hand.check_value(), 21)

class TestWallet(unittest.TestCase):
    def test_wallet_creation(self):
        wallet = Wallet(1000)
        self.assertEqual(wallet.cash, 1000)

    def test_wallet_place_bet(self):
        wallet = Wallet(1000)
        wallet.place_bet(100)
        self.assertEqual(wallet.cash, 900)

    def test_wallet_win_bet(self):
        wallet = Wallet(1000)
        wallet.place_bet(100)
        wallet.win_bet()
        self.assertEqual(wallet.cash, 1100)

    def test_wallet_blackJack(self):
        wallet = Wallet(1000)
        wallet.place_bet(100)
        wallet.blackJack()
        self.assertEqual(wallet.cash, 1300)

    def test_wallet_lose_bet(self):
        wallet = Wallet(1000)
        wallet.place_bet(100)
        wallet.lose_bet()
        self.assertEqual(wallet.cash, 900)

    def test_wallet_clear_bet(self):
        wallet = Wallet(1000)
        wallet.clear_bet()
        self.assertEqual(wallet.bet, 0)

    def test_wallet_tie(self):
        wallet = Wallet(1000)
        wallet.tie()
        self.assertEqual(wallet.cash, 1000)

if __name__ == '__main__':
    unittest.main()
