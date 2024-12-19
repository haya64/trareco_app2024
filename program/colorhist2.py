import csv
from PIL import Image
import math
import sys
import pandas as pd
import glob
import os
import re

def rgb2hsv(r, g, b):
    # RGBをHSVに変換
    mx = max(r, g, b)
    mn = min(r, g, b)
    diff = mx - mn

    if mx == mn:
        h = 0
    elif mx == r:
        h = 60 * ((g - b) / diff) % 360
    elif mx == g:
        h = 60 * ((b - r) / diff) + 120
    else:
        h = 60 * ((r - g) / diff) + 240

    s = 0 if mx == 0 else diff / mx
    v = mx / 255

    return h / 2, s * 255, v * 255  # 0-179, 0-255, 0-255にスケール

def godlove(h1, s1, v1, h2, s2, v2):
    # 色空間の距離を計算
    _1 = s1 * s2
    _4 = abs(h1 - h2) / 100
    _3 = math.cos(2 * math.pi * _4)
    _2 = 1 - _3
    _5 = (abs(s1 - s2)) ** 2
    _6 = (4 * abs(v1 - v2)) ** 2
    return (_1 * _2 + _5 + _6) / 2

def color_(path, colors, n):
    # 画像の色ヒストグラムを計算
    colorhist = [0] * n
    img = Image.open(path).convert('RGB').resize((400, 600))

    for x in range(400):
        for y in range(600):
            r1, g1, b1 = img.getpixel((x, y))
            h1, s1, v1 = rgb2hsv(r1, g1, b1)

            min_dist = float('inf')
            idx = -1

            for k, (r2, g2, b2) in enumerate(colors):
                h2, s2, v2 = rgb2hsv(r2, g2, b2)
                d = godlove(h1, s1, v1, h2, s2, v2)
                if d < min_dist:
                    min_dist = d
                    idx = k

            colorhist[idx] += 1

    return colorhist

def natural_sort_key(file_name):
    """
    自然順ソート用のキーを生成
    数値部分を抽出して比較に利用
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', file_name)]

def main():
    # 色データの読み込み
    csv_path = "/Users/haya/Development/university_class/mirai_pj/program/color2.csv"
    try:
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            colors = [list(map(int, row)) for row in reader]
    except Exception as e:
        print(f"Error reading {csv_path}: {e}")
        sys.exit(1)

    n = len(colors)

    # 画像のパスを取得
    global_path = "/Users/haya/Development/university_class/mirai_pj/trareco_system/program/flask/trarecoapp/static/return_images"
    file_list = glob.glob(os.path.join(global_path, '*.*'))
    if not file_list:
        print(f"No images found in {global_path}")
        sys.exit(1)

    # ファイル名の自然順ソート
    name_list = sorted([os.path.basename(file) for file in file_list], key=natural_sort_key)

    # ヒストグラム計算
    records = []
    for x, name in enumerate(name_list):
        img_path = os.path.join(global_path, name)
        try:
            hist = color_(img_path, colors, n)
            hist.insert(0, name)
            records.append(hist)
            print(f"{x + 1}/{len(name_list)}: Processed {name}")
        except Exception as e:
            print(f"Error processing {name}: {e}")

    # データフレーム作成
    cols = ['path', 'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'purple', 'black', 'gray', 'white']
    df = pd.DataFrame(records, columns=cols)

    # エクセルに保存
    output_path = "/Users/haya/Development/university_class/mirai_pj/data/データセット1.xlsx"
    try:
        df.to_excel(output_path, index=False, sheet_name='return_color', engine='openpyxl')
        print(f"Data saved to {output_path}")
    except Exception as e:
        print(f"Error saving to {output_path}: {e}")

if __name__ == "__main__":
    main()