import os
from datetime import datetime

from anthropic import Anthropic
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを取得
api_key = os.getenv("ANTHROPIC_API_KEY")

# クライアントインスタンスを作成
client = Anthropic(api_key=api_key)

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


def format_messages_for_api():
    """APIリクエスト用に履歴をフォーマットする関数"""
    # APIに送信するメッセージのみを抽出（最大10件程度に制限）
    messages = []
    for entry in conversation_history[-20:]:  # 直近20件までの履歴を使用
        if entry["role"] in ["user", "assistant"]:
            messages.append({
                "role": entry["role"],
                "content": entry["content"]
            })
    return messages


def get_claude_response(input_text):
    """Claude APIを使用して応答を取得する関数"""
    try:
        # 会話履歴をフォーマット
        messages = format_messages_for_api()

        messages.append({"role": "user", "content": input_text})

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            system="あなたは姓名占いをする占い師です。大吉,中吉,吉,凶のうちのひとつを回答します。",
            messages=messages,
            temperature=0.7,
        )
        return response
    except Exception as e:
        error_message = f"エラーが発生しました: {str(e)}"
        return error_message


if __name__ == "__main__":
    print("姓名判断プログラムを開始します")
    print("特別コマンド:")
    print("  - 'history': 会話履歴を表示")
    print("  - 'clear': 会話履歴をクリア")
    print("  - 'exit': プログラムを終了")

    while True:
        user_prompt = input("\nあなたの氏名を入力してください: ")

        # 特別コマンドの処理
        if user_prompt.lower() == "exit":
            print("プログラムを終了します")
            break
        elif user_prompt.lower() == "history":
            print(display_history())
            continue
        elif user_prompt.lower() == "clear":
            print(clear_history())
            continue

        if not user_prompt or user_prompt.strip() == "":
            print("空の入力は処理できません。何か入力してください。")
            continue

        # ユーザー入力を履歴に追加
        add_to_history("user", user_prompt)

        print("\n回答を生成中...\n")
        response = get_claude_response(user_prompt)

        # レスポンスがオブジェクトの場合と文字列の場合で処理を分ける
        if isinstance(response, str):
            # エラーメッセージの場合
            print(response)
            add_to_history("system", response)  # エラーはシステムメッセージとして保存
        else:
            # 正常なレスポンスの場合
            response_text = response.content[0].text
            print(response_text)
            add_to_history("assistant", response_text)

        print("-" * 50)
