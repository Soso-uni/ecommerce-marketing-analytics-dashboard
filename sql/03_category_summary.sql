CREATE OR REPLACE TABLE category_summary AS

WITH category_base AS (
    SELECT
        main_product_category,
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(DISTINCT customer_unique_id) AS total_customers,
        SUM(revenue) AS total_revenue,
        SUM(freight_value) AS total_freight,
        SUM(order_value) AS total_order_value,
        AVG(order_value) AS avg_order_value,
        AVG(revenue) AS avg_revenue_per_order,
        AVG(review_score) AS avg_review_score,
        AVG(delivery_days) AS avg_delivery_days,
        AVG(estimated_delivery_days) AS avg_estimated_delivery_days,
        AVG(delay_days) AS avg_delay_days,
        AVG(CASE WHEN is_delayed THEN 1 ELSE 0 END) AS delay_rate,
        SUM(item_count) AS total_items_sold,
        AVG(item_count) AS avg_items_per_order,
        COUNT(DISTINCT customer_state) AS state_count
    FROM order_master
    WHERE main_product_category IS NOT NULL
    GROUP BY main_product_category
),

category_ranked AS (
    SELECT
        *,
        RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank,
        RANK() OVER (ORDER BY total_orders DESC) AS order_rank,
        RANK() OVER (ORDER BY avg_review_score DESC NULLS LAST) AS review_rank,
        RANK() OVER (ORDER BY delay_rate DESC NULLS LAST) AS delay_risk_rank
    FROM category_base
)

SELECT
    main_product_category,
    total_orders,
    total_customers,
    total_revenue,
    total_freight,
    total_order_value,
    avg_order_value,
    avg_revenue_per_order,
    avg_review_score,
    avg_delivery_days,
    avg_estimated_delivery_days,
    avg_delay_days,
    delay_rate,
    total_items_sold,
    avg_items_per_order,
    state_count,
    revenue_rank,
    order_rank,
    review_rank,
    delay_risk_rank
FROM category_ranked;