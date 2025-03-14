from unittest.mock import MagicMock, patch

import PIL.Image

from gemini.gemini_03_image import analyze_image


class TestGeminiImage:
    """gemini_image.pyのテストクラス"""

    @patch("PIL.Image.open")
    @patch("gemini.gemini_image.model.generate_content")
    def test_analyze_image_success(self, mock_generate_content, mock_image_open):
        """画像分析が成功した場合のテスト"""
        # モックの設定
        mock_image = MagicMock()
        mock_image_open.return_value = mock_image

        mock_response = MagicMock()
        mock_response.text = "画像分析結果"
        mock_generate_content.return_value = mock_response

        # 関数の実行
        result = analyze_image("test_image.jpg", "画像について説明してください")

        # 検証
        assert result == "画像分析結果"
        mock_image_open.assert_called_once_with("test_image.jpg")
        mock_generate_content.assert_called_once_with(["画像について説明してください", mock_image])

    def test_analyze_image_empty_prompt(self):
        """空のプロンプトに対するテスト"""
        # 関数の実行
        result = analyze_image("test_image.jpg", "")

        # 検証
        assert result == "空の入力は処理できません。何か質問やプロンプトを入力してください。"

    @patch("PIL.Image.open")
    def test_analyze_image_file_not_found(self, mock_image_open):
        """ファイルが見つからない場合のテスト"""
        # モックの設定
        mock_image_open.side_effect = FileNotFoundError()

        # 関数の実行
        result = analyze_image("not_exist.jpg", "画像について説明してください")

        # 検証
        assert "エラー: ファイル 'not_exist.jpg' が見つかりません" == result

    @patch("PIL.Image.open")
    def test_analyze_image_invalid_image(self, mock_image_open):
        """無効な画像ファイルの場合のテスト"""
        # モックの設定
        mock_image_open.side_effect = PIL.UnidentifiedImageError("無効な画像ファイル")

        # 関数の実行
        result = analyze_image("invalid.jpg", "画像について説明してください")

        # 検証
        assert "エラー: 'invalid.jpg' は有効な画像ファイルではありません" == result

    @patch("PIL.Image.open")
    @patch("gemini.gemini_image.model.generate_content")
    def test_analyze_image_api_error(self, mock_generate_content, mock_image_open):
        """APIエラーが発生した場合のテスト"""
        # モックの設定
        mock_image = MagicMock()
        mock_image_open.return_value = mock_image

        error_message = "429 Resource has been exhausted"
        mock_generate_content.side_effect = Exception(error_message)

        # 関数の実行
        result = analyze_image("test_image.jpg", "画像について説明してください")

        # 検証
        assert "APIの使用量制限に達しました" in result

    @patch("PIL.Image.open")
    @patch("gemini.gemini_image.model.generate_content")
    def test_analyze_image_general_error(self, mock_generate_content, mock_image_open):
        """一般的なエラーが発生した場合のテスト"""
        # モックの設定
        mock_image = MagicMock()
        mock_image_open.return_value = mock_image

        error_message = "一般的なエラー"
        mock_generate_content.side_effect = Exception(error_message)

        # 関数の実行
        result = analyze_image("test_image.jpg", "画像について説明してください")

        # 検証
        assert "エラーが発生しました" in result
        assert error_message in result
