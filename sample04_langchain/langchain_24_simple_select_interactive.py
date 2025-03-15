import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 環境変数を読み込む
load_dotenv()


def get_response(query_topic):
    """ OpenAIのLLMを使用して姓名占いの応答を生成する関数

    :param str query_topic: ユーザーの入力（名前や質問）
    :returns: 生成された占い結果
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

    # プロンプトテンプレートを作成（マルチラインで柔軟性を向上）
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
    response = chain.invoke({"user_input": query_topic})

    return response


if __name__ == "__main__":
    # 対話モード
    print("姓名占いAIプログラム")
    print("-" * 50)

    while True:
        user_input = input("\n名前占いしたい人の名前を記入してください（終了する場合は 'exit'）: ")

        if user_input.lower() == "exit":
            print("プログラムを終了します")
            break

        if not user_input.strip():
            print("空の入力は処理できません。何か入力してください。")
            continue

        print("\n占いの結果を生成中...\n")
        try:
            result = get_response(user_input)
            print(result)
        except Exception as e:
            print(f"エラー: {e}")
