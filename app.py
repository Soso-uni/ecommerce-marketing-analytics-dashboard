from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

BRAND_BLUE = "#19aee5"
DEEP_BLUE = "#087fa8"
TEAL = "#2fc2b3"
AMBER = "#f0b620"
CLAY = "#d7604b"
MAUVE = "#9b6ca8"
SAGE = "#54b978"
INK = "#1f2430"
MUTED = "#4b5a6b"
PAGE_BG = "#f1f3f5"
CARD_BG = "#ffffff"
BORDER = "#cfe2ef"
GRID = "#dcebf5"
PALETTE = [BRAND_BLUE, TEAL, AMBER, CLAY, MAUVE, SAGE]
FONT_FAMILY = '"Inter", "SF Pro Text", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif'
PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True}
BLUE_SCALE = ["#eaf4fb", "#9ad3ee", BRAND_BLUE, DEEP_BLUE, "#123a70"]
TEAL_SCALE = ["#e8f7f4", "#95ded6", TEAL, "#257f78"]
RISK_SCALE = ["#f6dfd9", "#e79280", CLAY, "#b13f35"]


st.set_page_config(
    page_title="E-commerce Customer & Marketing Analytics Dashboard",
    layout="wide",
)


st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.35rem;
        padding-bottom: 2rem;
        max-width: 1360px;
    }
    .stApp {
        background: #f1f3f5;
        font-family: "Inter", "SF Pro Text", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
    }
    section[data-testid="stSidebar"] {
        background: #edf1f4;
        border-right: 1px solid #d7dee6;
        font-family: "Inter", "SF Pro Text", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
    }
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #20242c;
        font-weight: 700;
    }
    section[data-testid="stSidebar"] label {
        color: #3f4651;
        font-weight: 600;
    }
    h1,
    h1[data-testid="stHeading"],
    h1[data-testid="stHeading"] span {
        color: #20242c;
        font-size: clamp(1.9rem, 2.35vw, 2.45rem) !important;
        font-weight: 650;
        line-height: 1.18;
        letter-spacing: 0;
        margin-bottom: 0.3rem;
        font-family: "Inter", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
        white-space: nowrap;
    }
    @media (max-width: 1100px) {
        h1,
        h1[data-testid="stHeading"],
        h1[data-testid="stHeading"] span {
            white-space: nowrap;
            font-size: 1.75rem !important;
        }
    }
    h2, h3 {
        color: #20242c;
        letter-spacing: 0;
        font-weight: 650;
        line-height: 1.22;
        font-family: "Inter", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
    }
    h1 a, h2 a, h3 a {
        vertical-align: middle;
        margin-left: 0.35rem;
    }
    .stApp p,
    .stApp label,
    .stApp button,
    .stApp input,
    .stApp textarea {
        font-family: "Inter", "SF Pro Text", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
    }
    .stApp span[class*="material-symbols"],
    .stApp span[data-testid="stIconMaterial"] {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
        font-weight: normal !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        line-height: 1 !important;
    }
    div[data-testid="stCaptionContainer"] {
        color: #66717f;
        font-size: 1rem;
    }
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dde5ec;
        border-radius: 12px;
        padding: 15px 16px;
        min-height: 112px;
        height: 112px;
        box-sizing: border-box;
        box-shadow: 0 1px 3px rgba(31, 36, 48, 0.05);
    }
    div[data-testid="stMetric"] > div {
        overflow: visible;
    }
    div[data-testid="stMetricLabel"] p {
        color: #5b6675;
        font-size: 0.9rem;
        font-weight: 500;
        line-height: 1.28;
        white-space: normal;
        overflow-wrap: anywhere;
    }
    div[data-testid="stMetricValue"] {
        color: #2f3945;
        font-size: 1.52rem;
        font-weight: 650;
        line-height: 1.2;
        white-space: normal;
        overflow-wrap: anywhere;
    }
    div[data-testid="stMetricValue"] > div {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 0.9rem;
        font-weight: 600;
    }
    div[data-baseweb="tab-list"] {
        gap: 0.35rem;
        border-bottom: 1px solid #d7dee6;
        margin-bottom: 1.35rem;
    }
    div[data-baseweb="tab-highlight"] {
        display: none !important;
        transition: none !important;
        animation: none !important;
    }
    button[data-baseweb="tab"] {
        font-size: 1.02rem;
        font-weight: 550;
        color: #344456;
        padding: 0.85rem 0.9rem 0.78rem 0.9rem;
        line-height: 1.25;
        white-space: normal;
        cursor: pointer;
        transition: none !important;
        animation: none !important;
    }
    button[data-baseweb="tab"] * {
        transition: none !important;
        animation: none !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #1f2430;
        border-bottom: 0;
        box-shadow: inset 0 -3px 0 #ef3f3f;
    }
    button[data-baseweb="tab"]:hover {
        color: #087fa8;
        background: rgba(255, 255, 255, 0.35);
    }
    div[data-testid="stPlotlyChart"] {
        background: #ffffff;
        border: 1px solid #dde5ec;
        border-radius: 12px;
        padding: 10px 12px 4px 12px;
        box-shadow: 0 1px 3px rgba(31, 36, 48, 0.04);
    }
    div[data-testid="stDataFrame"] {
        background: #ffffff;
        border: 1px solid #dde5ec;
        border-radius: 12px;
        padding: 8px;
    }
    .business-note {
        border: 1px solid #e1e8ef;
        border-left: 3px solid #19aee5;
        background: #f8fafc;
        padding: 0.8rem 0.95rem;
        border-radius: 10px;
        color: #3f4651;
        font-size: 1rem;
        line-height: 1.48;
        margin: 0.5rem 0 0.8rem 0;
        box-shadow: none;
    }
    .section-copy {
        color: #66717f;
        font-size: 0.98rem;
        line-height: 1.45;
        margin-bottom: 1rem;
    }
    .dashboard-intro {
        background: #ffffff;
        border: 1px solid #dde5ec;
        border-left: 4px solid #19aee5;
        border-radius: 12px;
        padding: 0.95rem 1.1rem;
        margin: 0.65rem 0 1.3rem 0;
        max-width: 1080px;
        box-shadow: 0 1px 3px rgba(31, 36, 48, 0.04);
    }
    .dashboard-intro-label {
        color: #087fa8;
        font-family: "Inter", "SF Pro Text", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
        font-size: 0.92rem;
        font-weight: 600;
        letter-spacing: 0;
        text-transform: none;
        margin-bottom: 0.35rem;
    }
    .dashboard-intro-text {
        color: #3f4651;
        font-family: "Inter", "SF Pro Text", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
        font-size: 0.98rem;
        line-height: 1.55;
        margin: 0;
        white-space: normal;
        overflow-wrap: break-word;
    }
    .spacer {
        height: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = PALETTE


@st.cache_data
def load_data():
    order_master = pd.read_csv(PROCESSED_DIR / "order_master.csv")
    customer_summary = pd.read_csv(PROCESSED_DIR / "customer_summary.csv")
    category_summary = pd.read_csv(PROCESSED_DIR / "category_summary.csv")
    monthly_summary = pd.read_csv(PROCESSED_DIR / "monthly_summary.csv")

    order_master["order_purchase_timestamp"] = pd.to_datetime(
        order_master["order_purchase_timestamp"]
    )
    order_master["order_month"] = pd.to_datetime(order_master["order_month"])
    monthly_summary["order_month"] = pd.to_datetime(monthly_summary["order_month"])

    if "customer_segment" not in order_master.columns:
        order_master = order_master.merge(
            customer_summary[
                [
                    "customer_unique_id",
                    "customer_segment",
                    "purchase_frequency_group",
                    "recency_score",
                    "frequency_score",
                    "monetary_score",
                ]
            ],
            on="customer_unique_id",
            how="left",
        )

    return order_master, customer_summary, category_summary, monthly_summary


def format_currency(value):
    if pd.isna(value):
        return "R$ 0"
    return f"R$ {value:,.0f}"


def format_currency_precise(value):
    if pd.isna(value):
        return "R$ 0.00"
    return f"R$ {value:,.2f}"


def format_number(value):
    if pd.isna(value):
        return "0"
    return f"{value:,.0f}"


def format_percentage(value):
    if pd.isna(value):
        return "0.0%"
    return f"{value:.1%}"


def format_decimal(value):
    if pd.isna(value):
        return "0.00"
    return f"{value:.2f}"


def format_category(value):
    if pd.isna(value):
        return "Unknown"
    return str(value).replace("_", " ").title()


def format_segment_short(value):
    segment_labels = {
        "High-Value Occasional Customers": "High-Value Occ.",
        "High-Value Repeat Customers": "High-Value Repeat",
        "New High-Value Customers": "New High-Value",
        "Loyal High-Value Customers": "Loyal High-Value",
        "New or Recent Customers": "New / Recent",
        "Inactive One-Time Customers": "Inactive One-Time",
        "Inactive Low-Value Customers": "Inactive Low-Value",
        "At Risk Repeat Customers": "At Risk Repeat",
        "At Risk Customers": "At Risk",
        "Active Repeat Customers": "Active Repeat",
    }
    if pd.isna(value):
        return "N/A"
    return segment_labels.get(str(value), str(value).replace(" Customers", ""))


def style_figure(fig, y_money=False, x_money=False, y_percent=False, x_percent=False):
    fig.update_layout(
        font={"family": FONT_FAMILY, "color": INK, "size": 13},
        title={"font": {"size": 18, "color": INK, "family": FONT_FAMILY}},
        plot_bgcolor=CARD_BG,
        paper_bgcolor=CARD_BG,
        margin={"l": 16, "r": 16, "t": 58, "b": 28},
        hovermode="x unified",
        legend_title_text="",
    )
    fig.update_traces(marker_line_width=0)
    fig.update_traces(marker_cornerradius=3, selector={"type": "bar"})
    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        tickfont={"size": 12, "color": MUTED},
        title_font={"size": 13, "color": MUTED},
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        tickfont={"size": 12, "color": MUTED},
        title_font={"size": 13, "color": MUTED},
    )
    if y_money:
        fig.update_yaxes(tickprefix="R$ ", separatethousands=True)
    if x_money:
        fig.update_xaxes(tickprefix="R$ ", separatethousands=True)
    if y_percent:
        fig.update_yaxes(tickformat=".0%")
    if x_percent:
        fig.update_xaxes(tickformat=".0%")
    return fig


def style_bar_labels(fig):
    fig.update_traces(
        textposition="outside",
        textfont={"size": 12, "color": MUTED, "family": FONT_FAMILY},
        cliponaxis=False,
    )
    return fig


def spacer():
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)


def build_monthly_view(orders):
    return (
        orders.groupby("order_month", as_index=False)
        .agg(
            total_revenue=("revenue", "sum"),
            total_orders=("order_id", "nunique"),
            total_customers=("customer_unique_id", "nunique"),
            avg_order_value=("order_value", "mean"),
            avg_review_score=("review_score", "mean"),
        )
        .sort_values("order_month")
    )


def build_category_view(orders):
    return (
        orders.groupby("main_product_category", as_index=False)
        .agg(
            total_orders=("order_id", "nunique"),
            total_customers=("customer_unique_id", "nunique"),
            total_revenue=("revenue", "sum"),
            avg_order_value=("order_value", "mean"),
            avg_review_score=("review_score", "mean"),
            low_review_rate=(
                "review_score",
                lambda scores: (scores.dropna() <= 2).mean()
                if not scores.dropna().empty
                else None,
            ),
        )
        .sort_values("total_revenue", ascending=False)
    )


def build_segment_view(orders):
    return (
        orders.dropna(subset=["customer_segment"])
        .groupby("customer_segment", as_index=False)
        .agg(
            customers=("customer_unique_id", "nunique"),
            total_orders=("order_id", "nunique"),
            total_revenue=("revenue", "sum"),
            avg_order_value=("order_value", "mean"),
            avg_review_score=("review_score", "mean"),
        )
        .sort_values("customers", ascending=False)
    )


def build_review_distribution(orders):
    return (
        orders.dropna(subset=["review_score"])
        .assign(review_score=lambda frame: frame["review_score"].astype(int))
        .groupby("review_score", as_index=False)
        .agg(orders=("order_id", "nunique"))
        .sort_values("review_score")
    )


def build_segment_share_view(segment_view):
    if segment_view.empty:
        return segment_view.assign(
            customer_share=[],
            revenue_share=[],
            revenue_per_customer=[],
        )

    segment_share = segment_view.copy()
    total_segment_customers = segment_share["customers"].sum()
    total_segment_revenue = segment_share["total_revenue"].sum()
    segment_share["customer_share"] = (
        segment_share["customers"] / total_segment_customers
        if total_segment_customers
        else 0
    )
    segment_share["revenue_share"] = (
        segment_share["total_revenue"] / total_segment_revenue
        if total_segment_revenue
        else 0
    )
    segment_share["revenue_per_customer"] = (
        segment_share["total_revenue"] / segment_share["customers"]
    )
    return segment_share


def build_recommendations(orders, category_view, segment_view):
    if orders.empty:
        return []

    top_category = (
        format_category(category_view.iloc[0]["main_product_category"])
        if not category_view.empty
        else "the leading category"
    )
    top_segment = (
        segment_view.sort_values("total_revenue", ascending=False).iloc[0]["customer_segment"]
        if not segment_view.empty
        else "the highest-value customer segment"
    )

    min_orders = max(50, int(orders["order_id"].nunique() * 0.01))
    review_risk_categories = category_view[
        category_view["total_orders"] >= min_orders
    ].dropna(subset=["low_review_rate"])
    review_risk_category = (
        format_category(
            review_risk_categories.sort_values(
                "low_review_rate", ascending=False
            ).iloc[0][
                "main_product_category"
            ]
        )
        if not review_risk_categories.empty
        else "high-volume categories"
    )

    recommendations = [
        f"Product insight: {top_category} is the leading revenue contributor and should remain a priority for category-level performance monitoring.",
        f"Customer insight: {top_segment} generates the largest filtered revenue contribution and is a strong candidate for lifecycle marketing focus.",
        f"Satisfaction insight: {review_risk_category} has elevated low-review risk among meaningful-volume categories and may need closer experience monitoring.",
    ]

    return recommendations


order_master, customer_summary, category_summary, monthly_summary = load_data()


st.title("E-commerce Customer & Marketing Analytics Dashboard")
st.markdown(
    """
    <div class='dashboard-intro'>
        <div class='dashboard-intro-label'>Portfolio project · Olist marketplace data</div>
        <p class='dashboard-intro-text'>
            An interactive analytics dashboard showing how transaction data can support better
            business performance, marketing prioritisation, customer value, and retention decisions.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


st.sidebar.header("Filters")

min_month = order_master["order_month"].min()
max_month = order_master["order_month"].max()

selected_month_range = st.sidebar.slider(
    "Order month range",
    min_value=min_month.to_pydatetime(),
    max_value=max_month.to_pydatetime(),
    value=(min_month.to_pydatetime(), max_month.to_pydatetime()),
    format="YYYY-MM",
)

selected_states = st.sidebar.multiselect(
    "Customer states",
    options=sorted(order_master["customer_state"].dropna().unique()),
    default=[],
)

selected_categories = st.sidebar.multiselect(
    "Main product categories",
    options=sorted(order_master["main_product_category"].dropna().unique()),
    default=[],
    format_func=format_category,
)

selected_segments = st.sidebar.multiselect(
    "Customer segments",
    options=sorted(order_master["customer_segment"].dropna().unique()),
    default=[],
)

start_month = pd.to_datetime(selected_month_range[0]).to_period("M").to_timestamp()
end_month = pd.to_datetime(selected_month_range[1]).to_period("M").to_timestamp()
end_month_exclusive = end_month + pd.offsets.MonthBegin(1)

filtered_orders = order_master[
    (order_master["order_purchase_timestamp"] >= start_month)
    & (order_master["order_purchase_timestamp"] < end_month_exclusive)
].copy()

if selected_states:
    filtered_orders = filtered_orders[
        filtered_orders["customer_state"].isin(selected_states)
    ].copy()

if selected_categories:
    filtered_orders = filtered_orders[
        filtered_orders["main_product_category"].isin(selected_categories)
    ].copy()

if selected_segments:
    filtered_orders = filtered_orders[
        filtered_orders["customer_segment"].isin(selected_segments)
    ].copy()

st.sidebar.markdown("---")
st.sidebar.metric("Filtered orders", format_number(filtered_orders["order_id"].nunique()))
st.sidebar.metric(
    "Filtered revenue",
    format_currency(filtered_orders["revenue"].sum()),
)

if filtered_orders.empty:
    st.warning("No orders match the selected filters. Adjust the sidebar filters to continue.")
    st.stop()

monthly_filtered = build_monthly_view(filtered_orders)
monthly_trend = monthly_filtered.copy()
category_filtered = build_category_view(filtered_orders)
segment_summary = build_segment_view(filtered_orders)
segment_share_summary = build_segment_share_view(segment_summary)
review_distribution = build_review_distribution(filtered_orders)
recommendations = build_recommendations(
    filtered_orders, category_filtered, segment_summary
)


total_revenue = filtered_orders["revenue"].sum()
total_orders = filtered_orders["order_id"].nunique()
total_customers = filtered_orders["customer_unique_id"].nunique()
avg_order_value = filtered_orders["order_value"].mean()
avg_review_score = filtered_orders["review_score"].mean()
active_customer_ids = filtered_orders["customer_unique_id"].dropna().unique()
active_customer_history = customer_summary[
    customer_summary["customer_unique_id"].isin(active_customer_ids)
]
repeat_customer_rate = (
    (active_customer_history["total_orders"] > 1).mean()
    if not active_customer_history.empty
    else None
)
review_scores = filtered_orders["review_score"].dropna()
five_star_rate = (review_scores == 5).mean() if not review_scores.empty else None
low_review_rate = (review_scores <= 2).mean() if not review_scores.empty else None
low_review_revenue = filtered_orders.loc[
    filtered_orders["review_score"] <= 2, "revenue"
].sum()

top_category_name = "N/A"
top_category_share = None
highest_aov_category = "N/A"
highest_aov_value = None
highest_low_review_category = "N/A"
highest_low_review_rate = None
highest_value_segment = "N/A"
highest_value_segment_revenue = None
highest_value_segment_share = None
largest_segment = "N/A"
min_category_orders = max(50, int(total_orders * 0.01))
meaningful_categories = category_filtered[
    category_filtered["total_orders"] >= min_category_orders
].copy()
actionable_categories = meaningful_categories[
    meaningful_categories["main_product_category"].fillna("unknown").str.lower()
    != "unknown"
].copy()
low_review_categories = (
    actionable_categories
    .dropna(subset=["low_review_rate"])
    .sort_values("low_review_rate", ascending=False)
    .head(10)
    .copy()
)
low_review_categories["category_label"] = low_review_categories[
    "main_product_category"
].map(format_category)
low_review_categories["low_review_rate_label"] = low_review_categories[
    "low_review_rate"
].map(format_percentage)

if not category_filtered.empty:
    top_category_row = category_filtered.iloc[0]
    top_category_name = format_category(top_category_row["main_product_category"])
    top_category_share = (
        top_category_row["total_revenue"] / total_revenue if total_revenue else None
    )

    category_aov_base = (
        meaningful_categories if not meaningful_categories.empty else category_filtered
    )
    category_aov_row = category_aov_base.sort_values(
        "avg_order_value", ascending=False
    ).iloc[0]
    highest_aov_category = format_category(category_aov_row["main_product_category"])
    highest_aov_value = category_aov_row["avg_order_value"]

    if not low_review_categories.empty:
        review_category_row = low_review_categories.iloc[0]
        highest_low_review_category = format_category(
            review_category_row["main_product_category"]
        )
        highest_low_review_rate = review_category_row["low_review_rate"]

if not segment_summary.empty:
    largest_segment = format_segment_short(
        segment_summary.sort_values("customers", ascending=False).iloc[0][
            "customer_segment"
        ]
    )
    value_segment_row = segment_summary.sort_values(
        "total_revenue", ascending=False
    ).iloc[0]
    highest_value_segment = format_segment_short(value_segment_row["customer_segment"])
    highest_value_segment_revenue = value_segment_row["total_revenue"]
    highest_value_segment_share = (
        highest_value_segment_revenue / total_revenue if total_revenue else None
    )

if len(monthly_trend) >= 2:
    latest_month = monthly_trend.iloc[-1]
    previous_month = monthly_trend.iloc[-2]
    revenue_delta = (
        (latest_month["total_revenue"] - previous_month["total_revenue"])
        / previous_month["total_revenue"]
        if previous_month["total_revenue"] != 0
        else None
    )
    order_delta = (
        (latest_month["total_orders"] - previous_month["total_orders"])
        / previous_month["total_orders"]
        if previous_month["total_orders"] != 0
        else None
    )
else:
    revenue_delta = None
    order_delta = None

revenue_delta_text = format_percentage(revenue_delta) if revenue_delta is not None else None
order_delta_text = format_percentage(order_delta) if order_delta is not None else None


overview_tab, monthly_tab, category_tab, customer_tab, satisfaction_tab, methodology_tab = st.tabs(
    [
        "Executive Summary",
        "Revenue Trends",
        "Product Performance",
        "Customer Value & Retention",
        "Customer Satisfaction",
        "Data & Methodology",
    ]
)


with overview_tab:
    st.subheader("Executive Summary")
    st.markdown(
        "<div class='section-copy'><strong>Business question:</strong> How is the business performing overall?</div>",
        unsafe_allow_html=True,
    )

    kpi_1, kpi_2, kpi_3, kpi_4, kpi_5 = st.columns(5)

    kpi_1.metric("Total Revenue", format_currency(total_revenue), revenue_delta_text)
    kpi_2.metric("Total Orders", format_number(total_orders), order_delta_text)
    kpi_3.metric("Unique Customers", format_number(total_customers))
    kpi_4.metric("Average Order Value", format_currency_precise(avg_order_value))
    kpi_5.metric("Average Review Score", format_decimal(avg_review_score))

    spacer()
    st.markdown("#### Executive Insights")
    for recommendation in recommendations:
        st.markdown(
            f"<div class='business-note'>{recommendation}</div>",
            unsafe_allow_html=True,
        )

with monthly_tab:
    st.subheader("Revenue Trends")
    st.markdown(
        "<div class='section-copy'><strong>Business question:</strong> What is driving revenue performance over time?</div>",
        unsafe_allow_html=True,
    )

    chart_1, chart_2 = st.columns(2)
    with chart_1:
        fig_revenue = px.line(
            monthly_trend,
            x="order_month",
            y="total_revenue",
            markers=True,
            title="Revenue Trend",
            labels={"order_month": "Order Month", "total_revenue": "Revenue"},
        )
        style_figure(fig_revenue, y_money=True)
        st.plotly_chart(fig_revenue, width="stretch", config=PLOTLY_CONFIG)

    with chart_2:
        fig_orders = px.line(
            monthly_trend,
            x="order_month",
            y="total_orders",
            markers=True,
            title="Order Trend",
            labels={"order_month": "Order Month", "total_orders": "Orders"},
        )
        style_figure(fig_orders)
        st.plotly_chart(fig_orders, width="stretch", config=PLOTLY_CONFIG)

    spacer()
    fig_aov = px.line(
        monthly_trend,
        x="order_month",
        y="avg_order_value",
        markers=True,
        title="Average Order Value Trend",
        labels={"order_month": "Order Month", "avg_order_value": "AOV"},
    )
    style_figure(fig_aov, y_money=True)
    st.plotly_chart(fig_aov, width="stretch", config=PLOTLY_CONFIG)


with category_tab:
    st.subheader("Product Performance")
    st.markdown(
        "<div class='section-copy'><strong>Business question:</strong> Which product categories create the most business value?</div>",
        unsafe_allow_html=True,
    )
    if len(actionable_categories) < len(category_filtered):
        st.markdown(
            "<div class='business-note'>Category opportunity charts focus on meaningful-volume mapped categories; Unknown remains available in the detailed table.</div>",
            unsafe_allow_html=True,
        )

    category_kpi_1, category_kpi_2, category_kpi_3 = st.columns(3)
    category_kpi_1.metric("Top Revenue Category", top_category_name)
    category_kpi_2.metric(
        "Top Category Revenue Share",
        format_percentage(top_category_share),
    )
    category_kpi_3.metric(
        "Highest AOV Category",
        highest_aov_category,
        format_currency_precise(highest_aov_value),
    )

    spacer()
    top_categories = category_filtered.head(10).copy()
    top_categories["category_label"] = top_categories["main_product_category"].map(
        format_category
    )
    top_categories["revenue_share"] = (
        top_categories["total_revenue"] / total_revenue if total_revenue else 0
    )
    top_categories["revenue_share_label"] = top_categories["revenue_share"].map(
        format_percentage
    )
    product_driver_categories = (
        actionable_categories.sort_values("total_revenue", ascending=False)
        .head(10)
        .copy()
    )
    if product_driver_categories.empty:
        product_driver_categories = top_categories.copy()
    product_driver_categories["category_label"] = product_driver_categories[
        "main_product_category"
    ].map(format_category)
    product_driver_categories["revenue_share"] = (
        product_driver_categories["total_revenue"] / total_revenue
        if total_revenue
        else 0
    )
    product_driver_categories["order_share"] = (
        product_driver_categories["total_orders"] / total_orders
        if total_orders
        else 0
    )
    product_share_long = product_driver_categories[
        ["category_label", "revenue_share", "order_share"]
    ].melt(
        id_vars="category_label",
        value_vars=["revenue_share", "order_share"],
        var_name="share_type",
        value_name="share",
    )
    product_share_long["share_type"] = product_share_long["share_type"].map(
        {
            "revenue_share": "Revenue Share",
            "order_share": "Order Share",
        }
    )
    product_category_order = product_driver_categories.sort_values("revenue_share")[
        "category_label"
    ].tolist()

    chart_1, chart_2 = st.columns(2)
    with chart_1:
        fig_category_revenue = px.bar(
            top_categories,
            x="total_revenue",
            y="category_label",
            orientation="h",
            title="Top Categories by Revenue",
            labels={"total_revenue": "Revenue", "category_label": "Category"},
            color="total_revenue",
            color_continuous_scale=BLUE_SCALE,
            text="revenue_share_label",
        )
        fig_category_revenue.update_layout(
            yaxis={"categoryorder": "total ascending"},
            coloraxis_showscale=False,
        )
        style_figure(fig_category_revenue, x_money=True)
        if not top_categories.empty:
            fig_category_revenue.update_xaxes(
                range=[0, top_categories["total_revenue"].max() * 1.16]
            )
        fig_category_revenue.update_layout(margin={"l": 18, "r": 72, "t": 58, "b": 34})
        style_bar_labels(fig_category_revenue)
        st.plotly_chart(fig_category_revenue, width="stretch", config=PLOTLY_CONFIG)

    with chart_2:
        fig_product_driver = px.bar(
            product_share_long,
            x="share",
            y="category_label",
            orientation="h",
            color="share_type",
            barmode="group",
            title="Revenue Share vs Order Share",
            labels={
                "share": "Share",
                "category_label": "Category",
                "share_type": "",
            },
            color_discrete_map={
                "Revenue Share": BRAND_BLUE,
                "Order Share": TEAL,
            },
            text="share",
        )
        fig_product_driver.update_layout(
            yaxis={
                "categoryorder": "array",
                "categoryarray": product_category_order,
            },
            legend={
                "orientation": "h",
                "yanchor": "bottom",
                "y": 1.02,
                "xanchor": "left",
                "x": 0,
            },
        )
        style_figure(fig_product_driver, x_percent=True)
        if not product_share_long.empty:
            fig_product_driver.update_xaxes(
                range=[0, product_share_long["share"].max() * 1.18]
            )
        fig_product_driver.update_layout(margin={"l": 18, "r": 72, "t": 86, "b": 34})
        fig_product_driver.update_traces(texttemplate="%{text:.1%}")
        style_bar_labels(fig_product_driver)
        st.plotly_chart(fig_product_driver, width="stretch", config=PLOTLY_CONFIG)

    category_table = category_filtered[
        [
            "main_product_category",
            "total_orders",
            "total_customers",
            "total_revenue",
            "avg_order_value",
            "avg_review_score",
            "low_review_rate",
        ]
    ].copy()
    category_table["main_product_category"] = category_table[
        "main_product_category"
    ].map(format_category)
    category_table["total_revenue"] = category_table["total_revenue"].map(
        format_currency
    )
    category_table["avg_order_value"] = category_table["avg_order_value"].map(
        format_currency_precise
    )
    category_table["avg_review_score"] = category_table["avg_review_score"].map(
        format_decimal
    )
    category_table["low_review_rate"] = category_table["low_review_rate"].map(
        format_percentage
    )
    with st.expander("View detailed category performance table"):
        st.dataframe(
            category_table,
            width="stretch",
            hide_index=True,
            column_config={
                "main_product_category": "Main Product Category",
                "total_orders": "Orders",
                "total_customers": "Customers",
                "total_revenue": "Revenue",
                "avg_order_value": "AOV",
                "avg_review_score": "Review",
                "low_review_rate": "Low Review Rate",
            },
        )


with customer_tab:
    st.subheader("Customer Value & Retention")
    st.markdown(
        "<div class='section-copy'><strong>Business question:</strong> Which customer groups create the greatest value and should marketing prioritise?</div>",
        unsafe_allow_html=True,
    )

    customer_kpi_1, customer_kpi_2, customer_kpi_3, customer_kpi_4 = st.columns(4)
    customer_kpi_1.metric("Largest Customer Segment", largest_segment)
    customer_kpi_2.metric("Highest Revenue Segment", highest_value_segment)
    customer_kpi_3.metric(
        "Revenue Concentration",
        format_percentage(highest_value_segment_share),
    )
    customer_kpi_4.metric(
        "Repeat Customer Rate",
        format_percentage(repeat_customer_rate),
    )

    spacer()
    fig_segments = px.bar(
        segment_summary,
        x="customers",
        y="customer_segment",
        orientation="h",
        title="Customer Segment Size",
        labels={
            "customers": "Customers",
            "customer_segment": "Customer Segment",
        },
        color="customers",
        color_continuous_scale=TEAL_SCALE,
        text="customers",
    )
    fig_segments.update_layout(
        height=440,
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False,
        margin={"l": 18, "r": 72, "t": 58, "b": 34},
    )
    style_figure(fig_segments)
    if not segment_summary.empty:
        fig_segments.update_xaxes(range=[0, segment_summary["customers"].max() * 1.18])
    fig_segments.update_layout(margin={"l": 18, "r": 72, "t": 58, "b": 34})
    fig_segments.update_traces(texttemplate="%{text:,.0f}")
    style_bar_labels(fig_segments)
    st.plotly_chart(fig_segments, width="stretch", config=PLOTLY_CONFIG)

    spacer()
    segment_share_long = segment_share_summary[
        ["customer_segment", "customer_share", "revenue_share"]
    ].melt(
        id_vars="customer_segment",
        value_vars=["customer_share", "revenue_share"],
        var_name="share_type",
        value_name="share",
    )
    segment_share_long["share_type"] = segment_share_long["share_type"].map(
        {
            "customer_share": "Customer Share",
            "revenue_share": "Revenue Share",
        }
    )
    segment_order = segment_share_summary.sort_values("revenue_share")[
        "customer_segment"
    ].tolist()
    fig_segment_mix = px.bar(
        segment_share_long,
        x="share",
        y="customer_segment",
        orientation="h",
        color="share_type",
        barmode="group",
        title="Customer Share vs Revenue Share",
        labels={
            "share": "Share",
            "customer_segment": "Customer Segment",
            "share_type": "",
        },
        color_discrete_map={
            "Customer Share": TEAL,
            "Revenue Share": BRAND_BLUE,
        },
        text="share",
    )
    fig_segment_mix.update_layout(
        yaxis={"categoryorder": "array", "categoryarray": segment_order}
    )
    style_figure(fig_segment_mix, x_percent=True)
    if not segment_share_long.empty:
        fig_segment_mix.update_xaxes(range=[0, segment_share_long["share"].max() * 1.18])
    fig_segment_mix.update_layout(
        height=440,
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "left",
            "x": 0,
        },
        margin={"l": 18, "r": 72, "t": 86, "b": 34},
    )
    fig_segment_mix.update_traces(texttemplate="%{text:.1%}")
    style_bar_labels(fig_segment_mix)
    st.plotly_chart(fig_segment_mix, width="stretch", config=PLOTLY_CONFIG)

    spacer()
    fig_avg_customer_value = px.bar(
        segment_share_summary.sort_values("revenue_per_customer", ascending=False),
        x="revenue_per_customer",
        y="customer_segment",
        orientation="h",
        title="Customer Value Intensity by Segment",
        labels={
            "revenue_per_customer": "Revenue per Customer",
            "customer_segment": "Customer Segment",
        },
        color="revenue_per_customer",
        color_continuous_scale=BLUE_SCALE,
        text="revenue_per_customer",
    )
    fig_avg_customer_value.update_layout(
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False,
        height=390,
    )
    style_figure(fig_avg_customer_value, x_money=True)
    if not segment_share_summary.empty:
        fig_avg_customer_value.update_xaxes(
            range=[0, segment_share_summary["revenue_per_customer"].max() * 1.16]
        )
    fig_avg_customer_value.update_layout(margin={"l": 18, "r": 72, "t": 58, "b": 34})
    fig_avg_customer_value.update_traces(texttemplate="R$ %{text:,.2f}")
    style_bar_labels(fig_avg_customer_value)
    st.plotly_chart(fig_avg_customer_value, width="stretch", config=PLOTLY_CONFIG)

    segment_table = segment_share_summary.copy()
    segment_table["total_revenue"] = segment_table["total_revenue"].map(
        format_currency
    )
    segment_table["revenue_per_customer"] = segment_table[
        "revenue_per_customer"
    ].map(format_currency_precise)
    segment_table["avg_order_value"] = segment_table["avg_order_value"].map(
        format_currency_precise
    )
    segment_table["avg_review_score"] = segment_table["avg_review_score"].map(
        format_decimal
    )
    segment_table["customer_share"] = segment_table["customer_share"].map(
        format_percentage
    )
    segment_table["revenue_share"] = segment_table["revenue_share"].map(
        format_percentage
    )

    with st.expander("View detailed customer segment table"):
        st.dataframe(
            segment_table,
            width="stretch",
            hide_index=True,
            column_config={
                "customer_segment": "Customer Segment",
                "customers": "Customers",
                "total_orders": "Orders",
                "total_revenue": "Revenue",
                "revenue_per_customer": "Revenue per Customer",
                "avg_order_value": "AOV",
                "avg_review_score": "Review",
                "customer_share": "Customer Share",
                "revenue_share": "Revenue Share",
            },
        )


with satisfaction_tab:
    st.subheader("Customer Satisfaction")
    st.markdown(
        "<div class='section-copy'><strong>Business question:</strong> How satisfied are customers, and where is dissatisfaction concentrated?</div>",
        unsafe_allow_html=True,
    )

    (
        satisfaction_kpi_1,
        satisfaction_kpi_2,
        satisfaction_kpi_3,
        satisfaction_kpi_4,
    ) = st.columns(4)
    satisfaction_kpi_1.metric("Average Review Score", format_decimal(avg_review_score))
    satisfaction_kpi_2.metric("5-Star Rate", format_percentage(five_star_rate))
    satisfaction_kpi_3.metric("Low Review Rate", format_percentage(low_review_rate))
    satisfaction_kpi_4.metric(
        "Low-Review Revenue Exposure",
        format_currency(low_review_revenue),
    )

    spacer()
    chart_1, chart_2 = st.columns(2)
    with chart_1:
        fig_review_distribution = px.bar(
            review_distribution,
            x="review_score",
            y="orders",
            title="Review Score Distribution",
            labels={
                "review_score": "Review Score",
                "orders": "Orders",
            },
            color="orders",
            color_continuous_scale=BLUE_SCALE,
            text="orders",
        )
        fig_review_distribution.update_xaxes(dtick=1)
        fig_review_distribution.update_layout(coloraxis_showscale=False)
        style_figure(fig_review_distribution)
        if not review_distribution.empty:
            fig_review_distribution.update_yaxes(
                range=[0, review_distribution["orders"].max() * 1.16]
            )
        fig_review_distribution.update_layout(
            margin={"l": 18, "r": 36, "t": 58, "b": 34}
        )
        fig_review_distribution.update_traces(texttemplate="%{text:,.0f}")
        style_bar_labels(fig_review_distribution)
        st.plotly_chart(fig_review_distribution, width="stretch", config=PLOTLY_CONFIG)

    with chart_2:
        fig_low_review_category = px.bar(
            low_review_categories,
            x="low_review_rate",
            y="category_label",
            orientation="h",
            title="Low Review Rate by Category",
            labels={
                "low_review_rate": "Low Review Rate",
                "category_label": "Category",
            },
            color="low_review_rate",
            color_continuous_scale=RISK_SCALE,
            text="low_review_rate_label",
        )
        fig_low_review_category.update_layout(
            yaxis={"categoryorder": "total ascending"},
            coloraxis_showscale=False,
        )
        style_figure(fig_low_review_category, x_percent=True)
        if not low_review_categories.empty:
            fig_low_review_category.update_xaxes(
                range=[
                    0,
                    max(low_review_categories["low_review_rate"].max() * 1.18, 0.01),
                ]
            )
        fig_low_review_category.update_layout(
            margin={"l": 18, "r": 64, "t": 58, "b": 34}
        )
        style_bar_labels(fig_low_review_category)
        st.plotly_chart(
            fig_low_review_category,
            width="stretch",
            config=PLOTLY_CONFIG,
        )

with methodology_tab:
    st.subheader("Data & Methodology")
    st.markdown(
        "<div class='section-copy'><strong>Business question:</strong> How was the dashboard data model built and validated?</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        **Data source:** Olist Brazilian E-commerce public dataset.

        **Transformation approach:** raw CSV files are registered in DuckDB, transformed with SQL, and exported into dashboard-ready tables through a Python pipeline.

        **Processed tables:** `order_master.csv`, `customer_summary.csv`, `category_summary.csv`, and `monthly_summary.csv`.

        **Dashboard logic:** sidebar filters are applied to the order-level table first. Monthly, product, customer value, and satisfaction views are recalculated from the filtered order data so the analysis remains consistent across pages.

        **Customer segmentation:** customer groups are built with a full-period RFM-style framework and business-rule frequency scoring. Segments and repeat customer rate use lifetime customer history for customers active in the selected filters.

        **Analytical scope:** the dashboard focuses on descriptive and diagnostic analytics: business performance, revenue drivers, product performance, customer value, satisfaction, and marketing actions.
        """
    )

    with st.expander("View processed data samples"):
        st.subheader("Order Master")
        st.dataframe(order_master.head(20), width="stretch")

        st.subheader("Customer Summary")
        st.dataframe(customer_summary.head(20), width="stretch")

        st.subheader("Category Summary")
        st.dataframe(category_summary.head(20), width="stretch")

        st.subheader("Monthly Summary")
        st.dataframe(monthly_summary.head(20), width="stretch")
