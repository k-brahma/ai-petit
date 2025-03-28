"""
金額表記の正規化機能を追加したレシート一括処理モジュール

このモジュールは、指定されたディレクトリ内のレシート画像を一括処理し、
以下の情報を抽出してCSVとExcelファイルに保存します：
- 登録番号
- 購入店名
- 総支払額
- 消費税額

特徴：
- ディレクトリ内のJPG画像を一括処理
- 金額表記の正規化（「数字+円」形式に統一）
- 結果をCSVとExcelファイルに保存
- エラーハンドリング機能付き
- 進捗状況の表示

使用方法：
1. プログラムを実行
2. レシート画像が含まれるディレクトリ名を入力
3. 処理完了後、resultsディレクトリに結果ファイルが作成される
"""

import base64
import os
import json
import csv
import pandas as pd
from pathlib import Path
import openai
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

def encode_image(image_path):
    """画像をbase64エンコードする関数"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_receipt(image_path):
    """レシートの画像を分析し、必要な情報を抽出する関数"""
    try:
        # 画像を読み込む
        base64_image = encode_image(image_path)

        system_prompt = """あなたはレシートの情報を正確に抽出するAIアシスタントです。
金額の表記は必ず「数字+円」の形式で行ってください。
例：820円、495円、460円、950円

禁止事項：
- 通貨記号（¥や￥）の使用
- カンマ区切りの使用
- 小数点以下の使用
- 単位なしの数字のみの表記"""

        user_prompt = """
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

        金額は必ず「数字+円」の形式で表記してください。
        例：820円、495円、460円、950円"""

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        # JSONレスポンスを解析
        result = json.loads(response.choices[0].message.content)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except FileNotFoundError:
        return json.dumps({"error": f"ファイル '{image_path}' が見つかりません"}, ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        return json.dumps({"error": "JSONの解析に失敗しました"}, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": f"エラーが発生しました: {str(e)}"}, ensure_ascii=False, indent=2)

def normalize_amount(amount_str):
    """金額表記を正規化する関数"""
    if not amount_str or not isinstance(amount_str, str):
        return amount_str
    
    # 通貨記号とカンマを削除
    amount_str = amount_str.replace('¥', '').replace('￥', '').replace(',', '')
    
    # 数字以外の文字を削除
    amount = ''.join(filter(str.isdigit, amount_str))
    
    if not amount:
        return amount_str
    
    # 数字+円の形式に変換
    return f"{amount}円"

def normalize_results(results):
    """結果の金額表記を正規化する関数"""
    normalized_results = []
    for result in results:
        normalized_result = result.copy()
        if '総支払額' in normalized_result:
            normalized_result['総支払額'] = normalize_amount(normalized_result['総支払額'])
        if '消費税額' in normalized_result:
            normalized_result['消費税額'] = normalize_amount(normalized_result['消費税額'])
        normalized_results.append(normalized_result)
    return normalized_results

def save_results(results):
    """処理結果をCSVとExcelファイルに保存する関数"""
    if not results:
        print("警告: 保存する結果がありません")
        return
    
    # 金額表記を正規化
    normalized_results = normalize_results(results)
    
    # 結果ディレクトリの作成（現在のモジュールのディレクトリに作成）
    current_dir = Path(__file__).parent
    results_dir = current_dir / "results"
    results_dir.mkdir(exist_ok=True)
    
    # CSVファイルの作成
    csv_path = results_dir / "receipt_results.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=normalized_results[0].keys())
        writer.writeheader()
        writer.writerows(normalized_results)
    
    # Excelファイルの作成
    df = pd.DataFrame(normalized_results)
    excel_path = results_dir / "receipt_results.xlsx"
    df.to_excel(excel_path, index=False)
    
    print(f"\n処理が完了しました。")
    print(f"CSVファイル: {csv_path}")
    print(f"Excelファイル: {excel_path}")

def process_files_in_directory(dir_name):
    """指定されたディレクトリ内のJPG画像を処理し、結果をCSVとExcelファイルに保存する"""
    # 結果を格納するリスト
    results = []
    
    # ディレクトリ内のJPGファイルを取得
    image_files = list(Path(dir_name).glob("*.jpg"))
    
    if not image_files:
        print(f"警告: {dir_name} 内にJPGファイルが見つかりません")
        return
    
    print(f"処理を開始します。{len(image_files)}個のファイルが見つかりました。")
    
    # 各画像を処理
    for image_path in image_files:
        print(f"\n処理中: {image_path.name}")
        try:
            result_json = analyze_receipt(str(image_path))
            result_dict = json.loads(result_json)
            
            # ファイル名を追加
            result_dict['ファイル名'] = image_path.name
            results.append(result_dict)
            
        except Exception as e:
            print(f"エラー: {image_path.name} の処理中にエラーが発生しました: {str(e)}")
    
    if not results:
        print("警告: 処理可能なファイルがありませんでした")
        return
    
    # 結果を保存
    save_results(results)

def main():
    print("レシート画像一括処理プログラム")
    dir_name = input("\n画像が含まれるディレクトリ名を入力してください: ")
    
    if not os.path.exists(dir_name):
        print(f"エラー: ディレクトリ '{dir_name}' が見つかりません")
        return
        
    process_files_in_directory(dir_name)

if __name__ == "__main__":
    main() 