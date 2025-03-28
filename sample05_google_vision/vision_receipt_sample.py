"""
Google Cloud Vision APIを使用したレシート画像分析サンプル

このスクリプトは以下の機能を提供します：
- 指定されたレシート画像の読み込み
- Google Cloud Vision APIを使用したテキスト抽出
- 結果のJSONファイル保存
"""

import os
from pathlib import Path
import json
import base64
import requests
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()
api_key = os.getenv('GOOGLE_VISION_API_KEY')

def analyze_receipt(image_path):
    """レシート画像を分析し、テキストを抽出する関数"""
    try:
        url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
        headers = {"Content-Type": "application/json"}

        # 画像ファイルの読み込みとBase64エンコード
        with open(image_path, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')

        request_body = {
            "requests": [
                {
                    "image": {
                        "content": img_data
                    },
                    "features": [
                        {
                            "type": 'TEXT_DETECTION',
                            "maxResults": 10000
                        }
                    ],
                    "imageContext": {}
                }
            ],
            "parent": ''
        }

        data = json.dumps(request_body)
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()

        # 結果の整形
        if 'responses' not in result or not result['responses']:
            print("テキストが見つかりませんでした")
            return None

        text_annotations = result['responses'][0].get('textAnnotations', [])
        if not text_annotations:
            print("テキストが見つかりませんでした")
            return None

        formatted_result = {
            "full_text": text_annotations[0].get('description', ''),
            "text_blocks": []
        }

        # 個々のテキストブロックの情報を保存
        for text in text_annotations[1:]:
            block = {
                "text": text.get('description', ''),
                "confidence": text.get('confidence', 0),
                "bounding_box": {
                    "vertices": text.get('boundingPoly', {}).get('vertices', [])
                }
            }
            formatted_result["text_blocks"].append(block)

        return formatted_result

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return None

def save_results(result, output_dir, image_path):
    """結果をJSONファイルとして保存する関数"""
    # 結果ディレクトリの作成
    current_dir = Path(__file__).parent
    results_dir = current_dir / output_dir
    results_dir.mkdir(exist_ok=True)

    # 入力ファイルの名前を取得（拡張子なし）
    input_stem = Path(image_path).stem

    # JSONファイルに保存
    output_path = results_dir / f"{input_stem}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n結果を保存しました: {output_path}")

def main():
    print("Google Cloud Vision API レシート分析サンプル")
    
    # 画像パスの設定
    image_path = input("\n分析する画像ファイルのパスを入力してください: ")
    
    if not os.path.exists(image_path):
        print(f"エラー: ファイル '{image_path}' が見つかりません")
        return

    # レシートの分析
    print(f"\n'{image_path}' を分析中...")
    result = analyze_receipt(image_path)
    
    if result:
        # 結果の保存
        save_results(result, "results", image_path)
        print("\n処理が完了しました")
    else:
        print("\n処理に失敗しました")

if __name__ == "__main__":
    main() 