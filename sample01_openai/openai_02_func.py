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

    response = client.responses.create(
        model="gpt-4o",
        instructions=instructions,
        input=input_text,
    )
    return response


if __name__ == "__main__":
    instructions = "あなたは漢方の専門家です。"
    input_text = "花粉症にはどんな漢方が効きますか。"
    response = get_llm_response(instructions, input_text)
    print(response.output_text)
