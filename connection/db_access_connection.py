# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:27:27 2023

@author: taina.esteves
"""

#import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import logging
#import pymysql
#import mysql.connector
#from mysql.connector import errorcode


def write_df_into_table(database, df, tabela):
    
 
    user =  'auditor'
    pwd =  '4ud1t0r'
    hostname = 'auditordb.inep.gov.br'
           
    engine = create_engine("mariadb+pymysql://{user}:{pwd}@{host}/{db}".format(host=hostname, db=database, user=user, pwd=pwd))

    try:
        engine.connect()
        
    except SQLAlchemyError as err:
        logging.info("error", err.__cause__)  # this will give what kind of error
        
    else:
        logging.info("Conexão no DB realizada com sucesso")    
        df.to_sql(name=tabela, con=engine, if_exists='replace', index=True)
            

