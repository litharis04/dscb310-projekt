"""
Skript zur Fehlersuche in der Datei user.csv.

Dieses Skript analysiert user.csv auf verschiedene Datenqualitätsprobleme:
- Unmögliche/unrealistische Datenwerte (Alter, Datumsangaben)
- Falsche Datumsreihenfolge
- Inkonsistenzen zwischen first_booking_date und destination_country
- Tippfehler in Textspalten
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Daten laden
print("Lade user.csv...")
df_user = pd.read_csv('/home/runner/work/dscb310-projekt/dscb310-projekt/data/user.csv')

print(f"Gesamtzahl der Zeilen: {len(df_user)}")
print(f"Gesamtzahl der Spalten: {len(df_user.columns)}")
print(f"\nSpalten: {list(df_user.columns)}")

# Ausgabedatei öffnen (Markdown-Format)
output_file = '/home/runner/work/dscb310-projekt/dscb310-projekt/scripts/outputs/user_csv_fehler_bericht.md'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("# Fehleranalyse-Bericht für user.csv\n\n")
    f.write("=" * 80 + "\n\n")
    
    # 1. Altersanalyse
    f.write("## 1. Altersanalyse (user_age)\n\n")
    f.write("### Altersstatistik:\n\n")
    f.write(f"- **Minimalalter:** {df_user['user_age'].min()}\n")
    f.write(f"- **Maximalalter:** {df_user['user_age'].max()}\n")
    f.write(f"- **Durchschnittsalter:** {df_user['user_age'].mean():.2f}\n")
    f.write(f"- **Medianalter:** {df_user['user_age'].median()}\n\n")
    
    # Unrealistische Altersangaben prüfen (< 18 oder > 90)
    unrealistic_ages = df_user[(df_user['user_age'] < 18) | (df_user['user_age'] > 90)]
    f.write(f"### Benutzer mit unrealistischem Alter (< 18 oder > 90): **{len(unrealistic_ages)}**\n\n")
    if len(unrealistic_ages) > 0:
        f.write(f"Beispiele:\n\n")
        for idx, row in unrealistic_ages.head(10).iterrows():
            f.write(f"- user_id: `{row['user_id']}`, Alter: {row['user_age']}\n")
    f.write("\n")
    
    # Alter > 80 prüfen
    age_over_80 = df_user[df_user['user_age'] > 80]
    f.write(f"### Benutzer mit Alter > 80: **{len(age_over_80)}**\n\n")
    if len(age_over_80) > 0:
        f.write(f"Beispiele:\n\n")
        for idx, row in age_over_80.head(10).iterrows():
            f.write(f"- user_id: `{row['user_id']}`, Alter: {row['user_age']}\n")
    f.write("\n")
    
    # Extreme Altersangaben prüfen (< 0 oder > 120)
    extreme_ages = df_user[(df_user['user_age'] < 0) | (df_user['user_age'] > 120)]
    f.write(f"### Benutzer mit extremem Alter (< 0 oder > 120): **{len(extreme_ages)}**\n\n")
    if len(extreme_ages) > 0:
        f.write(f"Beispiele:\n\n")
        for idx, row in extreme_ages.head(10).iterrows():
            f.write(f"- user_id: `{row['user_id']}`, Alter: {row['user_age']}\n")
    f.write("\n")
    
    # 2. Datumsanalyse und Konvertierung
    f.write("## 2. Datumsanalyse\n\n")
    
    # Konvertierung der Datumsangaben
    # Temporär mit Timestamps für min/max Berechnung
    df_user['first_active_timestamp_dt'] = pd.to_datetime(df_user['first_active_timestamp'], format='%Y%m%d%H%M%S', errors='coerce')
    df_user['account_created_date_ts'] = pd.to_datetime(df_user['account_created_date'], errors='coerce')
    df_user['first_booking_date_ts'] = pd.to_datetime(df_user['first_booking_date'], errors='coerce')
    
    # Für Vergleiche: nur Datum ohne Zeit
    df_user['first_active_date'] = df_user['first_active_timestamp_dt'].dt.date
    df_user['account_created_date_dt'] = df_user['account_created_date_ts'].dt.date
    df_user['first_booking_date_dt'] = df_user['first_booking_date_ts'].dt.date
    
    f.write(f"### Datumsbereiche:\n\n")
    f.write(f"- **first_active_date:** {df_user['first_active_timestamp_dt'].min()} bis {df_user['first_active_timestamp_dt'].max()}\n")
    f.write(f"- **account_created_date:** {df_user['account_created_date_ts'].min()} bis {df_user['account_created_date_ts'].max()}\n")
    f.write(f"- **first_booking_date:** {df_user['first_booking_date_ts'].min()} bis {df_user['first_booking_date_ts'].max()}\n\n")
    
    # Zukünftige Datumsangaben prüfen
    now = datetime.now().date()
    future_active = df_user[df_user['first_active_date'] > now]
    future_created = df_user[df_user['account_created_date_dt'] > now]
    future_booking = df_user[df_user['first_booking_date_dt'] > now]
    
    f.write(f"### Zukünftige Datumsangaben:\n\n")
    f.write(f"- **first_active_date in der Zukunft:** {len(future_active)}\n")
    f.write(f"- **account_created_date in der Zukunft:** {len(future_created)}\n")
    f.write(f"- **first_booking_date in der Zukunft:** {len(future_booking)}\n\n")
    
    # Datumsangaben vor 2000 prüfen (unrealistisch für diese Plattform)
    date_2000 = pd.to_datetime('2000-01-01').date()
    old_active = df_user[df_user['first_active_date'] < date_2000]
    old_created = df_user[df_user['account_created_date_dt'] < date_2000]
    old_booking = df_user[df_user['first_booking_date_dt'] < date_2000]
    
    f.write(f"### Datumsangaben vor 2000:\n\n")
    f.write(f"- **first_active_date vor 2000:** {len(old_active)}\n")
    f.write(f"- **account_created_date vor 2000:** {len(old_created)}\n")
    f.write(f"- **first_booking_date vor 2000:** {len(old_booking)}\n\n")
    
    # 3. Datumsreihenfolge prüfen (nur Datum, keine Zeit)
    f.write("## 3. Fehler in der Datumsreihenfolge\n\n")
    f.write("**Hinweis:** Datumsvergleiche werden nur auf Basis des Datums ohne Zeitstempel durchgeführt.\n\n")
    
    # first_active_date sollte <= account_created_date sein
    error1 = df_user[(df_user['first_active_date'].notna()) & (df_user['account_created_date_dt'].notna()) & 
                (df_user['first_active_date'] > df_user['account_created_date_dt'])]
    f.write(f"### Zeilen mit first_active_date > account_created_date: **{len(error1)}**\n\n")
    if len(error1) > 0:
        f.write(f"Beispiele (erste 10):\n\n")
        for idx, row in error1.head(10).iterrows():
            f.write(f"- user_id: `{row['user_id']}`, first_active: {row['first_active_date']}, created: {row['account_created_date_dt']}\n")
    f.write("\n")
    
    # account_created_date sollte <= first_booking_date sein
    error2 = df_user[(df_user['account_created_date_dt'].notna()) & (df_user['first_booking_date_dt'].notna()) & 
                (df_user['account_created_date_dt'] > df_user['first_booking_date_dt'])]
    f.write(f"### Zeilen mit account_created_date > first_booking_date: **{len(error2)}**\n\n")
    if len(error2) > 0:
        f.write(f"Beispiele (erste 10):\n\n")
        for idx, row in error2.head(10).iterrows():
            f.write(f"- user_id: `{row['user_id']}`, created: {row['account_created_date_dt']}, booking: {row['first_booking_date_dt']}\n")
    f.write("\n")
    
    # first_active_date sollte <= first_booking_date sein
    error3 = df_user[(df_user['first_active_date'].notna()) & (df_user['first_booking_date_dt'].notna()) & 
                (df_user['first_active_date'] > df_user['first_booking_date_dt'])]
    f.write(f"### Zeilen mit first_active_date > first_booking_date: **{len(error3)}**\n\n")
    if len(error3) > 0:
        f.write(f"Beispiele (erste 10):\n\n")
        for idx, row in error3.head(10).iterrows():
            f.write(f"- user_id: `{row['user_id']}`, first_active: {row['first_active_date']}, booking: {row['first_booking_date_dt']}\n")
    f.write("\n")
    
    # 4. first_booking_date vs destination_country prüfen
    f.write("## 4. Konsistenz von first_booking_date und destination_country\n\n")
    
    # Wenn first_booking_date NaN ist, sollte destination_country NDF sein
    no_booking = df_user[df_user['first_booking_date'].isna()]
    f.write(f"### Benutzer ohne Buchungsdatum: **{len(no_booking)}**\n\n")
    
    error4 = df_user[(df_user['first_booking_date'].isna()) & (df_user['destination_country'] != 'NDF')]
    f.write(f"### Benutzer ohne Buchung, aber destination != NDF: **{len(error4)}**\n\n")
    if len(error4) > 0:
        f.write(f"Beispiele (erste 10):\n\n")
        for idx, row in error4.head(10).iterrows():
            f.write(f"- user_id: `{row['user_id']}`, booking_date: {row['first_booking_date']}, destination: {row['destination_country']}\n")
    else:
        f.write("✓ Keine Fehler gefunden\n")
    f.write("\n")
    
    # Umgekehrt prüfen: Benutzer mit Buchung, aber destination ist NDF
    error5 = df_user[(df_user['first_booking_date'].notna()) & (df_user['destination_country'] == 'NDF')]
    f.write(f"### Benutzer mit Buchung, aber destination = NDF: **{len(error5)}**\n\n")
    if len(error5) > 0:
        f.write(f"Beispiele (erste 10):\n\n")
        for idx, row in error5.head(10).iterrows():
            f.write(f"- user_id: `{row['user_id']}`, booking_date: {row['first_booking_date']}, destination: {row['destination_country']}\n")
    else:
        f.write("✓ Keine Fehler gefunden\n")
    f.write("\n")
    
    # 5. Analyse der Textspalten (auf Tippfehler prüfen)
    f.write("## 5. Analyse der Textspalten (Suche nach Tippfehlern)\n\n")
    
    string_columns = ['user_gender', 'signup_platform', 'signup_process', 'user_language', 
                      'marketing_channel', 'marketing_provider', 'first_tracked_affiliate',
                      'signup_application', 'first_device', 'first_web_browser', 'destination_country']
    
    for col in string_columns:
        unique_vals = df_user[col].value_counts()
        f.write(f"### {col}: {len(unique_vals)} eindeutige Werte\n\n")
        f.write(f"Top 15 Werte:\n\n")
        for val, count in unique_vals.head(15).items():
            f.write(f"- `{val}`: {count}\n")
        
        # Nach möglichen Tippfehlern suchen (Werte mit sehr geringer Häufigkeit)
        rare_values = unique_vals[unique_vals <= 5]
        if len(rare_values) > 0:
            f.write(f"\n**Seltene Werte (Anzahl ≤ 5):** {len(rare_values)}\n\n")
            for val, count in rare_values.head(10).items():
                f.write(f"- `{val}`: {count}\n")
        f.write("\n")
    
    # 6. Fehlende Werte
    f.write("## 6. Analyse fehlender Werte\n\n")
    
    missing = df_user.isnull().sum()
    f.write(f"Fehlende Werte nach Spalte:\n\n")
    for col, count in missing.items():
        if count > 0:
            pct = (count / len(df_user)) * 100
            f.write(f"- **{col}:** {count} ({pct:.2f}%)\n")
    f.write("\n")
    
    # 7. Leere Zeichenketten
    f.write("## 7. Analyse leerer Zeichenketten\n\n")
    
    empty_found = False
    for col in string_columns:
        empty_count = (df_user[col] == '').sum()
        if empty_count > 0:
            f.write(f"- **{col}:** {empty_count} leere Zeichenketten\n")
            empty_found = True
    
    if not empty_found:
        f.write("✓ Keine leeren Zeichenketten gefunden\n")
    f.write("\n")
    
    # 8. Zusammenfassung aller Fehler
    f.write("## 8. Zusammenfassung aller gefundenen Fehler\n\n")
    f.write("=" * 80 + "\n\n")
    
    total_errors = 0
    
    errors_list = []
    
    if len(unrealistic_ages) > 0:
        errors_list.append(("Unrealistisches Alter (< 18 oder > 90)", len(unrealistic_ages)))
        total_errors += len(unrealistic_ages)
    
    if len(age_over_80) > 0:
        errors_list.append(("Alter > 80 (Information)", len(age_over_80)))
    
    if len(extreme_ages) > 0:
        errors_list.append(("Extremes Alter (< 0 oder > 120)", len(extreme_ages)))
        total_errors += len(extreme_ages)
    
    if len(future_active) > 0:
        errors_list.append(("first_active_date in der Zukunft", len(future_active)))
        total_errors += len(future_active)
    
    if len(future_created) > 0:
        errors_list.append(("account_created_date in der Zukunft", len(future_created)))
        total_errors += len(future_created)
    
    if len(future_booking) > 0:
        errors_list.append(("first_booking_date in der Zukunft", len(future_booking)))
        total_errors += len(future_booking)
    
    if len(error1) > 0:
        errors_list.append(("first_active_date > account_created_date", len(error1)))
        total_errors += len(error1)
    
    if len(error2) > 0:
        errors_list.append(("account_created_date > first_booking_date", len(error2)))
        total_errors += len(error2)
    
    if len(error3) > 0:
        errors_list.append(("first_active_date > first_booking_date", len(error3)))
        total_errors += len(error3)
    
    if len(error4) > 0:
        errors_list.append(("Keine Buchung, aber destination != NDF", len(error4)))
        total_errors += len(error4)
    
    if len(error5) > 0:
        errors_list.append(("Buchung vorhanden, aber destination = NDF", len(error5)))
        total_errors += len(error5)
    
    f.write("| Fehlertyp | Anzahl |\n")
    f.write("|-----------|--------|\n")
    for err_name, err_count in errors_list:
        f.write(f"| {err_name} | {err_count} |\n")
    
    f.write(f"\n**Gesamtzahl der Fehler (mit möglichen Überschneidungen):** {total_errors}\n\n")
    f.write("=" * 80 + "\n")

print(f"\nAnalyse abgeschlossen. Ergebnisse gespeichert unter: {output_file}")
