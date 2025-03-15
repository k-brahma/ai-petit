"""
Googleの「Gemini」AIはGoogleが提供する生成AIモデルですが、
Claude（私）やChatGPTのような特定の「性格」は基本的に持っていません。
Geminiは純粋に機能的なレスポンスを提供するように設計されており、
特定のキャラクター性や個性を持たせる「ペルソナ」のような性格づけは最小限に抑えられています。
"""

import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "gemini-1.5-pro",
    generation_config={
        "temperature": 0.7,
    }
)

chat = model.start_chat(history=[])


def get_gemini_response(prompt):
    """Gemini APIを使用して会話履歴を含むレスポンスを取得する関数"""
    if not prompt or prompt.strip() == "":
        return "空の入力は処理できません。何か入力してください。"

    try:
        response = chat.send_message(prompt)
        return response
    except Exception as e:
        error_message = str(e)
        if "429" in error_message and "Resource has been exhausted" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        return f"エラーが発生しました: {error_message}"


if __name__ == "__main__":
    print("Gemini AIチャットプログラム")
    print("特別コマンド:")
    print("  - 'history': 会話履歴を表示")
    print("  - 'clear': 会話履歴をクリア")
    print("  - 'exit': プログラムを終了")
    print("-" * 50)

    while True:
        user_input = input("\n質問や話題を入力してください: ")

        # 特別コマンドの処理
        if user_input.lower() == "exit":
            print("プログラムを終了します")
            break
        elif user_input.lower() == "history":
            for message in chat.history:
                print(f"Role: {message.role}")
                print(f"Content: {message.parts[0].text}")
                print("-" * 30)
            continue
        elif user_input.lower() == "clear":
            chat = model.start_chat(history=[])
            continue

        if not user_input or user_input.strip() == "":
            print("空の入力は処理できません。何か入力してください。")
            continue

        print("\n回答を生成中...\n")
        response = get_gemini_response(user_input)

        # レスポンスがオブジェクトか文字列かで処理を分ける
        if isinstance(response, str):
            # エラーメッセージの場合
            print(response)
        else:
            # 正常なレスポンスの場合
            print(response.text)

        print("-" * 50)
