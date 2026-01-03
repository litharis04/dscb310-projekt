"""
Skript zur Datenbereinigung von user.csv

Dieses Skript führt eine systematische Datenbereinigung durch:
1. Laden und allgemeine Inspektion
2. Duplikatsprüfung und -entfernung
3. Datumskonvertierung
4. Datumsreihenfolge-Validierung
5. user_gender-Bereinigung
6. Altersfilterung
7. Analyse eindeutiger Werte
8. Abhängigkeitsprüfung first_booking_date ↔ destination_country
9. Analyse fehlender Werte

Eingabe: data/user.csv
Ausgabe: scripts/outputs/datenbereinigung_bericht.md
"""

import pandas as pd
import numpy as np
import os

# Ausgabeverzeichnis erstellen
os.makedirs('scripts/outputs', exist_ok=True)

# Ausgabedatei öffnen
output_file = 'scripts/outputs/datenbereinigung_bericht.md'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("# Datenbereinigung: user.csv\n\n")
    f.write("=" * 80 + "\n\n")
    
    # 1. Daten laden und Inspektion
    f.write("## 1. Daten laden und allgemeine Inspektion\n\n")
    df_user = pd.read_csv('data/user.csv')
    
    rows_initial = len(df_user)
    cols_count = len(df_user.columns)
    
    f.write(f"- **Anzahl Zeilen**: {rows_initial}\n")
    f.write(f"- **Anzahl Spalten**: {cols_count}\n")
    f.write(f"- **Spalten**: {', '.join(df_user.columns)}\n\n")
    
    # Datentypen
    f.write("### Datentypen:\n\n")
    for col, dtype in df_user.dtypes.items():
        f.write(f"- `{col}`: {dtype}\n")
    f.write("\n")
    
    # 2. Duplikatsprüfung
    f.write("## 2. Duplikatsprüfung\n\n")
    num_duplicates = df_user.duplicated().sum()
    f.write(f"- **Anzahl Duplikate**: {num_duplicates}\n")
    
    if num_duplicates > 0:
        f.write(f"- **Aktion**: Duplikate werden entfernt\n")
        df_user = df_user.drop_duplicates()
        f.write(f"- **Neue Zeilenanzahl**: {len(df_user)}\n")
    else:
        f.write(f"- ✓ Keine Duplikate gefunden\n")
    f.write("\n")
    
    rows_after_duplicates = len(df_user)
    
    # 3. Datumskonvertierung
    f.write("## 3. Datumskonvertierung\n\n")
    
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
    
    f.write("- `first_active_timestamp` → datetime + neues Feld `first_active_date` (normalisiert)\n")
    f.write("- `account_created_date` → datetime\n")
    f.write("- `first_booking_date` → datetime\n\n")
    
    f.write("### Datumsbereiche:\n\n")
    f.write(f"- **first_active_timestamp**: {df_user['first_active_timestamp'].min()} bis {df_user['first_active_timestamp'].max()}\n")
    f.write(f"- **first_active_date**: {df_user['first_active_date'].min()} bis {df_user['first_active_date'].max()}\n")
    f.write(f"- **account_created_date**: {df_user['account_created_date'].min()} bis {df_user['account_created_date'].max()}\n")
    f.write(f"- **first_booking_date**: {df_user['first_booking_date'].min()} bis {df_user['first_booking_date'].max()}\n\n")
    
    # 4. Datumsreihenfolge prüfen
    f.write("## 4. Datumsreihenfolge-Validierung\n\n")
    f.write("Korrekte Reihenfolge: first_active_date ≤ account_created_date ≤ first_booking_date\n\n")
    
    rows_before_date_check = len(df_user)
    
    # Fehler 1: first_active_date > account_created_date
    error1 = (df_user['first_active_date'].notna()) & \
             (df_user['account_created_date'].notna()) & \
             (df_user['first_active_date'] > df_user['account_created_date'])
    
    # Fehler 2: account_created_date > first_booking_date
    error2 = (df_user['account_created_date'].notna()) & \
             (df_user['first_booking_date'].notna()) & \
             (df_user['account_created_date'] > df_user['first_booking_date'])
    
    date_errors = error1 | error2
    num_date_errors = date_errors.sum()
    
    f.write(f"- **Fehler gefunden**: {num_date_errors}\n")
    f.write(f"  - first_active_date > account_created_date: {error1.sum()}\n")
    f.write(f"  - account_created_date > first_booking_date: {error2.sum()}\n")
    
    if num_date_errors > 0:
        f.write(f"- **Aktion**: Fehlerhafte Zeilen werden entfernt\n")
        df_user = df_user[~date_errors]
        f.write(f"- **Neue Zeilenanzahl**: {len(df_user)}\n")
    else:
        f.write(f"- ✓ Keine Fehler gefunden\n")
    f.write("\n")
    
    rows_after_date_check = len(df_user)
    
    # 5. user_gender Bereinigung
    f.write("## 5. user_gender Bereinigung\n\n")
    
    f.write("### Ursprüngliche Werte:\n\n")
    original_gender_counts = df_user['user_gender'].value_counts(dropna=False)
    for value, count in original_gender_counts.items():
        f.write(f"- `{value}`: {count}\n")
    f.write("\n")
    
    f.write("### Zulässige Werte: 'female', 'male', 'other', NaN\n\n")
    
    # Normalisierung: Groß-/Kleinschreibung
    df_user['user_gender'] = df_user['user_gender'].str.lower()
    
    # Ungültige Werte auf NaN setzen
    rows_before_gender = len(df_user)
    invalid_gender = ~df_user['user_gender'].isin(['female', 'male', 'other']) & df_user['user_gender'].notna()
    num_invalid_gender = invalid_gender.sum()
    
    f.write(f"- **Ungültige Werte gefunden**: {num_invalid_gender}\n")
    
    if num_invalid_gender > 0:
        f.write(f"- **Aktion**: Ungültige Werte werden auf NaN gesetzt\n")
        df_user.loc[~df_user['user_gender'].isin(['female', 'male', 'other']), 'user_gender'] = np.nan
    
    f.write("\n### Bereinigte Werte:\n\n")
    cleaned_gender_counts = df_user['user_gender'].value_counts(dropna=False)
    for value, count in cleaned_gender_counts.items():
        f.write(f"- `{value}`: {count}\n")
    f.write("\n")
    
    # 6. Altersfilterung
    f.write("## 6. Altersfilterung\n\n")
    f.write("Gültige Werte: 18 ≤ user_age ≤ 90\n\n")
    
    rows_before_age = len(df_user)
    
    f.write("### Altersstatistik vor Filterung:\n\n")
    f.write(f"- **Minimum**: {df_user['user_age'].min():.2f}\n")
    f.write(f"- **Maximum**: {df_user['user_age'].max():.2f}\n")
    f.write(f"- **Durchschnitt**: {df_user['user_age'].mean():.2f}\n")
    f.write(f"- **Median**: {df_user['user_age'].median():.2f}\n\n")
    
    age_too_young = df_user['user_age'] < 18
    age_too_old = df_user['user_age'] > 90
    invalid_age = age_too_young | age_too_old
    num_invalid_age = invalid_age.sum()
    
    f.write(f"- **Ungültige Altersangaben**: {num_invalid_age}\n")
    f.write(f"  - Alter < 18: {age_too_young.sum()}\n")
    f.write(f"  - Alter > 90: {age_too_old.sum()}\n")
    
    if num_invalid_age > 0:
        f.write(f"- **Aktion**: Zeilen mit ungültigem Alter werden entfernt\n")
        df_user = df_user[~invalid_age]
        f.write(f"- **Neue Zeilenanzahl**: {len(df_user)}\n")
    else:
        f.write(f"- ✓ Keine ungültigen Altersangaben gefunden\n")
    f.write("\n")
    
    rows_after_age = len(df_user)
    
    f.write("### Altersstatistik nach Filterung:\n\n")
    f.write(f"- **Minimum**: {df_user['user_age'].min():.2f}\n")
    f.write(f"- **Maximum**: {df_user['user_age'].max():.2f}\n")
    f.write(f"- **Durchschnitt**: {df_user['user_age'].mean():.2f}\n")
    f.write(f"- **Median**: {df_user['user_age'].median():.2f}\n\n")
    
    # 7. Analyse eindeutiger Werte
    f.write("## 7. Analyse eindeutiger Werte in Textspalten\n\n")
    f.write("Prüfung auf seltene Werte (< 10 Vorkommen) als mögliche Tippfehler\n\n")
    
    text_columns = [
        'user_gender', 'signup_platform', 'signup_process', 'user_language',
        'marketing_channel', 'marketing_provider', 'first_tracked_affiliate',
        'signup_application', 'first_device', 'first_web_browser', 'destination_country'
    ]
    
    for col in text_columns:
        value_counts = df_user[col].value_counts(dropna=False)
        rare_values = value_counts[value_counts < 10]
        
        f.write(f"### {col}\n\n")
        f.write(f"- **Anzahl eindeutiger Werte**: {len(value_counts)}\n")
        f.write(f"- **Seltene Werte (< 10)**: {len(rare_values)}\n\n")
        
        if len(rare_values) > 0:
            f.write("**Seltene Werte:**\n\n")
            for value, count in rare_values.head(15).items():
                f.write(f"- `{value}`: {count}\n")
            f.write("\n")
        
        f.write("**Top 10 häufigste Werte:**\n\n")
        for value, count in value_counts.head(10).items():
            percentage = (count / len(df_user)) * 100
            f.write(f"- `{value}`: {count} ({percentage:.2f}%)\n")
        f.write("\n")
    
    # 8. Abhängigkeitsprüfung
    f.write("## 8. Abhängigkeitsprüfung: first_booking_date ↔ destination_country\n\n")
    f.write("Erwartete Konsistenz:\n")
    f.write("- first_booking_date = NaN → destination_country = 'NDF'\n")
    f.write("- destination_country = 'NDF' → first_booking_date = NaN\n\n")
    
    # Fall 1: Keine Buchung, aber destination != NDF
    no_booking_but_dest = (df_user['first_booking_date'].isna()) & \
                          (df_user['destination_country'] != 'NDF')
    num_case1 = no_booking_but_dest.sum()
    
    # Fall 2: Buchung vorhanden, aber destination = NDF
    booking_but_ndf = (df_user['first_booking_date'].notna()) & \
                      (df_user['destination_country'] == 'NDF')
    num_case2 = booking_but_ndf.sum()
    
    f.write(f"### Inkonsistenzen:\n\n")
    f.write(f"- **Keine Buchung, aber destination != 'NDF'**: {num_case1}\n")
    f.write(f"- **Buchung vorhanden, aber destination = 'NDF'**: {num_case2}\n\n")
    
    total_inconsistencies = num_case1 + num_case2
    
    if total_inconsistencies == 0:
        f.write("✓ **Keine Inkonsistenzen gefunden - Daten sind konsistent**\n\n")
    else:
        f.write(f"❌ **Insgesamt {total_inconsistencies} inkonsistente Zeilen gefunden**\n\n")
    
    # Statistik
    no_booking_total = df_user['first_booking_date'].isna().sum()
    ndf_total = (df_user['destination_country'] == 'NDF').sum()
    
    f.write("### Statistik:\n\n")
    f.write(f"- **Zeilen ohne Buchungsdatum**: {no_booking_total}\n")
    f.write(f"- **Zeilen mit destination_country = 'NDF'**: {ndf_total}\n\n")
    
    # 9. Fehlende Werte
    f.write("## 9. Analyse fehlender Werte\n\n")
    
    missing_values = df_user.isnull().sum()
    missing_percent = (missing_values / len(df_user)) * 100
    
    f.write("### Fehlende Werte pro Spalte:\n\n")
    f.write("| Spalte | Anzahl fehlend | Prozent |\n")
    f.write("|--------|----------------|----------|\n")
    
    for col in df_user.columns:
        if missing_values[col] > 0:
            f.write(f"| {col} | {missing_values[col]} | {missing_percent[col]:.2f}% |\n")
    
    if missing_values.sum() == 0:
        f.write("\n✓ **Keine fehlenden Werte**\n")
    
    f.write("\n")
    
    # Zusammenfassung
    f.write("## Zusammenfassung\n\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("### Datenstatistik:\n\n")
    f.write(f"- **Ursprüngliche Zeilen**: {rows_initial}\n")
    f.write(f"- **Nach Duplikatsentfernung**: {rows_after_duplicates}\n")
    f.write(f"- **Nach Datumsvalidierung**: {rows_after_date_check}\n")
    f.write(f"- **Nach Altersfilterung**: {rows_after_age}\n")
    f.write(f"- **Finale Zeilenanzahl**: {len(df_user)}\n")
    f.write(f"- **Entfernte Zeilen gesamt**: {rows_initial - len(df_user)} ({((rows_initial - len(df_user)) / rows_initial * 100):.2f}%)\n\n")
    
    f.write("### Durchgeführte Bereinigungen:\n\n")
    f.write(f"1. Duplikate entfernt: {num_duplicates}\n")
    f.write(f"2. Datumsreihenfolgefehler entfernt: {num_date_errors}\n")
    f.write(f"3. user_gender normalisiert: {num_invalid_gender} Werte korrigiert\n")
    f.write(f"4. Ungültige Altersangaben entfernt: {num_invalid_age}\n")
    f.write(f"5. Abhängigkeitsprüfung: {total_inconsistencies} Inkonsistenzen gefunden\n\n")
    
    f.write("=" * 80 + "\n")

print(f"Analyse abgeschlossen. Bericht gespeichert unter: {output_file}")
print(f"\nFinale Statistik:")
print(f"  - Ursprüngliche Zeilen: {rows_initial}")
print(f"  - Finale Zeilen: {len(df_user)}")
print(f"  - Entfernte Zeilen: {rows_initial - len(df_user)} ({((rows_initial - len(df_user)) / rows_initial * 100):.2f}%)")
