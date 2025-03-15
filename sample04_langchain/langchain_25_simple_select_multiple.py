import os
from datetime import datetime
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# OpenAIのインポート
from langchain_openai import ChatOpenAI

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


def get_response(name_input):
    """ OpenAIを使用して姓名占いの応答を生成する関数

    :param str name_input: ユーザーからの入力（名前や質問）
    :returns: 生成された姓名占いの結果
    :rtype: str
    """
    # OpenAI APIキーを取得
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # LLMの初期化
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.7,
        openai_api_key=openai_api_key
    )

    # プロンプトテンプレートを作成
    prompt_template = PromptTemplate(
        input_variables=["user_input"],
        template="""
あなたは姓名占いをする占い師です。
ユーザーの入力から名前を抽出し、その名前を占ってください。
必ず「大吉」「中吉」「吉」「凶」のいずれかで結果を伝え、その理由も説明してください。
回答は50文字以内でお願いします。

名前が明確でない場合は、丁寧に名前を尋ねてください。

ユーザーの入力:
{user_input}
"""
    )

    # チェーンを作成
    chain = prompt_template | llm | StrOutputParser()

    # チェーンを実行
    response = chain.invoke({"user_input": name_input})

    return response


if __name__ == "__main__":
    print("姓名占いAIチャットプログラム")
    print("特別コマンド:")
    print("  - 'history': 会話履歴を表示")
    print("  - 'clear': 会話履歴をクリア")
    print("  - 'exit': プログラムを終了")
    print("-" * 50)

    while True:
        user_input = input("\nあなたの名前や質問を入力してください: ")

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

        print("\n占いの結果を生成中...\n")
        try:
            result = get_response(user_input)
            print(result)

            # AIの応答を履歴に追加
            add_to_history("assistant", result)

        except Exception as e:
            print(f"エラー: {e}")
            add_to_history("system", str(e))  # エラーはシステムメッセージとして保存