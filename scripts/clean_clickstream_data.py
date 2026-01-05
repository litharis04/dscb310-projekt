# Skript zur Datenbereinigung und Fehleranalyse von clickstreams.parquet
# Dieses Skript führt eine systematische Analyse und Bereinigung der Clickstream-Daten durch.
#
# Eingabedaten: data/clickstreams.parquet
# Ausgaben:
# - scripts/outputs/clickstreams_bereinigung_bericht.md (Analysebericht)
# - data/clickstreams-filtered.parquet (bereinigte Daten)

import numpy as np
import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt
import os

# Sicherstellen, dass der Output-Ordner existiert
os.makedirs('scripts/outputs', exist_ok=True)

# Ausgabedatei
output_file = 'scripts/outputs/clickstreams_bereinigung_bericht.md'

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("# Datenbereinigung und Fehleranalyse: clickstreams.parquet\n\n")
    
    # 1. Daten laden und allgemeine Inspektion
    f.write("## 1. Daten laden und allgemeine Inspektion\n\n")
    df_clickstreams = pd.read_parquet('data/clickstreams.parquet')
    rows_initial = len(df_clickstreams)
    
    f.write(f"- **Anzahl der Zeilen**: {rows_initial:,}\n")
    f.write(f"- **Anzahl der Spalten**: {len(df_clickstreams.columns)}\n")
    f.write(f"- **Spalten**: {list(df_clickstreams.columns)}\n\n")
    
    # Speicherverbrauch
    memory_usage = df_clickstreams.memory_usage(deep=True).sum() / 1024**2
    f.write(f"- **Speicherverbrauch**: {memory_usage:.2f} MB\n\n")
    
    # Datentypen
    f.write("### Datentypen\n\n")
    f.write("| Spalte | Datentyp |\n")
    f.write("|--------|----------|\n")
    for col, dtype in df_clickstreams.dtypes.items():
        f.write(f"| {col} | {dtype} |\n")
    f.write("\n")
    
    # 2. Prüfung auf Duplikate
    f.write("## 2. Prüfung auf Duplikate\n\n")
    num_duplicates = df_clickstreams.duplicated().sum()
    f.write(f"- **Anzahl der Duplikate**: {num_duplicates:,}\n")
    
    if num_duplicates > 0:
        f.write(f"- **Prozentsatz**: {num_duplicates / rows_initial * 100:.2f}%\n\n")
        f.write("⚠️ **Hinweis**: Duplikate werden beibehalten, da sie legitime wiederholte Aktionen sein könnten.\n")
        f.write("Falls gewünscht, können Duplikate in einer späteren Analyse entfernt werden.\n\n")
    else:
        f.write("✅ Keine Duplikate gefunden.\n\n")
    
    # 3. Analyse fehlender Werte
    f.write("## 3. Analyse fehlender Werte (vor Bereinigung)\n\n")
    missing_before = df_clickstreams.isnull().sum()
    missing_pct = (missing_before / rows_initial * 100).round(2)
    
    f.write("| Spalte | Fehlend | Prozent |\n")
    f.write("|--------|---------|--------|\n")
    for col in df_clickstreams.columns:
        f.write(f"| {col} | {missing_before[col]:,} | {missing_pct[col]}% |\n")
    f.write("\n")
    
    f.write("ℹ️ **Hinweis zu NaN-Werten in session_action_type und session_action_detail:**\n")
    f.write("Diese leeren Werte (None/NaN) sind **legitim** und repräsentieren technische Anfragen an die Website.\n")
    f.write("Sie werden nicht als Fehler betrachtet und bleiben unverändert.\n\n")
    
    # 4. Analyse von '-unknown-' Werten
    f.write("## 4. Analyse von '-unknown-' Werten\n\n")
    f.write("'-unknown-' ist ein Platzhalter für unbekannte Werte und sollte durch NaN ersetzt werden.\n\n")
    
    text_cols = ['session_action_type', 'session_action_detail', 'session_device_type']
    unknown_counts = {}
    
    f.write("| Spalte | '-unknown-' Anzahl | Prozent |\n")
    f.write("|--------|-------------------|--------|\n")
    for col in text_cols:
        count = (df_clickstreams[col] == '-unknown-').sum()
        pct = count / rows_initial * 100
        unknown_counts[col] = count
        f.write(f"| {col} | {count:,} | {pct:.2f}% |\n")
    f.write("\n")
    
    # Korrelation von -unknown- Werten
    f.write("### Korrelation von '-unknown-' Werten\n\n")
    unk_type = (df_clickstreams['session_action_type'] == '-unknown-')
    unk_detail = (df_clickstreams['session_action_detail'] == '-unknown-')
    unk_device = (df_clickstreams['session_device_type'] == '-unknown-')
    
    f.write(f"- session_action_type UND session_action_detail sind '-unknown-': {(unk_type & unk_detail).sum():,}\n")
    f.write(f"- NUR session_action_type ist '-unknown-': {(unk_type & ~unk_detail).sum():,}\n")
    f.write(f"- NUR session_action_detail ist '-unknown-': {(~unk_type & unk_detail).sum():,}\n")
    f.write(f"- session_device_type ist '-unknown-': {unk_device.sum():,}\n\n")
    
    # 5. Bereinigung: '-unknown-' durch NaN ersetzen
    f.write("## 5. Bereinigung durchführen\n\n")
    f.write("### 5.1 '-unknown-' durch NaN ersetzen\n\n")
    
    for col in text_cols:
        count_before = (df_clickstreams[col] == '-unknown-').sum()
        df_clickstreams[col] = df_clickstreams[col].replace('-unknown-', np.nan)
        count_after = (df_clickstreams[col] == '-unknown-').sum()
        f.write(f"- **{col}**: {count_before:,} Werte ersetzt\n")
    f.write("\n")
    
    # 6. Analyse der Spalten nach Bereinigung
    f.write("## 6. Analyse der Spalten nach Bereinigung\n\n")
    
    # session_action
    f.write("### session_action\n\n")
    f.write(f"- **Eindeutige Werte**: {df_clickstreams['session_action'].nunique()}\n")
    f.write(f"- **Fehlende Werte**: {df_clickstreams['session_action'].isna().sum():,}\n\n")
    
    f.write("**Top 10 häufigste Werte:**\n\n")
    action_counts = df_clickstreams['session_action'].value_counts().head(10)
    f.write("| Aktion | Anzahl | Prozent |\n")
    f.write("|--------|--------|--------|\n")
    for val, count in action_counts.items():
        pct = count / rows_initial * 100
        f.write(f"| {val} | {count:,} | {pct:.2f}% |\n")
    f.write("\n")
    
    # session_action_type
    f.write("### session_action_type\n\n")
    f.write(f"- **Eindeutige Werte**: {df_clickstreams['session_action_type'].nunique()}\n")
    f.write(f"- **Fehlende Werte**: {df_clickstreams['session_action_type'].isna().sum():,}\n\n")
    
    type_counts = df_clickstreams['session_action_type'].value_counts(dropna=False)
    f.write("| Typ | Anzahl | Prozent |\n")
    f.write("|-----|--------|--------|\n")
    for val, count in type_counts.items():
        pct = count / rows_initial * 100
        val_str = str(val) if val is not None else "NaN"
        f.write(f"| {val_str} | {count:,} | {pct:.2f}% |\n")
    f.write("\n")
    
    # session_action_detail
    f.write("### session_action_detail\n\n")
    f.write(f"- **Eindeutige Werte**: {df_clickstreams['session_action_detail'].nunique()}\n")
    f.write(f"- **Fehlende Werte**: {df_clickstreams['session_action_detail'].isna().sum():,}\n\n")
    
    detail_counts = df_clickstreams['session_action_detail'].value_counts().head(10)
    f.write("**Top 10 häufigste Werte:**\n\n")
    f.write("| Detail | Anzahl | Prozent |\n")
    f.write("|--------|--------|--------|\n")
    for val, count in detail_counts.items():
        pct = count / rows_initial * 100
        f.write(f"| {val} | {count:,} | {pct:.2f}% |\n")
    f.write("\n")
    
    # session_device_type
    f.write("### session_device_type\n\n")
    f.write(f"- **Eindeutige Werte**: {df_clickstreams['session_device_type'].nunique()}\n")
    f.write(f"- **Fehlende Werte**: {df_clickstreams['session_device_type'].isna().sum():,}\n\n")
    
    device_counts = df_clickstreams['session_device_type'].value_counts(dropna=False)
    f.write("| Gerät | Anzahl | Prozent |\n")
    f.write("|-------|--------|--------|\n")
    for val, count in device_counts.items():
        pct = count / rows_initial * 100
        val_str = str(val) if val is not None else "NaN"
        f.write(f"| {val_str} | {count:,} | {pct:.2f}% |\n")
    f.write("\n")
    
    # time_passed_in_seconds
    f.write("### time_passed_in_seconds\n\n")
    time_col = df_clickstreams['time_passed_in_seconds']
    f.write(f"- **Fehlende Werte**: {time_col.isna().sum():,}\n")
    f.write(f"- **Min**: {time_col.min()}\n")
    f.write(f"- **Max**: {time_col.max()}\n")
    f.write(f"- **Mittelwert**: {time_col.mean():.2f}\n")
    f.write(f"- **Median**: {time_col.median():.2f}\n")
    f.write(f"- **Standardabweichung**: {time_col.std():.2f}\n\n")
    
    # Extreme Werte
    extreme_time = time_col > 1000000  # > 11 Tage
    f.write(f"⚠️ **Extreme Werte (> 1.000.000 Sekunden / 11+ Tage)**: {extreme_time.sum():,}\n\n")
    
    # session_user_id
    f.write("### session_user_id\n\n")
    f.write(f"- **Eindeutige Benutzer**: {df_clickstreams['session_user_id'].nunique():,}\n")
    f.write(f"- **Fehlende Werte**: {df_clickstreams['session_user_id'].isna().sum():,}\n\n")
    
    # 7. Fehlende Werte nach Bereinigung
    f.write("## 7. Fehlende Werte nach Bereinigung\n\n")
    missing_after = df_clickstreams.isnull().sum()
    missing_pct_after = (missing_after / rows_initial * 100).round(2)
    
    f.write("| Spalte | Fehlend | Prozent |\n")
    f.write("|--------|---------|--------|\n")
    for col in df_clickstreams.columns:
        f.write(f"| {col} | {missing_after[col]:,} | {missing_pct_after[col]}% |\n")
    f.write("\n")
    
    # 8. Zusammenfassung
    f.write("## 8. Zusammenfassung\n\n")
    f.write(f"- **Ursprüngliche Anzahl der Zeilen**: {rows_initial:,}\n")
    f.write(f"- **Finale Anzahl der Zeilen**: {len(df_clickstreams):,}\n")
    f.write(f"- **Anzahl der Spalten**: {len(df_clickstreams.columns)}\n\n")
    
    f.write("### Durchgeführte Bereinigungen:\n\n")
    f.write("1. ✅ '-unknown-' in session_action_type durch NaN ersetzt\n")
    f.write("2. ✅ '-unknown-' in session_action_detail durch NaN ersetzt\n")
    f.write("3. ✅ '-unknown-' in session_device_type durch NaN ersetzt\n\n")
    
    f.write("### Legitime NaN-Werte (keine Bereinigung notwendig):\n\n")
    f.write("- NaN in session_action_type und session_action_detail: Technische Anfragen\n")
    f.write("- Diese Werte wurden **nicht** als Fehler behandelt\n\n")
    
    f.write("### Hinweise für weitere Analyse:\n\n")
    f.write("- Duplikate wurden beibehalten (könnten legitime wiederholte Aktionen sein)\n")
    f.write("- Extreme Zeitwerte wurden beibehalten (zur weiteren Untersuchung)\n")
    f.write("- Fehlende session_user_id könnten auf anonyme Sitzungen hinweisen\n")
    f.write("- Fehlende session_action könnten auf unvollständige Protokollierung hinweisen\n\n")

print("Bericht erstellt: scripts/outputs/clickstreams_bereinigung_bericht.md")

# 9. Visualisierung fehlender Werte mit missingno
print("Erstelle Visualisierungen...")

# Matrix-Plot
fig, ax = plt.subplots(figsize=(12, 6))
msno.matrix(df_clickstreams, ax=ax, sparkline=False)
ax.set_title('Matrix fehlender Werte in clickstreams.parquet', fontsize=14, pad=20)
plt.tight_layout()
plt.savefig('scripts/outputs/clickstreams_missing_matrix.png', dpi=150)
plt.close()
print("Matrix-Plot erstellt: scripts/outputs/clickstreams_missing_matrix.png")

# Bar-Plot
fig, ax = plt.subplots(figsize=(12, 6))
msno.bar(df_clickstreams, ax=ax)
ax.set_title('Vollständigkeit der Daten pro Spalte', fontsize=14, pad=20)
plt.tight_layout()
plt.savefig('scripts/outputs/clickstreams_missing_bar.png', dpi=150)
plt.close()
print("Bar-Plot erstellt: scripts/outputs/clickstreams_missing_bar.png")

# 10. Bereinigte Daten speichern
df_clickstreams.to_parquet('data/clickstreams-filtered.parquet', index=False)
print(f"Bereinigte Daten gespeichert: data/clickstreams-filtered.parquet")

print("\nDatenbereinigung abgeschlossen!")
