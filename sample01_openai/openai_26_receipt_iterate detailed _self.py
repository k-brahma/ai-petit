from pathlib import Path

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