import os
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを取得
api_key = os.getenv("OPENAI_API_KEY")

# クライアントインスタンスを作成
client = OpenAI(api_key=api_key)

# 会話履歴を配列で管理
messages = [
    {"role": "system", "content": "あなたは姓名占いをする占い師です。大吉,中吉,吉,凶のうちのひとつを回答します。"},
    {"role": "user", "content": "私の名前は山田太郎です。私の名前を占って！"}
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    temperature=0.7,
)

print(response.choices[0].message.content)

# 会話を続ける場合は、応答を履歴に追加
messages.append({"role": "assistant", "content": response.choices[0].message.content})
# 次のユーザー入力を追加
messages.append({"role": "user", "content": "あなたは私の名前を知っていますか。"})

print(messages)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
)

print(response.choices[0].message.content)

