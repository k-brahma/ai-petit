#!/bin/bash
echo "Linting Python files..."

# 仮想環境を有効化
source venv/bin/activate

# isortでインポート文を整理
echo "Running isort..."
python -m isort . --skip venv

# blackでコードをフォーマット
echo "Running black..."
python -m black . --exclude venv

# flake8でコードをチェック
echo "Running flake8..."
python -m flake8 . --exclude=venv

echo "Linting completed!" 