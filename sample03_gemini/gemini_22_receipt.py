"""
基本的なレシート分析機能を提供するモジュール

このモジュールは、レシート画像から以下の情報を抽出します：
- 登録番号
- 購入店名
- 総支払額
- 消費税額

特徴：
- 単一のレシート画像を処理
- 対話形式でファイルを指定
- 結果をJSON形式で出力
- エラーハンドリング機能付き

使用方法：
1. プログラムを実行
2. レシート画像のパスを入力
3. 分析結果を確認
4. 'exit'と入力して終了
"""

import os
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

        以下の形式でJSON形式で返してください：
        {
            "登録番号": "番号",
            "購入店": "店名",
            "総支払額": "金額",
            "消費税額": "金額"
        }
        """

        response = model.generate_content([prompt, image])
        return response.text

    except FileNotFoundError:
        return f"エラー: ファイル '{image_path}' が見つかりません"
    except PIL.UnidentifiedImageError:
        return f"エラー: '{image_path}' は有効な画像ファイルではありません"
    except Exception as e:
        error_message = str(e)
        if "429" in error_message and "Resource has been exhausted" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        return f"エラーが発生しました: {error_message}"

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
            
        result = analyze_receipt(image_path)
        print("\n分析結果:")
        print(result)

if __name__ == "__main__":
    main()