# Save as fetch_and_clean_india_gdp.py
import requests
import pandas as pd

# --- Parameters ---
country = "IN"
start_year = 2014
end_year = 2024
years = list(range(start_year, end_year + 1))

# Indicators (World Bank codes)
indicators = {
    "NY.GDP.MKTP.CD": "GDP_current_USD",
    "NY.GDP.MKTP.KD": "GDP_constant_2015_USD",
    "NY.GDP.MKTP.KD.ZG": "GDP_growth_pct",
    "NY.GDP.PCAP.CD": "GDP_per_capita_current_USD",
    "SP.POP.TOTL": "Population_total"
}

def fetch_indicator(indicator_code, short_name):
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator_code}"
    params = {"date": f"{start_year}:{end_year}", "format": "json", "per_page": 1000}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    if len(data) < 2 or data[1] is None:
        print(f"⚠️ No data found for {short_name}")
        return pd.DataFrame({"year": years, short_name: [None]*len(years)})
    records = data[1]
    rows = []
    for rec in records:
        year = int(rec["date"])
        value = rec["value"]
        rows.append({"year": year, short_name: value})
    return pd.DataFrame(rows)

# Fetch all indicators
dfs = {}
for code, short in indicators.items():
    print("Fetching", code)
    dfs[short] = fetch_indicator(code, short)

# Start with years DataFrame
df = pd.DataFrame({"year": years})

# Merge
for short, ind_df in dfs.items():
    df = df.merge(ind_df, on="year", how="left")

# Convert numeric
num_cols = [c for c in df.columns if c != "year"]
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# Interpolate missing
df_clean = df.copy()
for c in num_cols:
    if df_clean[c].isna().any():
        df_clean[c] = df_clean[c].interpolate(method="linear", limit_direction="both")

# Derived
df_clean["GDP_current_billion_USD"] = df_clean["GDP_current_USD"] / 1e9
df_clean["GDP_constant_2015_billion_USD"] = df_clean["GDP_constant_2015_USD"] / 1e9

# Flag imputed values
df_clean["notes_missing_imputed"] = False
for c in num_cols:
    imputed = df[c].isna() & df_clean[c].notna()
    df_clean.loc[imputed, "notes_missing_imputed"] = True

# Save
out_csv = "india_gdp_2014_2024.csv"
df_clean.to_csv(out_csv, index=False)
print("✅ Saved cleaned CSV to", out_csv)

# Preview
print(df_clean.head(12))
