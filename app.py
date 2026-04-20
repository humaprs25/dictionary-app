import streamlit as st
import google.generativeai as genai

# Streamlitの裏側からAPIキーを読み込む設定
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 使うAIモデルの指定
model = genai.GenerativeModel('gemini-2.5-flash')

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
            以下の単語の言語を判別し、必ず【英語 → スペイン語 → 日本語】の順番で、それぞれの意味と例文（対訳つき）を出力してください。
            見やすく整理されたフォーマットで出力してください。

            単語: {word}
            """
            # ストリーミングで1文字ずつ出す
            response = model.generate_content(prompt, stream=True)
            
            # 文字を次々に追加していくための空の箱（プレースホルダー）を用意
            message_placeholder = st.empty()
            full_text = ""
            
            # AIから少しずつ送られてくる文字を繋げて、画面を更新し続ける
            for chunk in response:
                full_text += chunk.text
                message_placeholder.markdown(full_text)
    else:
        st.warning("単語を入力してください！")
