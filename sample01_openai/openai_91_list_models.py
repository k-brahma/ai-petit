import os

import openai
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


def main():
    print("利用可能なOpenAIモデルのリスト:")
    print("=" * 50)

    try:
        # 利用可能なモデルをリストアップ
        models = openai.models.list()

        for model in models.data:
            print(f"モデル名: {model.id}")
            print(f"作成日時: {model.created}")
            print(f"所有者: {model.owned_by}")
            if hasattr(model, 'description') and model.description:
                print(f"説明: {model.description}")
            print("=" * 50)

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")


if __name__ == "__main__":
    main()