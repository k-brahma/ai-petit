import base64
import io
import os

import openai
from dotenv import load_dotenv
from pdf2image import convert_from_path

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


def convert_pdf_to_base64_image(pdf_path):
    """PDFの1ページ目を画像に変換してbase64エンコードする"""
    try:
        # 1ページ目だけ画像化（DPIはお好みで調整可能）
        images = convert_from_path(pdf_path, dpi=200)
        if not images:
            return "エラー: PDFから画像が生成できませんでした"

        img_byte_arr = io.BytesIO()
        images[0].save(img_byte_arr, format="JPEG")
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")
        return img_base64
    except FileNotFoundError:
        return f"エラー: ファイル '{pdf_path}' が見つかりません"
    except Exception as e:
        return f"PDFの画像変換中にエラーが発生しました: {str(e)}"


def analyze_image_with_vision(img_base64, prompt):
    """OpenAI Vision APIを使用して画像の内容を分析する関数"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "あなたはPDFドキュメント（画像化されたもの）の分析を得意とするAIアシスタントです。",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
                        },
                    ],
                },
            ],
            max_tokens=4096,
        )
        return response.choices[0].message.content
    except Exception as e:
        error_message = str(e)
        if "429" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        return f"エラーが発生しました: {error_message}"


def main():
    print("OpenAI Vision APIを使用したPDF（画像化）分析プログラム")
    print("終了するには 'exit' と入力してください")

    while True:
        pdf_path = input("\nPDFファイルのパスを入力してください (例: document.pdf): ")

        if pdf_path.lower() == "exit":
            print("プログラムを終了します")
            break

        if not os.path.exists(pdf_path):
            print(f"エラー: ファイル '{pdf_path}' が見つかりません")
            continue

        # PDFを画像（base64）化
        print("\nPDFを画像化しています...")
        img_base64 = convert_pdf_to_base64_image(pdf_path)

        if isinstance(img_base64, str) and img_base64.startswith("エラー:"):
            print(img_base64)
            continue

        prompt = input("PDFの内容に関する質問やプロンプトを入力してください: ")

        if not prompt or prompt.strip() == "":
            print("空の入力は処理できません。何か質問やプロンプトを入力してください。")
            continue

        print("\n分析中...\n")
        response = analyze_image_with_vision(img_base64, prompt)
        print(response)


if __name__ == "__main__":
    main()
