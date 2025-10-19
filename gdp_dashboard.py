import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Load Data
# -------------------------------
df = pd.read_csv("india_gdp_2014_2024.csv")
df["year"] = df["year"].astype(int)

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(page_title="Decoding a Decade: India's GDP Growth (2014–2024)",
                   layout="wide",
                   page_icon="🇮🇳")

# -------------------------------
# Dashboard Header
# -------------------------------
st.title("*Decoding a Decade: India’s GDP Growth (2014–2024)*")
st.markdown("""
A visual journey through India’s economic rise — highlighting key reforms, global shocks, and recovery trends.
""")
st.markdown("---")

# -------------------------------
# Latest Year KPIs
# -------------------------------
latest = df[df["year"] == df["year"].max()].iloc[0]
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 GDP (Trillion USD)", f"{latest['GDP_current_billion_USD']/1000:.2f}")
col2.metric("🏭 Real GDP (Trillion USD)", f"{latest['GDP_constant_2015_billion_USD']/1000:.2f}")
col3.metric("📈 GDP Growth (%)", f"{latest['GDP_growth_pct']:.2f}%")
col4.metric("👤 GDP per Capita (USD)", f"{latest['GDP_per_capita_current_USD']:.0f}")

# -------------------------------
# Year Range Selector
# -------------------------------
years = st.slider("Select Year Range",
                  int(df["year"].min()),
                  int(df["year"].max()),
                  (int(df["year"].min()), int(df["year"].max())))

filtered_df = df[(df["year"] >= years[0]) & (df["year"] <= years[1])]

# -------------------------------
# Chart 1: Bar Chart — GDP Growth (%)
# -------------------------------
st.subheader("📊 Annual GDP Growth Rate (%) — Bar Chart")
fig_bar = px.bar(filtered_df, x="year", y="GDP_growth_pct",
                 color="GDP_growth_pct",
                 color_continuous_scale=["#ff4b4b", "#ffd93d", "#4bb543"],
                 text="GDP_growth_pct",
                 title="India’s GDP Growth Rate (2014–2024)")
fig_bar.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig_bar.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
                      font=dict(color="white"), coloraxis_showscale=False)
st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------------
# Chart 2: Line Chart — Nominal vs Real GDP
# -------------------------------
st.subheader("💹 Nominal vs Real GDP (Billions USD) — Line Chart")
fig_line = px.line(filtered_df, x="year",
                   y=["GDP_current_billion_USD", "GDP_constant_2015_billion_USD"],
                   markers=True,
                   color_discrete_sequence=["#00C9A7", "#FFC300"],
                   labels={"value": "GDP (Billion USD)", "variable": "Type"},
                   title="Nominal vs Real GDP (2014–2024)")
fig_line.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
                       font=dict(color="white"))
st.plotly_chart(fig_line, use_container_width=True)

# -------------------------------
# Chart 3: Pie Chart — GDP share by year
# -------------------------------
st.subheader("🥧 GDP Share by Year — Pie Chart")
pie_df = filtered_df.copy()
pie_df["GDP_Share_%"] = (pie_df["GDP_current_billion_USD"] / pie_df["GDP_current_billion_USD"].sum()) * 100
fig_pie = px.pie(pie_df, names="year", values="GDP_current_billion_USD",
                 color_discrete_sequence=px.colors.qualitative.Safe,
                 title="Share of Each Year in Total GDP (2014–2024)",
                 hover_data=["GDP_Share_%"])
fig_pie.update_traces(textinfo='percent+label')
fig_pie.update_layout(paper_bgcolor="#0E1117", font=dict(color="white"))
st.plotly_chart(fig_pie, use_container_width=True)

# -------------------------------
# Chart 4: Scatter Plot — GDP Growth vs GDP per Capita
# -------------------------------
st.subheader("💡 Relationship Between GDP Growth and GDP per Capita — Scatter Plot")
fig_scatter = px.scatter(
    filtered_df,
    x="GDP_growth_pct",
    y="GDP_per_capita_current_USD",
    size="GDP_current_billion_USD",
    color="year",
    color_continuous_scale="Viridis",
    hover_name="year",
    title="GDP Growth (%) vs GDP per Capita (2014–2024)",
    labels={
        "GDP_growth_pct": "GDP Growth (%)",
        "GDP_per_capita_current_USD": "GDP per Capita (USD)"
    }
)
fig_scatter.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
fig_scatter.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
                          font=dict(color="white"))
st.plotly_chart(fig_scatter, use_container_width=True)

# -------------------------------
# Chart 5: Area Chart — GDP Level by Growth Category
# -------------------------------
st.subheader("🌄 GDP Level by Growth Category — Area Chart")
area_df = filtered_df.copy()
area_df["Growth_Category"] = pd.cut(
    area_df["GDP_growth_pct"],
    bins=[-10, 0, 5, 10],
    labels=["Negative", "Moderate", "High"]
)
fig_area = px.area(area_df, x="year", y="GDP_current_billion_USD",
                   color="Growth_Category",
                   color_discrete_map={"Negative": "#FF4B4B", "Moderate": "#FFD93D", "High": "#4BB543"},
                   title="GDP Level (Billions USD) Categorized by Growth Intensity",
                   labels={"GDP_current_billion_USD": "GDP (Billion USD)"})
fig_area.update_layout(plot_bgcolor="#0E1117", paper_bgcolor="#0E1117",
                       font=dict(color="white"))
st.plotly_chart(fig_area, use_container_width=True)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("""
📚 *Data Source:* World Bank (World Development Indicators)  
🧭 *Key Events:*
- 2015: GDP rebasing (2011–12 prices)
- 2016: Demonetization
- 2020: COVID-19 pandemic
- 2021–24: Economic recovery

✨ Built with Streamlit + Plotly
""")