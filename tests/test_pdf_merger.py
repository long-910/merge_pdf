import os
import tempfile
import unittest
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from py_merge_pdf import merge_pdfs, PdfMergeError


class TestPdfMerger(unittest.TestCase):
    def setUp(self):
        # テスト用の一時ディレクトリを作成
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_files = []

        # テスト用のPDFファイルを作成
        for i in range(3):
            file_path = os.path.join(self.test_dir.name, f"test_{i}.pdf")
            writer = PdfWriter()
            writer.add_blank_page(width=612, height=792)  # A4サイズの空白ページ
            with open(file_path, "wb") as f:
                writer.write(f)
            self.test_files.append(file_path)

    def tearDown(self):
        # 一時ディレクトリを削除
        self.test_dir.cleanup()

    def test_merge_pdfs_success(self):
        """正常系のテスト：PDFファイルの結合が成功することを確認"""
        output_path = os.path.join(self.test_dir.name, "output.pdf")
        merge_pdfs(self.test_files, output_path)

        # 出力ファイルが存在することを確認
        self.assertTrue(os.path.exists(output_path))

        # 結合されたPDFのページ数を確認
        with open(output_path, "rb") as f:
            pdf = PdfReader(f)
            self.assertEqual(len(pdf.pages), len(self.test_files))

    def test_merge_pdfs_no_files(self):
        """異常系のテスト：ファイルが見つからない場合の処理を確認"""
        with self.assertRaises(PdfMergeError):
            merge_pdfs(["nonexistent.pdf"])

    def test_merge_pdfs_invalid_file(self):
        """異常系のテスト：無効なPDFファイルの処理を確認"""
        # 無効なPDFファイルを作成
        invalid_pdf = os.path.join(self.test_dir.name, "invalid.pdf")
        with open(invalid_pdf, "wb") as f:
            f.write(b"invalid pdf content")

        output_path = os.path.join(self.test_dir.name, "output.pdf")
        with self.assertRaises(PdfMergeError):
            merge_pdfs([invalid_pdf], output_path)

        # 出力ファイルが作成されないことを確認
        self.assertFalse(os.path.exists(output_path))

    def test_merge_pdfs_with_pattern(self):
        """正常系のテスト：ワイルドカードパターンを使用した結合を確認"""
        output_path = os.path.join(self.test_dir.name, "output.pdf")
        pattern = os.path.join(self.test_dir.name, "test_*.pdf")
        merge_pdfs([pattern], output_path)

        # 出力ファイルが存在することを確認
        self.assertTrue(os.path.exists(output_path))

        # 結合されたPDFのページ数を確認
        with open(output_path, "rb") as f:
            pdf = PdfReader(f)
            self.assertEqual(len(pdf.pages), len(self.test_files))


if __name__ == "__main__":
    unittest.main()
