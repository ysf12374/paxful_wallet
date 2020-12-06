#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 20:26:55 2020

@author: yousuf
"""
import sqlite3
from sqlite3 import Error
from twython import Twython
from time import sleep,time
from datetime import datetime
from tqdm import tqdm
import pandas as pd
from pandas import read_sql
DB_PATH='/home/yousuf/Downloads/twitter_api/twitter_api/'
DB_NAME='twitter_tweets'
ACCESS_TOKEN="407011412-54PkRF8mmKa7tpheK5nGBBgML6iy5t1FapNnZra3"
ACCESS_TOKEN_SECRET="Sq2BYln4kFCDask9NQhUues29Pq9mwUi6JrIuX3O5j3eA"
API_KEY="raAdamXVlnxMd9JW4hiRFvu66"
API_SECRET_KEY="BjJsbrz1YpT0fp1r1Zwp27k1FUbkDD8cd9Fs7jnXzIsReYdtVR"

SEARCH_FOR='_KSU'
SEARCH_FOR_ID='18916965'
start=time()

twitter = Twython(
API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
user=twitter.lookup_user(screen_name='_KSU')
conn=sqlite3.connect(DB_PATH+DB_NAME)

tweets=read_sql('select * from tweets',con=conn,index_col=['id'])
influencers=read_sql('select * from influencers',con=conn,index_col=['id'])
users=read_sql('select * from users_ where screen_name="_KSU" order by inserted_at desc',con=conn,index_col=['id'])
mentions=influencers[influencers['to_id_str']!='{SEACH_OR_ID}']
retweets=influencers[influencers['to_id_str']=='{SEACH_OR_ID}']
influencers.index=list(range(1,len(influencers)+1))


tweets['retweet_count'] =pd.to_numeric(tweets['retweet_count'], errors ='coerce').fillna(0).astype('int')
tweets_=users['statuses_count'][0]
mentions_=len(mentions)
avg_retweets_=int(tweets['retweet_count'].mean())
followers_=users['followers_count'][0]
following_=users['friends_count'][0]
favourites_=users['favourites_count'][0]
retweets_mentions_by_user_=users['listed_count'][0]

retweets['created_at']=retweets['created_at'].apply(lambda x: datetime.strptime(x, '%a %b %d %H:%M:%S +0000 %Y'))
retweets['inserted_at']=retweets['inserted_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
tweets['created_at']=tweets['created_at'].apply(lambda x: datetime.strptime(x, '%a %b %d %H:%M:%S +0000 %Y'))
tweets['inserted_at']=tweets['inserted_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
tweets['created_date_md']=tweets['created_at'].apply(lambda x: str(x.day)+'/'+str(x.month)+'/'+str(x.year))
tweets_df = (tweets.groupby('created_date_md', as_index=False)
       .agg({'id_str':'count', 'retweet_count':'mean'})).reset_index(drop=True)

tweets_df['retweet_count']=tweets_df['retweet_count'].astype(int)

influencers['created_at']=influencers['created_at'].apply(lambda x: datetime.strptime(x, '%a %b %d %H:%M:%S +0000 %Y'))
influencers['inserted_at']=influencers['inserted_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
influencers['created_date_md']=influencers['created_at'].apply(lambda x: str(x.day)+'/'+str(x.month)+'/'+str(x.year))
influencers_df = (influencers.groupby('created_date_md', as_index=False)
       .agg({'id_str':'count'})).reset_index(drop=True)
influencers_df['create_date']=influencers_df['created_date_md'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y'))
influencers_df=influencers_df.sort_values('create_date')
from_screen_name=list(retweets['from_screen_name'].unique())


conn.close()
DB_NAME='twitter'
conn=sqlite3.connect(DB_PATH+DB_NAME)

followers=read_sql('select * from followers',con=conn,index_col=['id'])
followers['followers_count']=followers['followers_count'].astype(int)
followers['created_at']=followers['created_at'].apply(lambda x: datetime.strptime(x, '%a %b %d %H:%M:%S +0000 %Y'))
followers['inserted_at']=followers['inserted_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
followers['created_date_md']=followers['created_at'].apply(lambda x: int(((datetime.now()-x).days)/365))
followers_df = (followers.groupby('created_date_md', as_index=False)
       .agg({'id_str':'count'})).reset_index(drop=True)

"""0-1k
1k-2.5k
2.5k-5k
5k-10k
10k-25k
25k-50k
50k-1m
1m>"""


a0_250=0
a250_500=0
a500_1k=0
a1k_2_5k=0
a2_5k_5k=0
a5k_10k=0
a10k_25k=0
a25k_50k=0
a50k_100k=0
a_g_100k=0
conn.close()

DB_NAME='twitter_tweets'

conn=sqlite3.connect(DB_PATH+DB_NAME)

for i in tqdm(followers['followers_count'].iteritems(),total=len(followers['followers_count'])):
    f=i[1]
    if f<250:
        s='0-250'
        a0_250+=1        
    elif 251<f<500:
        s='250-500'
        a250_500+=1
    elif 501<f<1000:
        s='500-1K'
        a500_1k+=1
    elif 1001<f<2500:
        s='1K-2.5K'
        a1k_2_5k+=1
    elif 2501<f<5000:
        s='2.5K-5K'
        a2_5k_5k+=1
    elif 5001<f<10000:
        s='5K-10K'
        a5k_10k+=1
    elif 10001<f<25000:
        s='10K-25K'
        a10k_25k+=1
    elif 25001<f<50000:
        s='25K-50K'
        a25k_50k+=1
    elif 50001<f<100000:
        s='50K-100K'
        a50k_100k+=1
    else:
        s='>100K'
        a_g_100k+=1
#    sql=f"""UPDATE followers
#              SET lang = '{s}' 
#              WHERE id_str = '{i[7]}' """
#    conn.execute(sql)


sql=f"INSERT INTO `followers_followers`(a0_250,a250_500,a500_1k,a1k_2_5k,a2_5k_5k"\
        ",a5k_10k,a10k_25k,a25k_50k"\
        ",a50k_100k,a_g_100k,screen_name,id_str) "\
        f""" VALUES('{a0_250}','{a250_500}','{a500_1k}','{a1k_2_5k}',"{a2_5k_5k}",'{a5k_10k}','{a10k_25k}' """\
        f""",'{a25k_50k}','{a50k_100k}','{a_g_100k}','{SEARCH_FOR}','{SEARCH_FOR_ID}')  """
conn.execute(sql)
conn.commit()

conn=sqlite3.connect(DB_PATH+DB_NAME)

for i in followers_df.itertuples():
    years=i[1]
    count=i[2]
    sql=f"INSERT INTO `followers_age`(years,count,screen_name,id_str) "\
        f""" VALUES('{years}','{count}','{SEARCH_FOR}','{SEARCH_FOR_ID}')  """
    conn.execute(sql)
    conn.commit()












































conn.close()



