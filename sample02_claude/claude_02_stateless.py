import os

import anthropic
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    system="あなたは姓名占いをする占い師です。大吉,中吉,吉,凶のうちのひとつを回答します。",
    messages=[
        {"role": "user", "content": "私の名前は山田太郎です。私の名前を占って！"}
    ],
    temperature=0.7,
)

print(response.content[0].text)

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    system="あなたは姓名占いをする占い師です。大吉,中吉,吉,凶のうちのひとつを回答します。",
    messages=[
        {"role": "user", "content": "私の名前を覚えていますか？"}
    ],
    temperature=0.7,
)

print(response.content[0].text)
