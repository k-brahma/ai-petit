"""
Googleの「Gemini」AIはGoogleが提供する生成AIモデルですが、
Claude（私）やChatGPTのような特定の「性格」は基本的に持っていません。
Geminiは純粋に機能的なレスポンスを提供するように設計されており、
特定のキャラクター性や個性を持たせる「ペルソナ」のような性格づけは最小限に抑えられています。
"""

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
# モデルの設定 - temperatureパラメータを追加
model = genai.GenerativeModel(
    "gemini-1.5-pro",
    generation_config={
        "temperature": 0.7,  # 0.0〜1.0の間で設定（デフォルトは0.9）
    }
)


def generate_text(prompt):
    """Gemini APIを使用してテキストを生成する関数"""
    if not prompt or prompt.strip() == "":
        return "空の入力は処理できません。何か入力してください。"

    try:
        response = model.generate_content(prompt)
        return response
    except Exception as e:
        error_message = str(e)
        if "429" in error_message and "Resource has been exhausted" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        return f"エラーが発生しました: {error_message}"


if __name__ == "__main__":
    print("Gemini AIチャットプログラム")
    print("終了するには 'exit' と入力してください")
    print("-" * 50)

    while True:
        user_input = input("\n質問や話題を入力してください: ")

        if user_input.lower() == "exit":
            print("プログラムを終了します")
            break

        if not user_input or user_input.strip() == "":
            print("空の入力は処理できません。何か入力してください。")
            continue

        print("\n回答を生成中...\n")
        response = generate_text(user_input)

        # レスポンスがオブジェクトか文字列かで処理を分ける
        if isinstance(response, str):
            # エラーメッセージの場合
            print(response)
        else:
            # 正常なレスポンスの場合
            print(response.text)

        print("-" * 50)