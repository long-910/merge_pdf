[![Python application](https://github.com/long-910/merge_pdf/actions/workflows/python-app.yml/badge.svg)](https://github.com/long-910/merge_pdf/actions/workflows/python-app.yml)

# PDF ファイル結合ツール

このツールは、複数の PDF ファイルを簡単に結合するための Python スクリプトです。ワイルドカードパターンを使用して、複数の PDF ファイルを一度に結合することができます。

## 機能

- 複数の PDF ファイルを 1 つのファイルに結合
- ワイルドカードパターンによるファイル選択
- ファイルの存在確認とエラーハンドリング
- 進捗状況の表示
- Docker と DevContainer 対応
- ユニットテスト対応

## 必要条件

### ローカル環境の場合

- Python 3.6 以上
- PyPDF2 ライブラリ

### Docker を使用する場合

- Docker
- Docker Compose（オプション）

## インストール方法

### ローカル環境でのインストール

1. このリポジトリをクローンまたはダウンロードします：

```bash
git clone https://github.com/long-910/merge_pdf.git
cd merge_pdf
```

2. 必要なライブラリをインストールします：

```bash
pip install -r requirements.txt
```

### Docker を使用する場合

1. イメージをビルドします：

```bash
docker build -t pdf-merger .
```

2. コンテナを実行します：

```bash
docker run -v $(pwd):/app pdf-merger "document_*.pdf" -o output.pdf
```

### DevContainer を使用する場合

1. VS Code に「Remote - Containers」拡張機能をインストールします。
2. コマンドパレット（F1）を開き、「Remote-Containers: Reopen in Container」を選択します。
3. コンテナがビルドされ、開発環境が準備されます。

## テストの実行

### ローカル環境でのテスト実行

```bash
# すべてのテストを実行
python run_tests.py

# 特定のテストファイルを実行
python -m unittest tests/test_pdf_merger.py

# 特定のテストケースを実行
python -m unittest tests.test_pdf_merger.TestPdfMerger.test_merge_pdfs_success
```

### Docker でのテスト実行

```bash
# テストを実行
docker run -v $(pwd):/app pdf-merger python run_tests.py
```

## 使用方法

### 基本的な使用方法

```bash
python py_merge_pdf.py "パターン1" "パターン2" [オプション]
```

### 例

1. 特定のパターンに一致するすべての PDF ファイルを結合：

```bash
python py_merge_pdf.py "document_*.pdf"
```

2. 複数のパターンを指定して結合：

```bash
python py_merge_pdf.py "chapter_*.pdf" "appendix_*.pdf"
```

3. 出力ファイル名を指定：

```bash
python py_merge_pdf.py "*.pdf" -o combined_document.pdf
```

### Docker での使用例

```bash
# カレントディレクトリのPDFファイルを結合
docker run -v $(pwd):/app pdf-merger "*.pdf" -o combined.pdf

# 特定のディレクトリのPDFファイルを結合
docker run -v /path/to/pdfs:/app/pdfs pdf-merger "pdfs/*.pdf" -o pdfs/combined.pdf
```

### オプション

- `-o, --output`: 出力ファイル名を指定（デフォルト: output.pdf）

## 注意事項

- 入力ファイルは必ず PDF 形式である必要があります
- ファイル名に日本語を使用する場合は、システムの文字コード設定に注意してください
- 大量のファイルを結合する場合は、十分なメモリが必要です
- Docker を使用する場合、ボリュームマウントのパスは適切に設定してください

## 開発環境

このプロジェクトは DevContainer に対応しており、以下の機能が含まれています：

- Python 開発環境
- コードフォーマッター（Black）
- リンター（Pylint）
- Python 拡張機能
- Docker 拡張機能
- テスト実行環境

## テストカバレッジ

テストは以下の項目をカバーしています：

- 正常系の PDF 結合処理
- ファイルが見つからない場合のエラー処理
- 無効な PDF ファイルの処理
- ワイルドカードパターンを使用した結合処理

## ライセンス

MIT ライセンス

## 作者

[long-910](https://github.com/long-910)

## 貢献

バグ報告や機能改善の提案は、Issue または Pull Request でお願いします。
