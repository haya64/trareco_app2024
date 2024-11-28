import re
from dataaccess import DataAccess 
import data_pandas

# detaをinsertする

da = DataAccess()

# train_images_colors
query_train_1 = 'INSERT INTO train_images_colors (path, red, blue, green, yellow, purple, orange, black, gray,  white) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'

# train_images_details
query_train_2 = 'INSERT INTO train_images_details (path, name, category, subject, time, location_x, location_y) VALUES (%s, %s, %s, %s, %s, %s, %s);'

# test_images_colors
query_test_1 = 'INSERT INTO test_images_colors (path, red, blue, green, yellow, purple, orange, black, gray,  white) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'

# test_images_details
query_test_2 = 'INSERT INTO test_images_details (path, name, category, subject, time, location_x, location_y) VALUES (%s, %s, %s, %s, %s, %s, %s);'

# impressions_colors
query_impressions = 'INSERT INTO impressions_colors (impression, red, blue, green, yellow, purple, orange, black, gray, white) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'


# train_colors ok
"""
len_num = data_pandas.len_train()
for i in range(len_num):
    record = data_pandas.read_train(i)
    path = record[0]
    red = record[1]
    blue = record[2]
    green = record[3]
    yellow = record[4]
    purple = record[5]
    orange = record[6]
    black = record[7]
    gray = record[8]
    white = record[9]
    da.save_data_1(query_train_1, path, red, blue, green, yellow, purple, orange, black, gray, white)
"""

# train_details ok
"""
len_num = data_pandas.len_train()
for i in range(len_num):
    record = data_pandas.read_train_detail(i)
    path = record[0]
    name = record[1]
    category = record[2]
    subject = record[3]
    time = record[4]
    location_x = record[5]
    location_y = record[6]
    da.save_data_2(query_train_2, path, name, category, subject, time, location_x, location_y)
"""


# test_colors ok
"""
len_num = data_pandas.len_test()
for i in range(len_num):
    record = data_pandas.read_test(i)
    path = record[0]
    red = record[1]
    blue = record[2]
    green = record[3]
    yellow = record[4]
    purple = record[5]
    orange = record[6]
    black = record[7]
    gray = record[8]
    white = record[9]
    da.save_data_1(query_test_1, path, red, blue, green, yellow, purple, orange, black, gray, white)
"""

# test_details ok
len_num = data_pandas.len_test()
for i in range(len_num):
    record = data_pandas.read_test_detail(i)
    path = record[0]
    name = record[1]
    category = record[2]
    subject = record[3]
    time = record[4]
    location_x = record[5]
    location_y = record[6]
    da.save_data_2(query_test_2, path, name, category, subject, time, location_x, location_y)


# impressions_colors ok
"""
len_num = data_pandas.len_impression()
for i in range(len_num):
    record = data_pandas.read_impression(i)
    impression = record[0]
    red = record[1]
    blue = record[2]
    green = record[3]
    yellow = record[4]
    purple = record[5]
    orange = record[6]
    black = record[7]
    gray = record[8]
    white = record[9]
    da.save_data_impression(query_impressions, impression, red, blue, green, yellow, purple, orange, black, gray, white)
"""