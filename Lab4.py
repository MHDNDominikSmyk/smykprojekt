import pandas as pd

# Zadanie 1
df = pd.read_csv("Online_Retail.csv", encoding='ISO-8859-1')

df = df.dropna(subset=['CustomerID'])
df = df[df['Quantity'] > 0]
df = df[df['UnitPrice'] >= 0]
df = df.drop_duplicates()

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='mixed')
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month
df['Day'] = df['InvoiceDate'].dt.day

df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

fact_sales = df[['InvoiceNo', 'StockCode', 'CustomerID', 'InvoiceDate', 'Quantity', 'TotalAmount', 'Year', 'Month', 'Day']]
fact_sales.to_csv("fact_sales.csv", index=False)

print("=== PODSUMOWANIE ZADANIA 1 ===")
print("Stworzono plik: fact_sales.csv")
print("Dodano kolumny: Year, Month, Day oraz miarę TotalAmount.\n")

# Zadanie 2.1
df1 = pd.read_csv("Online_Retail.csv", encoding='ISO-8859-1')
df2 = pd.read_excel("online_retail_II.xlsx")

print("=== ODPOWIEDZI ZADANIE 2.1 ===")
print(f"Czy struktura danych jest identyczna? Nie, nazwy kolumn i formaty ID mogą się różnić między CSV a Excel.")
print(f"Czy dane można od razu połączyć? Nie, wymagane jest ujednolicenie nazw kolumn i typów danych.\n")

# Zadanie 2.2
df2.columns = df1.columns
df1['CustomerID'] = df1['CustomerID'].astype(float)
df2['CustomerID'] = df2['CustomerID'].astype(float)
df1['InvoiceDate'] = pd.to_datetime(df1['InvoiceDate'], format='mixed')
df2['InvoiceDate'] = pd.to_datetime(df2['InvoiceDate'], format='mixed')

print("=== ODPOWIEDZI ZADANIE 2.2 ===")
print("Który schemat przyjąć jako docelowy? Schemat z pliku Online_Retail.csv.")
print("Czy wszystkie kolumny są potrzebne? Nie, do tabeli faktów zbędne są opisy tekstowe (Description).\n")

# Zadanie 2.3
duplicates_count = df1.isin(df2.to_dict(orient='list')).all(axis=1).sum()

print("=== ODPOWIEDZI ZADANIE 2.3 ===")
print("Jak rozpoznać duplikat? Po unikalnej kombinacji: InvoiceNo, StockCode, CustomerID i InvoiceDate.")
print("Co zrobić z konfliktem danych? Należy zastosować regułę biznesową, np. priorytet dla nowszego źródła.")
print("Które źródło jest bardziej wiarygodne? Zazwyczaj system transakcyjny (plik CSV).\n")

# Zadanie 2.4
df1_c = df1.dropna(subset=['CustomerID']).drop_duplicates()
df2_c = df2.dropna(subset=['CustomerID']).drop_duplicates()
df_all = pd.concat([df1_c, df2_c], ignore_index=True)

print("=== ODPOWIEDZI ZADANIE 2.4 ===")
print("Czy użyć concat czy merge? Używamy concat (operacja UNION), aby połączyć rekordy pionowo.")
print("Czy zachować wszystkie rekordy? Nie, tylko te po procesie czyszczenia (Data Quality).\n")

# Zadanie 2.5
df_all.to_csv("fact_sales_integrated.csv", index=False)
print("=== PODSUMOWANIE ZADANIA 2.5 ===")
print("Stworzono zintegrowany plik: fact_sales_integrated.csv")