import pandas as pd
import glob
import os


cols = ['path', 'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'purple', 'black', 'gray', 'white']
df = pd.DataFrame(index=[], columns=cols)

file_list = glob.glob('/Users/haya/Development/aniversity_lecture/mirai_pj/test_pictures/*.*')
name_list = [os.path.basename(file) for file in file_list]

name_list = sorted(name_list)
print(name_list) # 画像のファイル名
image_num = len(name_list)


record = pd.Series(['hoge', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], index=df.columns)
for _ in range(image_num):
    df = df.append(record, ignore_index=True)

x = 0
for n in name_list:
    df.iloc[x,0] = n
    x +=1

print(df)