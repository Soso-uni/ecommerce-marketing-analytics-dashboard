CREATE OR REPLACE TABLE monthly_summary AS

WITH monthly_base AS (
    SELECT
        DATE_TRUNC('month', order_purchase_timestamp) AS order_month,
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
        COUNT(DISTINCT main_product_category) AS active_categories,
        COUNT(DISTINCT customer_state) AS active_states
    FROM order_master
    WHERE order_purchase_timestamp IS NOT NULL
    GROUP BY DATE_TRUNC('month', order_purchase_timestamp)
),

monthly_with_growth AS (
    SELECT
        *,
        LAG(total_revenue) OVER (ORDER BY order_month) AS previous_month_revenue,
        LAG(total_orders) OVER (ORDER BY order_month) AS previous_month_orders,

        total_revenue
            - LAG(total_revenue) OVER (ORDER BY order_month)
            AS revenue_change,

        total_orders
            - LAG(total_orders) OVER (ORDER BY order_month)
            AS order_change,

        CASE
            WHEN LAG(total_revenue) OVER (ORDER BY order_month) IS NULL
                OR LAG(total_revenue) OVER (ORDER BY order_month) = 0
                THEN NULL
            ELSE
                (total_revenue - LAG(total_revenue) OVER (ORDER BY order_month))
                / LAG(total_revenue) OVER (ORDER BY order_month)
        END AS revenue_growth_rate,

        CASE
            WHEN LAG(total_orders) OVER (ORDER BY order_month) IS NULL
                OR LAG(total_orders) OVER (ORDER BY order_month) = 0
                THEN NULL
            ELSE
                (total_orders - LAG(total_orders) OVER (ORDER BY order_month)) * 1.0
                / LAG(total_orders) OVER (ORDER BY order_month)
        END AS order_growth_rate
    FROM monthly_base
)

SELECT
    order_month,
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
    active_categories,
    active_states,
    previous_month_revenue,
    previous_month_orders,
    revenue_change,
    order_change,
    revenue_growth_rate,
    order_growth_rate
FROM monthly_with_growth
ORDER BY order_month;