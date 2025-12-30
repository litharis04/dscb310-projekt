"""
Create a comprehensive error summary document for user.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Load the data
df = pd.read_csv('/home/runner/work/dscb310-projekt/dscb310-projekt/data/user.csv')

# Convert dates
df['first_active_date'] = pd.to_datetime(df['first_active_timestamp'], format='%Y%m%d%H%M%S', errors='coerce')
df['account_created_date_dt'] = pd.to_datetime(df['account_created_date'], errors='coerce')
df['first_booking_date_dt'] = pd.to_datetime(df['first_booking_date'], errors='coerce')

# Open output file
output_file = '/home/runner/work/dscb310-projekt/dscb310-projekt/scripts/outputs/user_csv_errors_summary.txt'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 100 + "\n")
    f.write(" " * 30 + "ОШИБКИ В ФАЙЛЕ USER.CSV\n")
    f.write("=" * 100 + "\n\n")
    
    f.write("ОПИСАНИЕ ЗАДАЧИ:\n")
    f.write("-" * 100 + "\n")
    f.write("Найти ошибки в файле users.csv. Примеры ошибок:\n")
    f.write("- невозможные данные в столбцах (нереалистичные user_age, account_created_date...)\n")
    f.write("- неверный порядок дат (first_active_date < account_created_date < first_booking_date)\n")
    f.write("- если first_booking_date = NaN, то destination_country должно быть NDF\n")
    f.write("- опечатки в столбцах, содержащих строки\n\n")
    
    f.write("=" * 100 + "\n")
    f.write("НАЙДЕННЫЕ ОШИБКИ\n")
    f.write("=" * 100 + "\n\n")
    
    # Error 1: Unrealistic ages
    f.write("1. НЕРЕАЛИСТИЧНЫЙ ВОЗРАСТ (user_age)\n")
    f.write("-" * 100 + "\n")
    
    # Ages < 18
    young_ages = df[df['user_age'] < 18]
    f.write(f"a) Пользователи с возрастом < 18 лет: {len(young_ages)} записей\n")
    if len(young_ages) > 0:
        f.write(f"   Минимальный возраст: {young_ages['user_age'].min()}\n")
        f.write(f"   Примеры:\n")
        for idx, row in young_ages.head(20).iterrows():
            f.write(f"   - user_id: {row['user_id']}, age: {row['user_age']}\n")
    
    # Ages > 100
    old_ages = df[df['user_age'] > 100]
    f.write(f"\nb) Пользователи с возрастом > 100 лет: {len(old_ages)} записей\n")
    if len(old_ages) > 0:
        f.write(f"   Максимальный возраст: {old_ages['user_age'].max()}\n")
        f.write(f"   Примеры:\n")
        for idx, row in old_ages.head(20).iterrows():
            f.write(f"   - user_id: {row['user_id']}, age: {row['user_age']}\n")
    
    # Age = 2014 (likely year instead of age)
    year_ages = df[df['user_age'] >= 2000]
    f.write(f"\nc) Пользователи с возрастом >= 2000 (вероятно, год вместо возраста): {len(year_ages)} записей\n")
    if len(year_ages) > 0:
        f.write(f"   Примеры:\n")
        for idx, row in year_ages.head(20).iterrows():
            f.write(f"   - user_id: {row['user_id']}, age: {row['user_age']}\n")
    
    f.write("\n\n")
    
    # Error 2: Date ordering
    f.write("2. НЕПРАВИЛЬНЫЙ ПОРЯДОК ДАТ\n")
    f.write("-" * 100 + "\n")
    
    # first_active_date > account_created_date
    error1 = df[(df['first_active_date'].notna()) & (df['account_created_date_dt'].notna()) & 
                (df['first_active_date'] > df['account_created_date_dt'])]
    f.write(f"a) first_active_date > account_created_date: {len(error1)} записей\n")
    f.write(f"   (первая активность ПОСЛЕ создания аккаунта - невозможно)\n")
    if len(error1) > 0:
        f.write(f"   Примеры:\n")
        for idx, row in error1.head(20).iterrows():
            diff = (row['first_active_date'] - row['account_created_date_dt']).total_seconds() / 3600
            f.write(f"   - user_id: {row['user_id']}, first_active: {row['first_active_date']}, " +
                   f"created: {row['account_created_date_dt']} (разница: {diff:.1f} часов)\n")
    
    # account_created_date > first_booking_date
    error2 = df[(df['account_created_date_dt'].notna()) & (df['first_booking_date_dt'].notna()) & 
                (df['account_created_date_dt'] > df['first_booking_date_dt'])]
    f.write(f"\nb) account_created_date > first_booking_date: {len(error2)} записей\n")
    f.write(f"   (аккаунт создан ПОСЛЕ первого бронирования - невозможно)\n")
    if len(error2) > 0:
        f.write(f"   Примеры:\n")
        for idx, row in error2.head(20).iterrows():
            diff = (row['account_created_date_dt'] - row['first_booking_date_dt']).days
            f.write(f"   - user_id: {row['user_id']}, created: {row['account_created_date_dt']}, " +
                   f"booking: {row['first_booking_date_dt']} (разница: {diff} дней)\n")
    
    # first_active_date > first_booking_date
    error3 = df[(df['first_active_date'].notna()) & (df['first_booking_date_dt'].notna()) & 
                (df['first_active_date'] > df['first_booking_date_dt'])]
    f.write(f"\nc) first_active_date > first_booking_date: {len(error3)} записей\n")
    f.write(f"   (первая активность ПОСЛЕ первого бронирования - маловероятно)\n")
    if len(error3) > 0:
        f.write(f"   Примеры:\n")
        for idx, row in error3.head(20).iterrows():
            diff = (row['first_active_date'] - row['first_booking_date_dt']).total_seconds() / 3600
            f.write(f"   - user_id: {row['user_id']}, first_active: {row['first_active_date']}, " +
                   f"booking: {row['first_booking_date_dt']} (разница: {diff:.1f} часов)\n")
    
    f.write("\n\n")
    
    # Error 3: Booking date vs destination
    f.write("3. НЕСООТВЕТСТВИЕ first_booking_date И destination_country\n")
    f.write("-" * 100 + "\n")
    
    # No booking but destination != NDF
    error4 = df[(df['first_booking_date'].isna()) & (df['destination_country'] != 'NDF')]
    f.write(f"a) Нет даты бронирования, но destination_country != 'NDF': {len(error4)} записей\n")
    if len(error4) > 0:
        f.write(f"   (если нет бронирования, страна назначения должна быть 'NDF')\n")
        f.write(f"   Примеры:\n")
        for idx, row in error4.head(20).iterrows():
            f.write(f"   - user_id: {row['user_id']}, booking_date: {row['first_booking_date']}, " +
                   f"destination: {row['destination_country']}\n")
    else:
        f.write(f"   ✓ Ошибок не найдено\n")
    
    # Has booking but destination = NDF
    error5 = df[(df['first_booking_date'].notna()) & (df['destination_country'] == 'NDF')]
    f.write(f"\nb) Есть дата бронирования, но destination_country = 'NDF': {len(error5)} записей\n")
    if len(error5) > 0:
        f.write(f"   (если есть бронирование, страна назначения не должна быть 'NDF')\n")
        f.write(f"   Примеры:\n")
        for idx, row in error5.head(20).iterrows():
            f.write(f"   - user_id: {row['user_id']}, booking_date: {row['first_booking_date']}, " +
                   f"destination: {row['destination_country']}\n")
    else:
        f.write(f"   ✓ Ошибок не найдено\n")
    
    f.write("\n\n")
    
    # Error 4: String column analysis
    f.write("4. АНАЛИЗ СТРОКОВЫХ СТОЛБЦОВ (поиск опечаток)\n")
    f.write("-" * 100 + "\n")
    
    # Check for rare values that might be typos
    string_columns = ['user_gender', 'signup_platform', 'user_language', 
                      'marketing_channel', 'marketing_provider', 'signup_application',
                      'first_device', 'first_web_browser']
    
    potential_typos_found = False
    
    for col in string_columns:
        unique_vals = df[col].value_counts()
        rare_values = unique_vals[unique_vals <= 3]
        
        if len(rare_values) > 0 and len(unique_vals) > 5:
            if not potential_typos_found:
                f.write(f"Обнаружены редкие значения (возможные опечатки):\n\n")
                potential_typos_found = True
            
            f.write(f"{col}:\n")
            f.write(f"  Всего уникальных значений: {len(unique_vals)}\n")
            f.write(f"  Редких значений (count <= 3): {len(rare_values)}\n")
            for val, count in rare_values.items():
                f.write(f"  - '{val}': {count} раз(а)\n")
            f.write("\n")
    
    if not potential_typos_found:
        f.write("✓ Явных опечаток не обнаружено (все редкие значения выглядят корректно)\n")
    
    f.write("\n\n")
    
    # Summary table
    f.write("=" * 100 + "\n")
    f.write("ИТОГОВАЯ ТАБЛИЦА ОШИБОК\n")
    f.write("=" * 100 + "\n\n")
    
    f.write(f"{'Тип ошибки':<60} {'Количество':>15}\n")
    f.write("-" * 100 + "\n")
    
    total = 0
    
    errors = [
        ("Возраст < 18 лет", len(young_ages)),
        ("Возраст > 100 лет", len(old_ages)),
        ("Возраст >= 2000 (год вместо возраста)", len(year_ages)),
        ("first_active_date > account_created_date", len(error1)),
        ("account_created_date > first_booking_date", len(error2)),
        ("first_active_date > first_booking_date", len(error3)),
        ("Нет бронирования, но destination != NDF", len(error4)),
        ("Есть бронирование, но destination = NDF", len(error5)),
    ]
    
    for err_name, err_count in errors:
        if err_count > 0:
            f.write(f"{err_name:<60} {err_count:>15}\n")
            total += err_count
    
    f.write("-" * 100 + "\n")
    f.write(f"{'ВСЕГО ЗАПИСЕЙ С ОШИБКАМИ (с учетом возможных пересечений)':<60} {total:>15}\n")
    f.write("=" * 100 + "\n\n")
    
    # Recommendations
    f.write("РЕКОМЕНДАЦИИ ПО ИСПРАВЛЕНИЮ:\n")
    f.write("-" * 100 + "\n")
    f.write("1. Возраст >= 2000: заменить на NaN (вероятно, указан год рождения вместо возраста)\n")
    f.write("2. Возраст < 18 или > 120: заменить на NaN (нереалистичные значения)\n")
    f.write("3. Неправильный порядок дат:\n")
    f.write("   - Проверить исходные данные\n")
    f.write("   - Возможно, account_created_date указана без времени (00:00:00)\n")
    f.write("   - Рассмотреть возможность использования только даты (без времени) для сравнения\n")
    f.write("4. Несоответствия в booking/destination: проверить логику заполнения данных\n")
    f.write("=" * 100 + "\n")

print(f"Detailed summary created: {output_file}")

# Also print to console
with open(output_file, 'r', encoding='utf-8') as f:
    print(f.read())
