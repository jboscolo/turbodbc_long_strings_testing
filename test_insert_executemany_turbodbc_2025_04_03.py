
import turbodbc
from turbodbc import Megabytes
import pandas as pd

long_string_for_testing = 'ûéH'*556 #Funny enough if this was multiplied by 555 it would work, anything above fails
short_string = 'test_record'

#Server, database, schema and table names
loading_server='server_name_here
loading_db='db_name_here'
raw_schema='schema_name_here'
raw_table='table_to_test_long_string'

#Setup connection
options=turbodbc.make_options(parameter_sets_to_buffer= 1000
       						,read_buffer_size=Megabytes(250)
							,prefer_unicode = True
							,force_extra_capacity_for_unicode = True	
                            #,fetch_wchar_as_char = True#if this is enable both execute and excutemanycolumns would work - but in SQL server the characters will be incorrectly imported, e.g. Ã»Ã©H
							) 
connection=turbodbc.connect(driver='ODBC Driver 17 for SQL Server'
					 ,server=loading_server
					 ,database=loading_db
					 ,turbodbc_options=options
					 ,pwd=''
					 ,uid=''
					 ,Trusted_Connection='yes'
					 )

#Drop table
sql_drop_stm = f"DROP TABLE IF EXISTS [{loading_db}].[{raw_schema}].[{raw_table}];"
cursor = connection.cursor()
cursor.execute(sql_drop_stm)
connection.commit()

#Create table
sql_create_stm = f"CREATE TABLE [{loading_db}].[{raw_schema}].[{raw_table}] ([a] NVARCHAR(MAX) NULL, [b] NVARCHAR(MAX) NULL);"
cursor = connection.cursor()
cursor.execute(sql_create_stm)
connection.commit()

#Insert via execute
sql_insert_execute_stm = f"INSERT INTO [{loading_db}].[{raw_schema}].[{raw_table}] VALUES ('{short_string}', '{long_string_for_testing}')"
cursor.execute(sql_insert_execute_stm)
connection.commit() #this works!

#Insert via executemany / executemanycolumns
df=pd.DataFrame([[short_string,long_string_for_testing]], columns=list('ab'))
sql_insert_excecutemanycolumns_stm = f"INSERT INTO [{loading_db}].[{raw_schema}].[{raw_table}] VALUES ({'?,'.join(['' for i in df.columns]) + '?'});" 
cursor.executemanycolumns(sql_insert_excecutemanycolumns_stm, [df[column].values for column in df.columns])#this fails!
"""Error returned:
turbodbc.exceptions.DatabaseError: ODBC error
state: HY104
native error code: 0
"""
connection.commit() #this is not reached

