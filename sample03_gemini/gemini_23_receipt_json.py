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

import os
import json
import re
import PIL.Image
import google.generativeai as genai
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# モデルの設定
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_json_from_text(text):
    """テキストからJSONを抽出する関数"""
    # JSONブロックを見つける正規表現パターン
    json_pattern = r'({[\s\S]*?})'
    match = re.search(json_pattern, text)
    
    if match:
        json_str = match.group(1)
        return json_str
    return None

def analyze_receipt(image_path):
    """レシートの画像を分析し、必要な情報を抽出する関数"""
    try:
        # 画像を読み込む
        image = PIL.Image.open(image_path)

        prompt = """
        このレシートから以下の情報を抽出してください：
        1. 登録番号（登録番号もしくは事業者登録番号）
        2. 購入店名
        3. 総支払額
        4. 消費税額

        必ず次のJSON形式でのみ返答してください。余計な説明は含めないでください：
        {
            "登録番号": "番号",
            "購入店": "店名",
            "総支払額": "金額",
            "消費税額": "金額"
        }
        
        情報が見つからない場合は、該当項目を「不明」としてください。
        """

        # JSONレスポンスフォーマットを指定
        generation_config = {
            "response_mime_type": "application/json",
        }
        
        response = model.generate_content(
            [prompt, image],
            generation_config=generation_config
        )
        
        try:
            # JSON形式で直接返ってきた場合
            result = json.loads(response.text)
        except json.JSONDecodeError:
            # テキストからJSONを抽出してみる
            json_str = extract_json_from_text(response.text)
            if json_str:
                try:
                    result = json.loads(json_str)
                except json.JSONDecodeError:
                    return json.dumps({"error": "JSONの解析に失敗しました", "raw_response": response.text}, ensure_ascii=False, indent=2)
            else:
                # JSON形式ではない場合は、結果を構造化
                return json.dumps({
                    "error": "APIからの応答がJSON形式ではありません",
                    "raw_response": response.text
                }, ensure_ascii=False, indent=2)
                
        return json.dumps(result, ensure_ascii=False, indent=2)

    except FileNotFoundError:
        return json.dumps({"error": f"ファイル '{image_path}' が見つかりません"}, ensure_ascii=False, indent=2)
    except PIL.UnidentifiedImageError:
        return json.dumps({"error": f"'{image_path}' は有効な画像ファイルではありません"}, ensure_ascii=False, indent=2)
    except Exception as e:
        error_message = str(e)
        if "429" in error_message and "Resource has been exhausted" in error_message:
            return json.dumps({"error": "APIの使用量制限に達しました。しばらく待ってから再試行してください。"}, ensure_ascii=False, indent=2)
        return json.dumps({"error": f"エラーが発生しました: {error_message}"}, ensure_ascii=False, indent=2)

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

        # JSONをパースして辞書として表示
        try:
            result_dict = json.loads(result_json)
            if "error" not in result_dict:
                print("\n抽出情報:")
                for key, value in result_dict.items():
                    print(f"{key}: {value}")
        except json.JSONDecodeError:
            print("結果の表示中にエラーが発生しました。")

if __name__ == "__main__":
    main()