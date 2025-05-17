import streamlit as st
from calculate_winrate import simulate_winrate_shift_montecarlo, run_monte_carlo_simulation
from utils import parse_card_input
import pandas as pd

st.set_page_config(page_title="Winrate Analysis Tool", layout="wide")
st.title("テキサスホールデム 勝率変動分析ツール（相対変化表示つき）")

st.markdown("### プレイヤーのハンドを選択")
cols = st.columns(2)
card1 = cols[0].selectbox("カード1", parse_card_input())
card2 = cols[1].selectbox("カード2", parse_card_input())

st.markdown("### ボードカードを選択（3〜4枚）")
board_cols = st.columns(5)
board = []
for i in range(5):
    card = board_cols[i].selectbox(f"カード{i+1}", [""] + parse_card_input())
    if card:
        board.append(card)

st.markdown("### モンテカルロ試行回数")
num_simulations = st.selectbox("試行回数", [10000, 50000, 100000, 200000], index=2)

if st.button("勝率変動を計算開始"):
    if len(board) not in [3, 4]:
        st.warning("フロップ3枚またはターン4枚を指定してください。")
    else:
        st.info("計算中...（完了まで数分かかることがあります）")

        # 基準勝率（次カードなし）
        base_winrate = run_monte_carlo_simulation(card1, card2, board, [], num_simulations)

        # 次カードごとの勝率
        df = simulate_winrate_shift_montecarlo(card1, card2, board, [], num_simulations)

        # 相対変化列を追加
        df['Diff'] = df['Winrate'] - base_winrate

        st.success(f"計算完了！（基準勝率: {base_winrate:.2f}％）")
        st.dataframe(df.sort_values(by='Diff', ascending=False))

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("CSVをダウンロード", csv, file_name="winrate_shift_relative.csv", mime="text/csv")
