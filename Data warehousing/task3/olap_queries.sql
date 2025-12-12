-- DSA 2040 Exam - Section 1, Task 3: OLAP Queries

-- QUERY 1: ROLL-UP (Total Sales by Country and Quarter)
-- Explanation: We aggregate (roll-up) from individual sales to broader Country/Quarter view.
SELECT 
    c.Country,
    t.Year,
    t.Quarter,
    SUM(f.TotalSales) as Total_Revenue
FROM SalesFact f
JOIN CustomerDim c ON f.CustomerID = c.CustomerID
JOIN TimeDim t ON f.TimeID = t.TimeID
GROUP BY c.Country, t.Year, t.Quarter
ORDER BY c.Country, t.Year, t.Quarter;

-- QUERY 2: DRILL-DOWN (Sales details for 'United Kingdom' by Month)
-- Explanation: We go deeper from the country level down to the monthly level for a specific region.
SELECT 
    t.Month,
    SUM(f.Quantity) as Total_Quantity_Sold,
    SUM(f.TotalSales) as Monthly_Revenue
FROM SalesFact f
JOIN CustomerDim c ON f.CustomerID = c.CustomerID
JOIN TimeDim t ON f.TimeID = t.TimeID
WHERE c.Country = 'United Kingdom'
GROUP BY t.Month
ORDER BY t.Month;

-- QUERY 3: SLICE (Total Sales for 'Electronics' Category)
-- Explanation: We "slice" the cube to look ONLY at one specific dimension value (Electronics).
SELECT 
    p.Category,
    SUM(f.TotalSales) as Electronics_Revenue,
    COUNT(*) as Number_Of_Transactions
FROM SalesFact f
JOIN ProductDim p ON f.StockCode = p.StockCode
WHERE p.Category = 'Electronics'
GROUP BY p.Category;