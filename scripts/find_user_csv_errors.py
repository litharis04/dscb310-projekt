"""
Script to find errors in user.csv file.

This script analyzes user.csv for various data quality issues including:
- Impossible/unrealistic data values (ages, dates)
- Incorrect date ordering
- Inconsistencies between first_booking_date and destination_country
- Typos in string columns
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys

# Load the data
print("Loading user.csv...")
df = pd.read_csv('/home/runner/work/dscb310-projekt/dscb310-projekt/data/user.csv')

print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"\nColumns: {list(df.columns)}")

# Open output file
output_file = '/home/runner/work/dscb310-projekt/dscb310-projekt/scripts/outputs/user_csv_errors.txt'
with open(output_file, 'w') as f:
    f.write("=" * 80 + "\n")
    f.write("USER.CSV ERROR ANALYSIS REPORT\n")
    f.write("=" * 80 + "\n\n")
    
    # 1. Check for unrealistic ages
    f.write("1. AGE ANALYSIS\n")
    f.write("-" * 80 + "\n")
    f.write(f"Age statistics:\n")
    f.write(f"  Min age: {df['user_age'].min()}\n")
    f.write(f"  Max age: {df['user_age'].max()}\n")
    f.write(f"  Mean age: {df['user_age'].mean():.2f}\n")
    f.write(f"  Median age: {df['user_age'].median()}\n")
    
    # Check for unrealistic ages (< 18 or > 100)
    unrealistic_ages = df[(df['user_age'] < 18) | (df['user_age'] > 100)]
    f.write(f"\nUsers with unrealistic ages (< 18 or > 100): {len(unrealistic_ages)}\n")
    if len(unrealistic_ages) > 0:
        f.write(f"Examples:\n")
        for idx, row in unrealistic_ages.head(10).iterrows():
            f.write(f"  user_id: {row['user_id']}, age: {row['user_age']}\n")
    
    # Check for negative ages or ages > 120
    extreme_ages = df[(df['user_age'] < 0) | (df['user_age'] > 120)]
    f.write(f"\nUsers with extreme ages (< 0 or > 120): {len(extreme_ages)}\n")
    if len(extreme_ages) > 0:
        f.write(f"Examples:\n")
        for idx, row in extreme_ages.head(10).iterrows():
            f.write(f"  user_id: {row['user_id']}, age: {row['user_age']}\n")
    
    f.write("\n\n")
    
    # 2. Check date formats and convert
    f.write("2. DATE ANALYSIS\n")
    f.write("-" * 80 + "\n")
    
    # Convert first_active_timestamp to date
    df['first_active_date'] = pd.to_datetime(df['first_active_timestamp'], format='%Y%m%d%H%M%S', errors='coerce')
    
    # Convert other dates
    df['account_created_date_dt'] = pd.to_datetime(df['account_created_date'], errors='coerce')
    df['first_booking_date_dt'] = pd.to_datetime(df['first_booking_date'], errors='coerce')
    
    f.write(f"Date ranges:\n")
    f.write(f"  first_active_date: {df['first_active_date'].min()} to {df['first_active_date'].max()}\n")
    f.write(f"  account_created_date: {df['account_created_date_dt'].min()} to {df['account_created_date_dt'].max()}\n")
    f.write(f"  first_booking_date: {df['first_booking_date_dt'].min()} to {df['first_booking_date_dt'].max()}\n")
    
    # Check for future dates
    now = datetime.now()
    future_active = df[df['first_active_date'] > now]
    future_created = df[df['account_created_date_dt'] > now]
    future_booking = df[df['first_booking_date_dt'] > now]
    
    f.write(f"\nFuture dates:\n")
    f.write(f"  first_active_date in future: {len(future_active)}\n")
    f.write(f"  account_created_date in future: {len(future_created)}\n")
    f.write(f"  first_booking_date in future: {len(future_booking)}\n")
    
    # Check for dates before 2000 (unrealistic for this platform)
    old_active = df[df['first_active_date'] < '2000-01-01']
    old_created = df[df['account_created_date_dt'] < '2000-01-01']
    old_booking = df[df['first_booking_date_dt'] < '2000-01-01']
    
    f.write(f"\nDates before 2000:\n")
    f.write(f"  first_active_date before 2000: {len(old_active)}\n")
    f.write(f"  account_created_date before 2000: {len(old_created)}\n")
    f.write(f"  first_booking_date before 2000: {len(old_booking)}\n")
    
    f.write("\n\n")
    
    # 3. Check date ordering
    f.write("3. DATE ORDERING ERRORS\n")
    f.write("-" * 80 + "\n")
    
    # first_active_date should be <= account_created_date
    error1 = df[(df['first_active_date'].notna()) & (df['account_created_date_dt'].notna()) & 
                (df['first_active_date'] > df['account_created_date_dt'])]
    f.write(f"Rows where first_active_date > account_created_date: {len(error1)}\n")
    if len(error1) > 0:
        f.write(f"Examples (first 10):\n")
        for idx, row in error1.head(10).iterrows():
            f.write(f"  user_id: {row['user_id']}, first_active: {row['first_active_date']}, created: {row['account_created_date_dt']}\n")
    
    # account_created_date should be <= first_booking_date
    error2 = df[(df['account_created_date_dt'].notna()) & (df['first_booking_date_dt'].notna()) & 
                (df['account_created_date_dt'] > df['first_booking_date_dt'])]
    f.write(f"\nRows where account_created_date > first_booking_date: {len(error2)}\n")
    if len(error2) > 0:
        f.write(f"Examples (first 10):\n")
        for idx, row in error2.head(10).iterrows():
            f.write(f"  user_id: {row['user_id']}, created: {row['account_created_date_dt']}, booking: {row['first_booking_date_dt']}\n")
    
    # first_active_date should be <= first_booking_date
    error3 = df[(df['first_active_date'].notna()) & (df['first_booking_date_dt'].notna()) & 
                (df['first_active_date'] > df['first_booking_date_dt'])]
    f.write(f"\nRows where first_active_date > first_booking_date: {len(error3)}\n")
    if len(error3) > 0:
        f.write(f"Examples (first 10):\n")
        for idx, row in error3.head(10).iterrows():
            f.write(f"  user_id: {row['user_id']}, first_active: {row['first_active_date']}, booking: {row['first_booking_date_dt']}\n")
    
    f.write("\n\n")
    
    # 4. Check first_booking_date vs destination_country
    f.write("4. BOOKING DATE vs DESTINATION COUNTRY CONSISTENCY\n")
    f.write("-" * 80 + "\n")
    
    # If first_booking_date is NaN, destination_country should be NDF
    no_booking = df[df['first_booking_date'].isna()]
    f.write(f"Users without booking date: {len(no_booking)}\n")
    f.write(f"Users without booking where destination != NDF: ")
    
    error4 = df[(df['first_booking_date'].isna()) & (df['destination_country'] != 'NDF')]
    f.write(f"{len(error4)}\n")
    if len(error4) > 0:
        f.write(f"Examples (first 10):\n")
        for idx, row in error4.head(10).iterrows():
            f.write(f"  user_id: {row['user_id']}, booking_date: {row['first_booking_date']}, destination: {row['destination_country']}\n")
    
    # Check the opposite: users with booking but destination is NDF
    error5 = df[(df['first_booking_date'].notna()) & (df['destination_country'] == 'NDF')]
    f.write(f"\nUsers with booking date but destination = NDF: {len(error5)}\n")
    if len(error5) > 0:
        f.write(f"Examples (first 10):\n")
        for idx, row in error5.head(10).iterrows():
            f.write(f"  user_id: {row['user_id']}, booking_date: {row['first_booking_date']}, destination: {row['destination_country']}\n")
    
    f.write("\n\n")
    
    # 5. Check for typos/anomalies in string columns
    f.write("5. STRING COLUMN ANALYSIS (Checking for typos)\n")
    f.write("-" * 80 + "\n")
    
    string_columns = ['user_gender', 'signup_platform', 'signup_process', 'user_language', 
                      'marketing_channel', 'marketing_provider', 'first_tracked_affiliate',
                      'signup_application', 'first_device', 'first_web_browser', 'destination_country']
    
    for col in string_columns:
        unique_vals = df[col].value_counts()
        f.write(f"\n{col}: {len(unique_vals)} unique values\n")
        f.write(f"Top 15 values:\n")
        for val, count in unique_vals.head(15).items():
            f.write(f"  '{val}': {count}\n")
        
        # Check for potential typos (values with very low counts that might be similar to common values)
        rare_values = unique_vals[unique_vals <= 5]
        if len(rare_values) > 0:
            f.write(f"Rare values (count <= 5): {len(rare_values)}\n")
            for val, count in rare_values.head(10).items():
                f.write(f"  '{val}': {count}\n")
    
    f.write("\n\n")
    
    # 6. Check for missing values
    f.write("6. MISSING VALUES ANALYSIS\n")
    f.write("-" * 80 + "\n")
    
    missing = df.isnull().sum()
    f.write(f"Missing values by column:\n")
    for col, count in missing.items():
        if count > 0:
            pct = (count / len(df)) * 100
            f.write(f"  {col}: {count} ({pct:.2f}%)\n")
    
    f.write("\n\n")
    
    # 7. Check for empty strings
    f.write("7. EMPTY STRING ANALYSIS\n")
    f.write("-" * 80 + "\n")
    
    for col in string_columns:
        empty_count = (df[col] == '').sum()
        if empty_count > 0:
            f.write(f"  {col}: {empty_count} empty strings\n")
    
    f.write("\n\n")
    
    # 8. Summary of all errors
    f.write("=" * 80 + "\n")
    f.write("SUMMARY OF ERRORS FOUND\n")
    f.write("=" * 80 + "\n")
    
    total_errors = 0
    
    if len(unrealistic_ages) > 0:
        f.write(f"✗ Unrealistic ages (< 18 or > 100): {len(unrealistic_ages)} rows\n")
        total_errors += len(unrealistic_ages)
    
    if len(extreme_ages) > 0:
        f.write(f"✗ Extreme ages (< 0 or > 120): {len(extreme_ages)} rows\n")
        total_errors += len(extreme_ages)
    
    if len(future_active) > 0:
        f.write(f"✗ Future first_active_date: {len(future_active)} rows\n")
        total_errors += len(future_active)
    
    if len(future_created) > 0:
        f.write(f"✗ Future account_created_date: {len(future_created)} rows\n")
        total_errors += len(future_created)
    
    if len(future_booking) > 0:
        f.write(f"✗ Future first_booking_date: {len(future_booking)} rows\n")
        total_errors += len(future_booking)
    
    if len(error1) > 0:
        f.write(f"✗ first_active_date > account_created_date: {len(error1)} rows\n")
        total_errors += len(error1)
    
    if len(error2) > 0:
        f.write(f"✗ account_created_date > first_booking_date: {len(error2)} rows\n")
        total_errors += len(error2)
    
    if len(error3) > 0:
        f.write(f"✗ first_active_date > first_booking_date: {len(error3)} rows\n")
        total_errors += len(error3)
    
    if len(error4) > 0:
        f.write(f"✗ No booking date but destination != NDF: {len(error4)} rows\n")
        total_errors += len(error4)
    
    if len(error5) > 0:
        f.write(f"✗ Has booking date but destination = NDF: {len(error5)} rows\n")
        total_errors += len(error5)
    
    f.write(f"\nTotal error categories found: {total_errors}\n")
    f.write("=" * 80 + "\n")

print(f"\nAnalysis complete. Results saved to: {output_file}")
print("\nReading output file...")
with open(output_file, 'r') as f:
    print(f.read())
