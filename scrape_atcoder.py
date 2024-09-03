import requests
from bs4 import BeautifulSoup
import sys

def scrape_atcoder_samples(problem_url):
    response = requests.get(problem_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    samples = []
    sample_sections = soup.find_all('div', class_='part')

    for section in sample_sections:
        h3 = section.find('h3')
        if h3 and '入力例' in h3.text:
            input_pre = section.find('pre')
            if input_pre:
                input_text = input_pre.text.strip()
                # 対応する出力例を探す
                output_section = section.find_next_sibling('div', class_='part')
                if output_section:
                    output_pre = output_section.find('pre')
                    if output_pre:
                        output_text = output_pre.text.strip()
                        samples.append((input_text, output_text))

    return samples

def save_samples(samples, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, (input_text, output_text) in enumerate(samples, 1):
            f.write(f"[入力例 {i}]\n{input_text}\n\n")
            f.write(f"[出力例 {i}]\n{output_text}\n\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python scrape_atcoder.py <問題URL>")
        sys.exit(1)

    problem_url = sys.argv[1]
    samples = scrape_atcoder_samples(problem_url)

    if not samples:
        print("サンプルケースが見つかりませんでした。")
    else:
        save_samples(samples, 'formatted_input.txt')
        print(f"{len(samples)}個のサンプルケースを取得しました。結果は 'formatted_input.txt' に保存されています。")