import psycopg2
import pandas as pd
import streamlit as st

# Connection parameters for PostgreSQL
db_params = {
    'host': 'localhost',      
    'port': '5432',           
    'dbname': 'Retail_orders',
    'user': 'postgres',
    'password': '12345'
}

def get_db_connection(): #functions for the connection
    conn = psycopg2.connect(**db_params)
    return conn
def query_data(query): #function to fetch the data from database
    conn = get_db_connection()
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

st.title("Retail order analysis")

query_choice = st.selectbox("Select query:", ["Find top 10 highest revenue generating products", "Find the top 5 cities with the highest profit marginsy", "Calculate the total discount given for each category", "Find the average sale price per product category", "Find the region with the highest average sale price", "Find the total profit per category", "Identify the top 3 segments with the highest quantity of orders", "Determine the average discount percentage given per region", "Find the product category with the highest total profit", "Calculate the total revenue generated per year"])#dropdowns

queries = {
    "Find top 10 highest revenue generating products": "SELECT product_id, SUM(sale_price*quantity) as total_revenue FROM orders_table2 Group by product_id ORDER BY total_revenue DESC LIMIT 10;", 
    "Find the top 5 cities with the highest profit marginsy": "SELECT orders_table1.city, SUM(orders_table2.profit) AS total_profit FROM orders_table1 JOIN orders_table2 ON orders_table1.category = orders_table2.category GROUP BY orders_table1.city ORDER BY total_profit DESC LIMIT 5;", 
    "Calculate the total discount given for each category": "SELECT category,	SUM(discount) AS total_discount FROM orders_table2 GROUP BY category;", 
    "Find the average sale price per product category": "SELECT category,	AVG(sale_price) AS average_sale_price FROM orders_table2 GROUP BY category;", 
    "Find the region with the highest average sale price": "SELECT orders_table1.region,	AVG(orders_table2.sale_price) AS average_sale_price FROM orders_table1 JOIN orders_table2 ON orders_table1.category = orders_table2.category GROUP BY orders_table1.region ORDER BY average_sale_price DESC LIMIT 4;", 
    "Find the total profit per category": "SELECT category,	SUM(profit) AS total_profit FROM orders_table2 Group by category;", 
    "Identify the top 3 segments with the highest quantity of orders": "SELECT orders_table1.segment,	SUM(orders_table2.quantity) AS total_quantity FROM orders_table1 JOIN orders_table2 ON orders_table1.category = orders_table2.category GROUP BY orders_table1.segment ORDER BY total_quantity DESC LIMIT 3;", 
    "Determine the average discount percentage given per region": "SELECT orders_table1.region,	AVG(orders_table2.discount_percent) AS average_discount_percent FROM orders_table1 JOIN orders_table2 ON orders_table1.category=orders_table2.category Group by orders_table1.region;", 
    "Find the product category with the highest total profit": "SELECT category,	SUM(profit) AS total_profit FROM orders_table2 GROUP BY category ORDER BY total_profit DESC LIMIT 1;", 
    "Calculate the total revenue generated per year": "SELECT   EXTRACT(YEAR FROM orders_table1.order_date) AS order_year, SUM(orders_table2.sale_price*orders_table2.quantity) AS total_revenue FROM orders_table1 JOIN orders_table2 ON orders_table1.category=orders_table2.category GROUP BY order_year ORDER BY total_revenue DESC;"
} #provided the SQL queries

selected_query = queries[query_choice] #selecting the SQL query based on the dropdown

data = query_data(selected_query)
#query for output
st.write(f"Results for: {query_choice}")
st.write(data)

