from io import StringIO
from unittest.mock import MagicMock, patch

from gemini import gemini_01_list_models


class TestListModels:
    """list_models.pyのテストクラス"""

    @patch("sys.stdout", new_callable=StringIO)
    @patch("google.generativeai.list_models")
    def test_list_models_success(self, mock_list_models, mock_stdout):
        """モデル一覧の取得が成功した場合のテスト"""
        # モックの設定
        mock_model1 = MagicMock()
        mock_model1.name = "models/gemini-1.5-pro"
        mock_model1.display_name = "Gemini 1.5 Pro"
        mock_model1.description = "最も高性能なモデル"
        mock_model1.input_token_limit = 1000000
        mock_model1.output_token_limit = 8192
        mock_model1.supported_generation_methods = ["generateContent", "countTokens"]

        mock_model2 = MagicMock()
        mock_model2.name = "models/gemini-1.5-flash"
        mock_model2.display_name = "Gemini 1.5 Flash"
        mock_model2.description = "高速なモデル"
        mock_model2.input_token_limit = 1000000
        mock_model2.output_token_limit = 8192
        mock_model2.supported_generation_methods = ["generateContent", "countTokens"]

        mock_list_models.return_value = [mock_model1, mock_model2]

        # 関数の実行
        gemini_01_list_models.main()

        # 検証
        output = mock_stdout.getvalue()
        assert "利用可能なGeminiモデルのリスト:" in output
        assert "models/gemini-1.5-pro" in output
        assert "Gemini 1.5 Pro" in output
        assert "最も高性能なモデル" in output
        assert "models/gemini-1.5-flash" in output
        assert "Gemini 1.5 Flash" in output
        assert "高速なモデル" in output

    @patch("sys.stdout", new_callable=StringIO)
    @patch("google.generativeai.list_models")
    def test_list_models_error(self, mock_list_models, mock_stdout):
        """エラーが発生した場合のテスト"""
        # モックの設定
        error_message = "APIエラー"
        mock_list_models.side_effect = Exception(error_message)

        # 関数の実行
        gemini_01_list_models.main()

        # 検証
        output = mock_stdout.getvalue()
        assert "エラーが発生しました" in output
        assert error_message in output
