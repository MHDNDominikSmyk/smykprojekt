import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df1 = pd.read_csv('Online_Retail.csv', encoding='ISO-8859-1', on_bad_lines='skip', engine='python')
df2 = pd.read_csv('Online_Retail_II.csv', encoding='ISO-8859-1', on_bad_lines='skip', engine='python')
df = pd.concat([df1, df2], ignore_index=True)

df = df.dropna(subset=['CustomerID'])
df = df[df['Quantity'] > 0]
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month

rollup_df = df.groupby('Year')['TotalPrice'].sum()
drilldown_df = df.groupby(['Year', 'Month'])['TotalPrice'].sum()
slice_df = df[df['Country'] == 'United Kingdom']
dice_df = df[(df['Country'] == 'United Kingdom') & (df['Year'] == 2011)]
pivot_cube = pd.pivot_table(df, values='TotalPrice', index='Country', columns='Year', aggfunc='sum', fill_value=0)

print("Zadanie 1: Top 10 krajów pod względem sprzedaży")
top_10_countries = df.groupby('Country')['TotalPrice'].sum().nlargest(10)
print(top_10_countries)
print("\n")

print("Zadanie 2: Znajdź miesiąc o największej sprzedaży")
best_month = df.groupby('Month')['TotalPrice'].sum().idxmax()
best_month_value = df.groupby('Month')['TotalPrice'].sum().max()
print(f"Najlepszy miesiąc: {best_month}, Sprzedaż: {best_month_value:.2f}")
print("\n")

print("Zadanie 3: Kostka - wiersze: kraj, kolumny: miesiąc, wartości: sprzedaż")
cube_task3 = pd.pivot_table(df, values='TotalPrice', index='Country', columns='Month', aggfunc='sum', fill_value=0)
print(cube_task3.head())
print("\n")

print("Zadanie 4: Dla każdego kraju znajdź rok z najwyższą sprzedażą")
country_year_sales = df.groupby(['Country', 'Year'])['TotalPrice'].sum().reset_index()
idx_best_years = country_year_sales.groupby('Country')['TotalPrice'].idxmax()
best_year_per_country = country_year_sales.loc[idx_best_years]
print(best_year_per_country.head(10))
print("\n")

print("Zadanie 5 (challenge): Top 5 produktów w każdym kraju")
product_sales = df.groupby(['Country', 'StockCode'])['TotalPrice'].sum().reset_index()
product_sales = product_sales.sort_values(by=['Country', 'TotalPrice'], ascending=[True, False])
top_5_products_per_country = product_sales.groupby('Country').head(5)
print(top_5_products_per_country.head(15))
print("\n")

print("Bonus: Wizualizacja (heatmap)")
cube_for_heatmap = cube_task3.drop('United Kingdom', errors='ignore')
plt.figure(figsize=(14, 10))
sns.heatmap(cube_for_heatmap, cmap='viridis', annot=False, fmt=".0f")
plt.title('Heatmapa Sprzedaży: Kraj vs Miesiąc (bez UK)')
plt.xlabel('Miesiąc')
plt.ylabel('Kraj')
plt.tight_layout()
plt.show()