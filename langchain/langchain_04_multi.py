import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# 環境変数を読み込む
load_dotenv()

# APIキーを取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# モデル定数
OPENAI_MODEL = "gpt-4-turbo"
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
GEMINI_MODEL = "gemini-1.5-pro"

# 会話履歴を保存するリスト
conversation_history = []

def generate_text(prompt, model_name, history):
    """LangChainを使用してテキストを生成する関数"""
    if not prompt or prompt.strip() == "":
        return "空の入力は処理できません。何か入力してください。"
    
    # メッセージリストの作成
    messages = []
    
    # 会話履歴からメッセージを構築
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    
    # 新しいユーザーメッセージを追加
    messages.append(HumanMessage(content=prompt))
    
    try:
        # 選択されたモデルを初期化
        if model_name == "openai":
            if not OPENAI_API_KEY:
                return "OpenAI APIキーが設定されていません。.envファイルを確認してください。"
            chat = ChatOpenAI(model=OPENAI_MODEL, temperature=0.7, api_key=OPENAI_API_KEY)
            # OpenAI用のメッセージ構造（SystemMessageを追加）
            messages = [SystemMessage(content="あなたは役立つAIアシスタントです。")] + messages
        elif model_name == "anthropic":
            if not ANTHROPIC_API_KEY:
                return "Anthropic APIキーが設定されていません。.envファイルを確認してください。"
            chat = ChatAnthropic(model=CLAUDE_MODEL, temperature=0.7, api_key=ANTHROPIC_API_KEY)
            # Claude用のメッセージ構造（SystemMessageを追加）
            messages = [SystemMessage(content="あなたは役立つAIアシスタントです。")] + messages
        elif model_name == "gemini":
            if not GEMINI_API_KEY:
                return "Google APIキーが設定されていません。.envファイルを確認してください。"
            chat = ChatGoogleGenerativeAI(
                model=GEMINI_MODEL, 
                temperature=0.7,
                google_api_key=GEMINI_API_KEY
            )
            # Geminiはシステムメッセージを直接サポートしていないため、最初のメッセージに指示を追加
            if len(messages) > 0 and isinstance(messages[0], HumanMessage):
                first_msg = messages[0]
                messages[0] = HumanMessage(content=f"あなたは役立つAIアシスタントです。\n\n{first_msg.content}")
        
        # レスポンスを生成
        response = chat.invoke(messages)
        
        return response.content
    except Exception as e:
        error_message = str(e)
        if "429" in error_message:
            return "APIの使用量制限に達しました。しばらく待ってから再試行してください。"
        elif "401" in error_message or "authentication" in error_message.lower():
            return "APIキーが無効です。正しいAPIキーが設定されているか確認してください。"
        elif "Your default credentials were not found" in error_message:
            return "Gemini APIの認証に失敗しました。.envファイルにGEMINI_API_KEYが正しく設定されているか確認してください。"
        else:
            return f"エラーが発生しました: {error_message}"


def main():
    print("LangChainを使用したテキスト生成プログラム")
    print("使用するモデルを選択してください:")
    print("o: OpenAI (GPT-4)")
    print("a: Anthropic (Claude)")
    print("g: Google (Gemini)")
    
    # モデル選択 (プログラム開始時のみ)
    while True:
        model_choice = input("モデルを選択 (o/a/g): ").strip().lower()
        
        if model_choice == 'o':
            model_name = "openai"
            print("OpenAI (GPT-4) を使用します")
            break
        elif model_choice == 'a':
            model_name = "anthropic"
            print("Anthropic (Claude) を使用します")
            break
        elif model_choice == 'g':
            model_name = "gemini"
            print("Google (Gemini) を使用します")
            break
        else:
            print("無効な選択です。o, a, g のいずれかを入力してください。")
    
    print("\n終了するには 'exit' と入力してください")
    print("履歴を表示するには 'history' と入力してください")
    print("履歴をクリアするには 'clear' と入力してください")
    
    # APIメッセージ形式の会話履歴
    api_messages = []
    
    while True:
        user_input = input(f"\nプロンプトを入力してください: ")

        # 各種コマンド処理
        if user_input.lower() == "exit":
            print("プログラムを終了します")
            break

        if user_input.lower() == "history":
            print("\n===== 会話履歴 =====")
            for i, message in enumerate(conversation_history):
                role = "User" if i % 2 == 0 else "Agent"
                print(f"{role}: {message}")
            print("===================")
            continue

        if user_input.lower() == "clear":
            conversation_history.clear()
            api_messages.clear()
            print("会話履歴をクリアしました")
            continue

        if not user_input or user_input.strip() == "":
            print("空の入力は処理できません。何か入力してください。")
            continue

        # ユーザー入力を履歴に追加
        conversation_history.append(user_input)
        api_messages.append({"role": "user", "content": user_input})

        print("\n回答を生成中...\n")
        response = generate_text(user_input, model_name, api_messages)
        
        # エージェントの応答を履歴に追加
        conversation_history.append(response)
        api_messages.append({"role": "assistant", "content": response})
        
        print(response)


if __name__ == "__main__":
    main()