import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

from config import (
    CITYBILL_COLSPECS, ACCOUNT_COLSPECS, PARCEL_COLSPECS, NASH_COLSPECS,
    CITYBILL_COLUMNS, ACCOUNT_COLUMNS, PARCEL_COLUMNS, NASH_COLUMNS,
    CITYBILL_DTYPES, ACCOUNT_DTYPES, PARCEL_DTYPES, NASH_DTYPES,
    FINAL_COLUMN_LIST, FINAL_COLUMN_DTYPES, EXPORTER_COLMIN_WIDTH
)

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

# --- Implementation based on tasks.md ---

# T001: Load initial DataFrame
print("--- Starting Nash Tax Bill Processing ---")
nash_df = read_fwf_file('NASH.TXT', NASH_COLSPECS, NASH_COLUMNS, NASH_DTYPES)

# --- Phase 2: User Story 1 (T002) ---
print("\nStep 1: Separating REAL bills...")
nash_real_only = nash_df[(nash_df['ALT_PARCEL'].notnull()) & (nash_df['REAL_VALUE'] != 0)].copy()
print(f"Found {len(nash_real_only)} REAL records.")

# --- Phase 3: User Story 2 (T003) ---
print("\nStep 2: Separating PERSONAL bills...")
nash_personal_only = nash_df[(nash_df['PERSONAL_VALUE'] != 0) & (nash_df['REAL_VALUE'] == 0)].copy()
print(f"Found {len(nash_personal_only)} PERSONAL records.")

# --- Phase 4: User Story 3 (T004) ---
print("\nStep 3: Separating OTHER bills (no real or personal value)...")
nash_others = nash_df[(nash_df['PERSONAL_VALUE'] == 0) & (nash_df['REAL_VALUE'] == 0)].copy()
print(f"Found {len(nash_others)} OTHER records.")

# Define the final column order from config
final_column_list = FINAL_COLUMN_LIST

# --- Phase 5: User Story 4 (T005, T006) ---
print("\nStep 4: Merging DOGS with REAL bills...")
real_others_df = pd.merge(nash_real_only, nash_others, on='CUSTOMER_NO', how='left', suffixes=('_real', '_other'))
real_others_df['DOGS'] = real_others_df['DOGS_real'].fillna(0) + real_others_df['DOGS_other'].fillna(0)

# Select the columns from the left side of the merge and rename them
real_cols = {f'{col}_real': col for col in nash_real_only.columns if f'{col}_real' in real_others_df}
result_df1 = real_others_df[list(real_cols.keys())].rename(columns=real_cols)

result_df1['DOGS'] = real_others_df['DOGS'] # Add the summed DOGS column
for col in final_column_list:
    if col not in result_df1.columns:
        result_df1[col] = 0 if FINAL_COLUMN_DTYPES.get(col) in ['int64', 'float64'] else ''
result_df1 = result_df1[final_column_list]
print(f"Created REAL bills final DataFrame with shape {result_df1.shape}")

# --- Phase 6: User Story 5 (T007, T008) ---
print("\nStep 5: Merging DOGS with PERSONAL bills...")
personal_others_df = pd.merge(nash_personal_only, nash_others, on='CUSTOMER_NO', how='left', suffixes=('_pers', '_other'))
personal_others_df['DOGS'] = personal_others_df['DOGS_pers'].fillna(0) + personal_others_df['DOGS_other'].fillna(0)

# Select the columns from the left side of the merge and rename them
pers_cols = {f'{col}_pers': col for col in nash_personal_only.columns if f'{col}_pers' in personal_others_df}
result_df2 = personal_others_df[list(pers_cols.keys())].rename(columns=pers_cols)

result_df2['DOGS'] = personal_others_df['DOGS'] # Add the summed DOGS column
for col in final_column_list:
    if col not in result_df2.columns:
        result_df2[col] = 0 if FINAL_COLUMN_DTYPES.get(col) in ['int64', 'float64'] else ''
result_df2 = result_df2[final_column_list]
print(f"Created PERSONAL bills final DataFrame with shape {result_df2.shape}")

# --- Phase 7: User Story 6 (T009) ---
print("\nStep 6: Identifying standalone DOGS bills...")
dogs_only_df = nash_others[
    ~nash_others['CUSTOMER_NO'].isin(nash_real_only['CUSTOMER_NO']) &
    ~nash_others['CUSTOMER_NO'].isin(nash_personal_only['CUSTOMER_NO'])
].copy()
print(f"Found {len(dogs_only_df)} standalone DOGS records.")

# --- Phase 8: User Story 7 (T010, T011) ---
print("\nStep 7: Concatenating all bills into a final DataFrame...")
final_nash_df = pd.concat([result_df1, result_df2, dogs_only_df], ignore_index=True)
final_nash_df = final_nash_df[final_column_list]
print(f"Final concatenated DataFrame shape: {final_nash_df.shape}")

output_filename = "final_nash2025.csv"
final_nash_df.to_csv(output_filename, index=False)
print(f"\nSuccessfully saved the final data to {output_filename}")

# Final summary
print("\n--- Processing Summary ---")
print(f"Total REAL records (after merge): {len(result_df1)}")
print(f"Total PERSONAL records (after merge): {len(result_df2)}")
print(f"Total standalone OTHER records: {len(dogs_only_df)}")
print(f"Total records in final file: {len(final_nash_df)}")
print("--- End of Summary ---")