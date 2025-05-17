import random
import pandas as pd
import eval7
from utils import evaluate_hand, generate_deck, remove_known_cards

def run_monte_carlo_simulation(p1_card1, p1_card2, board, selected_range, num_simulations, next_card=None):
    wins = 0
    ties = 0

    deck = generate_deck()
    known_cards = [p1_card1, p1_card2] + board
    if next_card:
        known_cards.append(next_card)
    deck = remove_known_cards(deck, known_cards)

    if len(deck) < 2:
        return 0  # デッキ不足対策

    for _ in range(num_simulations):
        sim_deck = deck.copy()
        random.shuffle(sim_deck)

        if selected_range:
            opp_hand = random.sample(selected_range, 1)[0]
        else:
            if len(sim_deck) < 2:
                continue
            opp_hand = [sim_deck.pop(), sim_deck.pop()]

        if len(sim_deck) < (5 - len(board)):
            continue

        remaining_board = board + [sim_deck.pop() for _ in range(5 - len(board))]

        p1_hand = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in remaining_board]
        p2_hand = [eval7.Card(opp_hand[0]), eval7.Card(opp_hand[1])] + [eval7.Card(c) for c in remaining_board]

        p1_score = evaluate_hand(p1_hand)
        p2_score = evaluate_hand(p2_hand)

        if p1_score > p2_score:
            wins += 1
        elif p1_score == p2_score:
            ties += 1

    winrate = (wins + ties / 2) / num_simulations * 100
    return winrate


def simulate_winrate_shift_montecarlo(p1_card1, p1_card2, board, selected_range, num_simulations):
    results = []
    deck = generate_deck()
    known_cards = [p1_card1, p1_card2] + board
    deck = remove_known_cards(deck, known_cards)

    for card in deck:
        hypothetical_board = board + [card]
        if len(hypothetical_board) > 5:
            continue

        winrate = run_monte_carlo_simulation(
            p1_card1, p1_card2, board, selected_range, num_simulations, next_card=card
        )
        results.append({'Card': card, 'Winrate': winrate})

    df = pd.DataFrame(results).sort_values(by='Winrate', ascending=False)
    return df
