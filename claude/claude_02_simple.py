import os

import anthropic
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

# モデルの設定
# Claude 3 Sonnetを使用
MODEL = "claude-3-5-sonnet-20241022"


def generate_text(prompt):
    """Claude APIを使用してテキストを生成する関数"""
    if not prompt or prompt.strip() == "":
        return "空の入力は処理できません。何か入力してください。"

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.content[0].text
    except Exception as e:
        error_message = str(e)
        if "429" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        return f"エラーが発生しました: {error_message}"


def main():
    print("Claude APIを使用したテキスト生成プログラム")
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