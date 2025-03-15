"""
chat = model.start_chat(history=[]) で、空の会話履歴を持つチャットセッションを作成します。
chat.send_message を実行したあと、 chat オブジェクトは会話の文脈を保持しています。
なので、次のメッセージを送信する準備が整います。
"""

import os

import google.generativeai as genai
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "gemini-1.5-pro",
    generation_config={
        "temperature": 0.7,  # 0.0〜1.0の間で設定（デフォルトは0.9）
    }
)

chat = model.start_chat(history=[])

response = chat.send_message("私の名前は山田太郎です。名前占いをして！")

print(response.text)

# 会話を続ける
response2 = chat.send_message("あなたは、私の名前を知っていますか？")
print("\n2回目の応答:")

print(response2.text)
