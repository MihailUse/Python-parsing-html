import pymysql
import pymysql.cursors

def getConnection():
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='root',
                                 db='user_log',
                                 # charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    # connection = pymysql.connect('vacancy.sql')
    return connection