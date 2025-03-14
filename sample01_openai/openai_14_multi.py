import os
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI

# 環境変数を読み込む
load_dotenv()

# APIキーを取得
api_key = os.getenv("OPENAI_API_KEY")

# クライアントインスタンスを作成
client = OpenAI(api_key=api_key)

# メモリ内に会話履歴を保持するリスト
conversation_history = []


def add_to_history(role, content):
    """会話をメモリ内の履歴に追加する関数"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conversation_history.append({
        "timestamp": timestamp,
        "role": role,
        "content": content
    })


def display_history():
    """メモリ内の会話履歴を表示する関数"""
    if not conversation_history:
        return "履歴はまだありません。"

    result = "=== 会話履歴 ===\n"
    for i, entry in enumerate(conversation_history, 1):
        result += f"\n[{i}] {entry['timestamp']}\n"
        result += f"役割: {entry['role']}\n"
        result += f"内容: {entry['content'][:100]}...\n" if len(
            entry['content']) > 100 else f"内容: {entry['content']}\n"
        result += "-" * 40 + "\n"

    return result


def clear_history():
    """会話履歴をクリアする関数"""
    conversation_history.clear()
    return "履歴をクリアしました。"


def format_history_for_api():
    """APIリクエスト用に会話履歴をフォーマットする関数"""
    messages = []
    for entry in conversation_history:
        if entry["role"] in ["user", "assistant"]:
            messages.append({
                "role": entry["role"],
                "content": entry["content"]
            })
    return messages


def get_llm_response(instructions, input_text):
    """OpenAI APIを使用してレスポンスを取得する関数"""
    try:
        # 会話履歴をフォーマット
        messages = format_history_for_api()

        # 新しい入力を追加
        messages.append({"role": "user", "content": input_text})

        # APIリクエスト
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": instructions}] + messages,
            temperature=0.7,
        )

        return response.choices[0].message.content
    except Exception as e:
        error_message = str(e)
        if "429" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        return f"エラーが発生しました: {error_message}"


if __name__ == "__main__":
    print("姓名判断プログラムを開始します")
    print("特別コマンド:")
    print("  - 'history': 会話履歴を表示")
    print("  - 'clear': 会話履歴をクリア")
    print("  - 'exit': プログラムを終了")

    # システム指示をセット（履歴には残さない）
    system_prompt = "あなたは姓名占いをする占い師です。大吉,中吉,吉,凶のうちのひとつを回答します。"

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
        response = get_llm_response(system_prompt, user_prompt)

        # レスポンスがオブジェクトの場合とテキストの場合で処理を分ける
        if hasattr(response, 'choices'):
            output_text = response.choices[0].message.content
            print(output_text)
        else:
            # エラーメッセージなどの場合
            print(response)

        # 応答を履歴に追加
        add_to_history("assistant", response)