import os

import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# モデルの設定 (画像対応モデル)
# エラーメッセージで推奨されたモデルを使用
model = genai.GenerativeModel("gemini-1.5-flash")


def analyze_image(image_path, prompt):
    """Gemini APIを使用して画像を分析する関数"""
    if not prompt or prompt.strip() == "":
        return "空の入力は処理できません。何か質問やプロンプトを入力してください。"

    try:
        # 画像を読み込む
        image = PIL.Image.open(image_path)

        # 画像とプロンプトを送信
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
    print("Gemini APIを使用した画像分析プログラム")
    print("終了するには 'exit' と入力してください")

    while True:
        image_path = input("\n画像ファイルのパスを入力してください (例: image.jpg): ")

        if image_path.lower() == "exit":
            print("プログラムを終了します")
            break

        if not os.path.exists(image_path):
            print(f"エラー: ファイル '{image_path}' が見つかりません")
            continue

        prompt = input("画像に対する質問やプロンプトを入力してください: ")

        if not prompt or prompt.strip() == "":
            print("空の入力は処理できません。何か質問やプロンプトを入力してください。")
            continue

        print("\n分析中...\n")
        response = analyze_image(image_path, prompt)
        print(response)


if __name__ == "__main__":
    main()
