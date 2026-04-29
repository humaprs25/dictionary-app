import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta, timezone
import csv
import io

# タイムゾーンの設定 (日本時間)
JST = timezone(timedelta(hours=+9), 'JST')

# APIキーとAIの設定
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("🌐 3ヶ国語 辞書＆例文アプリ")
st.write("日本語、英語、スペイン語のいずれかの単語を入力してください。")

# 履歴を保存する「箱」を準備
if 'history' not in st.session_state:
    st.session_state.history = []

word = st.text_input("検索する単語を入力:")

if st.button("意味を調べる"):
    if word:
        # --- エラーが起きてもアプリを落とさない仕組み（try-except） ---
        try:
                        # AIへの指示（プロンプト）
            prompt = f"""
            あなたは優秀な多言語辞書アシスタントです。
            以下の単語の言語を判別し、まずはその単語の【語源や成り立ち】を学習者が覚えやすいようにわかりやすく説明してください。
            次に、その単語の【発音記号】と、日本人が発音する際のコツ（または近いカタカナ読み）を教えてください。
            その後、必ず【英語 → スペイン語 → 日本語】の順番で、それぞれの意味と例文（対訳つき）を出力してください。
            見やすく整理されたフォーマットにしてください。

            単語: {word}
            """

            # ストリーミング出力（文字をパラパラ出す）
            response = model.generate_content(prompt, stream=True)
            
            message_placeholder = st.empty()
            full_text = ""
            
            for chunk in response:
                full_text += chunk.text
                message_placeholder.markdown(full_text)

            # 履歴に追加
            now = datetime.now(JST).strftime("%Y/%m/%d %H:%M")
            st.session_state.history.append({
                "検索日時": now,
                "単語": word
            })
            
        except Exception as e:
            # エラーが起きた時の優しいメッセージ
            st.error("⚠️ AIが少し疲れているようです（利用制限）。1〜2分待ってからもう一度試してください！")
            
    else:
        st.warning("単語を入力してください！")

# 履歴の表示とダウンロード
if len(st.session_state.history) > 0:
    st.divider()
    st.subheader("📚 今日の検索履歴")
    st.table(st.session_state.history)

    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=["検索日時", "単語"])
    writer.writeheader()
    writer.writerows(st.session_state.history)

    st.download_button(
        label="📥 履歴をダウンロード (CSV)",
        data=csv_buffer.getvalue(),
        file_name="dictionary_history.csv",
        mime="text/csv"
    )
