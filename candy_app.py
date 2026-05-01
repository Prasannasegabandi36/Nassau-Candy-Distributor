import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Nassau Candy Shipping Analytics",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #111827 45%, #1e1b4b 100%);
        color: #f8fafc;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main title card */
    .hero-card {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.95), rgba(236, 72, 153, 0.88));
        padding: 34px 38px;
        border-radius: 28px;
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.35);
        margin-bottom: 28px;
        border: 1px solid rgba(255,255,255,0.18);
    }
    .hero-title {
        font-size: 44px;
        font-weight: 900;
        color: white;
        margin-bottom: 8px;
        letter-spacing: -0.04em;
    }
    .hero-subtitle {
        font-size: 18px;
        color: #fdf2f8;
        max-width: 920px;
        line-height: 1.55;
    }

    /* Section heading */
    .section-title {
        font-size: 25px;
        font-weight: 800;
        color: #f8fafc;
        margin-top: 10px;
        margin-bottom: 12px;
    }

    /* KPI cards */
    .kpi-card {
        background: rgba(15, 23, 42, 0.88);
        border: 1px solid rgba(148, 163, 184, 0.20);
        border-radius: 22px;
        padding: 22px 18px;
        box-shadow: 0 14px 32px rgba(0,0,0,0.28);
        min-height: 138px;
    }
    .kpi-label {
        font-size: 13px;
        color: #cbd5e1;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 30px;
        color: #ffffff;
        font-weight: 900;
        margin-bottom: 4px;
    }
    .kpi-note {
        font-size: 12px;
        color: #94a3b8;
    }

    /* Insight cards */
    .insight-card {
        background: rgba(30, 41, 59, 0.86);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 20px;
        padding: 20px 22px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.24);
        margin-bottom: 14px;
    }
    .insight-card h4 {
        color: #ffffff;
        margin-bottom: 8px;
    }
    .insight-card p, .insight-card li {
        color: #dbeafe;
        font-size: 15px;
        line-height: 1.55;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617 0%, #111827 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    /* Streamlit metric styling */
    div[data-testid="stMetric"] {
        background: rgba(15,23,42,0.82);
        border-radius: 18px;
        padding: 16px;
        border: 1px solid rgba(148,163,184,0.18);
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-weight: 700;
        border-radius: 14px 14px 0 0;
    }

    /* Dataframes */
    .stDataFrame {
        border-radius: 18px;
        overflow: hidden;
    }

    /* Buttons */
    .stButton > button, .stDownloadButton > button {
        border-radius: 14px;
        border: 0;
        font-weight: 800;
        background: linear-gradient(135deg, #7c3aed, #ec4899);
        color: white;
        padding: 0.7rem 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# FACTORY + PRODUCT MAPPING
# ============================================================
FACTORIES = {
    "Lot's O' Nuts":      {"lat": 32.881893, "lon": -111.768036},
    "Wicked Choccy's":    {"lat": 32.076176, "lon": -81.088371},
    "Sugar Shack":        {"lat": 48.11914,  "lon": -96.18115},
    "Secret Factory":     {"lat": 41.446333, "lon": -90.565487},
    "The Other Factory":  {"lat": 35.1175,   "lon": -89.971107},
}

PRODUCT_FACTORY = {
    "Wonka Bar - Nutty Crunch Surprise":   "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows":           "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious":      "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate":          "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel":   "Wicked Choccy's",
    "Laffy Taffy":                         "Sugar Shack",
    "SweeTARTS":                           "Sugar Shack",
    "Nerds":                               "Sugar Shack",
    "Fun Dip":                             "Sugar Shack",
    "Fizzy Lifting Drinks":                "Sugar Shack",
    "Everlasting Gobstopper":              "Secret Factory",
    "Lickable Wallpaper":                  "Secret Factory",
    "Wonka Gum":                           "Secret Factory",
    "Hair Toffee":                         "The Other Factory",
    "Kazookles":                           "The Other Factory",
}

STATE_ABBREV = {
    "Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR","California":"CA",
    "Colorado":"CO","Connecticut":"CT","Delaware":"DE","Florida":"FL","Georgia":"GA",
    "Hawaii":"HI","Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA",
    "Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME","Maryland":"MD",
    "Massachusetts":"MA","Michigan":"MI","Minnesota":"MN","Mississippi":"MS",
    "Missouri":"MO","Montana":"MT","Nebraska":"NE","Nevada":"NV","New Hampshire":"NH",
    "New Jersey":"NJ","New Mexico":"NM","New York":"NY","North Carolina":"NC",
    "North Dakota":"ND","Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Pennsylvania":"PA",
    "Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD","Tennessee":"TN",
    "Texas":"TX","Utah":"UT","Vermont":"VT","Virginia":"VA","Washington":"WA",
    "West Virginia":"WV","Wisconsin":"WI","Wyoming":"WY","District of Columbia":"DC",
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def money(value):
    return f"${value:,.0f}"


def pct(value):
    return f"{value:.1f}%"


def kpi_card(label, value, note=""):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def apply_chart_style(fig, height=430):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.35)",
        font=dict(color="#e5e7eb", family="Arial"),
        title=dict(font=dict(size=20, color="#ffffff")),
        margin=dict(l=25, r=25, t=60, b=25),
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,0.18)", zerolinecolor="rgba(148,163,184,0.18)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.18)", zerolinecolor="rgba(148,163,184,0.18)")
    return fig


@st.cache_data
def load_data():
    df = pd.read_csv("Nassau Candy Distributor.csv")

    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y", errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y", errors="coerce")

    df = df.dropna(subset=["Order Date", "Ship Date"]).copy()
    df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df = df[df["Lead Time"] >= 0].copy()

    df["Factory"] = df["Product Name"].map(PRODUCT_FACTORY).fillna("Unknown Factory")
    df["Route"] = df["Factory"] + " → " + df["State/Province"].astype(str)
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Profit Margin"] = np.where(df["Sales"] > 0, df["Gross Profit"] / df["Sales"] * 100, 0)
    df["State Code"] = df["State/Province"].map(STATE_ABBREV)
    return df


# ============================================================
# LOAD DATA
# ============================================================
try:
    df = load_data()
except FileNotFoundError:
    st.error("Dataset not found. Please make sure `Nassau Candy Distributor.csv` is in the same folder as app.py.")
    st.stop()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

if df.empty:
    st.error("No valid data available after cleaning.")
    st.stop()

# ============================================================
# HERO SECTION
# ============================================================
st.markdown("""
<div class="hero-card">
    <div class="hero-title">🍬 Nassau Candy Shipping Analytics</div>
    <div class="hero-subtitle">
        Factory-to-customer route efficiency dashboard for analyzing shipment delays, lead time performance,
        geographic bottlenecks, ship mode tradeoffs, sales impact, and logistics improvement opportunities.
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR FILTERS
# ============================================================
st.sidebar.markdown("## 🎛️ Dashboard Filters")
st.sidebar.caption("Use these filters to explore shipment performance by date, region, division, state, and shipping mode.")

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "📅 Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

ship_modes = st.sidebar.multiselect(
    "🚚 Ship Mode",
    sorted(df["Ship Mode"].dropna().unique()),
    default=sorted(df["Ship Mode"].dropna().unique())
)

regions = st.sidebar.multiselect(
    "🌎 Region",
    sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

divisions = st.sidebar.multiselect(
    "🏷️ Division",
    sorted(df["Division"].dropna().unique()),
    default=sorted(df["Division"].dropna().unique())
)

states = st.sidebar.multiselect(
    "📍 State / Province Optional",
    sorted(df["State/Province"].dropna().unique())
)

delay_threshold = st.sidebar.slider(
    "⏱️ Delay Threshold Days",
    min_value=1,
    max_value=30,
    value=7,
    help="Shipments above this lead time are counted as delayed."
)

show_only_delayed = st.sidebar.checkbox("⚠️ Show Delayed Shipments Only")

# ============================================================
# FILTER DATA
# ============================================================
fdf = df[
    (df["Order Date"].dt.date >= start_date) &
    (df["Order Date"].dt.date <= end_date) &
    (df["Ship Mode"].isin(ship_modes)) &
    (df["Region"].isin(regions)) &
    (df["Division"].isin(divisions))
].copy()

if states:
    fdf = fdf[fdf["State/Province"].isin(states)]

if show_only_delayed:
    fdf = fdf[fdf["Lead Time"] > delay_threshold]

if fdf.empty:
    st.warning("No shipments match the selected filters. Please change the sidebar filters.")
    st.stop()

# ============================================================
# METRICS
# ============================================================
total_shipments = len(fdf)
avg_lead_time = fdf["Lead Time"].mean()
median_lead_time = fdf["Lead Time"].median()
delayed_shipments = (fdf["Lead Time"] > delay_threshold).sum()
delay_rate = delayed_shipments / total_shipments * 100 if total_shipments else 0
total_sales = fdf["Sales"].sum()
total_profit = fdf["Gross Profit"].sum()
profit_margin = total_profit / total_sales * 100 if total_sales else 0
unique_routes = fdf["Route"].nunique()
max_lead = fdf["Lead Time"].max()
efficiency_score = max(0, 100 - (avg_lead_time / max_lead * 100)) if max_lead > 0 else 100

st.markdown('<div class="section-title">📊 Executive KPI Overview</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    kpi_card("Shipments", f"{total_shipments:,}", "Filtered records")
with k2:
    kpi_card("Avg Lead Time", f"{avg_lead_time:.1f}d", f"Median: {median_lead_time:.1f}d")
with k3:
    kpi_card("Delay Rate", pct(delay_rate), f"> {delay_threshold} days")
with k4:
    kpi_card("Total Sales", money(total_sales), "Revenue impact")
with k5:
    kpi_card("Gross Profit", money(total_profit), f"Margin: {profit_margin:.1f}%")
with k6:
    kpi_card("Efficiency", pct(efficiency_score), f"{unique_routes} routes")

st.markdown("<br>", unsafe_allow_html=True)

cbtn1, cbtn2 = st.columns([1, 1])
with cbtn1:
    st.download_button(
        "📥 Download Filtered Data",
        data=fdf.to_csv(index=False),
        file_name="nassau_candy_filtered_shipments.csv",
        mime="text/csv"
    )
with cbtn2:
    st.caption(f"Showing data from **{start_date}** to **{end_date}** across **{fdf['State/Province'].nunique()} states**.")

st.markdown("---")

# ============================================================
# PREPARE AGGREGATIONS
# ============================================================
route_stats = (
    fdf.groupby("Route")
    .agg(
        Avg_Lead_Time=("Lead Time", "mean"),
        Median_Lead_Time=("Lead Time", "median"),
        Shipments=("Lead Time", "count"),
        Delayed=("Lead Time", lambda x: (x > delay_threshold).sum()),
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum")
    )
    .reset_index()
)
route_stats["Delay Rate"] = route_stats["Delayed"] / route_stats["Shipments"] * 100
route_stats["Efficiency Score"] = 100 - (route_stats["Avg_Lead_Time"] / route_stats["Avg_Lead_Time"].max() * 100)
route_stats = route_stats.round(2)

state_stats = (
    fdf.groupby(["State/Province", "State Code"])
    .agg(
        Avg_Lead_Time=("Lead Time", "mean"),
        Shipments=("Lead Time", "count"),
        Delayed=("Lead Time", lambda x: (x > delay_threshold).sum()),
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum")
    )
    .reset_index()
)
state_stats["Delay Rate"] = state_stats["Delayed"] / state_stats["Shipments"] * 100
state_stats = state_stats.round(2)

mode_stats = (
    fdf.groupby("Ship Mode")
    .agg(
        Avg_Lead_Time=("Lead Time", "mean"),
        Median_Lead_Time=("Lead Time", "median"),
        Shipments=("Lead Time", "count"),
        Delayed=("Lead Time", lambda x: (x > delay_threshold).sum()),
        Avg_Cost=("Cost", "mean"),
        Avg_Sales=("Sales", "mean")
    )
    .reset_index()
)
mode_stats["Delay Rate"] = mode_stats["Delayed"] / mode_stats["Shipments"] * 100
mode_stats = mode_stats.round(2)

factory_stats = (
    fdf.groupby("Factory")
    .agg(
        Avg_Lead_Time=("Lead Time", "mean"),
        Shipments=("Lead Time", "count"),
        Delayed=("Lead Time", lambda x: (x > delay_threshold).sum()),
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum")
    )
    .reset_index()
)
factory_stats["Delay Rate"] = factory_stats["Delayed"] / factory_stats["Shipments"] * 100
factory_stats = factory_stats.round(2)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Overview",
    "🏆 Route Efficiency",
    "🗺️ Geographic Analysis",
    "🚚 Ship Mode",
    "🚧 Bottlenecks",
    "📋 Executive Summary"
])

# ============================================================
# TAB 1: OVERVIEW
# ============================================================
with tab1:
    st.markdown('<div class="section-title">🏠 Business Overview</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 1])

    with col1:
        monthly = fdf.groupby("Month").agg(
            Avg_Lead_Time=("Lead Time", "mean"),
            Shipments=("Lead Time", "count")
        ).reset_index()

        fig = px.line(
            monthly,
            x="Month",
            y="Avg_Lead_Time",
            markers=True,
            title="Monthly Average Lead Time Trend",
            labels={"Avg_Lead_Time": "Avg Lead Time Days", "Month": "Order Month"}
        )
        fig.add_hline(
            y=delay_threshold,
            line_dash="dash",
            annotation_text=f"Delay Threshold: {delay_threshold}d"
        )
        st.plotly_chart(apply_chart_style(fig, 420), use_container_width=True)

    with col2:
        fig = px.pie(
            fdf,
            names="Region",
            values="Sales",
            hole=0.55,
            title="Sales Contribution by Region",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(apply_chart_style(fig, 420), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        top_products = fdf.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(
            top_products,
            x="Sales",
            y="Product Name",
            orientation="h",
            title="Top 10 Products by Sales",
            color="Sales",
            color_continuous_scale="Plasma"
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(apply_chart_style(fig, 450), use_container_width=True)

    with col4:
        fig = px.histogram(
            fdf,
            x="Lead Time",
            nbins=25,
            title="Lead Time Distribution",
            labels={"Lead Time": "Lead Time Days"},
            color_discrete_sequence=["#a855f7"]
        )
        fig.add_vline(x=delay_threshold, line_dash="dash", annotation_text="Delay Threshold")
        st.plotly_chart(apply_chart_style(fig, 450), use_container_width=True)

# ============================================================
# TAB 2: ROUTE EFFICIENCY
# ============================================================
with tab2:
    st.markdown('<div class="section-title">🏆 Route Efficiency Leaderboard</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ✅ Top 10 Fastest Routes")
        st.dataframe(
            route_stats.sort_values("Avg_Lead_Time").head(10),
            use_container_width=True,
            hide_index=True
        )
    with col2:
        st.markdown("#### ⚠️ Top 10 Slowest Routes")
        st.dataframe(
            route_stats.sort_values("Avg_Lead_Time", ascending=False).head(10),
            use_container_width=True,
            hide_index=True
        )

    col3, col4 = st.columns(2)
    with col3:
        top_delay_routes = route_stats.sort_values("Delay Rate", ascending=False).head(12)
        fig = px.bar(
            top_delay_routes,
            x="Delay Rate",
            y="Route",
            orientation="h",
            color="Delay Rate",
            color_continuous_scale="Reds",
            title="Highest Delay Rate Routes"
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(apply_chart_style(fig, 520), use_container_width=True)

    with col4:
        fig = px.scatter(
            route_stats,
            x="Shipments",
            y="Avg_Lead_Time",
            size="Sales",
            color="Delay Rate",
            hover_name="Route",
            color_continuous_scale="Plasma",
            title="Route Volume vs Lead Time"
        )
        fig.add_hline(y=delay_threshold, line_dash="dash", annotation_text="Delay Threshold")
        st.plotly_chart(apply_chart_style(fig, 520), use_container_width=True)

# ============================================================
# TAB 3: GEOGRAPHIC ANALYSIS
# ============================================================
with tab3:
    st.markdown('<div class="section-title">🗺️ Geographic Shipping Performance</div>', unsafe_allow_html=True)

    map_metric = st.radio(
        "Choose map metric",
        ["Avg_Lead_Time", "Shipments", "Delay Rate", "Sales"],
        horizontal=True
    )

    fig = px.choropleth(
        state_stats.dropna(subset=["State Code"]),
        locations="State Code",
        locationmode="USA-states",
        color=map_metric,
        scope="usa",
        hover_name="State/Province",
        hover_data={
            "Avg_Lead_Time": ":.1f",
            "Shipments": True,
            "Delay Rate": ":.1f",
            "Sales": ":,.0f",
            "State Code": False
        },
        color_continuous_scale="Plasma",
        title=f"US State-Level Shipping Performance: {map_metric}"
    )

    factory_df = pd.DataFrame([
        {"Factory": name, "lat": info["lat"], "lon": info["lon"]}
        for name, info in FACTORIES.items()
    ])
    fig.add_trace(go.Scattergeo(
        lat=factory_df["lat"],
        lon=factory_df["lon"],
        text=factory_df["Factory"],
        mode="markers+text",
        textposition="top center",
        marker=dict(size=13, color="#facc15", symbol="star"),
        name="Factories"
    ))
    fig.update_layout(geo=dict(bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(apply_chart_style(fig, 590), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Best Performing States")
        st.dataframe(
            state_stats.sort_values("Avg_Lead_Time").head(10),
            use_container_width=True,
            hide_index=True
        )
    with col2:
        st.markdown("#### Delay-Prone States")
        st.dataframe(
            state_stats.sort_values("Delay Rate", ascending=False).head(10),
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# TAB 4: SHIP MODE
# ============================================================
with tab4:
    st.markdown('<div class="section-title">🚚 Ship Mode Performance Analysis</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.box(
            fdf,
            x="Ship Mode",
            y="Lead Time",
            color="Ship Mode",
            title="Lead Time Distribution by Ship Mode",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.add_hline(y=delay_threshold, line_dash="dash", annotation_text="Delay Threshold")
        st.plotly_chart(apply_chart_style(fig, 450), use_container_width=True)

    with col2:
        fig = px.bar(
            mode_stats,
            x="Ship Mode",
            y="Delay Rate",
            color="Ship Mode",
            title="Delay Rate by Ship Mode",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(apply_chart_style(fig, 450), use_container_width=True)

    st.markdown("#### Ship Mode Summary Table")
    st.dataframe(mode_stats, use_container_width=True, hide_index=True)

    heatmap_data = (
        fdf.groupby(["Division", "Ship Mode"])["Lead Time"]
        .mean()
        .round(1)
        .reset_index()
        .pivot(index="Division", columns="Ship Mode", values="Lead Time")
    )
    fig = px.imshow(
        heatmap_data,
        text_auto=True,
        color_continuous_scale="Plasma",
        title="Average Lead Time Heatmap: Division × Ship Mode"
    )
    st.plotly_chart(apply_chart_style(fig, 480), use_container_width=True)

# ============================================================
# TAB 5: BOTTLENECKS
# ============================================================
with tab5:
    st.markdown('<div class="section-title">🚧 Bottleneck Detection</div>', unsafe_allow_html=True)

    bottleneck_df = state_stats.copy()
    bottleneck_df["Bottleneck Score"] = (
        bottleneck_df["Shipments"].rank(pct=True) * 0.45 +
        bottleneck_df["Avg_Lead_Time"].rank(pct=True) * 0.35 +
        bottleneck_df["Delay Rate"].rank(pct=True) * 0.20
    ) * 100
    bottleneck_df = bottleneck_df.sort_values("Bottleneck Score", ascending=False).round(2)

    col1, col2 = st.columns([1.05, 1])
    with col1:
        fig = px.bar(
            bottleneck_df.head(12),
            x="Bottleneck Score",
            y="State/Province",
            orientation="h",
            color="Bottleneck Score",
            color_continuous_scale="Magma",
            title="Top Bottleneck States"
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(apply_chart_style(fig, 520), use_container_width=True)

    with col2:
        fig = px.scatter(
            state_stats,
            x="Shipments",
            y="Avg_Lead_Time",
            size="Sales",
            color="Delay Rate",
            hover_name="State/Province",
            color_continuous_scale="Plasma",
            title="Shipment Volume vs Avg Lead Time by State"
        )
        fig.add_hline(y=delay_threshold, line_dash="dash", annotation_text="Delay Threshold")
        st.plotly_chart(apply_chart_style(fig, 520), use_container_width=True)

    st.markdown("#### Bottleneck Priority Table")
    st.dataframe(bottleneck_df.head(15), use_container_width=True, hide_index=True)

# ============================================================
# TAB 6: EXECUTIVE SUMMARY
# ============================================================
with tab6:
    st.markdown('<div class="section-title">📋 Executive Summary</div>', unsafe_allow_html=True)

    best_route = route_stats.sort_values("Avg_Lead_Time").iloc[0]
    worst_route = route_stats.sort_values("Avg_Lead_Time", ascending=False).iloc[0]
    fastest_mode = mode_stats.sort_values("Avg_Lead_Time").iloc[0]
    slowest_mode = mode_stats.sort_values("Avg_Lead_Time", ascending=False).iloc[0]
    best_state = state_stats.sort_values("Avg_Lead_Time").iloc[0]
    worst_state = state_stats.sort_values("Avg_Lead_Time", ascending=False).iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="insight-card">
            <h4>✅ Key Wins</h4>
            <ul>
                <li><b>Fastest Route:</b> {best_route['Route']} with {best_route['Avg_Lead_Time']:.1f} days average lead time.</li>
                <li><b>Best State:</b> {best_state['State/Province']} with {best_state['Avg_Lead_Time']:.1f} days average lead time.</li>
                <li><b>Fastest Ship Mode:</b> {fastest_mode['Ship Mode']} with {fastest_mode['Avg_Lead_Time']:.1f} days average lead time.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="insight-card">
            <h4>⚠️ Risk Areas</h4>
            <ul>
                <li><b>Slowest Route:</b> {worst_route['Route']} with {worst_route['Avg_Lead_Time']:.1f} days average lead time.</li>
                <li><b>Worst State:</b> {worst_state['State/Province']} with {worst_state['Avg_Lead_Time']:.1f} days average lead time.</li>
                <li><b>Slowest Ship Mode:</b> {slowest_mode['Ship Mode']} with {slowest_mode['Avg_Lead_Time']:.1f} days average lead time.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card">
        <h4>📌 Business Interpretation</h4>
        <p>
            This dashboard shows that Nassau Candy Distributor's shipping performance varies across routes,
            states, factories, and ship modes. The current filtered view includes <b>{total_shipments:,}</b> shipments,
            with an average lead time of <b>{avg_lead_time:.1f} days</b> and a delay rate of <b>{delay_rate:.1f}%</b>
            using a delay threshold of <b>{delay_threshold} days</b>.
        </p>
        <p>
            The biggest improvement opportunity is to focus on high-volume states and routes where both lead time
            and delay rate are high. These bottlenecks can directly affect customer satisfaction, logistics cost,
            and delivery reliability.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card">
        <h4>💡 Recommendations</h4>
        <ol>
            <li>Prioritize optimization for high-volume, high-delay states identified in the bottleneck tab.</li>
            <li>Review slowest factory-to-state routes and compare them with top-performing routes.</li>
            <li>Use faster ship modes strategically for delay-prone regions and priority customers.</li>
            <li>Monitor monthly lead time trends to identify whether logistics performance is improving or worsening.</li>
            <li>Build a future predictive model to estimate delivery delays before shipment dispatch.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Factory Performance Table")
    st.dataframe(factory_stats, use_container_width=True, hide_index=True)
