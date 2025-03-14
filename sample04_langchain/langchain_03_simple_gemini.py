import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

# Google API Keyを環境変数から取得
google_api_key = os.getenv("GEMINI_API_KEY")

# LangChain用にGemini LLMを初期化
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=google_api_key,
    temperature=0.7
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