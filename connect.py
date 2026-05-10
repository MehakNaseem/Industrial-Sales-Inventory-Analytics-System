import psycopg2
import pandas as pd
conn = psycopg2.connect(
    host="localhost",
    database="industrial_analytics",
    user="postgres",
    password="cs231240",
)
print("connection successful")
#pull data from orders table
query = "SELECT * FROM orders"
df = pd.read_sql(query, conn)

print(df.head())
 #total revenue per customer
query2 = """
SELECT c.customer_name, SUM(o.total_amount) AS total_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'Delivered'
GROUP BY c.customer_name
ORDER BY total_revenue DESC
"""
df2 = pd.read_sql(query2, conn)
print(df2)
import matplotlib.pyplot as plt
import seaborn as sns
#plot revenue per customer
plt.figure(figsize=(10, 6))
sns.barplot(data=df2, x='total_revenue', y='customer_name', palette='viridis')
plt.title('Total Revenue per Customer')
plt.xlabel('Revenue')
plt.ylabel('Customer')
plt.tight_layout()
plt.show()
 #Profit per product query
query3 = """
SELECT p.product_name,
      SUM(o.quantity * (p.unit_price - p.cost_price)) AS total_profit
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'Delivered'
GROUP BY p.product_name
ORDER BY total_profit DESC
"""
df3 = pd.read_sql(query3, conn)

#plot
plt.figure(figsize=(10, 6))
sns.barplot(data=df3, x='total_profit', y='product_name', palette='magma')
plt.title('Total Profit per Product')
plt.xlabel('Profit')
plt.ylabel('Product')
plt.tight_layout()
plt.show()
# Monthly sales trend query
query4 = """
SELECT TO_CHAR(order_date, 'YYYY-MM') AS month,
SUM(total_amount) AS monthly_revenue
FROM orders
WHERE status = 'Delivered'
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY month ASC
"""

df4 = pd.read_sql(query4, conn)

# Plot
plt.figure(figsize=(10, 6))
sns.lineplot(data=df4, x='month', y='monthly_revenue', marker='o', color='green')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.tight_layout()
plt.show()