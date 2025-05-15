import  config
import  dataprocess
import  sqlite3
import  pandas as pd
import os

# Install the missing package
config.pkg_loader()
# Create and validate the Database
conn,cur= config.get_connection()
# Create the required table function
dataprocess.dataloading()

