-- data checks

SELECT * FROM Supply_chain_dataset

SELECT count(*) FROM Supply_chain_dataset
WHERE sales IS NULL;

--Delivery Days Check
SELECT
MIN(delivery_days),
MAX(delivery_days),
AVG(delivery_days)
FROM Supply_chain_dataset;

--Total Sale
SELECT SUM(sales) FROM Supply_chain_dataset

--Total Profit
SELECT
ROUND(SUM(profit_per_order),2) AS total_profit
FROM Supply_chain_dataset;

--Total Orders
SELECT DISTINCT
COUNT(order_id)
FROM Supply_chain_dataset;

--Total Customers
SELECT DISTINCT
COUNT(customer_id)
FROM Supply_chain_dataset;

--Top 5 Products
SELECT product_name, SUM(sales) AS revenue FROM Supply_chain_dataset
GROUP BY product_name
ORDER BY revenue DESC
OFFSET 0 ROWS
FETCH NEXT 5 ROWS ONLY;

--Top Categories
SELECT category_name, SUM(sales) AS revenue FROM Supply_chain_dataset
GROUP BY category_name
ORDER BY revenue;

--Category Profit
SELECT category_name, ROUND(SUM(profit_per_order),2) AS profit
FROM Supply_chain_dataset
GROUP BY category_name
ORDER BY profit DESC;

--Most Ordered Products
SELECT product_name,SUM(order_item_quantity) AS quantity
FROM Supply_chain_dataset
GROUP BY product_name
ORDER BY quantity DESC;

--Sales by Region
SELECT order_region,ROUND(SUM(sales),2) AS revenue
FROM Supply_chain_dataset
GROUP BY order_region
ORDER BY revenue DESC;

--Top Countries
SELECT customer_country,ROUND(SUM(sales),2) AS revenue
FROM Supply_chain_dataset
GROUP BY customer_country
ORDER BY revenue DESC;

--Delayed Orders
SELECT label,COUNT(*)
FROM Supply_chain_dataset
GROUP BY label;

--Delay Rate
SELECT
ROUND(
100.0 *
SUM(CASE WHEN label = 1 THEN 1 ELSE 0 END)
/ COUNT(*),
2
) AS delay_percentage
FROM Supply_chain_dataset;

--Shipping Mode Performance
SELECT
shipping_mode,
AVG(delivery_days)
FROM Supply_chain_dataset
GROUP BY shipping_mode;

--Average Delivery Days
SELECT shipping_mode,ROUND(AVG(delivery_days),2)
FROM Supply_chain_dataset
GROUP BY shipping_mode;

--Fastest Shipping Method
SELECT shipping_mode,AVG(delivery_days) avg_days
FROM Supply_chain_dataset
GROUP BY shipping_mode
ORDER BY avg_days;

--Monthly Sales
SELECT
    YEAR(order_date) AS year,
    MONTH(order_date) AS month,
    ROUND(SUM(sales), 2) AS revenue
FROM Supply_chain_dataset
GROUP BY YEAR(order_date),MONTH(order_date)
ORDER BY YEAR(order_date),MONTH(order_date);

--Monthly Profit
SELECT
    YEAR(order_date) AS year,
    MONTH(order_date) AS month,
    ROUND(SUM(profit_per_order), 2) AS profit
FROM Supply_chain_dataset
GROUP BY YEAR(order_date),MONTH(order_date)
ORDER BY YEAR(order_date),MONTH(order_date);

--Top Product in Every Category
WITH product_sales AS
(SELECT category_name,product_name,SUM(sales) revenue,
RANK() OVER(PARTITION BY category_name
ORDER BY SUM(sales) DESC) rnk
FROM Supply_chain_dataset
GROUP BY category_name, product_name)
SELECT *
FROM product_sales
WHERE rnk=1;