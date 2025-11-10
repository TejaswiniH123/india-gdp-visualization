# gdp_visualization.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load dataset
df = pd.read_csv("india_gdp_2014_2024.csv")

# --- 1. GDP Growth Line Chart ---
plt.figure(figsize=(8,5))
sns.lineplot(data=df, x="year", y="GDP_growth_pct", marker="o", color="green")
plt.title("India GDP Growth (%) Over Years")
plt.xlabel("Year")
plt.ylabel("Growth (%)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()

# --- 2. GDP Current vs Constant ---
plt.figure(figsize=(10,6))
sns.lineplot(data=df, x="year", y="GDP_current_billion_USD", marker="o", label="Current USD")
sns.lineplot(data=df, x="year", y="GDP_constant_2015_billion_USD", marker="o", label="Constant 2015 USD")
plt.title("India GDP (Billions USD)")
plt.xlabel("Year")
plt.ylabel("Billions USD")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()

# --- 3. GDP per Capita ---
fig = px.line(df, x="year", y="GDP_per_capita_current_USD",
              title="GDP per Capita (USD)",
              markers=True)
fig.show()

# --- 4. Population Growth ---
fig = px.bar(df, x="year", y="Population_total",
             title="India Population (2014–2024)",
             color="Population_total",
             color_continuous_scale="viridis")
fig.show()
