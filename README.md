# Gemini API プチプログラム

Google の Gemini API を使用した簡単なプログラム集です。テキスト生成と画像分析の機能を提供します。

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
uv pip install -r requirements.txt
```

#### 通常のpipを使用する場合:

```bash
pip install -r requirements.txt
```

3. `.env` ファイルに Gemini API キーを設定します：

```
GEMINI_API_KEY=your_api_key_here
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

### テキスト生成プログラム

テキスト生成プログラムを実行するには：

```bash
python gemini_app.py
```

プロンプトを入力すると、Gemini API がテキストを生成します。
終了するには `exit` と入力してください。

### 画像分析プログラム

画像分析プログラムを実行するには：

```bash
python gemini_image.py
```

画像ファイルのパスと、画像に対する質問やプロンプトを入力すると、Gemini API が画像を分析して回答します。
終了するには `exit` と入力してください。

## テストの実行

このプロジェクトには、各機能のユニットテストが含まれています。テストは `tests` ディレクトリに配置されています。テストを実行するには、仮想環境を有効化した状態で以下のコマンドを実行してください：

### すべてのテストを実行

```bash
python -m pytest tests/
```

### 特定のテストファイルを実行

```bash
# テキスト生成機能のテスト
python -m pytest tests/test_gemini_app.py

# 画像分析機能のテスト
python -m pytest tests/test_gemini_image.py

# モデル一覧表示機能のテスト
python -m pytest tests/test_list_models.py
```

### 詳細なテスト結果を表示

```bash
python -m pytest tests/ -v
```

### テストカバレッジを確認

テストカバレッジを確認するには、まず `pytest-cov` パッケージをインストールします：

```bash
pip install pytest-cov
```

そして、以下のコマンドでカバレッジレポートを生成します：

```bash
python -m pytest tests/ --cov=.
```

より詳細なHTMLレポートを生成するには：

```bash
python -m pytest tests/ --cov=. --cov-report=html
```

実行後、`htmlcov` ディレクトリ内の `index.html` をブラウザで開くと、詳細なカバレッジレポートを確認できます。

## コードの品質管理

このプロジェクトでは、コードの品質を維持するために以下のlinterツールを使用しています：

- **flake8**: コードスタイルとエラーチェック
- **black**: コードフォーマッター
- **isort**: インポート文の整理

### linterの実行

linterを実行するには、以下のコマンドをプロジェクトのルートディレクトリから実行します（scriptsディレクトリに移動せずに実行してください）：

#### Windows:
```bash
scripts\lint.bat
```

#### Linux/macOS:
```bash
scripts/lint.sh
```

### コードのフォーマット

コードを自動的にフォーマットするには、以下のコマンドをプロジェクトのルートディレクトリから実行します（scriptsディレクトリに移動せずに実行してください）：

#### Windows:
```bash
scripts\format_all.bat
```

#### Linux/macOS:
```bash
scripts/format_all.sh
```

これにより、コードが自動的にフォーマットされ、潜在的な問題が検出されます。

## プロジェクト構造

```
gemini-petit/
├── gemini_app.py        # テキスト生成プログラム
├── gemini_image.py      # 画像分析プログラム
├── list_models.py       # 利用可能なモデル一覧表示プログラム
├── requirements.txt     # 依存パッケージリスト
├── scripts/             # スクリプトディレクトリ
│   ├── setup.bat        # Windows用セットアップスクリプト
│   ├── setup.sh         # Linux/macOS用セットアップスクリプト
│   ├── lint.bat         # Windows用linter実行スクリプト
│   ├── lint.sh          # Linux/macOS用linter実行スクリプト
│   └── format_all.bat   # Windows用フォーマットスクリプト
├── setup.cfg            # flake8とisortの設定ファイル
├── pyproject.toml       # blackの設定ファイル
├── .env                 # 環境変数設定ファイル
├── tests/               # テストディレクトリ
│   ├── __init__.py      # Pythonパッケージ化
│   ├── conftest.py      # pytest設定ファイル
│   ├── test_gemini_app.py    # テキスト生成機能のテスト
│   ├── test_gemini_image.py  # 画像分析機能のテスト
│   └── test_list_models.py   # モデル一覧表示機能のテスト
└── README.md            # プロジェクト説明
```

## 注意事項

- Gemini API の利用には API キーが必要です。
- API の利用には Google の利用規約が適用されます。
- 画像分析には `PIL` ライブラリを使用しているため、対応している画像形式（JPG、PNG など）のみ使用できます。
- 仮想環境を使用することで、システム全体に影響を与えずにパッケージをインストールできます。