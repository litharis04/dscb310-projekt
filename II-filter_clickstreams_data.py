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

print("\n⚠️ Hinweis: Duplikate werden beibehalten, da sie legitime wiederholte Aktionen sein könnten.")

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

print("\nℹ️ Hinweis zu NaN-Werten in session_action_type und session_action_detail:")
print("Diese leeren Werte (None/NaN) sind LEGITIM und repräsentieren technische Anfragen an die Website.")
print("Sie werden nicht als Fehler betrachtet und bleiben unverändert.")

# %% [markdown]
# ## 4. Analyse und Bereinigung von '-unknown-' Werten
#
# '-unknown-' ist ein Platzhalter für unbekannte Werte und sollte durch NaN ersetzt werden.

# %%
# Analyse von '-unknown-' Werten
text_cols = ['session_action_type', 'session_action_detail', 'session_device_type']

print("Anzahl der '-unknown-' Werte pro Spalte:\n")
for col in text_cols:
    count = (df_clickstreams[col] == '-unknown-').sum()
    pct = count / rows_initial * 100
    print(f"{col}: {count:,} ({pct:.2f}%)")

# %%
# Korrelation von '-unknown-' Werten
unk_type = (df_clickstreams['session_action_type'] == '-unknown-')
unk_detail = (df_clickstreams['session_action_detail'] == '-unknown-')
unk_device = (df_clickstreams['session_device_type'] == '-unknown-')

print("Korrelation von '-unknown-' Werten:\n")
print(f"session_action_type UND session_action_detail sind '-unknown-': {(unk_type & unk_detail).sum():,}")
print(f"NUR session_action_type ist '-unknown-': {(unk_type & ~unk_detail).sum():,}")
print(f"NUR session_action_detail ist '-unknown-': {(~unk_type & unk_detail).sum():,}")
print(f"session_device_type ist '-unknown-': {unk_device.sum():,}")

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
df_clickstreams['session_action'].value_counts().head(10)

# %%
# session_action_type
print("=== session_action_type ===")
print(f"Eindeutige Werte: {df_clickstreams['session_action_type'].nunique()}")
print(f"Fehlende Werte: {df_clickstreams['session_action_type'].isna().sum():,}")
print("\nWertverteilung:")
df_clickstreams['session_action_type'].value_counts(dropna=False)

# %%
# session_action_detail
print("=== session_action_detail ===")
print(f"Eindeutige Werte: {df_clickstreams['session_action_detail'].nunique()}")
print(f"Fehlende Werte: {df_clickstreams['session_action_detail'].isna().sum():,}")
print("\nTop 10 häufigste Werte:")
df_clickstreams['session_action_detail'].value_counts().head(10)

# %%
# session_device_type
print("=== session_device_type ===")
print(f"Eindeutige Werte: {df_clickstreams['session_device_type'].nunique()}")
print(f"Fehlende Werte: {df_clickstreams['session_device_type'].isna().sum():,}")
print("\nWertverteilung:")
df_clickstreams['session_device_type'].value_counts(dropna=False)

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

extreme_time = time_col > 1000000  # > 11 Tage
print(f"\n⚠️ Extreme Werte (> 1.000.000 Sekunden / 11+ Tage): {extreme_time.sum():,}")

# %% [markdown]
# ## 6. Fehlende Werte nach Bereinigung

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
display(missing_df_after)

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

# %% [markdown]
# ## 8. Zusammenfassung

# %%
print(f"Ursprüngliche Anzahl der Zeilen: {rows_initial:,}")
print(f"Finale Anzahl der Zeilen: {len(df_clickstreams):,}")
print(f"Anzahl der Spalten: {len(df_clickstreams.columns)}")

print("\nDurchgeführte Bereinigungen:")
print("1. ✅ '-unknown-' in session_action_type durch NaN ersetzt")
print("2. ✅ '-unknown-' in session_action_detail durch NaN ersetzt")
print("3. ✅ '-unknown-' in session_device_type durch NaN ersetzt")

print("\nLegitime NaN-Werte (keine Bereinigung notwendig):")
print("- NaN in session_action_type und session_action_detail: Technische Anfragen")

print("\nDatentypen:")
df_clickstreams.info()

# %%
# Export der bereinigten Daten
df_clickstreams.to_parquet('data/clickstreams-filtered.parquet', index=False)
print("Bereinigte Daten erfolgreich in 'data/clickstreams-filtered.parquet' exportiert")

