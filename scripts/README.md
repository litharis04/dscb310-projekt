# User.csv Error Analysis Scripts

This directory contains scripts for analyzing and documenting errors in the `data/user.csv` file.

## Scripts

1. **find_user_csv_errors.py** - Initial comprehensive error detection script
   - Analyzes unrealistic ages
   - Checks date ordering
   - Validates booking/destination consistency
   - Searches for typos in string columns

2. **create_error_summary.py** - Creates detailed Russian-language error summary
   - Provides specific examples with user IDs
   - Includes recommendations for fixes
   - Generates comprehensive report

## Output Files

All analysis results are saved in the `outputs/` subdirectory:

- **user_csv_errors.txt** - Full technical analysis (English)
- **user_csv_errors_summary.txt** - Detailed summary (Russian)
- **FINAL_REPORT_RU.txt** - Comprehensive final report (Russian) ⭐ **MAIN REPORT**

## Quick Summary of Findings

### Errors Found:
1. **Age errors**: 3,103 records with unrealistic ages
2. **Date ordering errors**: 234,703 records (mostly due to time format issue)
3. **Booking consistency**: ✅ No errors found
4. **String typos**: ✅ No typos found

### Main Issue:
The `account_created_date` column stores dates WITHOUT time (00:00:00), while `first_active_timestamp` contains precise timestamps. This causes false positives when comparing dates.

### Recommendations:
1. Store `account_created_date` with precise time
2. Clean age data (replace unrealistic values with NaN)
3. For the 29 records where account_created_date > first_booking_date, investigate source data

## Usage

Run the scripts from the project root directory:

```bash
cd /home/runner/work/dscb310-projekt/dscb310-projekt
python scripts/find_user_csv_errors.py
python scripts/create_error_summary.py
```

## Integration with EDA.py

The finalized analysis code has been added to `EDA.py` in the project root, following the Jupytext percent format. This allows the analysis to be run as a Jupyter notebook.
