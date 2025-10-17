# Task Plan: Nash Tax Bills Processing

This plan outlines the tasks required to implement the Nash Tax Bills processing feature.

Step 1: Identify Target DOGS Records
Filter rows where REAL_VALUE == 0 and PERSONAL_VALUE == 0 and DOGS != 0.

Step 2: Merge by CUSTOMER_NO, Summing DOGS
Group these records by CUSTOMER_NO and sum the DOGS values.

Step 3: Reconstruct the Main DataFrame
For each unique CUSTOMER_NO in this target group:

If there are multiple such DOGS-only records per CUSTOMER_NO, combine them into one with the summed DOGS.

Retain all other records from the original data (not meeting the filter), unchanged.

Keep only one DOGS-only row per CUSTOMER_NO (with summed DOGS).

Step 4: Build List of Merged CUSTOMER_NO
Output the list of CUSTOMER_NO where merging happened (i.e., those that had more than one DOGS-only record combined).