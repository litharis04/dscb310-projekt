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
# ## Aufgabe
# Fehler in der Datei user.csv finden. Zu überprüfende Fehlertypen:
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
# Datumsumwandlung
# first_active_date aus first_active_timestamp erstellen (nur Datum für Vergleiche)
df_user['first_active_timestamp_dt'] = pd.to_datetime(df_user['first_active_timestamp'], format='%Y%m%d%H%M%S', errors='coerce')
df_user['first_active_date'] = df_user['first_active_timestamp_dt'].dt.date

df_user['account_created_date_ts'] = pd.to_datetime(df_user['account_created_date'], errors='coerce')
df_user['account_created_date_dt'] = df_user['account_created_date_ts'].dt.date

df_user['first_booking_date_ts'] = pd.to_datetime(df_user['first_booking_date'], errors='coerce')
df_user['first_booking_date_dt'] = df_user['first_booking_date_ts'].dt.date

print("Datumsbereiche:")
print(f"  first_active_date: {df_user['first_active_timestamp_dt'].min()} - {df_user['first_active_timestamp_dt'].max()}")
print(f"  account_created_date: {df_user['account_created_date_ts'].min()} - {df_user['account_created_date_ts'].max()}")
print(f"  first_booking_date: {df_user['first_booking_date_ts'].min()} - {df_user['first_booking_date_ts'].max()}")

# %% [markdown]
# ## 1. Altersanalyse (user_age)

# %%
# Altersstatistik
print("Altersstatistik:")
print(df_user['user_age'].describe())

# Unrealistische Werte prüfen
young_ages = df_user[df_user['user_age'] < 18]
old_ages = df_user[df_user['user_age'] > 90]
age_over_80 = df_user[df_user['user_age'] > 80]
extreme_ages = df_user[df_user['user_age'] > 120]
year_ages = df_user[df_user['user_age'] >= 2000]

print(f"\n❌ ALTERSFEHLER:")
print(f"  • Alter < 18 Jahre: {len(young_ages)} Einträge")
print(f"  • Alter > 90 Jahre: {len(old_ages)} Einträge")
print(f"  • Alter > 80 Jahre: {len(age_over_80)} Einträge")
print(f"  • Alter > 120 Jahre: {len(extreme_ages)} Einträge")
print(f"  • Alter >= 2000 (Geburtsjahr statt Alter): {len(year_ages)} Einträge")

print(f"\nBeispiele für unrealistisches Alter:")
display(df_user[df_user['user_age'] >= 2000][['user_id', 'user_age', 'account_created_date']].head(10))

# %% [markdown]
# ## 2. Überprüfung der Datumsreihenfolge
# 
# **Hinweis:** Datumsvergleiche werden nur auf Basis des Datums ohne Zeitstempel durchgeführt.

# %%
# Fehler 1: first_active_date > account_created_date
error_active_after_created = df_user[
    (df_user['first_active_date'].notna()) & 
    (df_user['account_created_date_dt'].notna()) & 
    (df_user['first_active_date'] > df_user['account_created_date_dt'])
]

print(f"❌ FEHLER IN DER DATUMSREIHENFOLGE:")
print(f"  • first_active_date > account_created_date: {len(error_active_after_created)} Einträge")
print(f"    (erste Aktivität NACH Kontoerstellung - unmöglich)")

if len(error_active_after_created) > 0:
    print(f"\nBeispiele:")
    display(error_active_after_created[['user_id', 'first_active_date', 'account_created_date_dt']].head(10))

# %%
# Fehler 2: account_created_date > first_booking_date
error_created_after_booking = df_user[
    (df_user['account_created_date_dt'].notna()) & 
    (df_user['first_booking_date_dt'].notna()) & 
    (df_user['account_created_date_dt'] > df_user['first_booking_date_dt'])
]

print(f"❌ account_created_date > first_booking_date: {len(error_created_after_booking)} Einträge")
print(f"   (Konto NACH erster Buchung erstellt - unmöglich)")

if len(error_created_after_booking) > 0:
    print(f"\nBeispiele:")
    display(error_created_after_booking[['user_id', 'account_created_date_dt', 'first_booking_date_dt']].head(10))

# %%
# Fehler 3: first_active_date > first_booking_date
error_active_after_booking = df_user[
    (df_user['first_active_date'].notna()) & 
    (df_user['first_booking_date_dt'].notna()) & 
    (df_user['first_active_date'] > df_user['first_booking_date_dt'])
]

print(f"❌ first_active_date > first_booking_date: {len(error_active_after_booking)} Einträge")
print(f"   (erste Aktivität NACH erster Buchung - unwahrscheinlich)")

if len(error_active_after_booking) > 0:
    print(f"\nBeispiele:")
    display(error_active_after_booking[['user_id', 'first_active_date', 'first_booking_date_dt']].head(10))

# %% [markdown]
# ## 3. Überprüfung der Konsistenz von first_booking_date und destination_country

# %%
# Fehler: keine Buchung, aber destination != NDF
error_no_booking_but_destination = df_user[
    (df_user['first_booking_date'].isna()) & 
    (df_user['destination_country'] != 'NDF')
]

print(f"❌ Kein Buchungsdatum, aber destination_country != 'NDF': {len(error_no_booking_but_destination)} Einträge")

if len(error_no_booking_but_destination) > 0:
    print(f"Beispiele:")
    display(error_no_booking_but_destination[['user_id', 'first_booking_date', 'destination_country']].head(10))
else:
    print("✓ Keine Fehler gefunden")

# %%
# Umgekehrt prüfen: Buchung vorhanden, aber destination = NDF
error_booking_but_ndf = df_user[
    (df_user['first_booking_date'].notna()) & 
    (df_user['destination_country'] == 'NDF')
]

print(f"❌ Buchungsdatum vorhanden, aber destination_country = 'NDF': {len(error_booking_but_ndf)} Einträge")

if len(error_booking_but_ndf) > 0:
    print(f"Beispiele:")
    display(error_booking_but_ndf[['user_id', 'first_booking_date', 'destination_country']].head(10))
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
    rare_values = unique_vals[unique_vals <= 3]
    
    print(f"{col}: {len(unique_vals)} eindeutige Werte")
    
    if len(rare_values) > 0 and len(unique_vals) > 5:
        print(f"  ⚠️  Seltene Werte (Anzahl ≤ 3): {len(rare_values)}")
        for val, count in rare_values.head(5).items():
            print(f"      - '{val}': {count}")
    
    print()

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
        len(error_active_after_created),
        len(error_created_after_booking),
        len(error_active_after_booking),
        len(error_no_booking_but_destination),
        len(error_booking_but_ndf)
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
