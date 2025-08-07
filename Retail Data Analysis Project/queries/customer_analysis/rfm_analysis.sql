SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    DATEDIFF(CURRENT_DATE(), MAX(o.order_date)) AS Recency,
    COUNT(DISTINCT o.order_id) AS Frequency,
    SUM(o.total_amount) AS Monetary
FROM
    Customers c
JOIN
    Orders o ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id, c.first_name, c.last_name
ORDER BY
    Recency ASC, Frequency DESC, Monetary DESC;