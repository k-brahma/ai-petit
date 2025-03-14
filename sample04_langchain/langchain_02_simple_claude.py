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

# プロンプトテンプレートを作成
prompt_template = PromptTemplate(
    input_variables=["topic"],
    template="あなたは漢方の専門家です。{topic}について詳しく説明してください。"
)

# 新しいスタイルでチェーンを作成
chain = prompt_template | llm | StrOutputParser()

# チェーンを実行
response = chain.invoke({"topic": "花粉症に効く漢方薬"})

print(response)
