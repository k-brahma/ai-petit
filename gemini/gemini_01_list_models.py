import os

import google.generativeai as genai
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


def main():
    print("利用可能なGeminiモデルのリスト:")
    print("=" * 50)

    try:
        # 利用可能なモデルをリストアップ
        models = genai.list_models()

        for model in models:
            print(f"モデル名: {model.name}")
            print(f"表示名: {model.display_name}")
            print(f"説明: {model.description}")
            print(f"入力モード: {model.input_token_limit}")
            print(f"出力モード: {model.output_token_limit}")
            print(f"サポートされている生成メソッド: {model.supported_generation_methods}")
            print("=" * 50)

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")


if __name__ == "__main__":
    main()
