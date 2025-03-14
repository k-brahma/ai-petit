import os

import openai
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# モデルの設定
# GPT-4 Turboを使用
MODEL = "gpt-4-turbo"


def generate_text(prompt):
    """OpenAI APIを使用してテキストを生成する関数"""
    if not prompt or prompt.strip() == "":
        return "空の入力は処理できません。何か入力してください。"

    try:
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "あなたは役立つAIアシスタントです。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        error_message = str(e)
        if "429" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        return f"エラーが発生しました: {error_message}"


def main():
    print("OpenAI APIを使用したテキスト生成プログラム")
    print("終了するには 'exit' と入力してください")

    while True:
        user_input = input("\nプロンプトを入力してください: ")

        if user_input.lower() == "exit":
            print("プログラムを終了します")
            break

        if not user_input or user_input.strip() == "":
            print("空の入力は処理できません。何か入力してください。")
            continue

        print("\n回答を生成中...\n")
        response = generate_text(user_input)
        print(response)


if __name__ == "__main__":
    main() 