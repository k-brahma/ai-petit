import os
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# 各LLMプロバイダーのインポート
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# 環境変数を読み込む
load_dotenv()

# 会話履歴を保存するリスト
conversation_history = []


def add_to_history(role, content):
    """会話を履歴に追加する関数"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conversation_history.append({
        "timestamp": timestamp,
        "role": role,
        "content": content
    })


def display_history():
    """会話履歴を表示する関数"""
    if not conversation_history:
        return "履歴はまだありません。"

    result = "=== 会話履歴 ===\n"
    for i, entry in enumerate(conversation_history, 1):
        result += f"\n[{i}] {entry['timestamp']}\n"
        result += f"役割: {entry['role']}\n"
        content_preview = entry['content'][:100] + "..." if len(entry['content']) > 100 else entry['content']
        result += f"内容: {content_preview}\n"
        result += "-" * 40 + "\n"

    return result


def clear_history():
    """会話履歴をクリアする関数"""
    conversation_history.clear()
    return "履歴をクリアしました。"


def format_history_for_langchain():
    """LangChain用に会話履歴をフォーマットする関数"""
    langchain_messages = []
    for entry in conversation_history:
        if entry["role"] == "user":
            langchain_messages.append(HumanMessage(content=entry["content"]))
        elif entry["role"] == "assistant":
            langchain_messages.append(AIMessage(content=entry["content"]))
    return langchain_messages


def get_response(llm_provider, query_topic):
    """ 指定されたLLMプロバイダーを使用して応答を生成する関数

    :param str llm_provider: 使用するLLMプロバイダー ('openai', 'anthropic', 'gemini')
    :param str query_topic: 質問トピック
    :returns: 生成されたレスポンス
    :rtype: str
    """
    # LLMプロバイダーに基づいてモデルを初期化
    if llm_provider.lower() == 'openai':
        openai_api_key = os.getenv("OPENAI_API_KEY")
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
            openai_api_key=openai_api_key
        )
    elif llm_provider.lower() == 'anthropic':
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        llm = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            temperature=0.7,
            anthropic_api_key=anthropic_api_key
        )
    elif llm_provider.lower() == 'gemini':
        google_api_key = os.getenv("GEMINI_API_KEY")
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.7,
            google_api_key=google_api_key
        )
    else:
        raise ValueError(f"サポートされていないLLMプロバイダー: {llm_provider}")

    # 会話履歴のメッセージを取得
    chat_history = format_history_for_langchain()

    # プロンプトテンプレートを作成（会話履歴を含む）
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "あなたは漢方の専門家です。専門知識を活かして質問に答えてください。"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    # チェーンを作成
    chain = prompt_template | llm | StrOutputParser()

    # チェーンを実行（会話履歴を含める）
    response = chain.invoke({
        "chat_history": chat_history,
        "input": query_topic
    })

    return response


if __name__ == "__main__":
    print("漢方専門家AIチャットプログラム")
    print("特別コマンド:")
    print("  - 'history': 会話履歴を表示")
    print("  - 'clear': 会話履歴をクリア")
    print("  - 'exit': プログラムを終了")
    print("-" * 50)

    # 使用するLLMプロバイダーを最初に選択
    print("LLMプロバイダーを選択してください (openai, anthropic, gemini): ", end="")
    provider = input().strip().lower()

    while True:
        user_input = input("\n質問を入力してください: ")

        # 特別コマンドの処理
        if user_input.lower() == "exit":
            print("プログラムを終了します")
            break
        elif user_input.lower() == "history":
            print(display_history())
            continue
        elif user_input.lower() == "clear":
            print(clear_history())
            continue

        if not user_input or user_input.strip() == "":
            print("空の入力は処理できません。何か入力してください。")
            continue

        # ユーザー入力を履歴に追加
        add_to_history("user", user_input)

        print("\n回答を生成中...\n")
        try:
            result = get_response(provider, user_input)
            print(result)

            # AIの応答を履歴に追加
            add_to_history("assistant", result)

        except ValueError as e:
            print(f"エラー: {e}")
            add_to_history("system", str(e))  # エラーはシステムメッセージとして保存
