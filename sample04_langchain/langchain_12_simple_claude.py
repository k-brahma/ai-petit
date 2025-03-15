import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# 環境変数を読み込む
load_dotenv()

# APIキーを環境変数から明示的に取得
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# LangChain用にAnthropicのLLMを初期化（APIキーを明示的に渡す）
llm = ChatAnthropic(
    model="claude-3-sonnet-20240229",
    temperature=0.7,
    anthropic_api_key=anthropic_api_key
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

# 新しいスタイルでチェーンを作成
chain = prompt_template | llm | StrOutputParser()

# チェーンを実行
response = chain.invoke({"user_input": "私の名前は山田太郎です。占ってください。"})

print(response)