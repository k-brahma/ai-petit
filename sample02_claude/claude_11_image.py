import base64
import os

import anthropic
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)

# モデルの設定
# Claude 3 Vision対応モデル
MODEL = "claude-3-opus-20240229"  # または "claude-3-sonnet-20240229" や "claude-3-haiku-20240307"


def get_mime_type(image_path):
    """ファイル拡張子からMIMEタイプを取得する関数"""
    extension = image_path.lower().split(".")[-1]
    mime_types = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp"
    }
    return mime_types.get(extension, "application/octet-stream")


def analyze_image(image_path, prompt):
    """Claude APIを使用して画像を分析する関数"""
    # 画像をbase64エンコード
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    mime_type = get_mime_type(image_path)

    try:
        # APIリクエスト
        response = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": mime_type,  # どんなデータを渡しているのか？
                                "data": base64_image  # データの中身
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )
        return response
    except FileNotFoundError:
        return f"エラー: ファイル '{image_path}' が見つかりません"
    except Exception as e:
        error_message = str(e)
        if "429" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        return f"エラーが発生しました: {error_message}"


def main():
    print("Claude APIを使用した画像分析プログラム")
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
        print(response.content[0].text)


if __name__ == "__main__":
    main()
