# =======================================================
# DSA 2040 Exam - Section 1, Task 2: ETL Process
# Student ID: [Your ID]
# =======================================================

import pandas as pd
import numpy as np
import sqlite3
import random
from datetime import datetime, timedelta
import sys
import matplotlib.pyplot as plt

# 1. EXTRACT (Generation & Extraction)

def generate_retail_data(num_rows=1000):
    """
    Generates synthetic retail data mimicking the UCI Online Retail dataset.
    """
    print(f"[{datetime.now()}] --- EXTRACT: Generating Synthetic Data ---")
    
    try:
        np.random.seed(42)
        random.seed(42)
        
        customer_ids = np.random.randint(10000, 99999, size=100) 
        countries = ['United Kingdom', 'France', 'Germany', 'Spain', 'Kenya']
        categories = ['Electronics', 'Clothing', 'Home', 'Books', 'Toys']
        
        data = []
        for i in range(num_rows):
            invoice_no = f"INV{10000 + i}"
            cust_id = np.random.choice(customer_ids)
            country = np.random.choice(countries, p=[0.6, 0.1, 0.1, 0.1, 0.1])
            
            start_date = datetime(2023, 1, 1)
            end_date = datetime(2025, 8, 12)
            random_days = random.randint(0, (end_date - start_date).days)
            invoice_date = start_date + timedelta(days=random_days)
            
            stock_code = f"PROD{random.randint(100, 200)}"
            category = np.random.choice(categories)
            quantity = np.random.randint(-5, 50) 
            unit_price = round(np.random.uniform(1.0, 100.0), 2)
            
            data.append([invoice_no, stock_code, category, quantity, invoice_date, unit_price, cust_id, country])
            
        columns = ['InvoiceNo', 'StockCode', 'Category', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']
        df = pd.DataFrame(data, columns=columns)
        
        print(f"[{datetime.now()}] Generated {len(df)} raw rows successfully.")
        return df
        
    except Exception as e:
        print(f"Error during Extraction: {e}")
        sys.exit(1)

# ==========================================
# 2. TRANSFORM (8 Marks - Cleaning & Logic)
# ==========================================
def transform_data(df):
    """
    Cleans data, handles outliers, and creates dimension attributes.
    """
    print(f"[{datetime.now()}] --- TRANSFORM: Cleaning and Processing ---")
    
    try:
        # Convert Date
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        
        # Handle Outliers (Quantity/Price <= 0)
        initial_count = len(df)
        df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)].copy()
        print(f"[{datetime.now()}] Dropped {initial_count - len(df)} invalid rows (returns/errors).")
        
        # Calculate Measure: Total Sales
        df['TotalSales'] = df['Quantity'] * df['UnitPrice']
        
        # Create Time Dimension Attributes
        df['Year'] = df['InvoiceDate'].dt.year
        df['Quarter'] = df['InvoiceDate'].dt.quarter
        df['Month'] = df['InvoiceDate'].dt.month
        df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()
        df['TimeID'] = df['InvoiceDate'].dt.strftime('%Y%m%d').astype(int)
        
        # Filter for "Last Year" (Assume Current Date is 2025-08-12)
        cutoff_date = pd.Timestamp("2024-08-12")
        df_recent = df[df['InvoiceDate'] >= cutoff_date].copy()
        
        print(f"[{datetime.now()}] Transformation Complete. Rows to load: {len(df_recent)}")
        return df_recent

    except Exception as e:
        print(f"Error during Transformation: {e}")
        sys.exit(1)

# ==========================================
# 3. LOAD (6 Marks - Database Loading)
# ==========================================
def load_to_warehouse(df, db_name='retail_dw.db'):
    """
    Loads data into SQLite Star Schema. 
    Includes Error Handling for Database Constraints (4 Marks).
    """
    print(f"[{datetime.now()}] --- LOAD: Writing to {db_name} ---")
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        # Define Schema (Idempotent: Drops/Creates fresh every run)
        cursor.executescript("""
            DROP TABLE IF EXISTS SalesFact;
            DROP TABLE IF EXISTS CustomerDim;
            DROP TABLE IF EXISTS ProductDim;
            DROP TABLE IF EXISTS TimeDim;

            CREATE TABLE CustomerDim (
                CustomerID INTEGER PRIMARY KEY,
                Country TEXT
            );
            CREATE TABLE ProductDim (
                StockCode TEXT PRIMARY KEY,
                Category TEXT,
                UnitPrice REAL
            );
            CREATE TABLE TimeDim (
                TimeID INTEGER PRIMARY KEY,
                Date DATE,
                Year INTEGER,
                Quarter INTEGER,
                Month INTEGER,
                DayOfWeek TEXT
            );
            CREATE TABLE SalesFact (
                SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
                CustomerID INTEGER,
                StockCode TEXT,
                TimeID INTEGER,
                Quantity INTEGER,
                TotalSales REAL,
                FOREIGN KEY(CustomerID) REFERENCES CustomerDim(CustomerID),
                FOREIGN KEY(StockCode) REFERENCES ProductDim(StockCode),
                FOREIGN KEY(TimeID) REFERENCES TimeDim(TimeID)
            );
        """)

        # --- A. Load CustomerDim ---
        cust_df = df[['CustomerID', 'Country']].drop_duplicates(subset=['CustomerID'])
        cust_df.set_index('CustomerID', inplace=True)
        cust_df.to_sql('CustomerDim', conn, if_exists='append', index=True)
        print(f"Loaded {len(cust_df)} rows into CustomerDim")

        # --- B. Load ProductDim ---
        prod_df = df[['StockCode', 'Category', 'UnitPrice']].drop_duplicates(subset=['StockCode'])
        prod_df.set_index('StockCode', inplace=True)
        prod_df.to_sql('ProductDim', conn, if_exists='append', index=True)
        print(f"Loaded {len(prod_df)} rows into ProductDim")

        # --- C. Load TimeDim ---
        time_df = df[['TimeID', 'InvoiceDate', 'Year', 'Quarter', 'Month', 'DayOfWeek']].drop_duplicates(subset=['TimeID'])
        time_df = time_df.rename(columns={'InvoiceDate': 'Date'})
        time_df.set_index('TimeID', inplace=True)
        time_df.to_sql('TimeDim', conn, if_exists='append', index=True)
        print(f"Loaded {len(time_df)} rows into TimeDim")

        # --- D. Load SalesFact ---
        fact_df = df[['CustomerID', 'StockCode', 'TimeID', 'Quantity', 'TotalSales']]
        fact_df.to_sql('SalesFact', conn, if_exists='append', index=False)
        print(f"Loaded {len(fact_df)} rows into SalesFact")
        
        conn.commit()
        print(f"[{datetime.now()}] --- ETL Process Completed Successfully ---")

    except sqlite3.IntegrityError as e:
        print(f"Database Integrity Error: {e}")
        conn.rollback()
    except Exception as e:
        print(f"General Database Error: {e}")
        conn.rollback()
    finally:
        conn.close()

# ==========================================
# 4. VERIFY (Shows Table Contents for Exam)
# ==========================================
def verify_and_display_data(db_name='retail_dw.db'):
    """
    Connects to the database and prints the top 5 rows of each table.
    Use this output for your 'post-load' screenshots.
    """
    print(f"\n[{datetime.now()}] === VERIFICATION: Displaying Top 5 Rows of Each Table ===")
    
    conn = sqlite3.connect(db_name)
    pd.set_option('display.max_columns', None) # Ensure all columns are visible
    pd.set_option('display.width', 1000)
    
    tables = ['CustomerDim', 'ProductDim', 'TimeDim', 'SalesFact']
    
    for table in tables:
        print(f"\n--- Table: {table} (Top 5 Rows) ---")
        try:
            df = pd.read_sql(f"SELECT * FROM {table} LIMIT 5", conn)
            print(df)
        except Exception as e:
            print(f"Could not read {table}: {e}")
            
    conn.close()

if __name__ == "__main__":
    # 1. Run Pipeline
    data = generate_retail_data()
    clean_data = transform_data(data)
    load_to_warehouse(clean_data)
    
    # 2. Show Results (Take Screenshot of this part!)
    verify_and_display_data()



conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute("CREATE TABLE CustomerDim (CustomerID INTEGER, Country TEXT)")
c.execute("CREATE TABLE TimeDim (TimeID INTEGER, Year INTEGER, Quarter INTEGER)")
c.execute("CREATE TABLE SalesFact (CustomerID INTEGER, TimeID INTEGER, TotalSales REAL)")

# Mock Data
c.execute("INSERT INTO CustomerDim VALUES (1, 'UK'), (2, 'France'), (3, 'UK')")
c.execute("INSERT INTO TimeDim VALUES (101, 2024, 1), (102, 2024, 1)")
c.execute("INSERT INTO SalesFact VALUES (1, 101, 100.0), (2, 102, 200.0), (3, 101, 50.0)")
conn.commit()

# Test the Query Logic
query = """
SELECT 
    c.Country,
    SUM(f.TotalSales) as Total_Revenue
FROM SalesFact f
JOIN CustomerDim c ON f.CustomerID = c.CustomerID
GROUP BY c.Country
ORDER BY Total_Revenue DESC
"""
df = pd.read_sql_query(query, conn)
print(df)

# Test Plotting Logic
plt.figure(figsize=(8, 5))
plt.bar(df['Country'], df['Total_Revenue'], color='skyblue')
plt.title('Total Sales by Country')
plt.xlabel('Country')
plt.ylabel('Revenue')
plt.show()