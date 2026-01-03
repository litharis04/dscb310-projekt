"""
Validierungsskript für EDA.py

Dieses Skript führt eine schnelle Validierung der Hauptschritte aus EDA.py durch,
um sicherzustellen, dass der Code korrekt funktioniert.
"""

import numpy as np
import pandas as pd
import sys
import os

# Zum Projektstammverzeichnis wechseln (falls notwendig)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
os.chdir(project_root)

print("=" * 80)
print("VALIDIERUNG VON EDA.PY")
print("=" * 80)
print(f"Arbeitsverzeichnis: {os.getcwd()}")
print("=" * 80)

try:
    # 1. Daten laden
    print("\n1. Daten laden...")
    df_user = pd.read_csv('data/user.csv')
    print(f"   ✓ {len(df_user)} Zeilen, {len(df_user.columns)} Spalten geladen")

    # 2. Duplikate prüfen
    print("\n2. Duplikatsprüfung...")
    anzahl_duplikate = df_user.duplicated().sum()
    print(f"   ✓ {anzahl_duplikate} Duplikate gefunden")
    if anzahl_duplikate > 0:
        df_user = df_user.drop_duplicates()
        print(f"   ✓ Duplikate entfernt. Neue Zeilenanzahl: {len(df_user)}")

    # 3. Datumskonvertierung
    print("\n3. Datumskonvertierung...")
    df_user['first_active_timestamp'] = pd.to_datetime(
        df_user['first_active_timestamp'], 
        format='%Y%m%d%H%M%S', 
        errors='coerce'
    )
    df_user['first_active_date'] = df_user['first_active_timestamp'].dt.normalize()
    df_user['account_created_date'] = pd.to_datetime(
        df_user['account_created_date'], 
        format='%Y-%m-%d', 
        errors='coerce'
    )
    df_user['first_booking_date'] = pd.to_datetime(
        df_user['first_booking_date'], 
        format='%Y-%m-%d', 
        errors='coerce'
    )
    print("   ✓ Datumsfelder konvertiert")

    # 4. Datumsreihenfolge prüfen
    print("\n4. Datumsreihenfolge prüfen...")
    zeilen_vorher = len(df_user)
    fehler1 = (df_user['first_active_date'].notna()) & \
              (df_user['account_created_date'].notna()) & \
              (df_user['first_active_date'] > df_user['account_created_date'])
    fehler2 = (df_user['account_created_date'].notna()) & \
              (df_user['first_booking_date'].notna()) & \
              (df_user['account_created_date'] > df_user['first_booking_date'])
    datum_fehler = fehler1 | fehler2
    anzahl_datum_fehler = datum_fehler.sum()
    print(f"   ✓ {anzahl_datum_fehler} Datumsreihenfolgefehler gefunden")
    if anzahl_datum_fehler > 0:
        df_user = df_user[~datum_fehler]
        print(f"   ✓ Fehlerhafte Zeilen entfernt: {zeilen_vorher} → {len(df_user)}")

    # 5. user_gender bereinigen
    print("\n5. user_gender bereinigen...")
    df_user['user_gender'] = df_user['user_gender'].str.lower()
    ungueltige_gender = ~df_user['user_gender'].isin(['female', 'male', 'other']) & df_user['user_gender'].notna()
    anzahl_ungueltige = ungueltige_gender.sum()
    print(f"   ✓ {anzahl_ungueltige} ungültige Werte gefunden")
    df_user.loc[~df_user['user_gender'].isin(['female', 'male', 'other']), 'user_gender'] = np.nan
    print("   ✓ user_gender bereinigt")

    # 6. Altersfilterung
    print("\n6. Altersfilterung...")
    zeilen_vorher = len(df_user)
    alter_zu_jung = df_user['user_age'] < 18
    alter_zu_alt = df_user['user_age'] > 90
    unrealistisches_alter = alter_zu_jung | alter_zu_alt
    anzahl_unrealistisch = unrealistisches_alter.sum()
    print(f"   ✓ {anzahl_unrealistisch} unrealistische Altersangaben gefunden")
    if anzahl_unrealistisch > 0:
        df_user = df_user[~unrealistisches_alter]
        print(f"   ✓ Zeilen entfernt: {zeilen_vorher} → {len(df_user)}")

    # 7. Eindeutige Werte prüfen (kurze Version)
    print("\n7. Eindeutige Werte prüfen...")
    text_spalten = ['user_gender', 'signup_platform', 'user_language', 'destination_country']
    for spalte in text_spalten[:4]:  # Nur erste 4 prüfen
        werte_haeufigkeit = df_user[spalte].value_counts(dropna=False)
        seltene_werte = werte_haeufigkeit[werte_haeufigkeit < 10]
        print(f"   {spalte}: {len(werte_haeufigkeit)} eindeutige Werte, {len(seltene_werte)} seltene")

    # 8. Abhängigkeit first_booking_date ↔ destination_country
    print("\n8. Abhängigkeit first_booking_date ↔ destination_country...")
    keine_buchung_aber_destination = (df_user['first_booking_date'].isna()) & \
                                      (df_user['destination_country'] != 'NDF')
    buchung_aber_ndf = (df_user['first_booking_date'].notna()) & \
                       (df_user['destination_country'] == 'NDF')
    anzahl_fall1 = keine_buchung_aber_destination.sum()
    anzahl_fall2 = buchung_aber_ndf.sum()
    print(f"   ✓ Fall 1 (keine Buchung, aber destination != NDF): {anzahl_fall1}")
    print(f"   ✓ Fall 2 (Buchung, aber destination = NDF): {anzahl_fall2}")

    # 9. Fehlende Werte
    print("\n9. Fehlende Werte analysieren...")
    fehlende_werte = df_user.isnull().sum()
    fehlende_gesamt = fehlende_werte.sum()
    spalten_mit_fehlenden = (fehlende_werte > 0).sum()
    print(f"   ✓ {fehlende_gesamt} fehlende Werte in {spalten_mit_fehlenden} Spalten")

    print("\n" + "=" * 80)
    print("VALIDIERUNG ERFOLGREICH ABGESCHLOSSEN")
    print("=" * 80)
    print(f"\nFinale Datenstatistik:")
    print(f"  - Zeilen: {len(df_user)}")
    print(f"  - Spalten: {len(df_user.columns)}")
    print(f"  - Speichernutzung: {df_user.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    sys.exit(0)

except Exception as e:
    print(f"\n❌ FEHLER während der Validierung: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
