import streamlit as st
import google.generativeai as genai

# Streamlitの裏側からAPIキーを読み込む設定
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 使うAIモデルの指定
model = genai.GenerativeModel('gemini-1.5-flash')

# 画面のデザイン
st.title("🌐 3ヶ国語 辞書＆例文アプリ")
st.write("日本語、英語、スペイン語のいずれかの単語を入力してください。")

# 入力欄とボタン
word = st.text_input("検索する単語を入力:")

if st.button("意味を調べる"):
    if word:
        with st.spinner('AIが3ヶ国語の辞書を作成中...'):
            # AIへの指示（プロンプト）
            prompt = f"""
            あなたは優秀な多言語辞書アシスタントです。
            以下の単語の言語を判別し、日本語、英語、スペイン語の3言語で意味と例文（対訳つき）を出力してください。
            見やすく整理されたフォーマットで出力してください。

            単語: {word}
            """
            # AIから回答をもらって画面に出力
            response = model.generate_content(prompt)
            st.write(response.text)
    else:
        st.warning("単語を入力してください！")
