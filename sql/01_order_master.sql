CREATE OR REPLACE TABLE order_master AS

WITH product_categories AS (
    SELECT
        p.product_id,
        COALESCE(
            ct.product_category_name_english,
            p.product_category_name,
            'unknown'
        ) AS product_category_english
    FROM products AS p
    LEFT JOIN category_translation AS ct
        ON p.product_category_name = ct.product_category_name
),

order_item_detail AS (
    SELECT
        oi.order_id,
        oi.order_item_id,
        oi.product_id,
        oi.seller_id,
        oi.price,
        oi.freight_value,
        pc.product_category_english
    FROM order_items AS oi
    LEFT JOIN product_categories AS pc
        ON oi.product_id = pc.product_id
),

item_summary AS (
    SELECT
        order_id,
        SUM(price) AS revenue,
        SUM(freight_value) AS freight_value,
        SUM(price) + SUM(freight_value) AS order_value,
        COUNT(*) AS item_count,
        COUNT(DISTINCT product_id) AS product_count,
        COUNT(DISTINCT seller_id) AS seller_count
    FROM order_item_detail
    GROUP BY order_id
),

category_counts AS (
    SELECT
        order_id,
        product_category_english,
        COUNT(*) AS category_item_count,
        SUM(price) AS category_revenue
    FROM order_item_detail
    GROUP BY
        order_id,
        product_category_english
),

main_category AS (
    SELECT
        order_id,
        product_category_english AS main_product_category
    FROM (
        SELECT
            order_id,
            product_category_english,
            ROW_NUMBER() OVER (
                PARTITION BY order_id
                ORDER BY
                    category_item_count DESC,
                    category_revenue DESC,
                    product_category_english ASC
            ) AS category_rank
        FROM category_counts
    )
    WHERE category_rank = 1
),

payment_by_type AS (
    SELECT
        order_id,
        payment_type,
        SUM(payment_value) AS payment_type_value
    FROM payments
    GROUP BY
        order_id,
        payment_type
),

main_payment_type AS (
    SELECT
        order_id,
        payment_type
    FROM (
        SELECT
            order_id,
            payment_type,
            ROW_NUMBER() OVER (
                PARTITION BY order_id
                ORDER BY
                    payment_type_value DESC,
                    payment_type ASC
            ) AS payment_type_rank
        FROM payment_by_type
    )
    WHERE payment_type_rank = 1
),

payment_summary AS (
    SELECT
        p.order_id,
        SUM(p.payment_value) AS payment_value,
        mpt.payment_type,
        MAX(p.payment_installments) AS payment_installments,
        COUNT(DISTINCT p.payment_type) AS payment_methods
    FROM payments AS p
    LEFT JOIN main_payment_type AS mpt
        ON p.order_id = mpt.order_id
    GROUP BY
        p.order_id,
        mpt.payment_type
),

review_summary AS (
    SELECT
        order_id,
        AVG(review_score) AS review_score,
        COUNT(DISTINCT review_id) AS review_count
    FROM reviews
    GROUP BY order_id
)

SELECT
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    o.order_status,
    CAST(o.order_purchase_timestamp AS TIMESTAMP) AS order_purchase_timestamp,
    DATE_TRUNC('month', CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS order_month,
    CAST(o.order_delivered_customer_date AS TIMESTAMP) AS order_delivered_customer_date,
    CAST(o.order_estimated_delivery_date AS TIMESTAMP) AS order_estimated_delivery_date,
    i.revenue,
    i.freight_value,
    i.order_value,
    i.item_count,
    i.product_count,
    i.seller_count,
    mc.main_product_category,
    p.payment_value,
    p.payment_type,
    p.payment_installments,
    p.payment_methods,
    r.review_score,
    r.review_count,
    DATE_DIFF(
        'day',
        CAST(o.order_purchase_timestamp AS TIMESTAMP),
        CAST(o.order_delivered_customer_date AS TIMESTAMP)
    ) AS delivery_days,
    DATE_DIFF(
        'day',
        CAST(o.order_purchase_timestamp AS TIMESTAMP),
        CAST(o.order_estimated_delivery_date AS TIMESTAMP)
    ) AS estimated_delivery_days,
    DATE_DIFF(
        'day',
        CAST(o.order_estimated_delivery_date AS TIMESTAMP),
        CAST(o.order_delivered_customer_date AS TIMESTAMP)
    ) AS delay_days,
    DATE_DIFF(
        'day',
        CAST(o.order_estimated_delivery_date AS TIMESTAMP),
        CAST(o.order_delivered_customer_date AS TIMESTAMP)
    ) > 0 AS is_delayed
FROM orders AS o
LEFT JOIN customers AS c
    ON o.customer_id = c.customer_id
LEFT JOIN item_summary AS i
    ON o.order_id = i.order_id
LEFT JOIN main_category AS mc
    ON o.order_id = mc.order_id
LEFT JOIN payment_summary AS p
    ON o.order_id = p.order_id
LEFT JOIN review_summary AS r
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
    AND i.revenue IS NOT NULL;
