SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS sales_month,
    SUM(total_amount) AS monthly_sales_amount
FROM
    Orders
GROUP BY
    sales_month
ORDER BY
    sales_month ASC;