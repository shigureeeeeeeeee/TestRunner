import sys
import os
import subprocess
import argparse

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"エラー: {stderr}")
        sys.exit(1)
    return stdout

def main():
    parser = argparse.ArgumentParser(description="AtCoder問題のスクレイピングとテスト実行")
    parser.add_argument("problem_url", help="AtCoder問題のURL")
    parser.add_argument("--file", default="../ABC/A.py", help="テスト対象のPythonファイルへのパス（デフォルト: ../ABC/A.py）")
    args = parser.parse_args()

    # カレントディレクトリをTestRunnerに変更
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("問題ページからサンプルケースを取得中...")
    scrape_result = run_command(f"python scrape_atcoder.py {args.problem_url}")
    print(scrape_result)

    if not os.path.exists("formatted_input.txt"):
        print("エラー: サンプルケースの取得に失敗しました。")
        sys.exit(1)

    # テスト対象ファイルの絶対パスを取得
    test_file = os.path.abspath(args.file)
    if not os.path.exists(test_file):
        print(f"エラー: テスト対象ファイル '{test_file}' が見つかりません。")
        sys.exit(1)

    print("テストを実行中...")
    test_output = run_command(f"python test_runner.py {test_file}")
    print(test_output)

    print("全ての処理が完了しました。")

if __name__ == "__main__":
    main()

    #C++に対応させるところからやる