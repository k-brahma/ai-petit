import os

import anthropic
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# APIキーを設定
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)


def main():
    print("利用可能なClaudeモデルのリストはAPIでは取得できません:")
    print("=" * 50)
    print("最新のモデル情報は公式ドキュメントを参照してください: https://docs.anthropic.com/en/docs/about-claude/models")
    print("=" * 50)


if __name__ == "__main__":
    main() 