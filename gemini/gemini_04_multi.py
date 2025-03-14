import os

import google.generativeai as genai
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# モデルの設定
# 利用可能なモデルリストから確認したモデル名を使用
# Gemini 1.5 Proを使用
model = genai.GenerativeModel("gemini-1.5-pro")

# 会話履歴を保存するリスト
conversation_history = []


def generate_text(prompt, history):
    """Gemini APIを使用してテキストを生成する関数"""
    if not prompt or prompt.strip() == "":
        return "空の入力は処理できません。何か入力してください。"

    try:
        # ヒストリーを含めて会話の文脈を維持
        response = model.generate_content(history + [{"role": "user", "parts": [prompt]}])
        return response.text
    except Exception as e:
        error_message = str(e)
        if "429" in error_message and "Resource has been exhausted" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        return f"エラーが発生しました: {error_message}"


def main():
    print("Gemini APIを使用したテキスト生成プログラム")
    print("終了するには 'exit' と入力してください")
    print("履歴を表示するには 'history' と入力してください")
    print("履歴をクリアするには 'clear' と入力してください")

    # 会話履歴のフォーマット用リスト
    chat_history = []

    while True:
        user_input = input("\nプロンプトを入力してください: ")

        if user_input.lower() == "exit":
            print("プログラムを終了します")
            break

        if user_input.lower() == "history":
            print("\n===== 会話履歴 =====")
            for i, message in enumerate(conversation_history):
                role = "User" if i % 2 == 0 else "Agent"
                print(f"{role}: {message}")
            print("===================")
            continue

        if user_input.lower() == "clear":
            conversation_history.clear()
            chat_history.clear()
            print("会話履歴をクリアしました")
            continue

        if not user_input or user_input.strip() == "":
            print("空の入力は処理できません。何か入力してください。")
            continue

        # ユーザー入力を履歴に追加
        conversation_history.append(user_input)
        chat_history.append({"role": "user", "parts": [user_input]})

        print("\n回答を生成中...\n")
        response = generate_text(user_input, chat_history)

        # エージェントの応答を履歴に追加
        conversation_history.append(response)
        chat_history.append({"role": "model", "parts": [response]})

        print(response)


if __name__ == "__main__":
    main()