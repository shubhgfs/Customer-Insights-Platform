import pandas as pd
import os
import urllib.parse
import sqlalchemy

connstring = "DRIVER={ODBC Driver 17 for SQL Server};server=evm02.prod.db.hfs.local,1272;database=Evolve;schema=dbo;Trusted_Connection=yes;"
quoted_conn_str = urllib.parse.quote_plus(connstring)
engine = sqlalchemy.create_engine(f'mssql+pyodbc:///?odbc_connect={quoted_conn_str}')

query = """
select * from HollardDW.dbo.FactSalesActivity
where dateid >= '2024-11-01'
and dateid < '2025-02-01'
"""

fact_sales = pd.read_sql_query(query, engine)

query = """"
select * from evolve.dbo.tblclient where clientid in (select distinct clientid from HollardDW.dbo.FactSalesActivity
where dateid >= '2024-11-01'
and dateid < '2025-02-01')
"""

client = pd.read_sql_query(query, engine)
