# Feature: Nash Tax Bills Processing

## Overview
This feature processes the Nash tax data to separate different bill types, handle records with dogs, and consolidate everything into a final bill file.

## User Stories

- **US1 (P1): Separate REAL BILLS**
  - As a tax processor, I want to isolate all records that represent real estate bills so they can be processed separately.

- **US2 (P1): Separate PERSONAL BILLS**
  - As a tax processor, I want to isolate all records that represent personal property bills.

- **US3 (P1): Separate Other BILLS**
  - As a tax processor, I want to isolate all records that have neither real nor personal value, as they represent other types of fees (like dogs).

- **US4 (P2): Merge DOGS with REAL BILLS**
  - As a tax processor, I want to merge the dog fees from the 'other' bills into the corresponding real estate bills for the same customer.

- **US5 (P2): Merge DOGS with PERSONAL BILLS**
  - As a tax processor, I want to merge the dog fees from the 'other' bills into the corresponding personal property bills for the same customer.

- **US6 (P3): Isolate Standalone DOGS Bills**
  - As a tax processor, I want to identify customers who have a dog fee but no corresponding real or personal property bill.

- **US7 (P4): Consolidate Final Bills**
  - As a tax processor, I want to combine the processed real bills, personal bills, and standalone dog bills into a single, final file for the Nash tax roll.
