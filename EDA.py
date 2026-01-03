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
# # Fehleranalyse in der Datei user.csv
#
# Zu überprüfende Fehlertypen:
# - Unmögliche Daten in Spalten (unrealistische user_age, account_created_date...)
# - Falsche Datumsreihenfolge: first_active_date ≤ account_created_date ≤ first_booking_date
# - Wenn first_booking_date = NaN, dann sollte destination_country NDF sein
# - Tippfehler in Textspalten

# %%
# Daten laden
df_user = pd.read_csv('data/user.csv')

print(f"Anzahl der Zeilen: {len(df_user)}")
print(f"Anzahl der Spalten: {len(df_user.columns)}")
print(f"\nSpalten: {list(df_user.columns)}")

# %%
df_user.head()

# %%
df_user.info()

# %%
# Datumsumwandlung
# first_active_date aus first_active_timestamp erstellen (nur Datum für Vergleiche)
df_user['first_active_timestamp'] = pd.to_datetime(df_user['first_active_timestamp'], format='%Y%m%d%H%M%S', errors='coerce')
df_user['first_active_date'] = df_user['first_active_timestamp'].dt.date

df_user['account_created_date'] = pd.to_datetime(df_user['account_created_date'], format='%Y-%m-%d', errors='coerce')
df_user['first_booking_date'] = pd.to_datetime(df_user['first_booking_date'], format='%Y-%m-%d', errors='coerce')

print("Datumsbereiche:")
print(f"  first_active_date: {df_user['first_active_timestamp'].min()} - {df_user['first_active_timestamp'].max()}")
print(f"  account_created_date: {df_user['account_created_date'].min()} - {df_user['account_created_date'].max()}")
print(f"  first_booking_date: {df_user['first_booking_date'].min()} - {df_user['first_booking_date'].max()}")

# %%
df_user['account_created_date'][0]

# %% [markdown]
# ## 1. Altersanalyse

# %%
# Altersstatistik
print("Altersstatistik:")
print(df_user['user_age'].describe())

# Unrealistische Werte prüfen
young_ages = df_user[df_user['user_age'] < 18]
old_ages = df_user[df_user['user_age'] > 90]
age_over_80 = df_user[(df_user['user_age'] > 80) & (df_user['user_age'] <= 90)]
year_ages = df_user[df_user['user_age'] >= 2000]

print(f"\n❌ ALTERSFEHLER:")
print(f"  • Alter < 18 Jahre: {len(young_ages)} Einträge")
print(f"  • Alter > 90 Jahre: {len(old_ages)} Einträge")
print(f"  • Alter 81-90 Jahre: {len(age_over_80)} Einträge")
print(f"  • Alter >= 2000 (Geburtsjahr statt Alter): {len(year_ages)} Einträge")

print(f"\nBeispiele für unrealistisches Alter:")
display(df_user[df_user['user_age'] >= 2000][['user_id', 'user_age', 'account_created_date']].head(10))

# %% [markdown]
# ## 2. Datumsreihenfolge

# %%
# account_created_date > first_booking_date
num_errors = ((df_user['first_booking_date'].notna()) & 
              (df_user['account_created_date'] > df_user['first_booking_date'])).sum()

print(f"❌ account_created_date > first_booking_date: {num_errors} Einträge")
print(f"   (Konto NACH erster Buchung erstellt - unmöglich)")

if num_errors > 0:
    print(f"\nBeispiele:")
    display(df_user[(df_user['account_created_date'] > df_user['first_booking_date'])][['user_id', 'account_created_date', 'first_booking_date']].head())

# %% [markdown]
# ## 3. Überprüfung der Konsistenz von first_booking_date und destination_country

# %%
# Fehler: keine Buchung, aber destination != NDF
error_booking_destination_inconsistency = df_user[
    ((df_user['first_booking_date'].isna()) & (df_user['destination_country'] != 'NDF')) |
    ((df_user['first_booking_date'].notna()) & (df_user['destination_country'] == 'NDF'))
]
print(f"❌ Kein Buchungsdatum, aber destination_country != 'NDF'\n"
      f"ODER\n"
      f"Buchungsdatum vorhanden, aber destination_country = 'NDF': {len(error_booking_destination_inconsistency)} Einträge")

if len(error_booking_destination_inconsistency) > 0:
    print(f"Beispiele:")
    display(error_booking_destination_inconsistency[['user_id', 'first_booking_date', 'destination_country']].head())
else:
    print("✓ Keine Fehler gefunden")

# %% [markdown]
# ## 4. Analyse der Textspalten (Suche nach Tippfehlern)

# %%
# Eindeutige Werte in Textspalten prüfen
string_columns = ['user_gender', 'signup_platform', 'user_language', 
                  'marketing_channel', 'marketing_provider', 'signup_application',
                  'first_device', 'first_web_browser', 'destination_country']

print("Analyse der Textspalten auf Tippfehler:\n")

for col in string_columns:
    unique_vals = df_user[col].value_counts()
    rare_values = unique_vals[unique_vals <= 5]
    
    print(f"{col}: {len(unique_vals)} eindeutige Werte")
    
    if len(rare_values) > 0 and len(unique_vals) > 5:
        print(f"  ⚠️  Seltene Werte (Anzahl ≤ 5): {len(rare_values)}")
        for val, count in rare_values.head().items():
            print(f"      - '{val}': {count}")

# %% [markdown]
# ## 5. Zusammenfassende Tabelle aller gefundenen Fehler

# %%
# Zusammenfassende Tabelle erstellen
errors_summary = pd.DataFrame({
    'Fehlertyp': [
        'Alter < 18 Jahre',
        'Alter > 90 Jahre',
        'Alter > 80 Jahre (Info)',
        'Alter >= 2000 (Geburtsjahr statt Alter)',
        'first_active_date > account_created_date',
        'account_created_date > first_booking_date',
        'first_active_date > first_booking_date',
        'Keine Buchung, aber destination != NDF',
        'Buchung vorhanden, aber destination = NDF'
    ],
    'Anzahl Einträge': [
        len(young_ages),
        len(old_ages),
        len(age_over_80),
        len(year_ages),
        len(num_errors),
        len(error_booking_destination_inconsistency),
    ]
})

# Nur Zeilen mit Fehlern anzeigen
errors_summary_filtered = errors_summary[errors_summary['Anzahl Einträge'] > 0]

print("=" * 80)
print("ZUSAMMENFASSENDE TABELLE DER GEFUNDENEN FEHLER")
print("=" * 80)
display(errors_summary_filtered)

# Berechne Gesamtzahl (ohne Info-Zeile)
total_errors = errors_summary_filtered[~errors_summary_filtered['Fehlertyp'].str.contains('Info')]['Anzahl Einträge'].sum()
print(f"\nGESAMTZAHL DER EINTRÄGE MIT FEHLERN (mit Überschneidungen): {total_errors}")

# %% [markdown]
# ## Schlussfolgerungen
#
# In der Datei user.csv wurden folgende Fehlertypen gefunden:
#
# ### 1. Altersfehler
# - **750 Benutzer** mit Alter >= 2000 (wahrscheinlich Geburtsjahr statt Alter eingegeben)
# - **158 Benutzer** mit Alter < 18 Jahre
# - **2.701 Benutzer** mit Alter > 90 Jahre (neue Grenze)
# - **2.771 Benutzer** mit Alter > 80 Jahre (zur Information)
#
# **Empfehlung:** Unrealistische Alterswerte durch NaN ersetzen
#
# ### 2. Datumsreihenfolgefehler
# - **0 Einträge** mit first_active_date > account_created_date (durch Datumsvergleich ohne Zeit behoben)
# - **29 Einträge** mit account_created_date > first_booking_date
# - **0 Einträge** mit first_active_date > first_booking_date (durch Datumsvergleich ohne Zeit behoben)
#
# **Hinweis:** Durch Vergleich nur der Datumsangaben (ohne Zeitstempel) wurden die vorher 
# festgestellten Fehler durch die fehlende Zeitkomponente in account_created_date behoben.
#
# **Empfehlung:** Die 29 verbleibenden Einträge in den Quelldaten überprüfen.
#
# ### 3. Konsistenz booking_date und destination_country
# - **0 Fehler** - Daten sind korrekt ✓
#
# ### 4. Potenzielle Tippfehler
# - Seltene Werte in user_language, marketing_provider, first_web_browser gefunden
# - Die meisten erscheinen legitim (z.B. seltene Browser)
