CREATE OR REPLACE TABLE customer_summary AS

WITH customer_base AS (
    SELECT
        customer_unique_id,
        MIN(order_purchase_timestamp) AS first_purchase_timestamp,
        MAX(order_purchase_timestamp) AS last_purchase_timestamp,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(revenue) AS total_revenue,
        SUM(order_value) AS total_order_value,
        AVG(order_value) AS avg_order_value,
        AVG(review_score) AS avg_review_score,
        AVG(CASE WHEN is_delayed THEN 1 ELSE 0 END) AS delay_rate,
        COUNT(DISTINCT customer_state) AS state_count,
        MODE(customer_state) AS main_customer_state
    FROM order_master
    WHERE customer_unique_id IS NOT NULL
    GROUP BY customer_unique_id
),

customer_metrics AS (
    SELECT
        *,
        DATE_DIFF(
            'day',
            last_purchase_timestamp,
            (SELECT MAX(order_purchase_timestamp) FROM order_master)
        ) AS recency_days,
        CASE
            WHEN total_orders >= 3 THEN 'repeat_customer'
            WHEN total_orders = 2 THEN 'second_order_customer'
            ELSE 'one_time_customer'
        END AS purchase_frequency_group
    FROM customer_base
),

rfm_scores AS (
    SELECT
        *,
        NTILE(5) OVER (
            ORDER BY recency_days DESC, customer_unique_id ASC
        ) AS recency_score,
        CASE
            WHEN total_orders >= 4 THEN 5
            WHEN total_orders = 3 THEN 4
            WHEN total_orders = 2 THEN 3
            ELSE 1
        END AS frequency_score,
        NTILE(5) OVER (
            ORDER BY total_revenue ASC, customer_unique_id ASC
        ) AS monetary_score
    FROM customer_metrics
),

customer_segments AS (
    SELECT
        *,
        recency_score + frequency_score + monetary_score AS rfm_total_score,
        CASE
            WHEN recency_score >= 4
                AND total_orders = 1
                THEN 'New Customers'

            WHEN recency_score >= 3
                AND total_orders >= 4
                THEN 'Loyal Customers'

            WHEN recency_score >= 3
                AND total_orders BETWEEN 2 AND 3
                THEN 'Active Repeat Customers'

            WHEN recency_score <= 2
                AND total_orders >= 2
                THEN 'At Risk Repeat Customers'

            ELSE 'Inactive One-Time Customers'
        END AS customer_lifecycle_segment,

        CASE
            WHEN monetary_score = 5
                THEN 'High Value'

            WHEN monetary_score IN (3, 4)
                THEN 'Mid Value'

            ELSE 'Low Value'
        END AS customer_value_tier,

        CASE
            WHEN recency_score >= 4
                AND total_orders >= 4
                AND monetary_score = 5
                THEN 'Champions'

            WHEN recency_score >= 4
                AND total_orders = 1
                AND monetary_score = 5
                THEN 'New High-Value Customers'

            WHEN recency_score <= 2
                AND total_orders >= 2
                THEN 'At Risk Repeat Customers'

            WHEN total_orders >= 4
                AND monetary_score = 5
                THEN 'High-Value Repeat Customers'

            WHEN total_orders BETWEEN 2 AND 3
                AND monetary_score = 5
                THEN 'High-Value Occasional Customers'

            WHEN recency_score <= 2
                AND total_orders = 1
                THEN 'Inactive One-Time Customers'

            WHEN recency_score >= 4
                AND total_orders = 1
                THEN 'New or Recent Customers'

            WHEN total_orders >= 2
                THEN 'Active Repeat Customers'

            ELSE 'Inactive One-Time Customers'
        END AS customer_segment
    FROM rfm_scores
)

SELECT
    customer_unique_id,
    first_purchase_timestamp,
    last_purchase_timestamp,
    recency_days,
    total_orders,
    total_revenue,
    total_order_value,
    avg_order_value,
    avg_review_score,
    delay_rate,
    purchase_frequency_group,
    main_customer_state,
    state_count,
    recency_score,
    frequency_score,
    monetary_score,
    rfm_total_score,
    customer_lifecycle_segment,
    customer_value_tier,
    customer_segment
FROM customer_segments;
