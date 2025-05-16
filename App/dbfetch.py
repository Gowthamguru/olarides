import sqlite3
import os
import pandas as pd
def fetchfrommysql(query):
    db_path = os.path.join('data','ola_rides.db')
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(query, conn)
    return df