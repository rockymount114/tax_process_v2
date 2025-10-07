# Technical Plan: Nash Tax Bills Processing

## Tech Stack
- **Language**: Python
- **Core Library**: pandas

## Project Structure
- The primary logic will be implemented in `nash.py`.
- The script will read the `NASH.TXT` fixed-width file.
- Intermediate and final DataFrames will be used to hold the state of the data as it's processed through the 7 steps.
- The final output will be a CSV file.

## Strategy
- The 7 steps will be implemented as sequential operations on pandas DataFrames.
- Each step will correspond to a user story from `spec.md`.
- DataFrame filtering, merging, and concatenation will be the primary methods used.
