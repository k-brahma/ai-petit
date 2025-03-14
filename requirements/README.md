# requirements/ ディレクトリにある .txt の読み込み順次について

以下の順序で読んでください。

1. `base.txt`
2. `main.txt`

## 背景:

Google Gemini を利用するのに必要なライブラリ `grpcio` は初回読み込み時に時間がかかることかあります。  
これに依存している `google-generativeai` を `grpcio` がない状態でインストールしようとすると、 Python version 3.13 では失敗します。(2025年3月14日現在)  
ref: [PyPI google-generativeai](https://pypi.org/project/google-generativeai/)

ついては、まずは `base.txt` で `grpcio` をインストールし、その後 `main.txt` で `google-generativeai` をインストールするようにしています。
