"""
LangChainを使用した画像分析プログラム

このモジュールは、LangChainを使用してOpenAIのGPT-4 VisionとAnthropicのClaude Visionを
利用した画像分析機能を提供します。

注意: 現在のLangChainはGoogle Gemini Vision APIには対応していません。
画像分析には、OpenAIまたはAnthropicのモデルを使用してください。
"""

import os
import base64
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

# 環境変数を読み込む
load_dotenv()

# APIキーを取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# モデル定数
OPENAI_MODEL = "gpt-4o"
CLAUDE_MODEL = "claude-3-opus-20240229"  # または "claude-3-sonnet-20240229"

def encode_image_to_base64(image_path):
    """画像をbase64エンコードする関数"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_text_with_image(prompt, image_path, model_name):
    """LangChainを使用して画像を含むテキストを生成する関数"""
    if not prompt or prompt.strip() == "":
        return "空の入力は処理できません。何か入力してください。"

    try:
        if model_name == "openai":
            # OpenAI Vision APIを使用
            if not OPENAI_API_KEY:
                return "OpenAI APIキーが設定されていません。.envファイルを確認してください。"
                
            # 画像をbase64エンコード
            base64_image = encode_image_to_base64(image_path)
            
            # ChatOpenAIモデルを初期化
            chat = ChatOpenAI(model=OPENAI_MODEL, temperature=0.7, api_key=OPENAI_API_KEY, max_tokens=1000)
            
            # 画像コンテンツを作成
            image_content = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
            
            # メッセージを作成
            messages = [
                SystemMessage(content="あなたは画像分析ができる役立つAIアシスタントです。"),
                HumanMessage(content=[
                    {"type": "text", "text": prompt},
                    image_content
                ])
            ]
            
            # レスポンスを生成
            response = chat.invoke(messages)
            return response.content
            
        elif model_name == "anthropic":
            # Claude Vision APIを使用
            if not ANTHROPIC_API_KEY:
                return "Anthropic APIキーが設定されていません。.envファイルを確認してください。"
                
            # 画像をbase64エンコード
            base64_image = encode_image_to_base64(image_path)
            
            # ChatAnthropicモデルを初期化
            chat = ChatAnthropic(model=CLAUDE_MODEL, temperature=0.7, api_key=ANTHROPIC_API_KEY, max_tokens=1000)
            
            # 画像コンテンツを作成
            image_content = {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": base64_image
                }
            }
            
            # メッセージを作成
            messages = [
                SystemMessage(content="あなたは画像分析ができる役立つAIアシスタントです。"),
                HumanMessage(content=[
                    {"type": "text", "text": prompt},
                    image_content
                ])
            ]
            
            # レスポンスを生成
            response = chat.invoke(messages)
            return response.content
            
        else:
            return "サポートされていないモデル名です。openai、anthropicのいずれかを使用してください。"
        
    except Exception as e:
        error_message = str(e)
        if "429" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        elif "401" in error_message or "authentication" in error_message.lower():
            return "APIキーが無効です。正しいAPIキーが設定されているか確認してください。"
        else:
            return f"エラーが発生しました: {error_message}"


def main():
    print("LangChainを使用した画像分析プログラム")
    print("使用するモデルを選択してください:")
    print("o: OpenAI (GPT-4 Vision)")
    print("a: Anthropic (Claude Vision)")
    print("注意: LangChainではGemini Vision APIは現在サポートされていません")
    
    # モデル選択 (プログラム開始時のみ)
    while True:
        model_choice = input("モデルを選択 (o/a): ").strip().lower()
        
        if model_choice == 'o':
            model_name = "openai"
            print("OpenAI (GPT-4 Vision) を使用します")
            break
        elif model_choice == 'a':
            model_name = "anthropic"
            print("Anthropic (Claude Vision) を使用します")
            break
        else:
            print("無効な選択です。o または a を入力してください。")
    
    print("\n終了するには 'exit' と入力してください")
    
    # 画像パス
    image_path = input("分析する画像のパスを入力してください: ")
    
    # 画像ファイルの存在確認
    if not os.path.exists(image_path):
        print(f"エラー: ファイル '{image_path}' が見つかりません。")
        return
    
    while True:
        user_input = input("\n画像に関するプロンプトを入力してください: ")

        if user_input.lower() == "exit":
            print("プログラムを終了します")
            break

        if not user_input or user_input.strip() == "":
            print("空の入力は処理できません。何か入力してください。")
            continue

        print("\n回答を生成中...\n")
        response = generate_text_with_image(user_input, image_path, model_name)
        print(response)


if __name__ == "__main__":
    main()