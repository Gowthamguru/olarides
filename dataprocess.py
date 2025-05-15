#Import important libraries
from sqlalchemy import  create_engine
from dotenv import find_dotenv, load_dotenv
import os
from urllib.parse import quote_plus
import pandas as pd
import sqlite3


def dataloading():
# Read the csv file and store the data in the data frame
    df = pd.read_excel('OLA_DataSet.xlsx')
#Verify the top 5 rows and column values
    print("Verify the data")

# Verify the data types of the data frame
    df.info()
#Converting the time object into datetime format
    df['Time'] = pd.to_datetime(df['Time'], format = '%H:%M:%S')
    print("Convert the respective format")
#Check the null value data
    print(df.isnull().sum())
    print("Check null values")
# Apply the 0 value in teh V_TAT & C_TAT Columns
    df['V_TAT'] = df['V_TAT'].fillna(0)
    df['C_TAT'] = df['C_TAT'].fillna(0)

#Apply the NA values in the Cancel_rides_by_customer,canceled_rides_by_Driver,incomplete_rides and Incomeplete ride reason
    df['Canceled_Rides_by_Customer']=df['Canceled_Rides_by_Customer'].fillna('NA')
    df['Canceled_Rides_by_Driver']=df['Canceled_Rides_by_Driver'].fillna('NA')
    df['Incomplete_Rides']=df['Incomplete_Rides'].fillna('NA')
    df['Incomplete_Rides_Reason']=df['Incomplete_Rides_Reason'].fillna('NA')
    df['Payment_Method']=df['Payment_Method'].fillna('NA')

#Apply mean value to Driver and customer ratings
    df['Driver_Ratings']=df['Driver_Ratings'].fillna(df['Driver_Ratings'].mean())
    df['Customer_Rating']=df['Customer_Rating'].fillna(df['Customer_Rating'].mean())
    print("Null value fixes applied")
# Validate the null check again
    print(df.isnull().sum())

#Validate the duplicate records
    print(df.duplicated().sum().any())
# Validate the path
    dotenv_path = find_dotenv()
# load the path
    env_val = load_dotenv(dotenv_path)
# MySQL connection string
    if env_val:
        _host = os.getenv("HOST")
        _userid = os.getenv("USER_ID")
        _password = quote_plus(os.getenv("PASSWORD"))
        _database = os.getenv("DATABASE")
        engine = create_engine(f'mysql+mysqlconnector://{_userid}:{_password}@{_host}/{_database}')
        df.to_sql('ola_bookings', con=engine, if_exists='replace', index=False)
        print('Data loading process completed')

# to Fetch the data from SQL tables to Data frame
def fetchfrommysql(query):
    dotenv_path = find_dotenv()
    env_val = load_dotenv(dotenv_path)
    if env_val:
        _host = os.getenv("HOST")
        _userid = os.getenv("USER_ID")
        _password = quote_plus(os.getenv("PASSWORD"))
        _database = os.getenv("DATABASE")
        engine = create_engine(f'mysql+mysqlconnector://{_userid}:{_password}@{_host}/{_database}')
        df = pd.read_sql(query, engine)
        return df
