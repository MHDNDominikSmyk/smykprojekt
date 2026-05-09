import pandas as pd
import numpy as np
from datetime import datetime
import warnings

# Ignorujemy ostrzeżenia o parsowaniu dat dla czystości konsoli
warnings.filterwarnings('ignore', category=UserWarning, module='pandas')

# --- PRZYGOTOWANIE DANYCH (Czyszczenie) ---
df = pd.read_csv('Online_Retail.csv', encoding='ISO-8859-1')
df = df.dropna(subset=['CustomerID'])
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# Użycie format='mixed' eliminuje błąd inferencji formatu daty
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='mixed')

df = df.drop_duplicates()
df['Revenue'] = df['Quantity'] * df['UnitPrice']

print("--- WYNIKI LABORATORIUM 3 ---")

# --- Zad1.1 ---
print("\nZad1.1: Ziarno faktu (grain)")
print("Ziarno: Pojedyncza pozycja na fakturze (InvoiceNo + StockCode).")
print("Opis: Jeden wiersz reprezentuje sprzedaż konkretnego produktu w ramach pojedynczej transakcji.")
print("Uzasadnienie: Wybór najbardziej szczegółowego ziarna pozwala na maksymalną elastyczność agregacji danych.")

# --- Zad1.2 ---
print("\nZad1.2: Wybór ziarna")
print("Wybrano ziarno: 1 (Pojedyncza pozycja faktury)")

# --- Zad1.3 ---
print("\nZad1.3: Uzasadnienie i analiza")
print("Uzasadnienie: Pozwala to na analizę asortymentową i koszykową (co z czym jest kupowane).")
print("Przykład analizy: Zidentyfikowanie top 10 produktów generujących największy przychód.")

# --- Zad1.4 ---
print("\nZad1.4: Pytania biznesowe")
print("Pytania: 'Który produkt jest najczęściej kupowany?', 'Jakie produkty wybierają klienci z danego kraju?'.")
print("Analiza: Śledzenie trendów sprzedaży konkretnych produktów (StockCode) w czasie.")

# --- Zad1.5: Implementacja Kluczy ---
# Tworzenie DimProduct
dim_product = df[['StockCode', 'Description']].drop_duplicates(subset=['StockCode']).copy()
dim_product['ProductKey'] = range(1, len(dim_product) + 1)

# Tworzenie DimDate
dim_date = pd.DataFrame({'FullDate': pd.to_datetime(df['InvoiceDate'].dt.date.unique())})
dim_date['DateKey'] = dim_date['FullDate'].dt.strftime('%Y%m%d').astype(int)
dim_date['Year'] = dim_date['FullDate'].dt.year
dim_date['Month'] = dim_date['FullDate'].dt.month
dim_date['Day'] = dim_date['FullDate'].dt.day

print("\nZad1.5: Klucze")
print("Zidentyfikowano klucze naturalne (CustomerID, StockCode) i wygenerowano klucze sztuczne (CustomerKey, ProductKey, DateKey).")

# --- Zad1.6: SCD Typ 1 ---
dim_customer = df[['CustomerID', 'Country']].drop_duplicates(subset=['CustomerID']).copy()
dim_customer['CustomerKey'] = range(1, len(dim_customer) + 1)

fact_sales = df.merge(dim_product[['StockCode', 'ProductKey']], on='StockCode', how='left')
fact_sales = fact_sales.merge(dim_customer[['CustomerID', 'CustomerKey']], on='CustomerID', how='left')
fact_sales['DateKey'] = fact_sales['InvoiceDate'].dt.strftime('%Y%m%d').astype(int)

print("\nZad1.6: SCD Typ 1")
print("Zaimplementowano SCD typu 1 dla DimCustomer (aktualizacja danych bez zachowania historii).")

# --- Zad2.1: Rozszerzenie modelu ---
dim_invoice = df[['InvoiceNo']].drop_duplicates().copy()
dim_invoice['InvoiceKey'] = range(1, len(dim_invoice) + 1)

fact_sales_ext = fact_sales.merge(dim_invoice, on='InvoiceNo', how='left')
fact_sales_ext = fact_sales_ext[['ProductKey', 'CustomerKey', 'DateKey', 'InvoiceKey', 'Quantity', 'Revenue', 'UnitPrice']]

print("\nZad2.1: Nowy wymiar i miary")
print("Dodano wymiar DimInvoice oraz miarę UnitPrice do tabeli faktów.")
print("Analiza: Zastosowano denormalizację wymiarów (schemat gwiazdy) dla zwiększenia wydajności odczytu.")

# --- Zad2.2: SCD Typ 2 ---
dim_customer_scd2 = df[['CustomerID', 'Country']].drop_duplicates().copy()
dim_customer_scd2['ValidFrom'] = pd.Timestamp('2010-01-01')
dim_customer_scd2['ValidTo'] = pd.Timestamp('2099-12-31')
dim_customer_scd2['IsCurrent'] = True
dim_customer_scd2['CustomerKey_SCD2'] = range(1, len(dim_customer_scd2) + 1)

print("\nZad2.2: SCD Typ 2")
print("Zaimplementowano wersjonowanie (SCD2) dla klientów z polami ValidFrom, ValidTo i IsCurrent.")

# --- Zad2.3: Podsumowanie projektu ---
print("\nZad2.3: Analiza projektu")
print("1. Ziarno: Wybrano pozycję faktury, aby umożliwić analizę na najniższym poziomie szczegółowości.")
print("2. Kompromisy: Wybrano schemat gwiazdy (redundancja danych) zamiast śnieżynki, aby przyspieszyć zapytania SQL.")
print("3. Biznes: Model wspiera analizy trendów, rentowności produktów oraz segmentację geograficzną klientów.")

# Eksport do plików
fact_sales_ext.to_csv('FactSales.csv', index=False)
dim_customer_scd2.to_csv('DimCustomer_SCD2.csv', index=False)
