import sqlite3
import pandas as pd

timeframes = ['2006-02']

for timeframe in timeframes :
    connection = sqlite3.connect('{}.db'.format(timeframe))
    c = connection.cursor()
    limit = 5000        # how much we are gonna pull at a time to throw into our pandas dataframe
    last_unix = 0       # helping to buffer our db
    cur_length = limit
    counter = 0
    test_done = False
    while cur_length == limit :
        df = pd.read_sql("SELECT * FROM parent_reply WHERE unix > {} AND parent NOT NULL AND score > 0 ORDER BY unix ASC LIMIT {}".format(last_unix,limit) , connection)
        print(df)
        last_unix = df.tail(1)['unix'].values[0]
        cur_length = len(df)
        if not test_done :
            with open ("test.from" , 'a' , encoding='utf8') as f :
                for content in df['paretn'].values :
                    f.write(content+'\n')
            with open ("test.to" , 'a' , encoding='utf8') as f :
                for content in df['comment'].values :
                    f.write(content+'\n')
            test_done = True
        else:
            with open ("train.from" , 'a' , encoding='utf8') as f :
                for content in df['paretn'].values :
                    f.write(content+'\n')
            with open ("train.to" , 'a' , encoding='utf8') as f :
                for content in df['comment'].values :
                    f.write(content+'\n')

        counter +=1
        if counter % 20 == 0:
            print(counter*limit , ' rows compeleted so far ...')


