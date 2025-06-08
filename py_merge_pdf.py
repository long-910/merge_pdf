#!/usr/bin/env python3
"""
PDFファイルを結合するスクリプト
"""

import os
import glob
from pathlib import Path
from typing import List, Union
from pypdf import PdfReader, PdfWriter
from tqdm import tqdm


class PdfMergeError(Exception):
    """PDFマージ処理中のエラーを表す例外クラス"""
    pass


def merge_pdfs(
    input_files: List[str],
    output_file: str = "merged.pdf",
    progress: bool = True
) -> None:
    """
    PDFファイルを結合する

    Args:
        input_files: 結合するPDFファイルのパスのリスト
        output_file: 出力ファイルのパス
        progress: 進捗表示の有効/無効

    Raises:
        PdfMergeError: PDFの結合に失敗した場合
    """
    # 出力ディレクトリが存在しない場合は作成
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 入力ファイルの展開
    expanded_files = []
    for file_pattern in input_files:
        expanded_files.extend(glob.glob(file_pattern))

    if not expanded_files:
        raise PdfMergeError("入力ファイルが見つかりません")

    # PDFの結合
    merger = PdfWriter()
    file_iterator = tqdm(expanded_files, desc="PDFファイルを結合中") if progress else expanded_files

    try:
        for file_path in file_iterator:
            if not os.path.exists(file_path):
                raise PdfMergeError(f"ファイルが見つかりません: {file_path}")

            try:
                reader = PdfReader(file_path)
                merger.append(reader)
            except Exception as e:
                raise PdfMergeError(f"PDFファイルの読み込みに失敗しました: {file_path} - {str(e)}")

        # 結合したPDFを保存
        with open(output_file, "wb") as output:
            merger.write(output)

    except Exception as e:
        # エラーが発生した場合は出力ファイルを削除
        if os.path.exists(output_file):
            os.remove(output_file)
        raise PdfMergeError(f"PDFの結合に失敗しました: {str(e)}")


def main():
    """コマンドラインから実行された場合のエントリーポイント"""
    import argparse

    parser = argparse.ArgumentParser(description="PDFファイルを結合する")
    parser.add_argument("input_files", nargs="+", help="結合するPDFファイルのパス")
    parser.add_argument("-o", "--output", default="merged.pdf", help="出力ファイルのパス")
    parser.add_argument("--no-progress", action="store_true", help="進捗表示を無効にする")

    args = parser.parse_args()

    try:
        merge_pdfs(args.input_files, args.output, not args.no_progress)
        print(f"PDFファイルを結合しました: {args.output}")
    except PdfMergeError as e:
        print(f"エラー: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    import sys
    main()
