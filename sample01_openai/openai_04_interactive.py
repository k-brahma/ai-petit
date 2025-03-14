import os
from dotenv import load_dotenv
from openai import OpenAI

# 環境変数を読み込む
load_dotenv()

# APIキーを取得
api_key = os.getenv("OPENAI_API_KEY")

# クライアントインスタンスを作成
client = OpenAI(api_key=api_key)


def get_llm_response(instructions, input_text):
    """OpenAI APIを使用してレスポンスを取得する関数"""
    try:
        response = client.responses.create(
            model="gpt-4o",
            instructions=instructions,
            input=input_text,
        )
        return response
    except Exception as e:
        error_message = str(e)
        if "429" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        return f"エラーが発生しました: {error_message}"


if __name__ == "__main__":
    print("漢方薬についてのチャットプログラム")
    print("終了するには 'exit' と入力してください")

    while True:
        user_input = input("\n漢方薬について何でも聞いてください: ")

        # exitコマンドの処理
        if user_input.lower() == "exit":
            print("プログラムを終了します")
            break

        if not user_input or user_input.strip() == "":
            print("空の入力は処理できません。何か入力してください。")
            continue

        print("\n回答を生成中...\n")
        response = get_llm_response("あなたは漢方の専門家です。", user_input)

        # レスポンスがオブジェクトの場合とテキストの場合で処理を分ける
        if hasattr(response, 'output_text'):
            output_text = response.output_text
            print(output_text)
        else:
            # エラーメッセージなどの場合
            print(response)