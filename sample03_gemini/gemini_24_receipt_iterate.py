"""
レシート画像の一括処理モジュール

このモジュールは、指定されたディレクトリ内のJPG画像を一括処理し、
以下の情報を抽出してCSVとExcelファイルに保存します：
- 登録番号
- 購入店名
- 総支払額
- 消費税額

特徴：
- ディレクトリ内のJPG画像を一括処理
- 結果をCSVとExcelファイルに保存
- エラーハンドリング機能付き
- 処理状況の表示
"""

import os
import json
import csv
import pandas as pd
from pathlib import Path
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
            text = response.text.strip()
            # 最初の { と最後の } の間のテキストを抽出
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                try:
                    result = json.loads(json_str)
                except json.JSONDecodeError:
                    print(f"エラー: '{image_path}' のJSON解析に失敗しました")
                    return None
            else:
                print(f"エラー: '{image_path}' の応答がJSON形式ではありません")
                return None
                
        return result

    except FileNotFoundError:
        print(f"エラー: ファイル '{image_path}' が見つかりません")
        return None
    except PIL.UnidentifiedImageError:
        print(f"エラー: '{image_path}' は有効な画像ファイルではありません")
        return None
    except Exception as e:
        error_message = str(e)
        if "429" in error_message and "Resource has been exhausted" in error_message:
            print("エラー: APIの使用量制限に達しました。しばらく待ってから再試行してください。")
        else:
            print(f"エラー: '{image_path}' の処理中にエラーが発生しました: {error_message}")
        return None

def save_results(results, output_dir_name):
    """結果をCSVとExcelファイルに保存する関数"""
    # 結果ディレクトリの作成（現在のモジュールのディレクトリに作成）
    current_dir = Path(__file__).parent
    results_dir = current_dir / output_dir_name
    results_dir.mkdir(exist_ok=True)
    
    # DataFrameを作成
    df = pd.DataFrame(results)
    
    # CSVファイルに保存
    csv_path = results_dir / "receipt_results.csv"
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"\nCSVファイルを保存しました: {csv_path}")
    
    # Excelファイルに保存
    excel_path = results_dir / "receipt_results.xlsx"
    df.to_excel(excel_path, index=False)
    print(f"Excelファイルを保存しました: {excel_path}")

def process_files_in_directory(directory):
    """ディレクトリ内のJPG画像を処理する関数"""
    results = []
    image_files = list(Path(directory).glob("*.jpg"))
    total_files = len(image_files)
    
    print(f"\n{total_files}個のJPGファイルを処理します...")
    
    for i, image_path in enumerate(image_files, 1):
        print(f"\n処理中: {image_path.name} ({i}/{total_files})")
        result = analyze_receipt(str(image_path))
        if result:
            result["ファイル名"] = image_path.name
            results.append(result)
    
    return results

def main():
    print("レシート一括分析プログラム")
    directory = input("\n画像ファイルが含まれるディレクトリ名を入力してください: ")
    
    if not os.path.exists(directory):
        print(f"エラー: ディレクトリ '{directory}' が見つかりません")
        return
    
    results = process_files_in_directory(directory)
    
    if results:
        save_results(results, "results")
        print(f"\n処理完了: {len(results)}個のファイルを処理しました")
    else:
        print("\n処理可能なファイルが見つかりませんでした")

if __name__ == "__main__":
    main() 