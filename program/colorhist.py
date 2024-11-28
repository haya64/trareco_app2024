import csv
from PIL import Image
import math
import sys

import Sensitivity


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
f = open("/Users/haya/gdrive/Development/mirai_pj/program/color.csv", "r")
reader = csv.reader(f, delimiter=",")

color = []
for row in reader:
    color.append(row)
# print(color)


# height = 800
# weight = 800

# color_num
n = 9

imagepath_train = Sensitivity.imagepath_train()
imagepath_test = Sensitivity.imagepath_test()
# path = '/Users/haya/gdrive/Development/mirai_pj/test/asakusa.jpeg'

def color_(path):
    # Make a color histogram
    colorhist = [0] * n

    # Load an image
    img = Image.open(path)
    img = img.convert('RGB')
    # img = img.resize((height, weight))

    for x in range(800):
        for y in range(800):
            flag = 0
            idx = 0
            k = 0
            r1, g1, b1 = img.getpixel((x, y)) # 1ピクセルのRGB
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

    # print(['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'black', 'grey', 'white'])
    print(path, colorhist)
    return colorhist


# for p in imagepath_train:
#     p_ = '/Users/haya/gdrive/Development/mirai_pj/train/' + p
#     colorhist = color_(p_)
#     Image_Color_train = Sensitivity.colorappend(p, colorhist)

# for p in imagepath_test:
#     p_ = '/Users/haya/gdrive/Development/mirai_pj/test/' + p
#     colorhist = color_(p_)
#     Image_color_test = Sensitivity.colorappend_test(p, colorhist)

# print(Image_Color_train)
# print(Image_color_test)

Sensitivity.to_csv()