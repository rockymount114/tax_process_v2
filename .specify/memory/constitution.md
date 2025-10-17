<!--
Sync Impact Report:
- Version change: 0.0.0 -> 1.0.0
- Added sections:
  - Core Principles
  - Governance
- Modified principles:
  - Added: I. Data Consolidation
  - Added: II. Mandatory Code Testing
- Removed sections:
  - Removed 3 of 5 principle placeholders.
  - Removed SECTION_2 and SECTION_3 placeholders.
- Templates requiring updates:
  - No templates found in .specify/templates/ to update.
- Follow-up TODOs:
  - TODO(RATIFICATION_DATE): Set the initial ratification date.
-->
# Nash Tax Bills Processing Constitution

## Core Principles

### I. Data Consolidation
All data cleaning and merging operations must be clearly defined and executed to ensure data integrity. For the `nash_df` DataFrame, records with a `DOGS` quantity but no `REAL_VALUE` or `PERSONAL_VALUE` must be merged with the corresponding `REAL` or `PERSONAL` record based on `CUSTOMER_NO`. The goal is to consolidate the `DOGS` quantity into a single, comprehensive record for each customer. if the record has already merged do not merge them into another record as may have multiple records for the same customer. 
After merge the record, then this DOG record must be remove from the dataset.

### II. Mandatory Code Testing
All code must be accompanied by tests. Any new feature or bug fix must include a test case that verifies the correctness of the implementation.

## Governance
Amendments to this constitution require a proposal, review, and approval process. All code contributions must adhere to the principles outlined herein.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): Set the initial ratification date. | **Last Amended**: 2025-10-07
