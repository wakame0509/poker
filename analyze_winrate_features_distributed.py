import pandas as pd
import argparse
from calculate_winrate import simulate_winrate_shift_montecarlo
from utils import generate_deck
import os

parser = argparse.ArgumentParser()
parser.add_argument('--hand-range', type=str, default="0-168", help="例: 0-50")
parser.add_argument('--board-index', type=int, default=None, help="ボードパターン番号（0-9）")
parser.add_argument('--output', type=str, default='result_part.csv', help="出力CSVファイル名")
args = parser.parse_args()

NUM_SIMULATIONS = 100000
SELECTED_RANGE = []

# 読み込むボードパターンCSV
board_df = pd.read_csv("optimized_board_patterns.csv")
board_patterns = board_df.values.tolist()

# 169ハンド生成
def generate_all_hands():
    ranks = 'A K Q J T 9 8 7 6 5 4 3 2'.split()
    hands = []
    for i, r1 in enumerate(ranks):
        for j, r2 in enumerate(ranks):
            if i < j:
                hands.append(f"{r1}{r2}s")
            elif i > j:
                hands.append(f"{r2}{r1}o")
            else:
                hands.append(f"{r1}{r1}")
    return hands

def analyze_features(hand, next_card, board):
    features = {
        'SetCompleted': False,
        'OvercardAppeared': False,
        'StraightCompleted': False,
    }
    ranks = '2 3 4 5 6 7 8 9 T J Q K A'.split()

    if next_card[0] == hand[0]:
        features['SetCompleted'] = True

    if ranks.index(next_card[0]) < ranks.index(hand[0]):
        features['OvercardAppeared'] = True

    combined_ranks = set([hand[0], hand[1]] + [c[0] for c in board] + [next_card[0]])
    for i in range(len(ranks) - 4):
        if set(ranks[i:i+5]).issubset(combined_ranks):
            features['StraightCompleted'] = True

    return features

# 実行処理
all_hands = generate_all_hands()
start_idx, end_idx = map(int, args.hand_range.split('-'))
target_hands = all_hands[start_idx:end_idx+1]
target_boards = [board_patterns[args.board_index]] if args.board_index is not None else board_patterns

results = []
for hand in target_hands:
    for board in target_boards:
        df = simulate_winrate_shift_montecarlo(
            hand[0] + 's',
            hand[1] + ('h' if 'o' in hand else 's'),
            board,
            SELECTED_RANGE,
            NUM_SIMULATIONS
        )

        for _, row in df.iterrows():
            features = analyze_features(hand, row['Card'], board)
            results.append({
                'Hand': hand,
                'Board': ''.join(board),
                'NextCard': row['Card'],
                'Winrate': row['Winrate'],
                **features
            })

df_out = pd.DataFrame(results)
df_out.to_csv(args.output, index=False)
print(f"保存完了: {args.output}")
