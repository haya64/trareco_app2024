from datetime import datetime
import psycopg2


dt_now = datetime.now()
dt_now_month = dt_now.month

print(dt_now_month)

# 気候学上の四季(1:春,2:夏,3:秋,4:冬)
if 3 <= dt_now_month <= 5:
    season = 1
    print('春')
elif 6 <= dt_now_month <= 8:
    season = 2
    print('夏')
elif 9 <= dt_now_month <= 11:
    season = 3
    print('秋')
else:
    season = 4
    print('冬')


'''
### 以下DBとの接続 ###

# connect postgreSQL
users = 'haya'
dbnames = 'sample'
passwords = 'Hayaki@4477'
conn = psycopg2.connect(" user=" + users +" dbname=" + dbnames +" password=" + passwords)

# excexute sql
cur = conn.cursor()
cur.execute('SELECT * FROM weather;')
results = cur.fetchall()

#output result
print(results)

cur.close()
conn.close()

'''