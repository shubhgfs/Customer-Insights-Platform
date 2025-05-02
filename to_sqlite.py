import pandas as pd
import pyodbc
import sqlite3

def sqlserver_to_sqlite(sqlserver_conn_str, sql_query, sqlite_db_path, sqlite_table):
    # Connect to SQL Server and fetch data
    sql_conn = pyodbc.connect(sqlserver_conn_str)
    df = pd.read_sql(sql_query, sql_conn)
    sql_conn.close()

    # Write DataFrame to SQLite
    with sqlite3.connect(sqlite_db_path) as sqlite_conn:
        df.to_sql(sqlite_table, sqlite_conn, if_exists="replace", index=False)
    print(f"Data from SQL Server loaded into {sqlite_db_path} (table: {sqlite_table})")

# Example usage:
if __name__ == "__main__":
    sqlserver_conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=evm02.prod.db.hfs.local,1272;"
        "Database=evolvekpi;"
        "Trusted_Connection=yes;"
    )
    sql_query = """
    -- Paste your final SQL query here
    select * 
    from
    [EvolveKPI].[dbo].[CIP_Lifestyle_Smoking]
    """
    sqlite_db_path = "output.sqlite.db"
    sqlite_table = "lifestyle_factors_smoking"
    sqlserver_to_sqlite(sqlserver_conn_str, sql_query, sqlite_db_path, sqlite_table)