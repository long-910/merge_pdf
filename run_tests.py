#!/usr/bin/env python
import unittest
import sys

if __name__ == "__main__":
    # テストディレクトリをPythonパスに追加
    sys.path.insert(0, ".")

    # テストを検出して実行
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests")

    # テストを実行
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)

    # テスト結果に基づいて終了コードを設定
    sys.exit(not result.wasSuccessful())
