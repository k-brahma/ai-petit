import os

import anthropic
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)


def generate_text(user_prompt):
    """Claude APIを使用してテキストを生成する関数"""
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        system="あなたは姓名占いをする占い師です。大吉,中吉,吉,凶のうちのひとつを回答します。",
        messages=[
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
    )
    return response


response = generate_text("私の名前は山田太郎です。私の名前を占って！")

print(response.content[0].text)
