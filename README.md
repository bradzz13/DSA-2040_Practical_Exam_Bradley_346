# DSA 2040 Practical Exam Report
# Student Name: Bradley Student ID: 346 Date: 2025-12-12

## Task 1: Data Warehouse Design
For this retail data warehouse, I implemented a Star Schema design consisting of one central fact table (SalesFact) and three dimension tables (CustomerDim, ProductDim, TimeDim).

### Design Rationale (Star vs. Snowflake): 
I chose the Star Schema over the Snowflake Schema because of its simplicity and query performance. 
In a Star Schema, dimensions are denormalized, meaning attributes like "Category" are stored directly in the ProductDim table rather than being split into sub-tables. 
This reduces the number of JOIN operations required during complex analytical queries (OLAP), leading to faster retrieval times.
It is also more intuitive for business analysts to understand when writing ad-hoc SQL queries.

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/d13563c3-1610-433f-8254-539f9cbb6595" />

## Task 2: ETL Process Implementation

The ETL (Extract, Transform, Load) pipeline was implemented in Python (etl_retail.py) using synthetic data generation to mimic the UCI Online Retail dataset.

###Extract: 

Generated 1,000 rows of synthetic transactional data, ensuring realistic weighting (e.g., 60% of customers located in the UK).

### Transform:

Cleaning: Removed invalid rows (Quantity $\le$ 0) to handle returns and errors4.

Enrichment: Calculated TotalSales (Quantity * UnitPrice) and derived time-based attributes (Year, Quarter, Month) from the invoice date5.

Filtering: Filtered data to strictly include sales from the last year (relative to the exam date of Aug 12, 2025)6.

Load: Loaded the processed data into an SQLite database (retail_dw.db). 

I implemented error handling using drop_duplicates to strictly enforce Unique Constraints on Primary Keys, preventing IntegrityError crashes7.


Task 3: OLAP Analysis & Insights

Using SQL queries on the data warehouse, the following insights were derived:

Top Performing Region (Roll-up Analysis): The aggregation of sales by Country and Quarter reveals that the United Kingdom is consistently the highest revenue-generating region.

This aligns with the data generation logic where the majority of the customer base is UK-centric. Strategic inventory decisions should prioritize UK distribution centers.

Seasonal Trends (Drill-down Analysis): Drilling down into the UK market by month highlights fluctuations in sales volume. 

This granular view supports inventory planning, allowing the company to stock up ahead of identified peak months.

Category Performance (Slice Analysis): Slicing the data for the 'Electronics' category shows it is a high-value segment.

The ratio of TotalSales to Number_Of_Transactions in this category suggests a high average basket size, indicating it is a prime target for premium marketing campaigns

<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/d149c2b4-fcd7-43b4-9734-f3d3d9b9b8a7" />


# Section 2: Data Mining
Task 1: Preprocessing & Exploration
The Iris dataset was loaded and split into training (80%) and testing (20%) sets.

Features were normalized using Min-Max scaling to ensure distance-based algorithms (like KNN and K-Means) perform optimally.

Exploratory Data Analysis (EDA) using Pairplots revealed that the Setosa species is linearly separable from the others, while Versicolor and Virginica show some overlap in feature space.


Task 2: Clustering Analysis (K-Means)

I applied K-Means clustering to the unlabeled feature data.

<img width="1366" height="655" alt="image" src="https://github.com/user-attachments/assets/689468e5-f273-425f-95fa-b31382fcb5a8" />

Optimal K:
The Elbow Method (plot included in submission) showed a distinct "elbow" at k=3, validating that the data naturally groups into 3 clusters, which corresponds to the 3 actual species of Iris.

<img width="1366" height="655" alt="image" src="https://github.com/user-attachments/assets/cf11a424-f6a6-4900-b4e6-55176e8bc880" />


Cluster Quality: The model achieved a high Adjusted Rand Index (ARI), indicating strong agreement between the discovered clusters and the ground truth labels.

Misclassifications: Misclassifications were primarily observed between Versicolor and Virginica due to their similar petal dimensions.

Application: In a real-world retail context, similar clustering techniques could be used for Customer Segmentation, grouping buyers based on spending habits (e.g., "High Spenders", "Discount Hunters") to tailor marketing strategies.


Task 3: Classification & Association Rules

Part A: Classification (Decision Tree vs. KNN) I compared a Decision Tree (Entropy-based) against K-Nearest Neighbors (k=5).

Performance: Both models achieved an identical Accuracy of 96.67%, misclassifying only 1 instance each on the test set.

<img width="640" height="547" alt="image" src="https://github.com/user-attachments/assets/963d260e-db01-4fb3-a171-c343de693c42" />

<img width="640" height="547" alt="image" src="https://github.com/user-attachments/assets/14d714c4-9c64-4111-9702-e4c0307ee631" />

Verdict: The Decision Tree is determined to be the better model for this specific use case. 

<img width="950" height="658" alt="image" src="https://github.com/user-attachments/assets/1a683d1a-a719-4085-b1d6-f56208daa6e6" />

Its interpretable nature allows biologists or analysts to clearly visualize the "rules" (e.g., Petal Width < 0.8 cm) that define a species. KNN, while accurate, operates as a "black box" based on distance, offering less explanatory power.

Part B: Association Rule Mining (Apriori) Using synthetic market basket data, I identified strong purchasing patterns. 

The top rule found was:
Rule: (Bread, Yogurt) -> (Milk)

Lift: 1.53

Confidence: ~70%

Interpretation: Customers who buy Bread and Yogurt are 1.53 times more likely to buy Milk than the average customer.

This strong correlation suggests these items form a "Breakfast Bundle."

Actionable Insight: The store should place these items in close proximity or run cross-promotions (e.g., "Buy Bread & Yogurt, get 10% off Milk") to increase basket size.

