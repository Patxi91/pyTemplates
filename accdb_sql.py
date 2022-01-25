import glob
import os
import sys
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

import pyodbc  # SQL Server, DSN connections
import psycopg2  # PostgreSQL
import win32api  # MS-Access: pydobc and win32api
import pymysql  # MySQL or MariaDB
import fdb  # Firebird
import cx_Oracle  # Oracle
import odf  # OpenDocument spreadsheets
import xlrd  # Excel spreadsheets (read only)

from psql_pass import my_pass
from constraints import add_pk, add_fk


# Access prep
dir_path = os.path.dirname(os.path.realpath(__file__))+'\\'
mdb = [file for file in glob.glob("*.accdb")].pop()  # MusterDB

# pyodbc can work with Access DBs that contain ODBC Linked Tables if we disable connection pooling before connecting
pyodbc.pooling = False

# Access-SQL connection
conn_acc = pyodbc.connect(
    Driver='{Microsoft Access Driver (*.mdb, *.accdb)}',
    DBQ=dir_path+mdb,
    UID='AzureAD\FrancsicoOyaga'
    )


try:
    # Azure SQL Verbindung
    my_pass = ['']
    conn_asql = pyodbc.connect(
        DRIVER='{ODBC Driver 17 for SQL Server}',
        SERVER='finversedb.database.windows.net',
        PORT='1433',
        DATABASE='Muster_DB',
        UID='finverse',
        PWD=my_pass.pop(),
        MARS_Connection='Yes')
    '''
    # PostgreSQL Lokal Verbindung
    conn_psql = psycopg2.connect(
        host="localhost",
        dbname="postgres",
        port='5432',
        user="postgres",
        password=my_pass.pop())
    '''
    print("PostgreSQL Verbindung erfolgreich aufgebaut")
except (Exception, psycopg2.DatabaseError) as error:
    print(error)


conn_sql = conn_asql
tables = [table.table_name for table in conn_acc.cursor().tables(tableType='TABLE')]

#connect = f"postgresql+psycopg2://{conn_sql.info.user}:{conn_sql.info.password}@{conn_sql.info.host}:{conn_sql.info.port}/{conn_sql.info.dbname}"
#engine = create_engine(connect, pool_pre_ping=True)
connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=finversedb.database.windows.net;DATABASE=Muster_DB;UID=finverse;PWD="
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
engine = create_engine(connection_url, pool_pre_ping=True, fast_executemany=True)


while tables:

    table_name = tables.pop(0)
    query = 'select * from ' + table_name
    try:
        DataFrame = pd.read_sql(query, conn_acc)
        startTime = datetime.now()
        # Driver
        DataFrame.to_sql(table_name,
                         con=engine,
                         schema=None,
                         if_exists='fail',  # fail, replace, append
                         index=True,
                         index_label=None,
                         chunksize=None,
                         dtype=None,
                         method=None)
        print(f'Tabelle "{table_name}" wurde hinzugefügt. Dauer:{datetime.now() - startTime}s.')
    except:
        print(f'Tabelle "{table_name}" wurde NICHT hinzugefügt.')
        pass
