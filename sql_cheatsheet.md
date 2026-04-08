# SQL Syntax
> Note: This document is based on SQL Server syntax. Other databases may differ slightly.
## Basic Query

```sql
SELECT TOP 50 *
FROM table
ORDER BY created_date DESC;
```

## COUNT

```sql
SELECT COUNT(*)
FROM table;
```
- COUNT(*) = count all rows
- COUNT(column) = count non-null values

## Date Handling (DATEDIFF)
```sql
SELECT DATEDIFF(day, start_date, end_date) AS diff_days
FROM table;
```

### Parameter Values

| Parameter    | Description |
|--------------|------------|
| interval     | Possible values:<br>year, yyyy, yy<br>quarter, qq, q<br>month, mm, m<br>dayofyear<br>day, dy, y<br>week, ww, wk<br>weekday, dw, w<br>hour, hh<br>minute, mi, n<br>second, ss, s<br>millisecond, ms |
| date1, date2 | Required. The two dates to calculate the difference between |


## Date Handling (DATEADD)

```sql
SELECT DATEADD(day, 7, order_date)
FROM table;
```

### Parameter Values

| Parameter | Description |
|----------|-------------|
| interval | Possible values:<br>year, yyyy, yy<br>quarter, qq, q<br>month, mm, m<br>dayofyear, dy, y<br>day, d<br>week, ww, wk<br>weekday, dw, w<br>hour, hh<br>minute, mi, n<br>second, ss, s<br>millisecond, ms |
| number   | Required. The number of intervals to add. |
| date     | Required. The date to be modified |

### Common Usage

```sql
SELECT DATEADD(day, -7, GETDATE());
```

- get the date 7 days ago
- negative value → go back in time
- positive value → go forward

## CASE WHEN

```sql
SELECT 
    column1,
    CASE 
        WHEN condition1 THEN result1
        WHEN condition2 THEN result2
        ELSE result
    END AS new_column
FROM table;
```
- CASE WHEN = conditional logic (like if-else in SQL)
- 
## CAST AS DATE

```sql
SELECT CAST(datetime_column AS DATE)
FROM table;
```
- remove time part from datetime
- keep only date (yyyy-mm-dd)
- The most basic one in date formating

## Date Format (CONVERT)

### Syntax

```sql
CONVERT(VARCHAR, date, style)
```

### Common Formats

| Style | Format     | Example   |
|-------|------------|-----------|
| 1     | mm/dd/yy   | 12/30/22  |
| 2     | yy.mm.dd   | 22.12.30  |
| 3     | dd/mm/yy   | 30/12/22  |
| 4     | dd.mm.yy   | 30.12.22  |
| 5     | dd-mm-yy   | 30-12-22  |
| 6     | dd Mon yy  | 30 Dec 22 |
| 7     | Mon dd, yy | Dec 30, 22|
| 10    | mm-dd-yy   | 12-30-22  |
| 11    | yy/mm/dd   | 22/12/30  |
| 12    | yymmdd     | 221230    |
| 23    | yyyy-mm-dd | 2024-01-01|


## FORMAT

```sql
SELECT FORMAT(date, 'yyyy-MM-dd')
```

- FORMAT = convert date/number to a custom string format
- use format string (not style number)

### Common Usage
```sql
SELECT FORMAT(GETDATE(), 'yyyy-MM')
```
extract year-month
```sql
SELECT FORMAT(GETDATE(), 'dd/MM/yyyy')
```
change display format
### Notes
- very flexible (you control the format)
- slower than CONVERT → avoid in large queries

## ISNULL

```sql
SELECT ISNULL(stk.stk_physical, 0) AS stock
FROM stock stk;
```
- ISNULL(value, replacement)
- replace NULL with a default value

## COALESCE

```sql
SELECT COALESCE(phone, mobile, 'N/A')
FROM customers;
```
- return the first non-null value
- evaluated from left to right

## JOIN Overview

- JOIN = combine rows from two tables based on a related column  

### Types of JOIN

- INNER JOIN → return only matching rows  

- LEFT JOIN → return all rows from left table + matched rows from right  

- RIGHT JOIN → return all rows from right table + matched rows from left  

- FULL OUTER JOIN → return all rows from both tables  

- SELF JOIN → join a table with itself
  
```sql
SELECT e.name, m.name AS manager_name
FROM employees e
LEFT JOIN employees m
ON e.manager_id = m.id;
```

- CROSS JOIN → combine every row from A with every row from B
  
```sql
SELECT *
FROM colors
CROSS JOIN sizes;

generate all possible combinations

- JOIN Same Table Multiple Times → join the same table multiple times using different aliases

```sql
SELECT o.id, c1.name AS customer_name, c2.name AS referrer_name
FROM orders o
LEFT JOIN customers c1 ON o.customer_id = c1.id
LEFT JOIN customers c2 ON o.referrer_id = c2.id;
```

## WHERE EXISTS

```sql
SELECT SupplierName
FROM Suppliers
WHERE EXISTS (
  SELECT ProductName
  FROM Products
  WHERE Products.SupplierID = Suppliers.supplierID AND Price = 22
);
```
- EXISTS = check if related data exists
- returns rows from A only if match found in B

## GROUP BY

```sql
SELECT Country, COUNT(CustomerID) AS [Number of Customers]
FROM Customers
GROUP BY Country
ORDER BY COUNT(CustomerID) DESC;
```
group rows, then apply aggregation

## HAVING

```sql
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5;
```
- WHERE → filter before grouping
- HAVING → filter after grouping

## Window Functions in SQL

### Basic Syntax

```sql
SELECT column_name1, 
       window_function(column_name2) 
       OVER ([PARTITION BY column_name3] [ORDER BY column_name4]) AS new_column
FROM table_name;
```
- PARTITION BY = divide data into groups
- ORDER BY = define order within each group

### Aggregate Window Functions

- `SUM()` → sum values within a window  
- `AVG()` → calculate average within a window  
- `COUNT()` → count rows within a window  
- `MAX()` → get maximum value in the window  
- `MIN()` → get minimum value in the window  

---

### Example
```sql
SELECT 
    customer_id,
    order_date,
    SUM(amount) OVER (PARTITION BY customer_id) AS total_spent
FROM orders;
```

### Ranking Window Functions

- `RANK()` → assign rank, with gaps for duplicates  
- `DENSE_RANK()` → assign rank, no gaps  
- `ROW_NUMBER()` → assign unique number to each row  
- `PERCENT_RANK()` → show relative rank between 0 and 1  

---

### Example
```sql
SELECT 
    Name,
    Department,
    Salary,
    RANK() OVER (
        PARTITION BY Department 
        ORDER BY Salary DESC
    ) AS emp_rank
FROM employee;
```

Users who have logged in for three consecutive days:
```sql
WITH t AS (
    SELECT 
        user_id,
        CAST(login_date AS DATE) AS login_date
    FROM customer
    GROUP BY user_id, CAST(login_date AS DATE)  
),

t2 AS (
    SELECT 
        user_id,
        login_date,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM t
),

t3 AS (
    SELECT 
        user_id,
        login_date,
        DATEADD(DAY, -rn, login_date) AS grp
    FROM t2
)

SELECT 
    user_id
FROM t3
GROUP BY user_id, grp
HAVING COUNT(*) >= 3
```

Find users who have logged in for at least 4 consecutive days within the last 14 days
```sql
WITH t AS (
    -- Step 1: Filter last 14 days and remove duplicates (one login per day per user)
    SELECT 
        user_id,
        CAST(login_date AS DATE) AS login_date
    FROM your_table
    WHERE login_date >= DATEADD(DAY, -13, CAST(GETDATE() AS DATE))
    GROUP BY user_id, CAST(login_date AS DATE)
),

t2 AS (
    -- Step 2: Assign row numbers ordered by login date for each user
    SELECT 
        user_id,
        login_date,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
    FROM t
),

t3 AS (
    -- Step 3: Shift dates by row number to identify consecutive sequences
    SELECT 
        user_id,
        login_date,
        DATEADD(DAY, -rn, login_date) AS grp
    FROM t2
)

-- Step 4: Group by user and sequence, keep users with at least 4 consecutive days
SELECT DISTINCT user_id
FROM t3
GROUP BY user_id, grp
HAVING COUNT(*) >= 4;
```


## CTE (Common Table Expression)

### Basic Syntax

```sql
WITH cte AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY POD_STOCK_CODE 
               ORDER BY POD_DATE DESC  
           ) AS rn
    FROM POP_DETAIL
)
SELECT 
    POD_STOCK_CODE,
suname
FROM cte
join pl_accounts on sucode=  POD_ACCOUNT
--join STK_LINK_ITEMS 
--    ON SUBSTRING(LINK_PARENT, 2, LEN(LINK_PARENT)) = STKCODE
WHERE rn = 1
```


## Database Modification

### CREATE TABLE

```sql
CREATE TABLE table_name (
    column1 datatype,
    column2 datatype
);
```

## SQL Constraints

- constraints = rules to control data in a table  
- prevent invalid data  
- ensure data accuracy  

---

### Common Constraints

- `NOT NULL` → column cannot be NULL  

- `UNIQUE` → all values must be different  

- `PRIMARY KEY` → unique identifier (NOT NULL + UNIQUE)  

- `FOREIGN KEY` → link between tables  

- `CHECK` → enforce condition (e.g. age > 0)  

- `DEFAULT` → set default value  

---

### Example

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    age INT CHECK (age >= 0),
    created_date DATE DEFAULT GETDATE()
);
```

### INSERT
```sql
INSERT INTO table_name (column1, column2)
VALUES (value1, value2);
insert new rows
```

### UPDATE
```sql
UPDATE table_name
SET column1 = value1
WHERE condition;
```

### DELETE
```sql
DELETE FROM table_name
WHERE condition;
```

### ALTER TABLE
```sql
ALTER TABLE table_name
ADD column_name datatype;
```

### Drop Column
```sql
ALTER TABLE table_name
DROP COLUMN column_name;
```

### DROP TABLE
```sql
DROP TABLE table_name;
```

### CREATE INDEX

```sql
CREATE INDEX index_name
ON table_name (column1, column2);
```
- create index to speed up data retrieval
- improves query performance










