# fetch_and_clean_india_gdp.py
import requests
import pandas as pd

# -------------------------------
# Parameters
# -------------------------------
country = "IN"
start_year = 2014
end_year = 2024
years = list(range(start_year, end_year + 1))

# World Bank Indicators
indicators = {
    "NY.GDP.MKTP.CD": "GDP_current_USD",
    "NY.GDP.MKTP.KD": "GDP_constant_2015_USD",
    "NY.GDP.MKTP.KD.ZG": "GDP_growth_pct",
    "NY.GDP.PCAP.CD": "GDP_per_capita_current_USD",
    "SP.POP.TOTL": "Population_total"
}

def fetch_indicator(indicator_code, short_name):
    """Fetch indicator data from World Bank API."""
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator_code}"
    params = {"date": f"{start_year}:{end_year}", "format": "json", "per_page": 1000}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    if len(data) < 2 or data[1] is None:
        print(f"⚠️ No data found for {short_name}")
        return pd.DataFrame({"year": years, short_name: [None]*len(years)})
    records = data[1]
    rows = [{"year": int(rec["date"]), short_name: rec["value"]} for rec in records]
    return pd.DataFrame(rows)

# -------------------------------
# Fetch all indicators
# -------------------------------
dfs = {}
for code, short in indicators.items():
    print("📡 Fetching:", code)
    dfs[short] = fetch_indicator(code, short)

# -------------------------------
# Merge all indicators into one DataFrame
# -------------------------------
df = pd.DataFrame({"year": years})
for short, ind_df in dfs.items():
    df = df.merge(ind_df, on="year", how="left")

# Convert to numeric
num_cols = [c for c in df.columns if c != "year"]
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors="coerce")

# Interpolate missing values
df_clean = df.interpolate(method="linear", limit_direction="both")

# Derived columns
df_clean["GDP_current_billion_USD"] = df_clean["GDP_current_USD"] / 1e9
df_clean["GDP_constant_2015_billion_USD"] = df_clean["GDP_constant_2015_USD"] / 1e9

# Save cleaned dataset
out_csv = "india_gdp_2014_2024.csv"
df_clean.to_csv(out_csv, index=False)
print(f"✅ Cleaned data saved as {out_csv}")
print(df_clean.head(10))
