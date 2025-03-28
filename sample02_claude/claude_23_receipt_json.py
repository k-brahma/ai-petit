"""
JSONレスポンス形式を改善したレシート分析モジュール

このモジュールは、レシート画像から以下の情報を抽出し、JSON形式で返します：
- 登録番号
- 購入店名
- 総支払額
- 消費税額

特徴：
- 単一のレシート画像を処理
- 対話形式でファイルを指定
- 結果をJSON形式で出力（response_format指定）
- エラーハンドリング機能付き
- 日本語文字化け対策（ensure_ascii=False）

使用方法：
1. プログラムを実行
2. レシート画像のパスを入力
3. 分析結果を確認
4. 'exit'と入力して終了
"""

import base64
import os
import json
import anthropic
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)


def encode_image(image_path):
    """画像をbase64エンコードする関数"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def analyze_receipt(image_path):
    """レシートの画像を分析し、必要な情報を抽出する関数"""
    try:
        # 画像を読み込む
        base64_image = encode_image(image_path)

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

        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64_image
                            }
                        }
                    ]
                }
            ]
        )
        
        # JSONレスポンスを解析
        result = json.loads(message.content[0].text)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except FileNotFoundError:
        return json.dumps({"error": f"ファイル '{image_path}' が見つかりません"}, ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        return json.dumps({"error": "JSONの解析に失敗しました"}, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": f"エラーが発生しました: {str(e)}"}, ensure_ascii=False, indent=2)


def main():
    print("レシート分析プログラム")
    print("終了するには 'exit' と入力してください")

    while True:
        image_path = input("\n画像ファイルのパスを入力してください (例: receipt.jpg): ")
        
        if image_path.lower() == 'exit':
            print("プログラムを終了します")
            break
            
        if not os.path.exists(image_path):
            print(f"エラー: ファイル '{image_path}' が見つかりません")
            continue
            
        result_json = analyze_receipt(image_path)
        print("\n分析結果:")
        print(result_json)

        # create a dictionary from the JSON string
        result_dict = json.loads(result_json)
        print(result_dict)


if __name__ == "__main__":
    main() 