# E-commerce Data Warehouse & Reporting Pipeline

A Python and PostgreSQL data engineering project that processes raw e-commerce data, cleans and validates it, separates rejected records, transforms the data, and loads the cleaned data into PostgreSQL for analysis and reporting.

## 📌 Project Overview

This project demonstrates a simple end-to-end data engineering pipeline using Python, Pandas, and PostgreSQL.

The pipeline takes raw CSV files containing customer, product, order, and payment data and processes them through several stages:

```text
Raw CSV Files
     ↓
Extraction
     ↓
Data Cleaning
     ↓
Data Validation
     ↓
Error Handling
     ↓
Transformation
     ↓
PostgreSQL
     ↓
SQL Reporting
```

The raw datasets intentionally contain issues such as duplicates, missing values, invalid dates, incorrect numeric values, cancelled orders, unsuccessful payments, and invalid relationships between tables.

## 🎯 Project Objectives

The pipeline is designed to:

* Read raw CSV files.
* Clean and standardize the data.
* Remove duplicate records.
* Handle missing and invalid values.
* Validate relationships between datasets.
* Separate rejected records from valid records.
* Record reasons for rejected records.
* Save rejected records in an `errors/` folder.
* Transform order data for analysis.
* Load cleaned data into PostgreSQL.
* Provide a foundation for SQL-based business reporting.
* Run the entire pipeline from one command.

## 🛠️ Technologies Used

* **Python**
* **Pandas**
* **CSV**
* **SQLAlchemy**
* **PostgreSQL**
* **python-dotenv**
* **Git & GitHub**

## 📂 Project Structure

```text
E-commerce Data Warehouse and Reporting Pipeline/
│
├── customers.csv
├── products.csv
├── orders.csv
├── payments.csv
├── script.py
├── .env
├── requirements.txt
│
└── errors/
    ├── orders_errors.csv
    └── payments_errors.csv
```

## 📊 Source Data

The pipeline processes four datasets:

### Customers

Contains customer information such as:

* Customer ID
* Name
* Email
* Phone
* Registration date
* City

### Products

Contains:

* Product ID
* Product name
* Category
* Price
* Stock quantity

### Orders

Contains:

* Order ID
* Customer ID
* Product ID
* Order date
* Quantity
* Unit price
* Order status

### Payments

Contains:

* Payment ID
* Order ID
* Payment date
* Amount
* Payment method
* Payment status

## 🧹 Data Cleaning

Each dataset goes through its own cleaning process.

### Customers

The pipeline:

* Removes duplicate customer IDs.
* Removes unnecessary whitespace from names.
* Standardizes names using title case.
* Converts empty values to missing values.
* Converts registration dates to datetime.
* Removes records missing important customer information.

### Products

The pipeline:

* Removes duplicate product IDs.
* Converts price and stock quantity to numeric values.
* Removes invalid/non-positive prices.
* Removes records missing required product information.

### Orders

The pipeline:

* Removes duplicate order IDs.
* Converts quantity and unit price to numeric values.
* Removes invalid/non-positive quantities and prices.
* Converts order dates to datetime.
* Removes records missing required fields.

### Payments

The pipeline:

* Removes duplicate payment IDs.
* Converts payment dates to datetime.
* Converts payment amounts to numeric values.
* Removes invalid/non-positive payment amounts.

## 🚨 Error Handling

After cleaning, the pipeline validates relationships between the datasets.

For orders, it checks whether:

```text
orders.customer_id → customers.customer_id
orders.product_id  → products.product_id
```

For payments, it checks whether:

```text
payments.order_id → valid_orders.order_id
```

Rejected records are given an `error_reason` explaining why they were rejected.

Examples include:

```text
MISSING CUSTOMER ID
MISSING PRODUCT ID
MISSING ORDER ID
UNSUCCESSFUL PAYMENT
CANCELLED ORDERS
```

The rejected records are automatically saved to:

```text
errors/orders_errors.csv
errors/payments_errors.csv
```

The `errors/` folder is created automatically when the pipeline runs.

## 🔄 Transformation

Valid order data is transformed to create a `total_amount` field:

```text
total_amount = quantity × unit_price
```

This creates a value that can be used for revenue and sales analysis.

## 🗄️ PostgreSQL Loading

The cleaned datasets are loaded into PostgreSQL using SQLAlchemy.

The pipeline creates/replaces the following tables:

```text
customers
products
valid_orders
valid_payments
```

Database credentials are stored in a `.env` file rather than being written directly into the Python script.

Example environment variables:

```text
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=your_database
```

## ▶️ Running the Pipeline

Install the required dependencies:

```bash
pip install pandas sqlalchemy psycopg2-binary python-dotenv
```

Make sure PostgreSQL is running and your `.env` file contains the correct database credentials.

Then run:

```bash
python script.py
```

The pipeline runs the following stages:

```text
Extracting...
Cleaning...
Saving errors...
Analyzing...
Loading...
🎉 Pipeline complete!
```

## 📈 Reporting

Once the data has been loaded into PostgreSQL, SQL queries can be used to generate business reports such as:

* Total revenue
* Number of completed orders
* Top-selling products
* Revenue by customer
* Revenue by city
* Monthly sales trends
* Successful vs unsuccessful payments
* Average order value

Example:

```sql
SELECT
    SUM(total_amount) AS total_revenue
FROM valid_orders;
```

## 🔐 Environment Variables

The `.env` file contains database credentials and should **not** be committed to GitHub.

Add it to `.gitignore`:

```text
.env
```

## 🧪 Future Improvements

Possible improvements to the project include:

* Add automated tests with `pytest`.
* Add logging instead of relying only on `print()` statements.
* Add column-name and data-type validation.
* Create separate SQL reporting files.
* Add more detailed error classifications.
* Add automated data quality checks.
* Create a dashboard for the generated reports.
* Improve the project structure by separating extraction, cleaning, transformation, loading, and reporting into different modules.

## 📚 Key Data Engineering Concepts Demonstrated

This project demonstrates practical experience with:

* ETL pipelines
* Data cleaning
* Data validation
* Data quality checks
* Handling rejected records
* Pandas
* CSV processing
* Relational data
* Primary and foreign key relationships
* Data transformation
* PostgreSQL
* SQLAlchemy
* Environment variables
* Automated pipeline execution
* Git/GitHub workflow

## 👩🏽‍💻 Author

Built as part of my data engineering learning journey to practice building an end-to-end data pipeline with Python, PostgreSQL, and SQL.
