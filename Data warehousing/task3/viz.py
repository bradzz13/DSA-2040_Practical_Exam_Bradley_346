import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the Warehouse
conn = sqlite3.connect('../Task_2_ETL/retail_dw.db') 

# 1. Execute Query: Total Sales by Country
query = """
SELECT 
    c.Country,
    SUM(f.TotalSales) as Total_Revenue
FROM SalesFact f
JOIN CustomerDim c ON f.CustomerID = c.CustomerID
GROUP BY c.Country
ORDER BY Total_Revenue DESC
"""

df = pd.read_sql(query, conn)

# 2. Visualize (Bar Chart)
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Country', y='Total_Revenue', palette='viridis')

plt.title('Total Sales by Country (OLAP Roll-up)', fontsize=14)
plt.xlabel('Country')
plt.ylabel('Total Revenue ($)')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save for submission
plt.savefig('sales_by_country_viz.png')
print("Visualization saved as 'sales_by_country_viz.png'")
plt.show()

conn.close()