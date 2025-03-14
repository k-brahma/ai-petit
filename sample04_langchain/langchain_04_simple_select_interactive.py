import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# 各LLMプロバイダーのインポート
from langchain_openai import OpenAI, ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

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

    # プロンプトテンプレートを作成（共通部分）
    prompt_template = PromptTemplate(
        input_variables=["topic"],
        template="あなたは漢方の専門家です。{topic}について詳しく説明してください。"
    )

    # チェーンを作成（共通部分）
    chain = prompt_template | llm | StrOutputParser()

    # チェーンを実行（共通部分）
    response = chain.invoke({"topic": query_topic})

    return response


if __name__ == "__main__":
    # 対話モード
    print("LLMプロバイダーを選択してください (openai, anthropic, gemini): ", end="")
    provider = input().strip()
    print("質問トピックを入力してください: ", end="")
    topic = input().strip()

    print("\n回答を生成中...\n")
    try:
        result = get_response(provider, topic)
        print(result)
    except ValueError as e:
        print(f"エラー: {e}")