import os

from anthropic import Anthropic
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを取得
api_key = os.getenv("ANTHROPIC_API_KEY")

# クライアントインスタンスを作成
client = Anthropic(api_key=api_key)


def get_claude_response(user_prompt):
    try:
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
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"


if __name__ == "__main__":
    while True:
        user_prompt = input("あなたの名前を入力してください (終了するには 'exit' と入力): ")
        if user_prompt.lower() == "exit":
            break
        response = get_claude_response(user_prompt)
        response_text = response.content[0].text
        print(response_text)
        print("-" * 50)
