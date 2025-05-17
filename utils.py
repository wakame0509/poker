import eval7

def evaluate_hand(cards):
    return eval7.evaluate(cards)

def generate_deck():
    ranks = '23456789TJQKA'
    suits = 'cdhs'
    return [r + s for r in ranks for s in suits]

def remove_known_cards(deck, known_cards):
    return [card for card in deck if card not in known_cards]

def parse_card_input():
    ranks = '2 3 4 5 6 7 8 9 T J Q K A'.split()
    suits = 'c d h s'.split()
    return [r + s for r in ranks for s in suits]
