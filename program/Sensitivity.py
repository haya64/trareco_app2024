import pandas as pd
import numpy as np


Image_Color_train = pd.read_excel('/Users/haya/gdrive/Development/mirai_pj/data/miraipj.xlsx', sheet_name=0)
Image_Color_test = pd.read_excel('/Users/haya/gdrive/Development/mirai_pj/data/miraipj.xlsx', sheet_name=2)
Impression_Color = pd.read_excel('/Users/haya/gdrive/Development/mirai_pj/data/miraipj.xlsx', sheet_name=1)


# print(Image_Color)
# print(Image_Color.iloc[:,1:])

# 画像のpath
def imagepath_train():
    path = Image_Color_train.iloc[:,0].values.tolist()
    # print(path)
    return path

def imagepath_test():
    path = Image_Color_test.iloc[:,0].values.tolist()
    # print(path)
    return path


color_9 = Image_Color_train.columns[1:]
def colorappend(path, colorhist):
    # color_9 = Image_Color.columns[1:]
    # path = 'acuaparkshinagawa.jpg'
    Image_Color_train.loc[Image_Color_train[Image_Color_train['Image'] == path].index, color_9] = colorhist
    print(Image_Color_train.loc[Image_Color_train[Image_Color_train['Image'] == path].index, color_9], '\n')
    return Image_Color_train

def colorappend_test(path, colorhist):
    # color_9 = Image_Color.columns[1:]
    # path = 'acuaparkshinagawa.jpg'
    Image_Color_test.loc[Image_Color_test[Image_Color_test['Image'] == path].index, color_9] = colorhist
    print(Image_Color_test.loc[Image_Color_test[Image_Color_test['Image'] == path].index, color_9], '\n')
    return Image_Color_test

def to_csv():
    Image_Color_train.to_csv('/Users/haya/gdrive/Development/mirai_pj/data/Image_Color_train.csv', sep=',')
    Image_Color_test.to_csv('/Users/haya/gdrive/Development/mirai_pj/data/Image_Color_test.csv', sep=',')
    Impression_Color.to_csv('/Users/haya/gdrive/Development/mirai_pj/data/Impression_Color.csv', sep=',')
