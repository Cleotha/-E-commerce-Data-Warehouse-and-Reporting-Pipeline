#Create a Python and SQL project that:
#Reads the raw CSV files.
#Validates the column names and data types.
#Cleans duplicates, missing values, invalid dates, and incorrect numeric values.
#Separates rejected records into an errors/ folder with a reason for rejection.
#Transforms the data into warehouse tables.
#Loads the cleaned data into PostgreSQL.
#Runs SQL queries that produce business reports.
#Can be run from one command.
#Includes tests, logging, documentation, and a clear Git history.

import csv
import pandas as pd

def read_csv(filename):
    with open(filename, 'r') as f:
        return list(csv.DictReader(f))

def clean_customers(df):
    df.drop_duplicates(subset = ['customer_id'], inplace = True)
    df['name'] = df['name'].str.strip().str.title()
    df.replace('', pd.NA,inplace = True)
    df['registration_date'] = pd.to_datetime(df['registration_date'], errors = 'coerce', format = 'mixed')
    df.dropna(subset = ['name', 'email', 'phone', 'registration_date'], inplace = True)
    return df

def clean_orders(df):
    df.drop_duplicates(subset = ['order_id'], inplace = True)
    df.replace('', pd.NA,inplace = True)
    df['quantity'] = pd.to_numeric(df['quantity'], errors = 'coerce')
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors = 'coerce')
    df['quantity'] = df['quantity'][df['quantity'] > 0]
    df['unit_price'] = df['unit_price'][df['unit_price'] > 0]
    df['order_date'] = pd.to_datetime(df['order_date'], errors = 'coerce', format = 'mixed')
    df.dropna(subset = ['customer_id', 'quantity', 'unit_price', 'status'], inplace = True)
    return df

def clean_payments(df):
    df.drop_duplicates(subset = ['payment_id'], inplace = True)
    df['payment_date'] = pd.to_datetime(df['payment_date'], errors = 'coerce', format = 'mixed')
    df['amount'] = pd.to_numeric(df['amount'], errors = 'coerce')
    df['amount'] = df['amount'][df['amount'] > 0]
    df.dropna(subset = ['amount'], inplace = True)
    return df

def clean_products(df):
    df.drop_duplicates(subset = ['product_id'], inplace = True)
    df['stock_quantity'] = pd.to_numeric(df['stock_quantity'], errors = 'coerce')
    df['price'] = pd.to_numeric(df['price'], errors = 'coerce')
    df['price'] = df['price'][df['price'] > 0]
    df.dropna(subset = ['product_name', 'price', 'stock_quantity'], inplace = True)
    return df

def handle_order_errors(customers, orders):
    valid_orders = []
    error_orders = []
    valid_orders = orders[orders['customer_id'].isin(customers['customer_id'])]
    error_orders = orders[~orders['customer_id'].isin(customers['customer_id'])]
    return f"VALID ORDERS", valid_orders, "MISSING CUSTOMER ID/CANCELLED ORDER", error_orders

def handle_payment_errors(orders, payments):
    valid_payments = []
    error_payments = []
    valid_payments = payments[(payments['order_id'].isin(orders['order_id'])) & (payments['payment_status'].str.lower() == 'successful')]
    error_payments = payments[(~payments['order_id'].isin(orders['order_id'])) | (payments['payment_status'].str.lower() != 'successful')]
    return f"VALID PAYMENTS", valid_payments, "MISSING ORDER ID/UNSUCCESSFUL PAYMENT", error_payments

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

def load_to_postgres(sales):
    load_dotenv()
    engine = create_engine(
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    sales.to_sql('sales', engine, if_exists='replace', index=False)
    print("✅ Loaded to PostgreSQL!")
""

def run_pipeline():
    print("Extracting...")
    raw_customers = read_csv('/Users/Marydoris/Cleotha/ E-commerce Data Warehouse and Reporting Pipeline/customers.csv')
    raw_orders = read_csv('/Users/Marydoris/Cleotha/ E-commerce Data Warehouse and Reporting Pipeline/orders.csv')
    raw_payments = read_csv('/Users/Marydoris/Cleotha/ E-commerce Data Warehouse and Reporting Pipeline/payments.csv')
    raw_products = read_csv('/Users/Marydoris/Cleotha/ E-commerce Data Warehouse and Reporting Pipeline/products.csv')


    print("Cleaning...")
    customers = clean_customers(pd.DataFrame(raw_customers))
    orders = clean_orders(pd.DataFrame(raw_orders))
    payments = clean_payments(pd.DataFrame(raw_payments))
    products = clean_products(pd.DataFrame(raw_products))
    print('customers')
    print(customers)
    print('orders')
    print(orders)
    print('payments')
    print(payments)
    print('products')
    print(products)

    print("Cleaning errors...")
    order_error = handle_order_errors(customers, orders)
    payment_error = handle_payment_errors(orders, payments)
    print("\n")
    print(order_error)
    print("\n")
    print(payment_error)

    print("Loading...")
#    load_to_postgres()

    print("🎉 Pipeline complete!")
run_pipeline()
