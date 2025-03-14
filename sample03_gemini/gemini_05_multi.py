"""
Googleの「Gemini」AIはGoogleが提供する生成AIモデルですが、
Claude（私）やChatGPTのような特定の「性格」は基本的に持っていません。
Geminiは純粋に機能的なレスポンスを提供するように設計されており、
特定のキャラクター性や個性を持たせる「ペルソナ」のような性格づけは最小限に抑えられています。
"""

import os
from datetime import datetime

import google.generativeai as genai
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 会話履歴を保存するリスト
conversation_history = []


def add_to_history(role, content):
    """会話を履歴に追加する関数"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conversation_history.append({
        "timestamp": timestamp,
        "role": role,
        "content": content
    })


def display_history():
    """会話履歴を表示する関数"""
    if not conversation_history:
        return "履歴はまだありません。"

    result = "=== 会話履歴 ===\n"
    for i, entry in enumerate(conversation_history, 1):
        result += f"\n[{i}] {entry['timestamp']}\n"
        result += f"役割: {entry['role']}\n"
        content_preview = entry['content'][:100] + "..." if len(entry['content']) > 100 else entry['content']
        result += f"内容: {content_preview}\n"
        result += "-" * 40 + "\n"

    return result


def clear_history():
    """会話履歴をクリアする関数"""
    conversation_history.clear()
    return "履歴をクリアしました。"


def format_history_for_chat():
    """Gemini API用に会話履歴をフォーマットする関数"""
    # Geminiはチャット履歴をChatオブジェクトで管理
    chat = model.start_chat(history=[])

    # 履歴をチャットに追加
    for entry in conversation_history:
        if entry["role"] == "user":
            chat.history.append({"role": "user", "parts": [entry["content"]]})
        elif entry["role"] == "model":
            chat.history.append({"role": "model", "parts": [entry["content"]]})

    return chat


def get_gemini_response(prompt):
    """Gemini APIを使用して会話履歴を含むレスポンスを取得する関数"""
    if not prompt or prompt.strip() == "":
        return "空の入力は処理できません。何か入力してください。"

    try:
        # 会話履歴がある場合はチャットセッションを使用
        if conversation_history:
            chat = format_history_for_chat()
            response = chat.send_message(prompt)
        else:
            # 初回は通常のレスポンス生成
            response = model.generate_content(prompt)

        return response
    except Exception as e:
        error_message = str(e)
        if "429" in error_message and "Resource has been exhausted" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        return f"エラーが発生しました: {error_message}"


# モデルの設定
model = genai.GenerativeModel(
    "gemini-1.5-pro",
    generation_config={
        "temperature": 0.7,
    }
)

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
            print(display_history())
            continue
        elif user_input.lower() == "clear":
            print(clear_history())
            continue

        if not user_input or user_input.strip() == "":
            print("空の入力は処理できません。何か入力してください。")
            continue

        # ユーザー入力を履歴に追加
        add_to_history("user", user_input)

        print("\n回答を生成中...\n")
        response = get_gemini_response(user_input)

        # レスポンスがオブジェクトか文字列かで処理を分ける
        if isinstance(response, str):
            # エラーメッセージの場合
            print(response)
            add_to_history("system", response)  # エラーはシステムメッセージとして保存
        else:
            # 正常なレスポンスの場合
            print(response.text)
            add_to_history("model", response.text)

        print("-" * 50)