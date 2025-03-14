import os

from dotenv import load_dotenv
from openai import OpenAI

# 環境変数を読み込む
load_dotenv()

# APIキーを取得
api_key = os.getenv("OPENAI_API_KEY")


def get_llm_response(instructions, input_text):
    # クライアントインスタンスを作成
    client = OpenAI(api_key=api_key)

    try:
        response = client.responses.create(
            model="gpt-4o",
            instructions=instructions,
            input=input_text,
        )
        return response
    except Exception as e:
        error_message = str(e)
        if "429" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        return f"エラーが発生しました: {error_message}"


if __name__ == "__main__":
    instructions = "あなたは漢方の専門家です。"
    input_text = "花粉症にはどんな漢方が効きますか。"
    response = get_llm_response(instructions, input_text)
    print(response.output_text)
