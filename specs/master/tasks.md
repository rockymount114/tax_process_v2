# Task Plan: Nash Tax Bills Processing

This plan outlines the tasks required to implement the Nash Tax Bills processing feature.

## Phase 1: Foundational Setup

These tasks set up the basic script structure. All user stories depend on this phase.

- **T001**: [US1, US2, US3] In `nash.py`, ensure the initial `nash_df` DataFrame is loaded correctly from `NASH.TXT`.

## Phase 2: User Story 1 - Separate REAL BILLS

- **Goal**: Isolate records that represent real estate bills.
- **Independent Test**: The resulting `nash_real_only` DataFrame should contain only records where `REAL_VALUE` is not 0 and `ALT_PARCEL` is not null.

- **T002**: [US1] In `nash.py`, create a new DataFrame `nash_real_only` by filtering `nash_df` for records where `REAL_VALUE != 0` and `ALT_PARCEL` is not null.

## Phase 3: User Story 2 - Separate PERSONAL BILLS

- **Goal**: Isolate records that represent personal property bills.
- **Independent Test**: The resulting `nash_personal_only` DataFrame should contain only records where `PERSONAL_VALUE` is not 0 and `REAL_VALUE` is 0.

- **T003**: [US2] In `nash.py`, create a new DataFrame `nash_personal_only` by filtering `nash_df` for records where `PERSONAL_VALUE != 0` and `REAL_VALUE == 0`.

## Phase 4: User Story 3 - Separate Other BILLS

- **Goal**: Isolate records with no real or personal value.
- **Independent Test**: The `nash_others` DataFrame should contain records where both `PERSONAL_VALUE` and `REAL_VALUE` are 0.

- **T004**: [US3] In `nash.py`, create a new DataFrame `nash_others` by filtering `nash_df` for records where `PERSONAL_VALUE == 0` and `REAL_VALUE == 0`.

## Phase 5: User Story 4 - Merge DOGS with REAL BILLS

- **Goal**: Merge dog fees into real estate bills.
- **Independent Test**: The resulting `result_df1` should have a `DOGS` column that is the sum of dogs from the real and other bills for each `CUSTOMER_NO`.

- **T005**: [US4] In `nash.py`, perform a left merge from `nash_real_only` to `nash_others` on `CUSTOMER_NO`.
- **T006**: [US4] Create the final `result_df1` DataFrame, calculating the `DOGS` column by summing the `DOGS` values from the merged tables.

## Phase 6: User Story 5 - Merge DOGS with PERSONAL BILLS

- **Goal**: Merge dog fees into personal property bills.
- **Independent Test**: The `result_df2` should have a `DOGS` column that is the sum of dogs from the personal and other bills for each `CUSTOMER_NO`.

- **T007**: [US5] [P] In `nash.py`, perform a left merge from `nash_personal_only` to `nash_others` on `CUSTOMER_NO`.
- **T008**: [US5] [P] Create the final `result_df2` DataFrame, calculating the `DOGS` column by summing the `DOGS` values from the merged tables.

## Phase 7: User Story 6 - Isolate Standalone DOGS Bills

- **Goal**: Identify customers with only a dog fee.
- **Independent Test**: The `dogs_only_df` should contain records from `nash_others` for customers not present in the real or personal bills.

- **T009**: [US6] In `nash.py`, create `dogs_only_df` by filtering `nash_others` to include only `CUSTOMER_NO`s not in `nash_real_only` or `nash_personal_only`.

## Phase 8: User Story 7 - Consolidate Final Bills

- **Goal**: Combine all processed bills into a single file.
- **Independent Test**: The final DataFrame should have a row count equal to the sum of rows in `result_df1`, `result_df2`, and `dogs_only_df`.

- **T010**: [US7] In `nash.py`, concatenate `result_df1`, `result_df2`, and `dogs_only_df` into a single `final_nash_df`.
- **T011**: [US7] Save the `final_nash_df` to a CSV file named `final_nash2025.csv`.

## Dependencies
- (US1, US2, US3) can run in parallel after Phase 1.
- US4 depends on US1 and US3.
- US5 depends on US2 and US3.
- US6 depends on US1, US2, and US3.
- US7 depends on US4, US5, and US6.

## Parallel Execution
- Within Phase 6, tasks T007 and T008 are marked with [P] and can be worked on in parallel.
