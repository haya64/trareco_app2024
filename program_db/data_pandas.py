from operator import index
import pandas as pd
import numpy as np


# Image_Color_train = pd.read_excel('/Users/haya/gdrive/Development/mirai_pj/data/miraipj.xlsx', sheet_name=0)
# Image_Color_test = pd.read_excel('/Users/haya/gdrive/Development/mirai_pj/data/miraipj.xlsx', sheet_name=2)
# Impression_Color = pd.read_excel('/Users/haya/gdrive/Development/mirai_pj/data/miraipj.xlsx', sheet_name=1,)
Image_Color_train = pd.read_csv('/Users/haya/gdrive/Development/mirai_pj/data/Image_Color_train.csv', index_col=0)
Image_Color_test = pd.read_csv('/Users/haya/gdrive/Development/mirai_pj/data/Image_Color_test.csv', index_col=0)
Impression_Color = pd.read_csv('/Users/haya/gdrive/Development/mirai_pj/data/Impression_Color.csv', index_col=0)

# print(Image_Color_train)
# print(Image_Color_test)
# print(Impression_Color)

# impressions_colors
def len_impression():
    Impression_Color = pd.read_excel('/Users/haya/gdrive/Development/mirai_pj/data/miraipj.xlsx', sheet_name=1,)
    len_num = len(Impression_Color.index)
    return len_num

# image_color_train, image_train_detail
def len_train():
    Image_Color_train = pd.read_excel('/Users/haya/gdrive/Development/mirai_pj/data/miraipj.xlsx', sheet_name=0)
    len_num = len(Image_Color_train.index)
    return len_num

# image_color_test, image_test_detail
def len_test():
    Image_Color_test = pd.read_excel('/Users/haya/gdrive/Development/mirai_pj/data/miraipj.xlsx', sheet_name=2)
    len_num = len(Image_Color_test.index)
    return len_num

# impressions_colors
def read_impression(num):
    Impression_Color = pd.read_excel('/Users/haya/gdrive/Development/mirai_pj/data/miraipj.xlsx', sheet_name=1)
    Impression_Color_record = Impression_Color.iloc[num,:].values
    return Impression_Color_record

# image_color_train
def read_train(num):
    Image_Color_train = pd.read_excel('/Users/haya/gdrive/Development/mirai_pj/data/miraipj.xlsx', sheet_name=0)
    Image_Color_train_record = Image_Color_train.iloc[num,:].values
    return Image_Color_train_record

# image_color_test
def read_test(num):
    Image_Color_test = pd.read_excel('/Users/haya/gdrive/Development/mirai_pj/data/miraipj.xlsx', sheet_name=2)
    Image_Color_test_record = Image_Color_test.iloc[num,:].values
    return Image_Color_test_record

# image_train_detail
def read_train_detail(num):
    Image_train_detail = pd.read_excel('/Users/haya/gdrive/Development/mirai_pj/data/miraipj.xlsx', sheet_name=3)
    Image_train_detail_record = Image_train_detail.iloc[num,:].values
    return Image_train_detail_record

# image_test_detail
def read_test_detail(num):
    Image_test_detail = pd.read_excel('/Users/haya/gdrive/Development/mirai_pj/data/miraipj.xlsx', sheet_name=4)
    Image_test_detail_record = Image_test_detail.iloc[num,:].values
    return Image_test_detail_record

def to_xlsx(Image_Color_train, Image_Color_test, Impression_Color):
    with pd.ExcelWriter('/Users/haya/gdrive/Development/mirai_pj/data/data.xlsx') as writer:
        Image_Color_train.to_excel(writer, sheet_name='Image_Color_train', index=False)
        Image_Color_test.to_excel(writer, sheet_name='Image_Color_test', index=False)
        Impression_Color.to_excel(writer, sheet_name='Impression_Color', index=False)
    
# to_xlsx(Image_Color_train, Image_Color_test, Impression_Color)