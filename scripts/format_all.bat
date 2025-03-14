@echo off
echo Formatting all Python files...

:: 仮想環境を有効化
call venv\Scripts\activate.bat

:: isortでインポート文を整理
echo Running isort...
python -m isort . --skip venv

:: blackでコードをフォーマット
echo Running black...
python -m black . --exclude venv

:: flake8でコードをチェック
echo Running flake8...
python -m flake8 . --exclude=venv

echo Formatting completed! 