import os
import glob
import argparse
import sys
from PyPDF2 import PdfMerger
from PyPDF2.errors import PdfReadError


class PdfMergeError(Exception):
    """PDF結合処理中のエラーを表す例外クラス"""
    pass


def merge_pdfs(pdf_patterns, output_path="output.pdf"):
    merger = PdfMerger()
    pdf_files = []
    total_files = 0
    processed_files = 0

    # 各パターンに対してglobを実行し、ファイルリストを作成
    for pattern in pdf_patterns:
        matched_files = sorted(glob.glob(pattern))
        if not matched_files:
            print(
                f"警告: パターン '{pattern}' に一致するPDFファイルが見つかりませんでした。"
            )
        pdf_files.extend(matched_files)

    total_files = len(pdf_files)
    if not pdf_files:
        print("エラー: 処理可能なPDFファイルが見つかりませんでした。")
        raise PdfMergeError("処理可能なPDFファイルが見つかりませんでした。")

    print(f"合計 {total_files} 個のPDFファイルを処理します。")

    # PDFファイルを結合
    for pdf in pdf_files:
        if os.path.exists(pdf):
            try:
                print(f"処理中 ({processed_files + 1}/{total_files}): {pdf}")
                merger.append(pdf)
                processed_files += 1
            except PdfReadError:
                print(
                    f"エラー: {pdf} は有効なPDFファイルではありません。スキップします。"
                )
            except Exception as e:
                print(f"エラー: {pdf} の処理中に問題が発生しました: {str(e)}")
        else:
            print(f"警告: {pdf} が見つかりませんでした。スキップします。")

    if processed_files == 0:
        print("エラー: 処理可能なPDFファイルがありませんでした。")
        raise PdfMergeError("処理可能なPDFファイルがありませんでした。")

    try:
        merger.write(output_path)
        merger.close()
        print(f"\n結合完了: {output_path}")
        print(f"処理したファイル数: {processed_files}/{total_files}")
    except Exception as e:
        print(f"エラー: 出力ファイルの作成中に問題が発生しました: {str(e)}")
        raise PdfMergeError(f"出力ファイルの作成中に問題が発生しました: {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description="複数のPDFファイルを結合します。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python py_merge_pdf.py "document_*.pdf"
  python py_merge_pdf.py "chapter_*.pdf" "appendix_*.pdf" -o combined_document.pdf
        """,
    )
    parser.add_argument(
        "patterns", nargs="+", help="結合するPDFファイルのパターン（例：document_202*.pdf）"
    )
    parser.add_argument(
        "-o",
        "--output",
        default="output.pdf",
        help="出力ファイル名（デフォルト: output.pdf）",
    )

    args = parser.parse_args()
    try:
        merge_pdfs(args.patterns, args.output)
    except PdfMergeError as e:
        print(f"エラー: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
