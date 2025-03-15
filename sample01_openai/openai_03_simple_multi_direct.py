import os
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを取得
api_key = os.getenv("OPENAI_API_KEY")

# クライアントインスタンスを作成
client = OpenAI(api_key=api_key)

# 会話履歴をリストで管理
messages = [
    {"role": "system", "content": "あなたは姓名占いをする占い師です。大吉,中吉,吉,凶のうちのひとつを回答します。"},
    {"role": "user", "content": "私の名前は山田太郎です。私の名前を占って！"},
    {"role": "assistant", "content": "山田太郎さんですね。大吉です。"},
    {"role": "user", "content": "私の名前についてもっといろいろ説明してください。"}
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    temperature=0.7,
)

print(response.choices[0].message.content)
