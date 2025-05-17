import streamlit as st
from calculate_winrate import simulate_winrate_shift_montecarlo
from utils import parse_card_input
import pandas as pd

st.set_page_config(page_title="Winrate Analysis Tool", layout="wide")
st.title("テキサスホールデム 勝率変動分析ツール")

st.markdown("### プレイヤーのハンドを選択")
cols = st.columns(2)
card1 = cols[0].selectbox("カード1", parse_card_input())
card2 = cols[1].selectbox("カード2", parse_card_input())

st.markdown("### ボード（フロップ3枚）を選択")
board_cols = st.columns(3)
board = []
for i in range(3):
    card = board_cols[i].selectbox(f"ボード{i+1}", [""] + parse_card_input())
    if card:
        board.append(card)

st.markdown("### モンテカルロ試行回数")
num_simulations = st.selectbox("試行回数", [10000, 50000, 100000, 200000], index=2)

if st.button("勝率変動を計算開始"):
    if len(board) != 3:
        st.warning("フロップ3枚を指定してください。")
    else:
        st.info("計算中...（完了まで数分かかることがあります）")
        df = simulate_winrate_shift_montecarlo(card1, card2, board, [], num_simulations)
        st.success("計算完了！")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("CSVをダウンロード", csv, file_name="winrate_shift.csv", mime="text/csv")
