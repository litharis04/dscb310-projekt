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
import plotly.express as px
import matplotlib.pyplot as plt
from IPython.display import display

# %%
df_user_raw = pd.read_parquet('data/user_filtered.parquet')

# %%
df_user = df_user_raw.copy()

# %%
df_user.head(25)

# %%
# Zähle die Häufigkeit jedes Wertes in 'first_web_browser'
browser_counts = df_user['first_web_browser'].value_counts()

# Identifiziere Werte mit Häufigkeit < 500
rare_browsers = browser_counts[browser_counts < 500].index.tolist()

# Ersetze diese Werte durch 'Other'
df_user['first_web_browser'] = df_user['first_web_browser'].replace(rare_browsers, 'Other')

# %%
# Speicherung der Analyse in txt-Datei

# Definiere die zu analysierenden Spalten
columns_to_analyze = ['user_gender', 'signup_platform', 'signup_process', 'user_language', 
                      'marketing_channel', 'marketing_provider', 'first_tracked_affiliate',
                      'signup_application', 'first_device', 'first_web_browser', 'destination_country']

# Erstelle den Inhalt der Datei
output_lines = ["Zusammenfassung der eindeutigen Werte pro Spalte in df_user_filtered"]
output_lines.append("=" * 60)
output_lines.append("")

for column in columns_to_analyze:
    if column in df_user.columns:
        # Zähle eindeutige Werte und deren Häufigkeiten
        value_counts = df_user[column].value_counts()
        total_count = len(df_user)
        
        output_lines.append(f"Spalte: {column}")
        output_lines.append(f"Anzahl eindeutiger Werte: {len(value_counts)}")
        output_lines.append("Wert - Anzahl - Prozent")
        
        for value, count in value_counts.items():
            percentage = (count / total_count) * 100
            output_lines.append(f"'{value}' - {count} - {percentage:.2f}%")
        
        output_lines.append("")
        output_lines.append("-" * 60)
        output_lines.append("")

# Speichere in Datei
output_file_path = 'scripts/outputs/df_user_filtered_unique_values_summary.txt'
with open(output_file_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"Datei erfolgreich gespeichert: {output_file_path}")

# %%
