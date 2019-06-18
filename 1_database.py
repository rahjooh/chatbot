__name__ = "__hadi__"

import sqlite3 , json
from datetime import datetime

timeframe = '2006-02'
sql_transaction = []

connection = sqlite3.connect('{}.db'.format(timeframe))
c = connection.cursor()

def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS parent_reply(
                            parent_id TEXT PRIMARY KEY,
                            comment_id TEXT UNIQUE ,
                            parent TEXT ,
                            comment TEXT ,
                            subreddit Text,
                            unix INT ,
                            score INT)""")

def format_data(data):
    return data.replace("\n" , " newlinechar ").replace("\r" , " newlinechar ").replace('"', "'")

def find_existing_score(pid):
    try:
        sql = "SELECT score FROM parent_reply WHERE parent_id = '{}' LIMIT 1".format(pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else:
            return False
    except Exception as e:
        print("find_existing_score",e)
        return False

def acceptable(data):
    if len(data.split(' ')) > 50 or len(data) < 1 :
        return False
    elif len(data) > 1000 :
        return False
    elif data =='[deleted]' or data =='[removed]' :
        return False
    else:
        return True

def transaction_bldr(sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 1000:
        c.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                c.execute(s)
            except:
                pass
        connection.commit()
        sql_transaction = []

def sql_insert_replace_comment(commentid,parentid,parent,comment,subreddit,time,score):
    try:
        sql = """UPDATE parent_reply SET parent_id = ?, comment_id = ?, parent = ?, comment = ?, subreddit = ?, unix = ?, score = ? WHERE parent_id =?;""".format(parentid, commentid, parent, comment, subreddit, int(time), score, parentid)
        transaction_bldr(sql)
    except Exception as e:
        print('s-Update insertion',str(e))

def sql_insert_has_parent(commentid,parentid,parent,comment,subreddit,time,score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}","{}",{},{});""".format(parentid, commentid, parent, comment, subreddit, int(time), score)
        transaction_bldr(sql)
    except Exception as e:
        print('s-Parent insertion',str(e))

def sql_insert_no_parent(commentid,parentid,comment,subreddit,time,score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}",{},{});""".format(parentid, commentid, comment, subreddit, int(time), score)
        transaction_bldr(sql)
    except Exception as e:
        print('s-No_Parent  insertion',str(e))

def find_parent(pid):
    try:
        sql = "SELECT comment FROM parent_reply WHERE comment_id = '{}' LIMIT 1".format(pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else:
            return False
    except Exception as e:
        print("find_parent",e)
        return False

if __name__ == "__hadi__" :
    create_table()
    row_counter = 0    # tedad satr
    paired_rows = 0     # tedad comment haye mortabet

    with open("Data/reddit_comments/{}/RC_{}".format(timeframe.split('-')[0] , timeframe),buffering =1000)  as f :
        for row in f:
            row_counter+=1
            row = json.loads(row)
            parent_id = row['parent_id']
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']
            comment_id = row['link_id']
            parent_data = find_parent(parent_id)

            if score >= 2 :
                print(1,end='')
                if acceptable(body):
                    print(2,end='')
                    existing_comment_score = find_existing_score(parent_id)
                    if existing_comment_score :
                        print(3, end='')
                        if score > existing_comment_score:
                            print(4, end='')
                            sql_insert_replace_comment(comment_id , parent_id , parent_data , body , subreddit ,created_utc , score )
                    else:
                        if acceptable(body):
                            print(-3, end='')
                            if parent_data :
                                print(5, end='')
                                sql_insert_has_parent(comment_id , parent_id , parent_data , body , subreddit ,created_utc , score )
                            else:
                                print(-5, end='')
                                sql_insert_no_parent(comment_id , parent_id , body , subreddit ,created_utc , score )
                print()

            if row_counter % 100000 == 0:
                print('Total Rows Read: {}, Paired Rows: {}, Time: {}'.format(row_counter, paired_rows, str(datetime.now())))
