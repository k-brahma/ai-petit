import os

import anthropic
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)


def generate_text(system, prompt):
    """Claude APIを使用してテキストを生成する関数"""
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            system="あなたは日本の伝統的な漢方医学の専門家です。長年の研究と臨床経験を持ち、東洋医学の知識が豊富です。"
                   "質問に対して科学的根拠と伝統的な知恵の両方を活用して回答してください。"
                   "患者の体質や症状に合わせた漢方薬の選び方、食事療法、生活習慣のアドバイスなどを提供できます。"
                   "専門的でありながらも一般の人にもわかりやすい説明を心がけてください。",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response
    except Exception as e:
        error_message = str(e)
        if "429" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        return f"エラーが発生しました: {error_message}"


if __name__ == "__main__":
    system = "あなたは漢方の専門家です。"
    prompt = "花粉症にはどんな漢方が効きますか。"
    response = generate_text(system, prompt)
    print(response.content[0].text)