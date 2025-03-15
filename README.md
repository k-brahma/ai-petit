# AI API プチプログラム

OpenAI、Anthropic、Gemini, Langchani の API を使用した簡単なプログラム集です。テキスト生成と画像分析の機能を提供します。

## セットアップ

### 自動セットアップ（推奨）

セットアップスクリプトを使用して、必要なパッケージを自動的にインストールできます：

- Windows: プロジェクトのルートディレクトリから `scripts\setup.bat` を実行します。（scriptsディレクトリに移動せずに実行してください）
- Linux/macOS: プロジェクトのルートディレクトリから `scripts/setup.sh` を実行します。（scriptsディレクトリに移動せずに実行してください）

セットアップスクリプトは以下の処理を行います：
1. Python仮想環境を作成
2. 仮想環境を有効化
3. uvをインストール
4. 必要なパッケージをインストール

### 手動セットアップ

1. Python仮想環境を作成して有効化します：

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate.bat
```

#### Linux/macOS:
```bash
python -m venv venv
source venv/bin/activate
```

2. 必要なパッケージをインストールします：

#### uvを使用する場合（推奨・高速）:

```bash
# uvのインストール
pip install uv

# uvを使用してパッケージをインストール
uv pip install -r requirements/base.txt
uv pip install -r requirements/main.txt
```

#### 通常のpipを使用する場合:

```bash
pip install -r requirements/base.txt
pip install -r requirements/main.txt
```

3. `.env` ファイルに各APIのキーを設定します：

```
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
LANGCHANI_API_KEY=your_langchani_api_key_here
```

実際の API キーに書き換えてください。

## 使い方

プログラムを実行する前に、仮想環境を有効化してください：

#### Windows:
```bash
venv\Scripts\activate.bat
```

#### Linux/macOS:
```bash
source venv/bin/activate
```


## 注意事項

- 各APIの利用にはそれぞれのAPIキーが必要です。
- API の利用には各プロバイダーの利用規約が適用されます。
- 画像分析には `PIL` ライブラリを使用しているため、対応している画像形式（JPG、PNG など）のみ使用できます。
- 仮想環境を使用することで、システム全体に影響を与えずにパッケージをインストールできます。