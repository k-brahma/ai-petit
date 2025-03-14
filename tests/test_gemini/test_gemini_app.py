from unittest.mock import MagicMock, patch

from gemini.gemini_app import generate_text


class TestGeminiApp:
    """gemini_app.pyのテストクラス"""

    @patch("gemini.gemini_app.model.generate_content")
    def test_generate_text_success(self, mock_generate_content):
        """テキスト生成が成功した場合のテスト"""
        # モックの設定
        mock_response = MagicMock()
        mock_response.text = "テスト回答"
        mock_generate_content.return_value = mock_response

        # 関数の実行
        result = generate_text("テストプロンプト")

        # 検証
        assert result == "テスト回答"
        mock_generate_content.assert_called_once_with("テストプロンプト")

    @patch("gemini.gemini_app.model.generate_content")
    def test_generate_text_empty_input(self, mock_generate_content):
        """空の入力に対するテスト"""
        # 関数の実行
        result = generate_text("")

        # 検証
        assert result == "空の入力は処理できません。何か入力してください。"
        mock_generate_content.assert_not_called()

    @patch("gemini.gemini_app.model.generate_content")
    def test_generate_text_api_error(self, mock_generate_content):
        """APIエラーが発生した場合のテスト"""
        # モックの設定
        error_message = "429 Resource has been exhausted"
        mock_generate_content.side_effect = Exception(error_message)

        # 関数の実行
        result = generate_text("テストプロンプト")

        # 検証
        assert "APIの使用量制限に達しました" in result
        mock_generate_content.assert_called_once_with("テストプロンプト")

    @patch("gemini.gemini_app.model.generate_content")
    def test_generate_text_general_error(self, mock_generate_content):
        """一般的なエラーが発生した場合のテスト"""
        # モックの設定
        error_message = "一般的なエラー"
        mock_generate_content.side_effect = Exception(error_message)

        # 関数の実行
        result = generate_text("テストプロンプト")

        # 検証
        assert "エラーが発生しました" in result
        assert error_message in result
        mock_generate_content.assert_called_once_with("テストプロンプト")
