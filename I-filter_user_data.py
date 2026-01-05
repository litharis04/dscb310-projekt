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
import missingno as msno
import matplotlib.pyplot as plt
from IPython.display import display

# %% [markdown]
# # Datenaufbereitung und Fehleranalyse: user.csv
#
# Dieser Notebook führt eine systematische Datenbereinigung und Fehleranalyse durch:
# 1. Laden und allgemeine Inspektion der Daten
# 2. Prüfung und Entfernung von Duplikaten
# 3. Konvertierung von Datumsangaben
# 4. Prüfung und Korrektur der Datumsreihenfolge
# 5. Bereinigung von user_gender
# 6. Filterung unrealistischer Altersangaben
# 7. Prüfung eindeutiger Werte und seltener Einträge
# 8. Analyse der Abhängigkeit zwischen first_booking_date und destination_country
# 9. Visualisierung fehlender Werte

# %% [markdown]
# ## 1. Daten laden und allgemeine Inspektion

# %%
# Daten laden
df_user_raw = pd.read_csv('data/user.csv')
df_user = df_user_raw.copy()

rows_initial = len(df_user)
print(f"Anzahl der Zeilen: {rows_initial}")
print(f"Anzahl der Spalten: {len(df_user.columns)}")
print(f"\nSpalten: {list(df_user.columns)}")

# %%
df_user.head()

# %%
df_user.info()

# %%
# Grundlegende Statistiken
df_user.describe()

# %% [markdown]
# ## 2. Prüfung auf Duplikate

# %%
# Duplikate prüfen
num_duplicates = df_user.duplicated().sum()
print(f"Anzahl der Duplikate: {num_duplicates}")

if num_duplicates > 0:
    print(f"\nBeispiele für Duplikate:")
    display(df_user[df_user.duplicated(keep=False)].head())
    
    # Duplikate entfernen
    df_user = df_user.drop_duplicates()
    print(f"\n{num_duplicates} Duplikate wurden entfernt")
    print(f"Neue Anzahl der Zeilen: {len(df_user)}")
else:
    print("Keine Duplikate gefunden")

# %% [markdown]
# ## 3. Konvertierung von Datumsangaben
#
# Die Datumsfelder werden in datetime-Format konvertiert:
# - `first_active_timestamp` -> datetime (in-place) + neues Feld `first_active_date` (nur Datum)
# - `account_created_date` -> datetime (in-place)
# - `first_booking_date` -> datetime (in-place)

# %%
# Datumskonvertierung
# first_active_timestamp konvertieren und first_active_date erstellen
df_user['first_active_timestamp'] = pd.to_datetime(
    df_user['first_active_timestamp'], 
    format='%Y%m%d%H%M%S', 
    errors='coerce'
)
df_user['first_active_date'] = df_user['first_active_timestamp'].dt.normalize()

# account_created_date konvertieren
df_user['account_created_date'] = pd.to_datetime(
    df_user['account_created_date'], 
    format='%Y-%m-%d', 
    errors='coerce'
)

# first_booking_date konvertieren
df_user['first_booking_date'] = pd.to_datetime(
    df_user['first_booking_date'], 
    format='%Y-%m-%d', 
    errors='coerce'
)

print("Datumsbereiche:")
print(f"  first_active_timestamp: {df_user['first_active_timestamp'].min()} bis {df_user['first_active_timestamp'].max()}")
print(f"  account_created_date: {df_user['account_created_date'].min()} bis {df_user['account_created_date'].max()}")
print(f"  first_booking_date: {df_user['first_booking_date'].min()} bis {df_user['first_booking_date'].max()}")

# %% [markdown]
# ## 4. Prüfung der Datumsreihenfolge
#
# Korrekte Reihenfolge: first_active_date ≤ account_created_date ≤ first_booking_date
#
# Zeilen mit Fehlern werden identifiziert und entfernt.

# %%
# Fehlerhafte Datumsreihenfolge identifizieren
# first_active_date > account_created_date
error1 = (df_user['first_active_date'] > df_user['account_created_date'])

# account_created_date > first_booking_date  
error2 = (df_user['first_booking_date'].notna()) & \
         (df_user['account_created_date'] > df_user['first_booking_date'])

# Kombinierte Fehlermaske
date_errors = error1 | error2

num_date_errors = date_errors.sum()
print(f"Anzahl der Zeilen mit fehlerhafter Datumsreihenfolge: {num_date_errors}")
print(f"  - first_active_date > account_created_date: {error1.sum()}")
print(f"  - account_created_date > first_booking_date: {error2.sum()}")

if num_date_errors > 0:
    print(f"\nBeispiele für fehlerhafte Datumsreihenfolge:")
    display(df_user[date_errors][['user_id', 'first_active_date', 'account_created_date', 'first_booking_date']].head())
    
    # Fehlerhafte Zeilen entfernen
    df_user = df_user[~date_errors]
    print(f"\n{num_date_errors} Zeilen mit fehlerhafter Datumsreihenfolge wurden entfernt.")
else:
    print("Keine Fehler in der Datumsreihenfolge gefunden")

# %% [markdown]
# ## 5. Bereinigung von user_gender
#
# Zulässige Werte: 'female', 'male', 'other', NaN
#
# Zunächst Analyse der ursprünglichen Werte, dann Bereinigung.

# %%
# Analyse der ursprünglichen Werte in user_gender
print("Ursprüngliche eindeutige Werte in user_gender:")
print(df_user['user_gender'].value_counts(dropna=False))
print()

# %%
# Normalisierung: Groß-/Kleinschreibung vereinheitlichen
df_user['user_gender'] = df_user['user_gender'].str.lower()

# Ungültige Werte auf NaN setzen
df_user['user_gender'] = df_user['user_gender'].replace('-unknown-', np.nan)

print("\nBereinigte Werte:")
print(df_user['user_gender'].value_counts(dropna=False))

# %% [markdown]
# ## 6. Filterung unrealistischer Altersangaben
#
# Zeilen mit user_age < 18 oder > 90 werden entfernt.

# %%
# Altersstatistik vor der Bereinigung
print("Altersstatistik vor der Bereinigung:")
print(df_user['user_age'].describe())
print()

# Unrealistische Altersangaben identifizieren
age_too_young = df_user['user_age'] < 18
age_too_old = df_user['user_age'] > 90
invalid_age = age_too_young | age_too_old

num_invalid_age = invalid_age.sum()
print(f"Anzahl der Zeilen mit unrealistischem Alter: {num_invalid_age}")
print(f"  - Alter < 18: {age_too_young.sum()}")
print(f"  - Alter > 90: {age_too_old.sum()}")



# %%
print(f"\nBeispiele für unrealistische Altersangaben:")
display(df_user[invalid_age][['user_id', 'user_age', 'account_created_date']].head())
    
# Zeilen mit unrealistischem Alter entfernen
df_user = df_user[~invalid_age]
print(f"\n{num_invalid_age} Zeilen mit unrealistischem Alter wurden entfernt")

# Konvertierung von user_age in Integer
df_user['user_age'] = df_user['user_age'].astype('int', errors='ignore')

print("\nAltersstatistik nach der Bereinigung:")
print(df_user['user_age'].describe())

# %% [markdown]
# ## 7. Prüfung eindeutiger Werte in Textspalten
#
# Seltene Werte (< 10 Vorkommen) werden auf mögliche Tippfehler untersucht.

# %%
# Zu prüfende Textspalten
text_columns = [
    'user_gender', 'signup_platform', 'signup_process', 'user_language',
    'marketing_channel', 'marketing_provider', 'first_tracked_affiliate',
    'signup_application', 'first_device', 'first_web_browser', 'destination_country'
]

for col in text_columns:
    print(f"\n{col}:")
    
    counts = df_user[col].value_counts(dropna=False)
    print(f"Anzahl eindeutiger Werte: {len(counts)}")
    
    # Seltene Werte (< 10 Vorkommen)
    rare_values = counts[counts < 10]
    
    if len(rare_values) > 0:
        print(f"Seltene Werte (< 10 Vorkommen): {len(rare_values)}")
        print("\nTop 10 seltene Werte:")
        for value, count in rare_values.head(10).items():
            print(f"  - '{value}': {count}")
    else:
        print("Keine seltenen Werte gefunden")
    
    # Top 10 häufigste Werte
    print(f"\nTop 10 häufigste Werte:")
    for value, count in counts.head(10).items():
        percentage = (count / len(df_user)) * 100
        print(f"  - '{value}': {count} ({percentage:.2f}%)")
    print("-" * 80)

# %%
# Bereinigung von first_web_browser
print(f"Zeilen mit unbekanntem first_web_browser: {(df_user['first_web_browser'] == '-unknown-').sum()}")
df_user['first_web_browser'] = df_user['first_web_browser'].replace('-unknown-', np.nan)

# %% [markdown]
# ## 8. Analyse der Abhängigkeit: first_booking_date ↔ destination_country
#
# Zweiseitige Prüfung:
# - Wenn first_booking_date = NaN => destination_country sollte 'NDF' sein
# - Wenn destination_country = 'NDF' => first_booking_date sollte NaN sein

# %%
# Fall 1: Keine Buchung (first_booking_date = NaN), aber destination != NDF
no_booking_but_dest = (df_user['first_booking_date'].isna()) & \
                       (df_user['destination_country'] != 'NDF')
num_case1 = no_booking_but_dest.sum()

print(f"\n1. Zeilen ohne Buchungsdatum, aber destination_country != 'NDF': {num_case1}")

if num_case1 > 0:
    print("INKONSISTENZ gefunden!")
    print("\n   Beispiele:")
    display(df_user[no_booking_but_dest][['user_id', 'first_booking_date', 'destination_country']].head())
else:
    print("Keine Inkonsistenz")

# Fall 2: Buchung vorhanden (first_booking_date != NaN), aber destination = NDF
booking_but_ndf = (df_user['first_booking_date'].notna()) & \
                   (df_user['destination_country'] == 'NDF')
num_case2 = booking_but_ndf.sum()

print(f"\n2. Zeilen mit Buchungsdatum, aber destination_country = 'NDF': {num_case2}")

if num_case2 > 0:
    print("INKONSISTENZ gefunden!")
    print("\n   Beispiele:")
    display(df_user[booking_but_ndf][['user_id', 'first_booking_date', 'destination_country']].head())
else:
    print("Keine Inkonsistenz")

# Zusammenfassung
print("\n\nZUSAMMENFASSUNG:")
total_inconsistencies = num_case1 + num_case2

if total_inconsistencies == 0:
    print("Die Abhängigkeit zwischen first_booking_date und destination_country ist konsistent")
else:
    print(f"Insgesamt {total_inconsistencies} inkonsistente Zeilen gefunden")

# Statistik
print(f"  - Zeilen ohne Buchungsdatum: {df_user['first_booking_date'].isna().sum()}")
print(f"  - Zeilen mit destination_country = 'NDF': {(df_user['destination_country'] == 'NDF').sum()}")

# %% [markdown]
# ## 9. Visualisierung fehlender Werte

# %%
# Fehlende Werte pro Spalte
print("Fehlende Werte pro Spalte:\n")
missing_values = df_user.isnull().sum()
missing_percent = round((missing_values / len(df_user)) * 100, 2)

missing_df = pd.DataFrame({
    'Spalte': missing_values.index,
    'Anzahl fehlend': missing_values.values,
    'Prozent fehlend': missing_percent.values
})
missing_df = missing_df[missing_df['Anzahl fehlend'] > 0].sort_values('Anzahl fehlend', ascending=False)

if len(missing_df) > 0:
    display(missing_df)
else:
    print("Keine fehlenden Werte gefunden")

# %%
# Visualisierung mit missingno

# Matrix-Plot
msno.matrix(df_user, sparkline=False, figsize=(12, 6))
plt.title('Matrix fehlender Werte in user.csv', fontsize=14, pad=20)
plt.tight_layout()
plt.show()
    
# Bar-Plot
msno.bar(df_user, figsize=(12, 6))
plt.title('Vollständigkeit der Daten pro Spalte', fontsize=14, pad=20)
plt.tight_layout()
plt.show()
    
# Heatmap-Plot
msno.heatmap(df_user, figsize=(12, 8))
plt.title('Korrelation fehlender Werte', fontsize=14, pad=20)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Zusammenfassung der Datenbereinigung
#
# Nach allen Bereinigungsschritten:

# %%
print(f"\nUrsprüngliche Anzahl der Zeilen: {rows_initial}")
print(f"Finale Anzahl der Zeilen: {len(df_user)}")
print(f"Entfernte Zeilen gesamt: {rows_initial - len(df_user)} ({((rows_initial - len(df_user)) / rows_initial * 100):.2f}%)")
print(f"Anzahl der Spalten: {len(df_user.columns)}")

print(f"\nDatentypen:")
df_user.info()

# %%
# Exportieren
df_user.to_parquet('data/users_filtered.parquet', index=False)
print("df_user erfolgreich in 'data/users_filtered.parquet' exportiert")
