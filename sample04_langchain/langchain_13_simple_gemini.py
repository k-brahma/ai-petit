import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

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
