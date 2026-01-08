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
        # Получи значения и их количество
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
# Vorbereitung der Daten: NDF ausschließen und Geschlechter filtern
df_filtered = df_user[(df_user['user_gender'].notna()) & 
                     (df_user['user_gender'] != 'other') & 
                     (df_user['destination_country'] != 'NDF')].copy()

# 1. Vergleich: US vs. Rest der Welt
df_filtered['destination_group'] = df_filtered['destination_country'].apply(
    lambda x: 'US' if x == 'US' else 'rest_of_the_world'
)

# Prozentsätze für US vs. Rest berechnen
grouped_us_rest = df_filtered.groupby(['user_gender', 'destination_group']).size().reset_index(name='count')
total_per_gender_us_rest = grouped_us_rest.groupby('user_gender')['count'].transform('sum')
grouped_us_rest['percentage'] = (grouped_us_rest['count'] / total_per_gender_us_rest) * 100

# Erster Plot: US vs. Rest der Welt
plt.figure(figsize=(10, 6))
sns.barplot(data=grouped_us_rest, x='destination_group', y='percentage', hue='user_gender', palette='Set2')
plt.xlabel('Destination Gruppe')
plt.ylabel('Prozentsatz der Buchungen (%)')
plt.title('Buchungsvergleich: US vs. Rest der Welt nach Geschlecht')
plt.legend(title='Geschlecht')
plt.tight_layout()
plt.show()

# 2. Vergleich: Alle Länder außer US
df_non_us = df_filtered[df_filtered['destination_country'] != 'US'].copy()

# Prozentsätze für Länder außer US berechnen
grouped_non_us = df_non_us.groupby(['user_gender', 'destination_country']).size().reset_index(name='count')
total_per_gender_non_us = grouped_non_us.groupby('user_gender')['count'].transform('sum')
grouped_non_us['percentage'] = (grouped_non_us['count'] / total_per_gender_non_us) * 100

# Sortierung für den zweiten Plot nach Gesamthäufigkeit
grouped_total_non_us = grouped_non_us.groupby('destination_country')['count'].sum().reset_index(name='total_count')
destination_order_non_us = [dest for dest in grouped_total_non_us.sort_values('total_count', ascending=False)['destination_country'].tolist() if dest != 'other']
if 'other' in grouped_total_non_us['destination_country'].values:
    destination_order_non_us.append('other')

# Zweiter Plot: Länder außer US
plt.figure(figsize=(12, 6))
sns.barplot(data=grouped_non_us, x='destination_country', y='percentage', hue='user_gender', palette='Set2', order=destination_order_non_us)
plt.xticks(rotation=45)
plt.xlabel('Zieldestination (exkl. US)')
plt.ylabel('Prozentsatz der Buchungen (%)')
plt.title('Präferenzen bei der Wahl der Destination nach Geschlecht (exkl. US)')
plt.tight_layout()
plt.show()
