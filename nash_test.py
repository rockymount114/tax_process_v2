import pandas as pd
from db import read_fwf_file
from config import (NASH_COLSPECS, NASH_COLUMNS, NASH_DTYPES)

# Step 1: Load data and filter DOGS-only records with no property value
nash_df = read_fwf_file('NASH.TXT', NASH_COLSPECS, NASH_COLUMNS, NASH_DTYPES)
print(f"original nash has:  {len(nash_df)}")
# Assume nash_df is loaded

# 1. Find DOGS-only records (REAL_VALUE == 0 & PERSONAL_VALUE == 0 & DOGS != 0)
dogs_only_mask = (
    (nash_df['REAL_VALUE'] == 0) &
    (nash_df['PERSONAL_VALUE'] == 0) &
    (nash_df['DOGS'] != 0)
)
dogs_only_df = nash_df[dogs_only_mask]
print(f"dogs only records: {len(dogs_only_df)}")

# 2. For each CUSTOMER_NO in dogs_only_df, check for another row with same CUSTOMER_NO
for customer_no in dogs_only_df['CUSTOMER_NO'].unique():
    # Get indices of DOGS-only
    dogs_idx = dogs_only_df[dogs_only_df['CUSTOMER_NO'] == customer_no].index
    # Get indices of all records for that CUSTOMER_NO
    all_idx = nash_df[nash_df['CUSTOMER_NO'] == customer_no].index
    # Find non-DOGS-only records for that CUSTOMER_NO
    non_dogs_idx = [i for i in all_idx if i not in dogs_idx]
    if non_dogs_idx:
        # Merge: increment DOGS in the non-DOGS record by the sum in dogs-only
        total_dogs = nash_df.loc[all_idx, 'DOGS'].sum()
        # Assign summed DOGS to the non-DOGS row (take first if multiple)
        nash_df.loc[non_dogs_idx[0], 'DOGS'] = total_dogs
        # Drop DOGS-only records
        nash_df = nash_df.drop(dogs_idx)
    # Else, if there's only DOGS-only record(s), leave as is

# Save final
nash_df.to_csv('final_nash2025.csv', index=False)
print(f"final has: {len(nash_df)}")
