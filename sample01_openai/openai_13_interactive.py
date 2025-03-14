import os

from dotenv import load_dotenv
from openai import OpenAI

# 環境変数を読み込む
load_dotenv()

# APIキーを取得
api_key = os.getenv("OPENAI_API_KEY")


def get_llm_response(system_prpmpt, user_prompt):
    # クライアントインスタンスを作成
    client = OpenAI(api_key=api_key)

    # 会話履歴を配列で管理
    messages = [
        {"role": "system", "content": system_prpmpt},
        {"role": "user", "content": user_prompt},
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
        )
        return response
    except Exception as e:
        error_message = str(e)
        if "429" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        return f"エラーが発生しました: {error_message}"


if __name__ == "__main__":
    print("姓名判断プログラムを開始します")
    print("終了するには 'exit' と入力してください")

    system_prompt = "あなたは姓名占いをする占い師です。大吉,中吉,吉,凶のうちのひとつを回答します。"

    while True:
        user_prompt = input("\nあなたの氏名を入力してください: ")

        # exitコマンドの処理
        if user_prompt.lower() == "exit":
            print("プログラムを終了します")
            break

        if not user_prompt or user_prompt.strip() == "":
            print("空の入力は処理できません。何か入力してください。")
            continue

        print("\n回答を生成中...\n")
        response = get_llm_response(system_prompt, user_prompt)

        # レスポンスがオブジェクトの場合とテキストの場合で処理を分ける
        if hasattr(response, 'choices'):
            output_text = response.choices[0].message.content
            print(output_text)
        else:
            # エラーメッセージなどの場合
            print(response)
