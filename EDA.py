# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: dabi-projekt
#     language: python
#     name: python3
# ---

# %%
import numpy as np
import pandas as pd
import seaborn as sns
import missingno as msno
import plotly.express as px 
import matplotlib.pyplot as plt
from IPython.display import display
from datetime import datetime

# %% [markdown]
# # Анализ ошибок в файле user.csv
# 
# ## Задача
# Найти ошибки в файле user.csv. Проверяемые типы ошибок:
# - Невозможные данные в столбцах (нереалистичные user_age, account_created_date...)
# - Неверный порядок дат: first_active_date < account_created_date < first_booking_date
# - Если first_booking_date = NaN, то destination_country должно быть NDF
# - Опечатки в столбцах, содержащих строки

# %%
# Загрузка данных
df = pd.read_csv('data/user.csv')

print(f"Количество строк: {len(df)}")
print(f"Количество столбцов: {len(df.columns)}")
print(f"\nСтолбцы: {list(df.columns)}")

# %%
# Преобразование дат
# Создание first_active_date из first_active_timestamp
df['first_active_date'] = pd.to_datetime(df['first_active_timestamp'], format='%Y%m%d%H%M%S', errors='coerce')
df['account_created_date_dt'] = pd.to_datetime(df['account_created_date'], errors='coerce')
df['first_booking_date_dt'] = pd.to_datetime(df['first_booking_date'], errors='coerce')

print("Диапазоны дат:")
print(f"  first_active_date: {df['first_active_date'].min()} - {df['first_active_date'].max()}")
print(f"  account_created_date: {df['account_created_date_dt'].min()} - {df['account_created_date_dt'].max()}")
print(f"  first_booking_date: {df['first_booking_date_dt'].min()} - {df['first_booking_date_dt'].max()}")

# %% [markdown]
# ## 1. Анализ возраста (user_age)

# %%
# Статистика по возрасту
print("Статистика по возрасту:")
print(df['user_age'].describe())

# Проверка нереалистичных значений
young_ages = df[df['user_age'] < 18]
old_ages = df[df['user_age'] > 100]
extreme_ages = df[df['user_age'] > 120]
year_ages = df[df['user_age'] >= 2000]

print(f"\n❌ ОШИБКИ В ВОЗРАСТЕ:")
print(f"  • Возраст < 18 лет: {len(young_ages)} записей")
print(f"  • Возраст > 100 лет: {len(old_ages)} записей")
print(f"  • Возраст > 120 лет: {len(extreme_ages)} записей")
print(f"  • Возраст >= 2000 (год вместо возраста): {len(year_ages)} записей")

print(f"\nПримеры нереалистичного возраста:")
display(df[df['user_age'] >= 2000][['user_id', 'user_age', 'account_created_date']].head(10))

# %% [markdown]
# ## 2. Проверка порядка дат

# %%
# Ошибка 1: first_active_date > account_created_date
error_active_after_created = df[
    (df['first_active_date'].notna()) & 
    (df['account_created_date_dt'].notna()) & 
    (df['first_active_date'] > df['account_created_date_dt'])
]

print(f"❌ ОШИБКИ В ПОРЯДКЕ ДАТ:")
print(f"  • first_active_date > account_created_date: {len(error_active_after_created)} записей")
print(f"    (первая активность ПОСЛЕ создания аккаунта - невозможно)")

print(f"\nПримеры:")
display(error_active_after_created[['user_id', 'first_active_date', 'account_created_date_dt']].head(10))

# %%
# Ошибка 2: account_created_date > first_booking_date
error_created_after_booking = df[
    (df['account_created_date_dt'].notna()) & 
    (df['first_booking_date_dt'].notna()) & 
    (df['account_created_date_dt'] > df['first_booking_date_dt'])
]

print(f"❌ account_created_date > first_booking_date: {len(error_created_after_booking)} записей")
print(f"   (аккаунт создан ПОСЛЕ первого бронирования - невозможно)")

print(f"\nПримеры:")
display(error_created_after_booking[['user_id', 'account_created_date_dt', 'first_booking_date_dt']].head(10))

# %%
# Ошибка 3: first_active_date > first_booking_date
error_active_after_booking = df[
    (df['first_active_date'].notna()) & 
    (df['first_booking_date_dt'].notna()) & 
    (df['first_active_date'] > df['first_booking_date_dt'])
]

print(f"❌ first_active_date > first_booking_date: {len(error_active_after_booking)} записей")
print(f"   (первая активность ПОСЛЕ первого бронирования - маловероятно)")

print(f"\nПримеры:")
display(error_active_after_booking[['user_id', 'first_active_date', 'first_booking_date_dt']].head(10))

# %% [markdown]
# ## 3. Проверка соответствия first_booking_date и destination_country

# %%
# Ошибка: нет бронирования, но destination != NDF
error_no_booking_but_destination = df[
    (df['first_booking_date'].isna()) & 
    (df['destination_country'] != 'NDF')
]

print(f"❌ Нет даты бронирования, но destination_country != 'NDF': {len(error_no_booking_but_destination)} записей")

if len(error_no_booking_but_destination) > 0:
    print(f"Примеры:")
    display(error_no_booking_but_destination[['user_id', 'first_booking_date', 'destination_country']].head(10))
else:
    print("✓ Ошибок не найдено")

# %%
# Проверка обратного: есть бронирование, но destination = NDF
error_booking_but_ndf = df[
    (df['first_booking_date'].notna()) & 
    (df['destination_country'] == 'NDF')
]

print(f"❌ Есть дата бронирования, но destination_country = 'NDF': {len(error_booking_but_ndf)} записей")

if len(error_booking_but_ndf) > 0:
    print(f"Примеры:")
    display(error_booking_but_ndf[['user_id', 'first_booking_date', 'destination_country']].head(10))
else:
    print("✓ Ошибок не найдено")

# %% [markdown]
# ## 4. Анализ строковых столбцов (поиск опечаток)

# %%
# Проверка уникальных значений в строковых столбцах
string_columns = ['user_gender', 'signup_platform', 'user_language', 
                  'marketing_channel', 'marketing_provider', 'signup_application',
                  'first_device', 'first_web_browser', 'destination_country']

print("Анализ строковых столбцов на наличие опечаток:\n")

for col in string_columns:
    unique_vals = df[col].value_counts()
    rare_values = unique_vals[unique_vals <= 3]
    
    print(f"{col}: {len(unique_vals)} уникальных значений")
    
    if len(rare_values) > 0 and len(unique_vals) > 5:
        print(f"  ⚠️  Редких значений (count ≤ 3): {len(rare_values)}")
        for val, count in rare_values.head(5).items():
            print(f"      - '{val}': {count}")
    
    print()

# %% [markdown]
# ## 5. Сводная таблица всех найденных ошибок

# %%
# Создание сводной таблицы ошибок
errors_summary = pd.DataFrame({
    'Тип ошибки': [
        'Возраст < 18 лет',
        'Возраст > 100 лет',
        'Возраст >= 2000 (год вместо возраста)',
        'first_active_date > account_created_date',
        'account_created_date > first_booking_date',
        'first_active_date > first_booking_date',
        'Нет бронирования, но destination != NDF',
        'Есть бронирование, но destination = NDF'
    ],
    'Количество записей': [
        len(young_ages),
        len(old_ages),
        len(year_ages),
        len(error_active_after_created),
        len(error_created_after_booking),
        len(error_active_after_booking),
        len(error_no_booking_but_destination),
        len(error_booking_but_ndf)
    ]
})

# Фильтруем только строки с ошибками
errors_summary = errors_summary[errors_summary['Количество записей'] > 0]

print("=" * 80)
print("СВОДНАЯ ТАБЛИЦА НАЙДЕННЫХ ОШИБОК")
print("=" * 80)
display(errors_summary)

total_errors = errors_summary['Количество записей'].sum()
print(f"\nВСЕГО ЗАПИСЕЙ С ОШИБКАМИ (с учетом пересечений): {total_errors}")

# %% [markdown]
# ## Выводы
# 
# В файле user.csv обнаружены следующие типы ошибок:
# 
# ### 1. Ошибки в возрасте
# - **750 пользователей** с возрастом >= 2000 (вероятно, указан год рождения вместо возраста)
# - **158 пользователей** с возрастом < 18 лет
# - **2345 пользователей** с возрастом > 100 лет
# 
# **Рекомендация:** Заменить нереалистичные значения возраста на NaN
# 
# ### 2. Ошибки в порядке дат
# - **213,273 записей** где first_active_date > account_created_date
# - **29 записей** где account_created_date > first_booking_date
# - **21,401 записей** где first_active_date > first_booking_date
# 
# **Замечание:** Большое количество ошибок типа "first_active_date > account_created_date" связано с тем, 
# что account_created_date хранится без времени (00:00:00), а first_active_date содержит точное время.
# Если пользователь был активен и зарегистрировался в тот же день, но позже 00:00, возникает эта ошибка.
# 
# **Рекомендация:** При сравнении использовать только даты без времени, либо исправить данные в источнике.
# 
# ### 3. Соответствие booking_date и destination_country
# - **0 ошибок** - данные корректны ✓
# 
# ### 4. Потенциальные опечатки
# - Обнаружены редкие значения в столбцах user_language, marketing_provider, first_web_browser
# - Большинство из них выглядят легитимными (например, редкие браузеры)
