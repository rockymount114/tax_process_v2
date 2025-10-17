# Checklist: Data Processing Requirements

**Purpose**: This checklist is for the developer to self-check the data processing requirements for clarity, completeness, and coverage before or during implementation.
**Created**: 2025-10-07

## Requirement Completeness
- [ ] CHK001 - Are the criteria for identifying a 'REAL BILL' (US1) exhaustive, or are there other conditions to consider? [Gap]
- [ ] CHK002 - Does the spec define the expected behavior if the `NASH.TXT` input file is not found, is empty, or does not match the expected fixed-width format? [Gap, Error Handling]
- [ ] CHK003 - Are logging requirements specified for key stages of the data processing (e.g., number of records read, filtered, merged)? [Gap]
- [ ] CHK004 - Are requirements defined for the final output file format, including delimiter, encoding, and header naming? [Completeness, Spec §US7]

## Requirement Clarity
- [ ] CHK005 - Is the definition of a 'PERSONAL BILL' (US2) sufficiently clear to avoid ambiguity with 'REAL BILLS' that might have a personal property component but are primarily real estate? [Clarity, Spec §US2]
- [ ] CHK006 - In US4 and US5, is the term 'merge' defined with a specific join type (e.g., left, inner) and are the columns to be merged explicitly listed? [Clarity, Spec §US4, §US5]
- [ ] CHK007 - For the merge logic, is the rule for summing the `DOGS` quantity explicitly defined, especially how to handle null or zero values from either side of the merge? [Clarity, Spec §US4, §US5]

## Requirement Consistency
- [ ] CHK008 - Is the `CUSTOMER_NO` format, data type, and meaning consistent across all user stories where it is used as a key? [Consistency]
- [ ] CHK009 - Do the definitions of 'REAL', 'PERSONAL', and 'Other' bills in US1, US2, and US3 cover all possible records in `nash_df` without overlap? [Consistency, Spec §US1, §US2, §US3]

## Scenario & Edge Case Coverage
- [ ] CHK010 - Does the spec clarify if a single `CUSTOMER_NO` can have multiple 'REAL' or 'PERSONAL' bills, and if so, how the 'DOGS' records should be merged in that case? [Edge Case, Gap]
- [ ] CHK011 - Are there requirements for handling records where both `REAL_VALUE` and `PERSONAL_VALUE` are non-zero? [Edge Case, Gap]
- [ ] CHK012 - Does the spec define how to handle duplicate `CUSTOMER_NO`s within the initial `nash_real_only` or `nash_personal_only` dataframes before any merging happens? [Edge Case, Gap]
- [ ] CHK013 - Does the requirement for identifying 'Standalone DOGS Bills' (US6) explicitly state that these are customers who do *not* appear in *either* the final real or personal bills? [Clarity, Spec §US6]
- [ ] CHK014 - Is the expected behavior defined for a `DOGS` record in `nash_others` that has a `CUSTOMER_NO` that does not exist in either `nash_real_only` or `nash_personal_only`? [Coverage, Spec §US6]

## Non-Functional Requirements
- [ ] CHK015 - Are there any performance requirements for how long the entire data processing script should take to run? [Gap, Performance]
- [ ] CHK016 - Are there any memory usage constraints defined for the script, especially concerning the size of the pandas DataFrames? [Gap, Performance]
