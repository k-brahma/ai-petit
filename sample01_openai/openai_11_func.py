import os

from dotenv import load_dotenv
from openai import OpenAI

# 環境変数を読み込む
load_dotenv()

# APIキーを取得
api_key = os.getenv("OPENAI_API_KEY")


def get_llm_response(system_prompt, user_prompt):
    # クライアントインスタンスを作成
    client = OpenAI(api_key=api_key)

    # 会話履歴をリストで管理
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7,
    )
    return response


if __name__ == "__main__":
    system_prompt = "あなたは姓名占いをする占い師です。大吉,中吉,吉,凶のうちのひとつを回答します。"
    user_prompt = "私の名前は山田太郎です。私の名前を占って！"
    response = get_llm_response(system_prompt, user_prompt)
    print(response.choices[0].message.content)
