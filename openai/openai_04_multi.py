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

# 会話履歴を保存するリスト
conversation_history = []

def generate_text(prompt, messages):
    """OpenAI APIを使用してテキストを生成する関数"""
    if not prompt or prompt.strip() == "":
        return "空の入力は処理できません。何か入力してください。"

    try:
        # システムメッセージを先頭に追加し、残りの会話履歴とユーザーの新しい入力を含める
        current_messages = [{"role": "system", "content": "あなたは役立つAIアシスタントです。"}] + messages + [{"role": "user", "content": prompt}]
        
        response = openai.chat.completions.create(
            model=MODEL,
            messages=current_messages,
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
    print("履歴を表示するには 'history' と入力してください")
    print("履歴をクリアするには 'clear' と入力してください")

    # OpenAI API用のメッセージ履歴リスト
    messages_history = []

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
            messages_history.clear()
            print("会話履歴をクリアしました")
            continue

        if not user_input or user_input.strip() == "":
            print("空の入力は処理できません。何か入力してください。")
            continue

        # ユーザー入力を履歴に追加
        conversation_history.append(user_input)

        print("\n回答を生成中...\n")
        response = generate_text(user_input, messages_history)
        
        # エージェントの応答を履歴に追加
        conversation_history.append(response)
        
        # API用の会話履歴も更新
        messages_history.append({"role": "user", "content": user_input})
        messages_history.append({"role": "assistant", "content": response})
        
        print(response)


if __name__ == "__main__":
    main()