

import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

from config import (CITYBILL_COLSPECS, ACCOUNT_COLSPECS, PARCEL_COLSPECS, NASH_COLSPECS,
                    CITYBILL_COLUMNS, ACCOUNT_COLUMNS, PARCEL_COLUMNS, NASH_COLUMNS,
                    CITYBILL_DTYPES, ACCOUNT_DTYPES, PARCEL_DTYPES, NASH_DTYPES,
                    FINAL_COLUMN_LIST, FINAL_COLUMN_DTYPES, EXPORTER_COLMIN_WIDTH)

load_dotenv('.env', override=True)

current_dir = os.path.dirname(os.path.abspath(__file__))

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



nash_df = read_fwf_file('NASH.TXT', NASH_COLSPECS, NASH_COLUMNS, NASH_DTYPES)

nash_df['ZIPC'] = pd.to_numeric(nash_df['ZIPC'], errors='coerce').fillna(0).astype(int).astype(str).str.zfill(5)

# nash_df.to_csv('nash.csv', index=False)

nash_real_only = nash_df[(nash_df['ALT_PARCEL'].notnull()) & (nash_df['REAL_VALUE'] != 0)]

nash_personal_only = nash_df[(nash_df['PERSONAL_VALUE'] != 0) & (nash_df['REAL_VALUE'] == 0)]

nash_others = nash_df[(nash_df['PERSONAL_VALUE'] == 0) & (nash_df['REAL_VALUE'] == 0)]



### Merge dog quantities into REAL dataset start

real_others_df = pd.merge(nash_real_only, nash_others, on='CUSTOMER_NO', how='left', suffixes=('_x', '_y'))

# Calculate the DOGS column by summing values from both sources
real_others_df['DOGS'] = real_others_df['DOGS_x'].fillna(0) + real_others_df['DOGS_y'].fillna(0)

# Select columns from the merge result, preferring the '_x' (nash_real_only) values
final_df1 = real_others_df[['CUSTOMER_NO']].copy()

# Columns to take from the left side of the merge (_x)
cols_from_x = [
    'JURISDICTION', 'PROPERTY_ID', 'ZIPC', 'NAM1', 'NAM2', 'ADRS1', 'ADRS2', 'CITY',
    'STATUS', 'EXEMPT_VALUE', 'DEFER_VALUE', 'REAL_VALUE', 'PERSONAL_VALUE',
    'LATE_LIST', 'LENDER_CODE', 'LL_VALUE', 'LEGAL_DESCRIPTION', 'ACRE',
    'LAND_VALUE', 'BUILDING_VALUE', 'SPECIAL_DISTRICT', 'ALT_PARCEL',
    'LOC_STREET#', 'LOC_SUFFIX', 'LOC_STREET', 'LOC_UNIT'
]

for col in cols_from_x:
    final_df1[col] = real_others_df[f'{col}_x']

# Add the calculated DOGS column
final_df1['DOGS'] = real_others_df['DOGS']

# Define the final column order
final_column_list = [
    'JURISDICTION', 'PROPERTY_ID', 'ZIPC', 'NAM1', 'NAM2', 'ADRS1', 'ADRS2', 'CITY',
    'STATUS', 'EXEMPT_VALUE', 'DEFER_VALUE', 'REAL_VALUE', 'PERSONAL_VALUE',
    'LATE_LIST', 'LENDER_CODE', 'LL_VALUE', 'LEGAL_DESCRIPTION', 'ACRE',
    'DOGS', 'LAND_VALUE', 'BUILDING_VALUE', 'SPECIAL_DISTRICT', 'ALT_PARCEL',
    'LOC_STREET#', 'LOC_SUFFIX', 'LOC_STREET', 'LOC_UNIT', 'CUSTOMER_NO'
]

# Reorder columns and assign back to result_df
result_df1 = final_df1[final_column_list]

# print(result_df1.shape)

### Merge dog quantities into REAL dataset start


### Merge dog quantities into PERSONAL dataset start

personal_others_df = pd.merge(nash_personal_only, nash_others, on='CUSTOMER_NO', how='left', suffixes=('_x', '_y'))

# Calculate the DOGS column by summing values from both sources
personal_others_df['DOGS'] = personal_others_df['DOGS_x'].fillna(0) + personal_others_df['DOGS_y'].fillna(0)

# Select columns from the merge result, preferring the '_x' (nash_personal_only) values
final_df2 = personal_others_df[['CUSTOMER_NO']].copy()

# Columns to take from the left side of the merge (_x)
cols_from_x = [
    'JURISDICTION', 'PROPERTY_ID', 'ZIPC', 'NAM1', 'NAM2', 'ADRS1', 'ADRS2', 'CITY',
    'STATUS', 'EXEMPT_VALUE', 'DEFER_VALUE', 'REAL_VALUE', 'PERSONAL_VALUE',
    'LATE_LIST', 'LENDER_CODE', 'LL_VALUE', 'LEGAL_DESCRIPTION', 'ACRE',
    'LAND_VALUE', 'BUILDING_VALUE', 'SPECIAL_DISTRICT', 'ALT_PARCEL',
    'LOC_STREET#', 'LOC_SUFFIX', 'LOC_STREET', 'LOC_UNIT'
]

for col in cols_from_x:
    final_df2[col] = personal_others_df[f'{col}_x']

# Add the calculated DOGS column
final_df2['DOGS'] = personal_others_df['DOGS']

# Reorder columns and assign back to result_df
result_df2 = final_df2[final_column_list]




dogs_only_df = nash_others[
    ~nash_others['CUSTOMER_NO'].isin(nash_real_only['CUSTOMER_NO']) &
    ~nash_others['CUSTOMER_NO'].isin(nash_personal_only['CUSTOMER_NO'])
]

# Concatenate result_df1, result_df2, and dogs_only_df into final_nash_df
final_nash_df = pd.concat([result_df1, result_df2, dogs_only_df], ignore_index=True)

# Ensure the final_nash_df has the columns in final_column_list
final_nash_df = final_nash_df[final_column_list]

print(final_nash_df.head())
print(final_nash_df.shape)
print(result_df1.shape)
print(result_df2.shape)

final_nash_df.to_csv("final_nash2025.csv", index=False)

### Merge dog quantities into PERSONAL dataset end







# from db import tots216
# tots216('nash.csv', 'nash2025')




