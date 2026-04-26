import pandas as pd
 
# Zadanie 1
url = "https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/07_Visualization/Online_Retail/Online_Retail.csv"
df = pd.read_csv(url, encoding="ISO-8859-1")
 
print("--- ZADANIE 1: Wczytanie danych ---")
print("Liczba rekordów w strefie stagingowej:", len(df))
print("Liczba kolumn:", df.shape[1])
print("Podgląd danych:")
print(df.head())
 
# Zadanie 2
print("\n--- ZADANIE 2: Identyfikacja encji i atrybutów ---")
print("1. Customers  | PK: CustomerID | Atrybuty: Country")
print("2. Products   | PK: StockCode  | Atrybuty: Description")
print("3. Orders     | PK: InvoiceNo  | Atrybuty: InvoiceDate | FK: CustomerID")
print("4. OrderItems | PK: (InvoiceNo, StockCode) | Atrybuty: Quantity, UnitPrice | FK: InvoiceNo, StockCode")
print("5. Date       | PK: InvoiceDate | Atrybuty: Year, Month")
 
# Zadanie 3
df_clean = df.dropna(subset=['CustomerID']).copy()
 
customers = df_clean[['CustomerID', 'Country']].drop_duplicates(subset=['CustomerID'])
products = df_clean[['StockCode', 'Description']].drop_duplicates(subset=['StockCode'])
orders = df_clean[['InvoiceNo', 'InvoiceDate', 'CustomerID']].drop_duplicates(subset=['InvoiceNo'])
order_items = df_clean[['InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice']]
 
dates = pd.DataFrame()
dates['InvoiceDate'] = df_clean['InvoiceDate'].drop_duplicates()
dates['Year'] = pd.to_datetime(dates['InvoiceDate']).dt.year
dates['Month'] = pd.to_datetime(dates['InvoiceDate']).dt.month
 
print("\n--- ZADANIE 3: Model 3NF - Weryfikacja poprawności ---")
print("Czy PK Customers (CustomerID) jest unikalne?:", customers['CustomerID'].is_unique)
print("Czy PK Products (StockCode) jest unikalne?:", products['StockCode'].is_unique)
print("Czy PK Orders (InvoiceNo) jest unikalne?:", orders['InvoiceNo'].is_unique)
 
print("\nWeryfikacja więzów spójności (Klucze Obce):")
check_fk_products = order_items['StockCode'].isin(products['StockCode']).all()
check_fk_orders = order_items['InvoiceNo'].isin(orders['InvoiceNo']).all()
print("Czy wszystkie produkty w OrderItems istnieją w tabeli Products?:", check_fk_products)
print("Czy wszystkie faktury w OrderItems istnieją w tabeli Orders?:", check_fk_orders)
 
# Zadanie 4
print("\n--- ZADANIE 4: Refleksja ---")
print("Dlaczego model 3NF nie jest wygodny do analiz OLAP?")
print("Odpowiedź: Dane są zbyt mocno poszatkowane, przez co komputer musi się napracować, żeby je poskładać w czytelny raport.")
print("Co wymagałoby wielu joinów?")
print("Odpowiedź: Joiny są niezbędne do łączenia informacji rozbitych na wiele drobnych tabel (np. kategorie czy regiony)")