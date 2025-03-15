import os
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate

# 環境変数を読み込む
load_dotenv()

# APIキーを環境変数から明示的に取得
openai_api_key = os.getenv("OPENAI_API_KEY")

# LangChain用にOpenAIのLLMを初期化
llm = OpenAI(
    temperature=0.7,
    openai_api_key=openai_api_key
)

# 姓名占い用のカスタムプロンプトテンプレート
template = """あなたは姓名占いをする占い師です。
ユーザーの入力から名前を抽出し、その名前を占ってください。
必ず「大吉」「中吉」「吉」「凶」のいずれかで結果を伝え、その理由も説明してください。
回答は50文字以内でお願いします。

名前が明確でない場合は、丁寧に名前を尋ねてください。

現在の会話の履歴:
{history}

人間: {input}
AI占い師: """

# メモリと会話チェーンの設定
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=PromptTemplate.from_template(template),
    verbose=False
)

# 対話型インターフェースの実装
if __name__ == "__main__":
    print("姓名占いAIチャットプログラム")
    print("特別コマンド:")
    print("  - 'history': 会話履歴を表示")
    print("  - 'exit': プログラムを終了")
    print("  - 会話履歴のクリアはできません")
    print("-" * 50)

    while True:
        user_input = input("\nあなたの名前や質問を入力してください: ")

        if user_input.lower() == "exit":
            print("プログラムを終了します")
            break

        if not user_input.strip():
            print("空の入力は処理できません。何か入力してください。")
            continue

        # 現在の会話履歴を表示するオプション
        if user_input.lower() == "history":
            print("\n=== 会話履歴 ===")
            print(memory.buffer)
            continue

        # 会話チェーンを使って応答を取得
        response = conversation.predict(input=user_input)
        print(f"\n{response}")

