import streamlit as st
import pandas as pd
from datetime import date
import os

# タイトル
st.title("ゴルフ・メモ帳（ユーザー別）")

# ユーザー名入力
username = st.text_input("お名前を入力してください（例：taro）")

# 入力があるときのみ続行
if username:
    filename = f"{username}_golf_memo_list.csv"

    # CSV読み込み（空ファイル対策付き）
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame(columns=["No", "日付", "気になった事", "試した事", "重要"])

    # 入力フォーム
    with st.form("task_form"):
        task = st.text_input("気になった事")
        document = st.text_input("試した事")
        submitted = st.form_submit_button("新規追加")
        if submitted:
            if len(df) >= 30:
                st.warning("最大30件までです。古いメモを削除してください。")
            elif task:
                new_task = {
                    "No": len(df) + 1,
                    "日付": date.today().isoformat(),
                    "気になった事": task,
                    "試した事": document,
                    "重要": False,
                }
                df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)
                df["No"] = range(1, len(df) + 1)
                df.to_csv(filename, index=False)
                st.rerun()

    # 表示と操作
    for i, row in df.iterrows():
        cols = st.columns([1, 2, 3, 2, 1, 1])
        cols[0].write(int(row["No"]))
        cols[1].write(row["日付"])
        cols[2].write(row["気になった事"])
        cols[3].write(row["試した事"])
        done = cols[4].checkbox("重要", value=row["重要"], key=f"done_{i}")
        delete = cols[5].button("削除", key=f"delete_{i}")

        if done != row["重要"]:
            df.at[i, "重要"] = done
            df.to_csv(filename, index=False)

        if delete:
            df = df.drop(index=i).reset_index(drop=True)
            df["No"] = range(1, len(df) + 1)
            df.to_csv(filename, index=False)
            st.rerun()
else:
    st.info("はじめにお名前を入力してください。")