import csv
from PIL import Image
import math
import sys
import pandas as pd
import glob
import os

def rgb2hsv(r, g, b):
    # R, G, Bの値を取得して0～1の範囲内にする
    #[b, g, r] = src[y][x]/255.0
    # R, G, Bの値から最大値と最小値を計算
    mx = max(r, g, b)
    mn = min(r, g, b)

    # 最大値 - 最小値
    diff = mx - mn

    # Hの値を計算
    if mx == mn : h = 0
    elif mx == r : h = 60 * ((g-b)/diff)
    elif mx == g : h = 60 * ((b-r)/diff) + 120
    elif mx == b : h = 60 * ((r-g)/diff) + 240
    if h < 0 : h = h + 360
    # Sの値を計算
    if mx != 0:s = diff/mx
    else: s = 0

    # Vの値を計算
    v = mx

    # Hを0～179, SとVを0～255の範囲の値に変換
    return h * 0.5, s * 255, v * 255

def godlove(h1, s1, v1, h2, s2, v2):
    _1 = s1*s2
    _4 = abs(h1 - h2) / 100
    _3 = math.cos(2*math.pi*_4)
    _2 = (1 - _3) 
    _5 = (abs(s1 - s2)) * (abs(s1 - s2))
    _6 = (4 * abs(v1 - v2)) * (4 * abs(v1 - v2))
    r = (math.trunc(_1 * _2 + _5 + _6)) / 2
    return r

args = sys.argv

# Read CSV file
f = open("/Users/haya/Development/aniversity_lecture/mirai_pj/program/color2.csv", "r")
reader = csv.reader(f, delimiter=",")

color = []
for row in reader:
    color.append(row)
# print(color)


# height = 800
# weight = 800

# color_num
n = 10

def color_(path):
    # Make a color histogram
    colorhist = [0] * n

    # Load an image
    img = Image.open(path)
    # img = cv2.imread(path)
    # print("リサイズ前(高さ,幅,色)="+str(img.size))
    img = img.convert('RGB')
    # 画像の拡大・縮小（INTER_NEAREST)
    n_img = img.resize((400,600))
    # print("リサイズ後(高さ,幅,色)="+str(n_img.size))

    for x in range(400):
        for y in range(600):
            flag = 0
            idx = 0
            k = 0
            r1, g1, b1 = n_img.getpixel((x, y)) # 1ピクセルのRGB
            h1, s1, v1 = rgb2hsv(r1, g1, b1)

            for k in range(n):
                r2 = int(color[k][0])
                g2 = int(color[k][1])
                b2 = int(color[k][2])
                h2, s2, v2 = rgb2hsv(r2, g2, b2)
                d = godlove(h1, s1, v1, h2, s2, v2)


                if flag == 1:
                    if m > d:
                        m = d
                        idx = k
                else:
                    m = d
                    flag = 1

            colorhist[idx] = colorhist[idx] + 1

    # print(['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'purple', 'black', 'gray', 'white'])
    # 色
    # print(f'\n',
    #       'red %d'%colorhist[0], '\n',
    #       'orange %d'%colorhist[1], '\n',
    #       'yellow %d'%colorhist[2], '\n',
    #       'green %d'%colorhist[3], '\n',
    #       'blue %d'%colorhist[4], '\n',
    #       'indigo %d'%colorhist[5], '\n',
    #       'purple %d'%colorhist[6], '\n',
    #       'black %d'%colorhist[7], '\n',
    #       'gray %d'%colorhist[8], '\n',
    #       'white %d'%colorhist[9], '\n',)
    # print(colorhist)
    # print(sum(colorhist))
    return colorhist

# 画像

# global_path = '/Users/haya/Development/aniversity_lecture/mirai_pj/test_pictures/'
global_path = '/Users/haya/Development/aniversity_lecture/mirai_pj/return_spot/'

# ファイル名
file_list = glob.glob(global_path+'*.*')
name_list = [os.path.basename(file) for file in file_list]

name_list = sorted(name_list)
# print(name_list) # 画像のファイル名
image_num = len(name_list)

# df

cols = ['path', 'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'purple', 'black', 'gray', 'white']
df = pd.DataFrame(index=[], columns=cols)

record = pd.Series(['hoge', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], index=df.columns)
for _ in range(image_num):
    df = df.append(record, ignore_index=True)

x = 0
for p in name_list:
    print(x, '列')
    c = color_(global_path+p)
    c.insert(0, p)
    df.iloc[x] = c
    # print(df)
    x +=1
    # print(c)

print(df)

# excelシートに書き込み
df.to_excel('/Users/haya/Development/aniversity_lecture/mirai_pj/data/2_.xlsx', sheet_name='return_color')