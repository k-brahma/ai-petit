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

# 会話履歴を保存するリスト
conversation_history = []


def generate_text(prompt, messages):
    """Claude APIを使用してテキストを生成する関数"""
    if not prompt or prompt.strip() == "":
        return "空の入力は処理できません。何か入力してください。"

    try:
        # 会話履歴を含めてAPIを呼び出す
        response = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            messages=messages + [{"role": "user", "content": prompt}],
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
    print("履歴を表示するには 'history' と入力してください")
    print("履歴をクリアするには 'clear' と入力してください")

    # API用の会話履歴
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

        print("\n回答を生成中...\n")
        response = generate_text(user_input, chat_history)
        
        # エージェントの応答を履歴に追加
        conversation_history.append(response)
        
        # API用の会話履歴も更新
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": response})
        
        print(response)


if __name__ == "__main__":
    main()