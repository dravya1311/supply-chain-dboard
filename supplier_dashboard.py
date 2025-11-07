import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Supply Chain Dashboard | Ravindra Yadav",
    page_icon="📦",
    layout="wide"
)

# -------------------------
# Title Section
# -------------------------
st.title("📊 Supply Chain Analytics Dashboard")
st.caption("Developed by **Ravindra Yadav** — Streamlit + Plotly")

# -------------------------
# Load Data Automatically
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("supply_chain_data.csv")
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ 'supply_chain_data.csv' not found. Place it in the same folder as this script.")
    st.stop()

st.success("✅ Data loaded successfully!")

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("🔍 Filters")

suppliers = st.sidebar.multiselect("Select Supplier(s)", df['supplier_name'].dropna().unique())
origins = st.sidebar.multiselect("Select Origin(s)", df['origin'].dropna().unique())
destinations = st.sidebar.multiselect("Select Destination(s)", df['destination'].dropna().unique())

filtered_df = df.copy()
if suppliers:
    filtered_df = filtered_df[filtered_df['supplier_name'].isin(suppliers)]
if origins:
    filtered_df = filtered_df[filtered_df['origin'].isin(origins)]
if destinations:
    filtered_df = filtered_df[filtered_df['destination'].isin(destinations)]

# -------------------------
# KPI Metrics
# -------------------------
total_revenue = filtered_df['revenue_generated'].sum()
total_cost = filtered_df['costs'].sum()
total_volume = filtered_df['production_volumes'].sum()
avg_lead_time = filtered_df['lead_time'].mean()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
kpi2.metric("💸 Total Cost", f"₹{total_cost:,.0f}")
kpi3.metric("🏭 Total Production Volume", f"{total_volume:,.0f}")
kpi4.metric("⏱ Avg Lead Time (Days)", f"{avg_lead_time:.1f}")

st.markdown("---")

# -------------------------
# Dashboard Tabs
# -------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🛣️ Route Cost", "🏭 Supplier Performance", "📦 Product Demand",
    "🌍 Origin Overview", "📈 Cost vs Revenue Trend"
])

# --- Tab 1: Route Cost ---
with tab1:
    st.subheader("🛣️ Average Route-wise Cost")
    route_df = filtered_df.groupby(['origin', 'destination'])['costs'].mean().reset_index()
    if not route_df.empty:
        fig1 = px.scatter(route_df, x='origin', y='destination', size='costs', color='costs',
                          color_continuous_scale='tealrose', title="Average Route-wise Cost")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("No data available for selected filters.")

# --- Tab 2: Supplier Performance ---
with tab2:
    st.subheader("🏭 Top 5 Suppliers by Production Volume")
    supplier_vol = filtered_df.groupby(['supplier_name', 'product_type'])['production_volumes'].sum().reset_index()
    top5_suppliers = supplier_vol.groupby('supplier_name')['production_volumes'].sum().nlargest(5).index
    top_df = supplier_vol[supplier_vol['supplier_name'].isin(top5_suppliers)]
    if not top_df.empty:
        fig2 = px.bar(top_df, x='supplier_name', y='production_volumes',
                      color='product_type', text_auto=True,
                      title="Top 5 Suppliers by Production Volume (Product Split)",
                      template='plotly_white')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("No supplier data available.")

# --- Tab 3: Product Demand ---
with tab3:
    st.subheader("📦 Top 5 Most Demanded Products")
    demand_df = filtered_df.groupby('product_type')['number_of_products_sold'].sum().nlargest(5).reset_index()
    if not demand_df.empty:
        fig3 = px.bar(demand_df, x='product_type', y='number_of_products_sold',
                      color='product_type', text_auto=True,
                      title="Top 5 Most Demanded Products", template='seaborn')
        st.plotly_chart(fig3, use_container_width=True)
    else:
