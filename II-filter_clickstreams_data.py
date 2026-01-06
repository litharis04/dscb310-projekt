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
# # Datenaufbereitung und Fehleranalyse: clickstreams.parquet
#
# Dieser Notebook führt eine systematische Datenbereinigung und Fehleranalyse durch:
# 1. Laden und allgemeine Inspektion der Daten
# 2. Prüfung auf Duplikate
# 3. Analyse fehlender Werte
# 4. Bereinigung von '-unknown-' Werten
# 5. Detaillierte Analyse aller Spalten
# 6. Visualisierung fehlender Werte mit missingno
# 7. Export der bereinigten Daten

# %% [markdown]
# ## 1. Daten laden und allgemeine Inspektion

# %%
# Daten laden
df_clickstreams = pd.read_parquet('data/clickstreams.parquet')

rows_initial = len(df_clickstreams)
print(f"Anzahl der Zeilen: {rows_initial:,}")
print(f"Anzahl der Spalten: {len(df_clickstreams.columns)}")
print(f"\nSpalten: {list(df_clickstreams.columns)}")

# Speicherverbrauch
memory_usage = df_clickstreams.memory_usage(deep=True).sum() / 1024**2
print(f"\nSpeicherverbrauch: {memory_usage:.2f} MB")

# %%
df_clickstreams.head(25)

# %%
df_clickstreams.info()

# %%
# Grundlegende Statistiken für numerische Spalten
df_clickstreams.describe()

# %% [markdown]
# ## 2. Prüfung auf Duplikate

# %%
# Duplikate prüfen
num_duplicates = df_clickstreams.duplicated().sum()
print(f"Anzahl der Duplikate: {num_duplicates:,}")
print(f"Prozentsatz: {num_duplicates / rows_initial * 100:.2f}%")
print('-' * 60)

# Duplikate in separaten DataFrame speichern
df_duplicates = df_clickstreams[df_clickstreams.duplicated()]
print(f"Anzahl der Duplikate im separaten DataFrame: {len(df_duplicates):,}")

# Eindeutige Werte für session_action
print("\nEindeutige Werte in session_action:")
unique_action = df_duplicates['session_action'].value_counts(dropna=False)
print(unique_action)
print(f"Anzahl eindeutiger Werte: {df_duplicates['session_action'].nunique(dropna=False)}\n")
print(f"Prozentuale Verteilung:\n{(unique_action / len(df_duplicates) * 100).round(2)}")
print('-' * 60)

# Eindeutige Werte für session_action_type
print("\nEindeutige Werte in session_action_type:")
unique_action_type = df_duplicates['session_action_type'].value_counts(dropna=False)
print(unique_action_type)
print(f"Anzahl eindeutiger Werte: {df_duplicates['session_action_type'].nunique(dropna=False)}\n")
print(f"Prozentuale Verteilung:\n{(unique_action_type / len(df_duplicates) * 100).round(2)}")
print('-' * 60)

# Eindeutige Werte für session_action_detail
print("\nEindeutige Werte in session_action_detail:")
unique_action_detail = df_duplicates['session_action_detail'].value_counts(dropna=False)
print(unique_action_detail)
print(f"Anzahl eindeutiger Werte: {df_duplicates['session_action_detail'].nunique(dropna=False)}\n")
print(f"Prozentuale Verteilung:\n{(unique_action_detail / len(df_duplicates) * 100).round(2)}")
print('-' * 60)

# Statistiken für time_passed_in_seconds
print("\nStatistiken für time_passed_in_seconds:")
print(df_duplicates['time_passed_in_seconds'].describe())

# Anzahl eindeutiger session_user_id
# Duplikate aus df_clickstreams entfernen
df_clickstreams = df_clickstreams.drop_duplicates()

# df_duplicates löschen
del df_duplicates

print('-' * 60)
print('Duplikate entfernt.')


# %% [markdown]
# ## 3. Analyse fehlender Werte (vor Bereinigung)

# %%
# Fehlende Werte pro Spalte
missing_before = df_clickstreams.isnull().sum()
missing_pct = (missing_before / rows_initial * 100).round(2)

missing_df = pd.DataFrame({
    'Spalte': missing_before.index,
    'Fehlend': missing_before.values,
    'Prozent': missing_pct.values
})
missing_df = missing_df.sort_values('Fehlend', ascending=False)
display(missing_df)

# %% [markdown]
# ## 4. Analyse und Bereinigung von '-unknown-' Werten
#
# '-unknown-' ist ein Platzhalter für unbekannte Werte und sollte durch NaN ersetzt werden.

# %%
# Analyse von '-unknown-' Werten
text_cols = ['session_user_id', 'session_action_type', 'session_action_detail', 'session_device_type']

print("Anzahl der '-unknown-' Werte pro Spalte:\n")
for col in text_cols:
    count = (df_clickstreams[col] == '-unknown-').sum()
    pct = count / rows_initial * 100
    print(f"{col}: {count:,} ({pct:.2f}%)")

# %%
# Bereinigung: '-unknown-' durch NaN ersetzen
print("Bereinigung durchführen: '-unknown-' durch NaN ersetzen\n")

for col in text_cols:
    count_before = (df_clickstreams[col] == '-unknown-').sum()
    df_clickstreams[col] = df_clickstreams[col].replace('-unknown-', np.nan)
    print(f"{col}: {count_before:,} Werte ersetzt")

# %% [markdown]
# ## 5. Analyse der Spalten nach Bereinigung

# %%
# session_user_id
print("=== session_user_id ===")
print(f"Eindeutige Benutzer: {df_clickstreams['session_user_id'].nunique():,}")
print(f"Fehlende Werte: {df_clickstreams['session_user_id'].isna().sum():,}")

# %%
# session_action
print("=== session_action ===")
print(f"Eindeutige Werte: {df_clickstreams['session_action'].nunique()}")
print(f"Fehlende Werte: {df_clickstreams['session_action'].isna().sum():,}")
print("\nTop 10 häufigste Werte:")

counts = df_clickstreams['session_action'].value_counts().head(10)
for val, count in counts.items():
    pct = (count / len(df_clickstreams) * 100)
    print(f"'{val}' - {count:,} - {pct:.2f}%")

# %%
# session_action_type
print("=== session_action_type ===")
print(f"Eindeutige Werte: {df_clickstreams['session_action_type'].nunique()}")
print(f"Fehlende Werte: {df_clickstreams['session_action_type'].isna().sum():,}")
print("\nTop 10 häufigste Werte:")

counts = df_clickstreams['session_action_type'].value_counts().head(10)
for val, count in counts.items():
    pct = (count / len(df_clickstreams) * 100)
    print(f"'{val}' - {count:,} - {pct:.2f}%")

# %%
# session_action_detail
print("=== session_action_detail ===")
print(f"Eindeutige Werte: {df_clickstreams['session_action_detail'].nunique()}")
print(f"Fehlende Werte: {df_clickstreams['session_action_detail'].isna().sum():,}")
print("\nTop 10 häufigste Werte:")

counts = df_clickstreams['session_action_detail'].value_counts().head(10)
for val, count in counts.items():
    pct = (count / len(df_clickstreams) * 100)
    print(f"'{val}' - {count:,} - {pct:.2f}%")

# %%
# session_device_type
print("=== session_device_type ===")
print(f"Eindeutige Werte: {df_clickstreams['session_device_type'].nunique()}")
print(f"Fehlende Werte: {df_clickstreams['session_device_type'].isna().sum():,}")
print("\nTop 10 häufigste Werte:")

counts = df_clickstreams['session_device_type'].value_counts().head(10)
for val, count in counts.items():
    pct = (count / len(df_clickstreams) * 100)
    print(f"'{val}' - {count:,} - {pct:.2f}%")

# %% [markdown]
# # 6. Zeitanalyse

# %%
# time_passed_in_seconds
print("=== time_passed_in_seconds ===")
time_col = df_clickstreams['time_passed_in_seconds']
print(f"Fehlende Werte: {time_col.isna().sum():,}")
print(f"Min: {time_col.min()}")
print(f"Max: {time_col.max()}")
print(f"Mittelwert: {time_col.mean():.2f}")
print(f"Median: {time_col.median():.2f}")
print(f"Standardabweichung: {time_col.std():.2f}")

extreme_time = time_col > 1800  # > 30 Minuten
print(f"\nUnrealistische Werte (> 30 Minuten): {extreme_time.sum():,} ({(extreme_time.sum() / len(df_clickstreams) * 100):.2f}%)")

zero_time = time_col == 0 # = 0 Sekunden
print(f"Null-Werte (= 0 Sekunden): {zero_time.sum():,} ({(zero_time.sum() / len(df_clickstreams) * 100):.2f}%)")

# %% [markdown]
# Mehr als 30 Minuten Inaktivität innerhalb einer Sitzung sind ein unrealistischer Wert.
#
# Möglicherweise entstehen solche Werte, wenn ein Benutzer den Tab geöffnet lässt und weggeht, später zurückkehrt und die nächste Aktion ausführt. Es handelt sich dann eigentlich bereits um eine neue Sitzung.
#
# Daher fügen wir eine Spalte `is_new_session` hinzu, in der 1 steht, wenn `time_passed_in_seconds` größer als 30 Minuten ist, und 0, wenn sie kleiner ist.

# %%
df_clickstreams['is_new_session'] = extreme_time  # Markiere als neue Sitzung, wenn Zeit > 30 Minuten

# %%
# Detaillierte Analyse der Einträge mit time_passed_in_seconds == 0
df_zero_time = df_clickstreams[time_col == 0]

print("=== session_action ===")
print(f"Eindeutige Werte: {df_zero_time['session_action'].nunique()}")
print(f"Fehlende Werte: {df_zero_time['session_action'].isna().sum():,}")
print("\nTop 10 häufigste Werte:")

counts = df_zero_time['session_action'].value_counts().head(10)
for val, count in counts.items():
    pct = (count / len(df_zero_time) * 100)
    print(f"'{val}' - {count:,} - {pct:.2f}%")

print("\n=== session_action_type ===")
print(f"Eindeutige Werte: {df_zero_time['session_action_type'].nunique()}")
print(f"Fehlende Werte: {df_zero_time['session_action_type'].isna().sum():,}")
print("\nTop 10 häufigste Werte:")

counts = df_zero_time['session_action_type'].value_counts().head(10)
for val, count in counts.items():
    pct = (count / len(df_zero_time) * 100)
    print(f"'{val}' - {count:,} - {pct:.2f}%")

print("\n=== session_action_detail ===")
print(f"Eindeutige Werte: {df_zero_time['session_action_detail'].nunique()}")
print(f"Fehlende Werte: {df_zero_time['session_action_detail'].isna().sum():,}")
print("\nTop 10 häufigste Werte:")  

counts = df_zero_time['session_action_detail'].value_counts().head(10)
for val, count in counts.items():
    pct = (count / len(df_zero_time) * 100)
    print(f"'{val}' - {count:,} - {pct:.2f}%")

print("\n=== session_device_type ===")
print(f"Eindeutige Werte: {df_zero_time['session_device_type'].nunique()}")
print(f"Fehlende Werte: {df_zero_time['session_device_type'].isna().sum():,}")
print("\nTop 10 häufigste Werte:")  
counts = df_zero_time['session_device_type'].value_counts().head(10)
for val, count in counts.items():
    pct = (count / len(df_zero_time) * 100)
    print(f"'{val}' - {count:,} - {pct:.2f}%")

# %% [markdown]
# In `df_zero_time` wird eine Verteilung der Werte beobachtet, die sich vom `df_clickstreams` unterscheidet:
#
# - `session_action`:
#     - 'pending': 7.54%, in `df_clickstreams` nicht in den Top-15;
# - `session_action_type`:
#     - 'message_post': 8.36%, in `df_clickstreams`: 0.82%;
#     - 'booking_request': 7.52%, in `df_clickstreams`: 0.18%;
# - `session_action_detail`:
#     - 'message_post': 8.36%, in `df_clickstreams` nicht in den Top-15;
#     - 'pending': 7.52%, in `df_clickstreams` nicht in den Top-15;
#
# Möglicherweise sind solche Zeilen automatische Einträge, die unmittelbar nach irgendwelcher anderen Aktion entstehen. 
# Zum Beispiel gibt es insgesamt 4.333 Zeilen mit `session_action_type=booking_request` und `time_passed_in_seconds=0`, was einen erheblichen Anteil aller 18.773 Buchungen ausmacht. Daher wurde entschieden, die Zeilen mit `time_passed_in_seconds=0` zu behalten.

# %% [markdown]
# ## 7. Fehlende Werte nach Bereinigung

# %%
# Fehlende Werte nach Bereinigung
missing_after = df_clickstreams.isnull().sum()
missing_pct_after = (missing_after / rows_initial * 100).round(2)

missing_df_after = pd.DataFrame({
    'Spalte': missing_after.index,
    'Fehlend': missing_after.values,
    'Prozent': missing_pct_after.values
})
missing_df_after = missing_df_after.sort_values('Fehlend', ascending=False)
missing_df_after

# %%
# Löschen der Zeilen mit fehlenden session_user_id, session_action und time_passed_in_seconds
df_clickstreams = df_clickstreams.dropna(subset=['session_user_id', 'session_action', 'time_passed_in_seconds'])

del missing_df_after

# %% [markdown]
# ## 7. Visualisierung fehlender Werte mit missingno

# %%
# Matrix-Plot
msno.matrix(df_clickstreams, sparkline=False, figsize=(12, 6))
plt.title('Matrix fehlender Werte in clickstreams.parquet', fontsize=14, pad=20)
plt.tight_layout()
plt.show()

# %%
# Bar-Plot
msno.bar(df_clickstreams, figsize=(12, 6))
plt.title('Vollständigkeit der Daten pro Spalte', fontsize=14, pad=20)
plt.tight_layout()
plt.show()

# %%
# Heatmap-Plot
msno.heatmap(df_clickstreams, figsize=(12, 8))
plt.title('Korrelation fehlender Werte', fontsize=14, pad=20)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 8. Zusammenfassung

# %%
print(f"Ursprüngliche Anzahl der Zeilen: {rows_initial:,}")
print(f"Finale Anzahl der Zeilen: {len(df_clickstreams):,}")
print(f"Entfernte Zeilen gesamt: {rows_initial - len(df_clickstreams)} ({((rows_initial - len(df_clickstreams)) / rows_initial * 100):.2f}%)")
print(f"Anzahl der Spalten: {len(df_clickstreams.columns)}")

print("\nDurchgeführte Bereinigungen:")
print("1. Duplikate entfernt;")
print("2. `-unknown-` in `session_action_type`, `session_action_detail` und `session_device_type` durch NaN ersetzt;")
print("3. Zeilen mit fehlenden `session_user_id`, `session_action` und `time_passed_in_seconds` entfernt.")

# %%
# Export der bereinigten Daten
df_clickstreams.to_parquet('data/clickstreams_filtered.parquet', index=False)
print("Bereinigte Daten erfolgreich in 'data/clickstreams_filtered.parquet' exportiert")

