# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:27:27 2023

@author: taina.esteves
"""

import pyodbc 
import pandas as pd

connection_string = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\Public\MyTest.accdb;'
)
cnxn = pyodbc.connect(connection_string, autocommit=True)
crsr = cnxn.cursor()

# prepare test environment
table_name = "monitoramento"
if list(crsr.tables(table_name)):
    crsr.execute(f"DROP TABLE [{table_name}]")
crsr.execute(f"CREATE TABLE [{table_name}] (ID COUNTER PRIMARY KEY, employee_id TEXT(25))")

# test data
df = pd.DataFrame([[1, 'employee1'], [2, 'employee2']], columns=['ID', 'employee_id'])

# insert the rows from the DataFrame into the Access table    
crsr.executemany(
    f"INSERT INTO [{table_name}] (ID, employee_id) VALUES (?, ?)",
    df.itertuples(index=False))