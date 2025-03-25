import os

import openai
import PyPDF2
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


def extract_text_from_pdf(pdf_path):
    """PDFファイルからテキストを抽出する関数"""
    try:
        with open(pdf_path, "rb") as file:
            # PDFリーダーオブジェクトを作成
            pdf_reader = PyPDF2.PdfReader(file)

            # 全ページのテキストを結合
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"

            return text
    except FileNotFoundError:
        return f"エラー: ファイル '{pdf_path}' が見つかりません"
    except Exception as e:
        return f"PDFの読み込み中にエラーが発生しました: {str(e)}"


def analyze_pdf_content(text, prompt):
    """OpenAI APIを使用してPDFの内容を分析する関数"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "あなたはPDFドキュメント分析を得意とするAIアシスタントです。",
                },
                {
                    "role": "user",
                    "content": f"以下のPDFの内容について質問に答えてください:\n\n{text}\n\n質問: {prompt}",
                },
            ],
            max_tokens=1000,
        )
        return response
    except Exception as e:
        error_message = str(e)
        if "429" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        return f"エラーが発生しました: {error_message}"


def main():
    print("OpenAI APIを使用したPDF分析プログラム")
    print("終了するには 'exit' と入力してください")

    while True:
        pdf_path = input("\nPDFファイルのパスを入力してください (例: document.pdf): ")

        if pdf_path.lower() == "exit":
            print("プログラムを終了します")
            break

        if not os.path.exists(pdf_path):
            print(f"エラー: ファイル '{pdf_path}' が見つかりません")
            continue

        # PDFからテキストを抽出
        print("\nPDFを読み込んでいます...")
        pdf_text = extract_text_from_pdf(pdf_path)

        if pdf_text.startswith("エラー:"):
            print(pdf_text)
            continue

        prompt = input("PDFの内容に関する質問やプロンプトを入力してください: ")

        if not prompt or prompt.strip() == "":
            print("空の入力は処理できません。何か質問やプロンプトを入力してください。")
            continue

        print("\n分析中...\n")
        response = analyze_pdf_content(pdf_text, prompt)
        print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
