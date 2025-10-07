import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from db import read_fwf_file
from config import (
    NASH_COLSPECS, NASH_COLUMNS, NASH_DTYPES,
    FINAL_COLUMN_LIST, FINAL_COLUMN_DTYPES
)

load_dotenv('.env', override=True)

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

# --- Phase 5: User Story 4 (T005, T006, T007) ---
print("\nStep 4: Merging DOGS with REAL bills...")
# T005: Perform a left merge
real_others_df = pd.merge(nash_real_only, nash_others, on='CUSTOMER_NO', how='left', suffixes=('_real', '_other'))

# T006: Calculate DOGS and create result_df1
real_others_df['DOGS'] = real_others_df['DOGS_real'].fillna(0) + real_others_df['DOGS_other'].fillna(0)

# Correctly select and rename columns for result_df1
real_cols = {f'{col}_real': col for col in nash_real_only.columns if f'{col}_real' in real_others_df}
result_df1 = real_others_df[list(real_cols.keys())].rename(columns=real_cols)
result_df1['DOGS'] = real_others_df['DOGS'] # Add the summed DOGS column

for col in FINAL_COLUMN_LIST:
    if col not in result_df1.columns:
        result_df1[col] = 0 if FINAL_COLUMN_DTYPES.get(col) in ['int64', 'float64'] else ''
result_df1 = result_df1[FINAL_COLUMN_LIST]
print(f"Created REAL bills final DataFrame with shape {result_df1.shape}")

# T007: Create remaining_others
merged_customers = nash_real_only['CUSTOMER_NO'].unique()
remaining_others = nash_others[~nash_others['CUSTOMER_NO'].isin(merged_customers)].copy()
print(f"{len(remaining_others)} OTHER records remaining after REAL merge.")

# --- Phase 6: User Story 5 (T008, T009) ---
print("\nStep 5: Merging DOGS with PERSONAL bills...")
# T008: Perform a left merge with remaining_others
personal_others_df = pd.merge(nash_personal_only, remaining_others, on='CUSTOMER_NO', how='left', suffixes=('_pers', '_other'))

# T009: Calculate DOGS and create result_df2
personal_others_df['DOGS'] = personal_others_df['DOGS_pers'].fillna(0) + personal_others_df['DOGS_other'].fillna(0)

# Correctly select and rename columns for result_df2
pers_cols = {f'{col}_pers': col for col in nash_personal_only.columns if f'{col}_pers' in personal_others_df}
result_df2 = personal_others_df[list(pers_cols.keys())].rename(columns=pers_cols)
result_df2['DOGS'] = personal_others_df['DOGS'] # Add the summed DOGS column

for col in FINAL_COLUMN_LIST:
    if col not in result_df2.columns:
        result_df2[col] = 0 if FINAL_COLUMN_DTYPES.get(col) in ['int64', 'float64'] else ''
result_df2 = result_df2[FINAL_COLUMN_LIST]
print(f"Created PERSONAL bills final DataFrame with shape {result_df2.shape}")

# --- Phase 7: User Story 6 (T010) ---
print("\nStep 6: Identifying standalone DOGS bills...")
# T010: Create dogs_only_df
personal_merged_customers = nash_personal_only['CUSTOMER_NO'].unique()
dogs_only_df = remaining_others[~remaining_others['CUSTOMER_NO'].isin(personal_merged_customers)].copy()
print(f"Found {len(dogs_only_df)} standalone DOGS records.")

# --- Phase 8: User Story 7 (T011, T012) ---
print("\nStep 7: Concatenating all bills into a final DataFrame...")
# T011: Concatenate DataFrames
final_nash_df = pd.concat([result_df1, result_df2, dogs_only_df], ignore_index=True)
final_nash_df = final_nash_df[FINAL_COLUMN_LIST]
print(f"Final concatenated DataFrame shape: {final_nash_df.shape}")

# T012: Save to CSV
output_filename = "final_nash2025.csv"
final_nash_df.to_csv(output_filename, index=False)
print(f"\nSuccessfully saved the final data to {output_filename}")

# Final summary
print("\n--- Processing Summary ---")
print(f"Total {len(nash_df)} records in original NASH file.")
print(f"Total REAL records (after merge): {len(result_df1)}")
print(f"Total PERSONAL records (after merge): {len(result_df2)}")
print(f"Total standalone OTHER records: {len(dogs_only_df)}")
print(f"Total records in final file: {len(final_nash_df)}")
print("--- End of Summary ---")
