import subprocess
import sys

def run_test(command, input_data):
    result = subprocess.run(command, input=input_data, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def compare_output(expected, actual):
    return expected.strip() == actual.strip()

def run_tests(script_path):
    with open('formatted_input.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    test_cases = content.split('[入力例')[1:]
    total_tests = len(test_cases)
    passed_tests = 0

    for i, test_case in enumerate(test_cases, 1):
        parts = test_case.split('[出力例')
        input_data = parts[0].split(']', 1)[1].strip()
        expected_output = parts[1].split(']', 1)[1].strip()

        # 入力データの空行を削除
        input_data = '\n'.join(line for line in input_data.split('\n') if line.strip())

        print(f"\nテストケース {i}:")
        print(f"入力:\n{input_data}")
        print(f"期待される出力:\n{expected_output}")

        actual_output, error, return_code = run_test(['python', script_path], input_data)

        if return_code != 0:
            print(f"エラー (終了コード {return_code}):")
            print(error)
            continue

        print(f"実際の出力:\n{actual_output}")

        if compare_output(expected_output, actual_output):
            print("結果: 正解")
            passed_tests += 1
        else:
            print("結果: 不正解")

    print(f"\nテスト結果: {passed_tests}/{total_tests} 正解")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python test_runner.py <テスト対象のPythonファイル>")
        sys.exit(1)

    script_path = sys.argv[1]
    run_tests(script_path)