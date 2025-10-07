# This file is used to get data from Munis database and save to CSV
# Then upload to ts SQL server

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import logging
import os, time
from dotenv import load_dotenv

load_dotenv('.env', override=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVER_NAME = 'MU19PRODDB1'
DATABASE_NAME= 'munprod'

current_dir = os.path.dirname(os.path.abspath(__file__))

def normalize_value(value):
    if isinstance(value, str):
        return value.strip().lower()
    return value

def read_fwf_file(file_path: str, colspecs: list, columns: list, dtypes: dict) -> pd.DataFrame:
    """Read a fixed-width file and return a pandas DataFrame, trying multiple encodings."""
    encodings = ['cp1252', 'windows-1252', 'latin1', 'iso-8859-1', 'utf-8']  # Added 'utf-8'
    df = None
    
    for encoding in encodings:
        try:
            df = pd.read_fwf(
                file_path,
                colspecs=colspecs,
                names=columns,
                encoding=encoding,
                on_bad_lines='skip'  # Skip problematic lines
            )
            print(f"Successfully read file {file_path} with encoding {encoding}")
            break
        except UnicodeDecodeError:
            print(f"UnicodeDecodeError with {encoding} for {file_path}")
            continue
        except Exception as e:
            print(f"Error with {encoding} for {file_path}: {str(e)}")
            continue
    
    if df is None:
        raise Exception(f"Could not read file {file_path} with any of the attempted encodings")
    
    # Post-processing similar to TAX.py
    for col in df.columns:
        if col in dtypes and dtypes[col] == 'object' or dtypes[col] == 'string':
            df[col] = df[col].astype(str).str.strip()
    
    # Handle numeric columns gracefully
    numeric_cols = [col for col, dtype in dtypes.items() if dtype in ['int64', 'float64']]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(dtypes[col])
    
    # handle parcel number issue for citybill    
    if 'PARCEL' in df.columns:
        df['PARCEL'] = df['PARCEL'].apply(lambda x: "{:.0f}".format(x) if pd.notna(x) and isinstance(x, (int, float)) else str(x) if pd.notna(x) else '')
    return df

def get_munis_parcels():
    server = SERVER_NAME
    database = DATABASE_NAME
    driver = 'ODBC Driver 17 for SQL Server'

    try:
        engine = create_engine(
            f'mssql+pyodbc://{server}/{database}?trusted_connection=yes&driver={driver}',
            connect_args={'autocommit': False}
        )
        with engine.connect() as connection:  # Use context manager for connection
            query = """
                SELECT 
                    d.* 
                FROM (
                    SELECT
                        c.a_ar_customer_cid,
                        RTRIM(LTRIM(b.arbh_parcel))      as arbh_parcel,
                        b.arbh_year,
                        UPPER(RTRIM(LTRIM(c.c_cid_name1))) AS c_cid_name1,
                        UPPER(RTRIM(LTRIM(c.c_cid_name2))) AS c_cid_name2,
                        UPPER(RTRIM(LTRIM(c.c_addr_line1))) AS c_addr_line1,
                        UPPER(RTRIM(LTRIM(c.c_addr_line2))) AS c_addr_line2,
                        UPPER(RTRIM(LTRIM(c.c_cid_city))) AS c_cid_city,
                        UPPER(RTRIM(LTRIM(c.c_cid_state))) AS c_cid_state,
                        CASE 
                            WHEN c_cid_city <> '' THEN CONCAT(UPPER(RTRIM(LTRIM(c.c_cid_city))), ', ', UPPER(RTRIM(LTRIM(c.c_cid_state)))) 
                            ELSE '' 
                        END AS city_st,
                        UPPER(RTRIM(LTRIM(c.c_cid_zip))) AS c_cid_zip,
                        ROW_NUMBER() OVER (PARTITION BY RTRIM(LTRIM(b.arbh_parcel)) ORDER BY b.arbh_year DESC) AS rnk,
                        GETDATE() AS updated_at
                    FROM dbo.ar_customer AS c
                    LEFT JOIN dbo.arbilhdr AS b  
                    ON c.a_ar_customer_cid = b.arbh_acct
                    WHERE b.arbh_parcel <> '' AND LEN(b.arbh_parcel) >= 12
                ) d
                WHERE d.rnk = 1
            """
            df = pd.read_sql(query, connection)

        # Normalize data using apply() and map()
        df = df.apply(lambda col: col.map(normalize_value) if col.dtype == 'object' else col)

        # Strip any remaining whitespace
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.strip()

        # Save to CSV
        df.to_csv(os.path.join(current_dir, 'munis_parcels.csv'), index=False, encoding='utf-8')
        logger.info(f"Data successfully saved to munis_parcels.csv. Total rows: {len(df)}")

    except Exception as e:
        logger.error(f"Failed to fetch data: {e}")
        raise

    finally:
        engine.dispose()  # Dispose of the engine to release resources
    
    
def get_munis_customer():
    # Get munis customer list, use munis name field to match those empty CITY column, particularly for personal tax in Nash data
    # Not including parcel number as the parcel number has already been used for replace city etc..
    server = SERVER_NAME
    database = DATABASE_NAME
    driver = 'ODBC Driver 17 for SQL Server'

    try:
        engine = create_engine(
            f'mssql+pyodbc://{server}/{database}?trusted_connection=yes&driver={driver}',
            connect_args={'autocommit': False}
        )
        with engine.connect() as connection:        
            query = """SELECT 
                        d.*
                    FROM (
                        SELECT 
                            a_ar_customer_cid
                            , RTRIM(LTRIM(REPLACE(c_cid_name1, ',', ''))) AS c_cid_name1
                            , RTRIM(LTRIM(c_cid_name2)) AS c_cid_name2
                            , RTRIM(LTRIM(c_addr_line1)) AS c_addr_line1
                            , RTRIM(LTRIM(c_addr_line2)) AS c_addr_line2
                            , RTRIM(LTRIM(c_cid_city)) AS c_cid_city
                            , RTRIM(LTRIM(c_cid_state)) AS c_cid_state
                            , CONCAT(RTRIM(LTRIM(c_cid_city)), ', ', RTRIM(LTRIM(c_cid_state))) AS city_st
                            , RTRIM(LTRIM(c_cid_zip)) AS c_cid_zip
                            , c_updated_date
                            , c_updated_by
                            , ROW_NUMBER() OVER (PARTITION BY RTRIM(LTRIM(REPLACE(c_cid_name1, ',', ''))) ORDER BY c_updated_date DESC) AS rnk
                            , GETDATE() AS updated_at
                        FROM dbo.ar_customer
                        WHERE c_cid_name1 IS NOT NULL AND c_cid_name1 <> 'NAM1'
                    ) d
                    WHERE d.rnk = 1
                    """
            df = pd.read_sql(query, engine)
            
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.strip()
            
        df.to_csv(os.path.join(current_dir, 'munis_customer.csv'), index=False)
        return df

    except Exception as e:
        print(f"Failed to create database connection: {e}")
        raise

    finally:
        # Only dispose of the engine after all operations
        if 'engine' in locals():
            engine.dispose()
    
    


def get_cleaned_data():
    """
    Connect to SQL database, retrieve data from v_final view,
    clean the data, and save to CSV.
    Returns a pandas DataFrame with the cleaned data.
    """
   

    # Load credentials from environment
    username = os.getenv("TSDB_USERNAME")
    password = os.getenv("TSDB_PASSWORD")

    # Database connection info
    connection_string = URL.create(
        "mssql+pyodbc",
        username=username,
        password=password,
        host="172.20.21.115",  # Use IP to avoid DNS issues
        database="tax_import",
        query={"driver": "ODBC Driver 17 for SQL Server"}
    )

    # Create engine and execute query using context managers for automatic cleanup
    try:
        engine = create_engine(connection_string, echo=False)
        with engine.connect() as conn:
            df = pd.read_sql("SELECT * FROM dbo.v_final", conn)
            
            # Clean data - convert all columns to string and replace NaN values
            df = df.astype(str).replace(r'^\s*$|^nan$|^None$|^NaN$', '', regex=True).apply(lambda x: x.str.strip())
            df.to_csv(os.path.join(current_dir, 'final_cleaned.csv'), index=False)
            return df
            
    except Exception as e:
        print(f"Database operation failed: {e}")
        raise
    finally:
        # Make sure engine is disposed even if an exception occurs
        if 'engine' in locals():
            engine.dispose()

    
    

    


def tots(file_path, table_name):
    # Ensure the file exists
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return

    server = '172.20.21.115'
    DB_Name = os.getenv("EXPORT_DBNAME")
    username = os.getenv("TSDB_USERNAME")
    password = os.getenv("TSDB_PASSWORD")
    
    connection_string =  URL.create(
                            "mssql+pyodbc",
                            username=username,
                            password=password,
                            host=server,
                            database=DB_Name,
                            query={"driver": "ODBC Driver 17 for SQL Server",
                                   "connect_timeout":"60",
                                   "trusted_connection": "no",     # Use SQL auth instead of Windows auth on Linux
                                   "TrustServerCertificate": "yes", # Skip certificate validation
                                   }
                        )
    
    try:
        # Create engine
        engine = create_engine(connection_string, echo=False)
        
        # Read CSV file in chunks if it's large
        chunksize = 100000  # Adjust based on your memory constraints
        df_iter = pd.read_csv(file_path, low_memory=False, chunksize=chunksize)
        
        total_rows = 0
        # Iterate over chunks and write to SQL
        for i, df_chunk in enumerate(df_iter):
            df_chunk.to_sql(
                table_name, 
                con=engine, 
                if_exists='replace' if i == 0 else 'append', 
                index=False
            )
            
            total_rows += len(df_chunk)
            logger.info(f"Processed chunk {i + 1}, total rows so far: {total_rows}")
        
        logger.info(f"{table_name} has been saved in database, total rows: {total_rows}")
        return total_rows
        
    except Exception as e:
        logger.error(f"An error occurred while uploading data to SQL server: {e}")
        return None
    finally:
        # Make sure engine is disposed even if an exception occurs
        if 'engine' in locals():
            engine.dispose()
        

def tots216(file_path, table_name):
    # Ensure the file exists
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return

    server = '172.20.22.216'
    DB_Name = os.getenv("EXPORT_DBNAME")
    username = os.getenv("TSDB_USERNAME")
    password = os.getenv("TSDB_PASSWORD")
    
    connection_string =  URL.create(
                            "mssql+pyodbc",
                            username=username,
                            password=password,
                            host=server,
                            database=DB_Name,
                            query={"driver": "ODBC Driver 17 for SQL Server",
                                   "connect_timeout":"60",
                                   "trusted_connection": "no",     # Use SQL auth instead of Windows auth on Linux
                                   "TrustServerCertificate": "yes", # Skip certificate validation
                                   }
                        )
    
    try:
        # Create engine
        engine = create_engine(connection_string, echo=False)
        
        # Read CSV file in chunks if it's large
        chunksize = 100000  # Adjust based on your memory constraints
        df_iter = pd.read_csv(file_path, low_memory=False, chunksize=chunksize)
        
        total_rows = 0
        # Iterate over chunks and write to SQL
        for i, df_chunk in enumerate(df_iter):
            df_chunk.to_sql(
                table_name, 
                con=engine, 
                if_exists='replace' if i == 0 else 'append', 
                index=False
            )
            
            total_rows += len(df_chunk)
            logger.info(f"Processed chunk {i + 1}, total rows so far: {total_rows}")
        
        logger.info(f"{table_name} has been saved in database, total rows: {total_rows}")
        return total_rows
        
    except Exception as e:
        logger.error(f"An error occurred while uploading data to SQL server: {e}")
        return None
    finally:
        # Make sure engine is disposed even if an exception occurs
        if 'engine' in locals():
            engine.dispose()

# if __name__ == '__main__':
#     get_munis_parcels()
#     get_munis_customer()
    # get_cleaned_data()
    # tots('df_final.csv', 'flask_data')
    
    # save Munis parcel and customer data into ts server
    # Only need run once before tax import
    
    # tots('munis_parcels.csv', 'munis_parcel')
    # tots('munis_customer.csv', 'munis_customer')
    
    