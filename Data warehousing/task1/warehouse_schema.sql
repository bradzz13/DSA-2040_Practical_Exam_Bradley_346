-- DSA 2040 Exam - Section 1, Task 1: Data Warehouse Design
-- Star Schema Implementation for Retail Company

-- 1. Dimension: Customer
-- Stores attributes about who bought the product
CREATE TABLE CustomerDim (
    CustomerID INTEGER PRIMARY KEY,
    CustomerName TEXT,
    Country TEXT,
    Region TEXT
);

-- 2. Dimension: Product
-- Stores attributes about what was sold (Categories, Names)
CREATE TABLE ProductDim (
    ProductID TEXT PRIMARY KEY,
    ProductName TEXT,
    Category TEXT,
    UnitPrice REAL
);

-- 3. Dimension: Time
-- Stores broken-down dates to allow drilling up/down (Year -> Quarter -> Month)
CREATE TABLE TimeDim (
    TimeID INTEGER PRIMARY KEY, -- Can be formatted like YYYYMMDD
    FullDate DATE,
    Year INTEGER,
    Quarter INTEGER, -- 1, 2, 3, 4
    Month INTEGER,
    DayOfWeek TEXT
);

-- 4. Fact Table: SalesFact
-- Stores the quantitative metrics and links to dimensions
CREATE TABLE SalesFact (
    SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerID INTEGER,
    ProductID TEXT,
    TimeID INTEGER,
    Quantity INTEGER,
    TotalSales REAL, -- Calculated as Quantity * UnitPrice
    
    -- Foreign Key Constraints
    FOREIGN KEY (CustomerID) REFERENCES CustomerDim(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES ProductDim(ProductID),
    FOREIGN KEY (TimeID) REFERENCES TimeDim(TimeID)
);