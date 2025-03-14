import os
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを取得
api_key = os.getenv("OPENAI_API_KEY")

# クライアントインスタンスを作成
client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-4o",
    instructions="あなたは漢方の専門家です。",
    input="花粉症にはどんな漢方が効きますか。",
)

print(response.output_text)

