import sqlite3
import os
from sqlite3 import Error
from twython import Twython
from time import sleep,time
from datetime import datetime
from tqdm import tqdm
import pandas as pd
from pandas import read_sql
DB_PATH=f'{os.getcwd()}/'
DB_NAME='db.sqlite3'
conn=sqlite3.connect(DB_PATH+DB_NAME)
sql=f"INSERT INTO `pages_wallet`(wallet_id,name,email,private_key,public_key"\
        ",private_key_wif) "\
        f""" VALUES('{a0_250}','{a250_500}','{a500_1k}','{a1k_2_5k}',"{a2_5k_5k}",'{a5k_10k}','{a10k_25k}' """\
        f""",'{a25k_50k}','{a50k_100k}','{a_g_100k}','{SEARCH_FOR}','{SEARCH_FOR_ID}')  """
conn.execute(sql)
conn.commit()





conn.close()