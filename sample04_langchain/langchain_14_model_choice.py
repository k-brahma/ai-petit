import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
# 各LLMプロバイダーのインポート
from langchain_openai import ChatOpenAI

# 環境変数を読み込む
load_dotenv()


def get_response(llm_provider, query_topic):
    """ 指定されたLLMプロバイダーを使用して応答を生成する関数

    :param str llm_provider: 使用するLLMプロバイダー ('openai', 'anthropic', 'gemini')
    :param str query_topic: 質問トピック
    :returns: 生成されたレスポンス
    :rtype: str
    """
    # LLMプロバイダーに基づいてモデルを初期化
    if llm_provider.lower() == 'openai':
        print("openai が選択されました")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
            openai_api_key=openai_api_key
        )
    elif llm_provider.lower() == 'anthropic':
        print("anthropic が選択されました")
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        llm = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            temperature=0.7,
            anthropic_api_key=anthropic_api_key
        )
    elif llm_provider.lower() == 'gemini':
        print("gemini が選択されました")
        google_api_key = os.getenv("GEMINI_API_KEY")
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.7,
            google_api_key=google_api_key
        )
    else:
        raise ValueError(f"サポートされていないLLMプロバイダー: {llm_provider}")

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

    # 新しいスタイルでチェーンを作成
    chain = prompt_template | llm | StrOutputParser()

    # チェーンを実行
    response = chain.invoke({"user_input": query_topic})

    return response


if __name__ == "__main__":
    # 対話モード
    print("LLMプロバイダーを選択してください (openai, anthropic, gemini): ", end="")
    provider = input().strip()
    print("名前占いしたい人の名前を記入してください: ", end="")
    query_topic = input().strip()

    print("\n回答を生成中...\n")
    try:
        result = get_response(provider, query_topic)
        print(result)
    except ValueError as e:
        print(f"エラー: {e}")
