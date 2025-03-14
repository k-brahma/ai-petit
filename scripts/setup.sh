#!/bin/bash
echo "Gemini API プチプログラム セットアップ"
echo "=============================="

echo "1. 仮想環境を作成しています..."
python -m venv venv

echo "2. 仮想環境を有効化しています..."
source venv/bin/activate

echo "3. uvをインストールしています..."
pip install uv

echo "4. 必要なパッケージをインストールしています..."
python -m uv pip install -r requirements/base.txt
python -m uv pip install -r requirements/main.txt
python -m uv pip install -r requirements/test.txt

echo "セットアップが完了しました！"
echo ""
echo "プログラムを実行する前に、仮想環境を有効化してください:"
echo "  source venv/bin/activate" 