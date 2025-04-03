"""
基本的なレシート分析機能を提供するモジュール

このモジュールは、OCR結果のJSONから以下の情報を抽出します：
- 登録番号
- 購入店名
- 総支払額
- 消費税額

特徴：
- OCR結果のJSONを処理
- OpenAI APIを使用して分析
- 結果をJSON形式で出力
- エラーハンドリング機能付き

使用方法：
1. プログラムを実行
2. OCR結果のJSONファイルのパスを入力
3. 分析結果を確認
4. 'exit'と入力して終了
"""

import json
import os

import openai
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


def analyze_receipt_json(json_path):
    """OCR結果のJSONからレシートの情報を抽出する関数"""
    try:
        # JSONファイルを読み込む
        with open(json_path, "r", encoding="utf-8") as file:
            ocr_data = json.load(file)

        # OCR結果からテキストを取得
        if "text" in ocr_data:
            text_content = ocr_data["text"]
        else:
            text_content = json.dumps(ocr_data)

        prompt = """
        このレシートから以下の情報を抽出してください：
        1. 登録番号（登録番号もしくは事業者登録番号）
        2. 購入店名
        3. 総支払額
        4. 消費税額

        以下の形式でJSON形式で返してください：
        {
            "登録番号": "番号",
            "購入店": "店名",
            "総支払額": "金額",
            "消費税額": "金額"
        }
        """

        # OpenAI APIを使用して分析
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt + "\n\nOCRのテキスト結果:\n" + text_content}
                    ]
                }
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except FileNotFoundError:
        return f"エラー: ファイル '{json_path}' が見つかりません"
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"


def main():
    print("レシート分析プログラム (OCR結果JSON版)")
    print("終了するには 'exit' と入力してください")

    while True:
        json_path = input("\nOCR結果のJSONファイルのパスを入力してください (例: ocr_result.json): ")

        if json_path.lower() == 'exit':
            print("プログラムを終了します")
            break

        if not os.path.exists(json_path):
            print(f"エラー: ファイル '{json_path}' が見つかりません")
            continue

        result = analyze_receipt_json(json_path)
        print("\n分析結果:")
        print(result)


if __name__ == "__main__":
    main()