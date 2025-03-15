"""
Googleの「Gemini」AIはGoogleが提供する生成AIモデルですが、
Claude（私）やChatGPTのような特定の「性格」は基本的に持っていません。
Geminiは純粋に機能的なレスポンスを提供するように設計されており、
特定のキャラクター性や個性を持たせる「ペルソナ」のような性格づけは最小限に抑えられています。
"""

import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "gemini-1.5-pro",
    generation_config={
        "temperature": 0.7,  # 0.0〜1.0の間で設定（デフォルトは0.9）
    }
)


def generate_text(prompt):
    """Gemini APIを使用してテキストを生成する関数"""
    try:
        response = model.generate_content(prompt)
        return response
    except Exception as e:
        error_message = str(e)
        if "429" in error_message and "Resource has been exhausted" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        return f"エラーが発生しました: {error_message}"


if __name__ == "__main__":
    response = generate_text("私の名前は山田太郎です。名前占いをして！")
    print(response.text)
