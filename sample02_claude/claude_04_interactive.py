import os

from anthropic import Anthropic
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを取得
api_key = os.getenv("ANTHROPIC_API_KEY")

# クライアントインスタンスを作成
client = Anthropic(api_key=api_key)


def get_claude_response(input_text):
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            system="あなたは日本の伝統的な漢方医学の専門家です。長年の研究と臨床経験を持ち、東洋医学の知識が豊富です。"
                   "質問に対して科学的根拠と伝統的な知恵の両方を活用して回答してください。"
                   "患者の体質や症状に合わせた漢方薬の選び方、食事療法、生活習慣のアドバイスなどを提供できます。"
                   "専門的でありながらも一般の人にもわかりやすい説明を心がけてください。",
            messages=[
                {"role": "user", "content": input_text}
            ],
            temperature=0.7,
        )
        return response
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"


if __name__ == "__main__":
    while True:
        user_input = input("漢方についての質問を入力してください (終了するには 'exit' と入力): ")
        if user_input.lower() == "exit":
            break
        response = get_claude_response(user_input)
        response_text = response.content[0].text
        print(response_text)
        print("-" * 50)
