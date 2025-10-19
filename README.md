# 🇮🇳 Decoding a Decade: Visualizing India’s GDP Growth (2014–2024)

### 📊 A Data Visualization Project using Streamlit, Plotly, and Python

---

## 🧠 Project Overview

**"Decoding a Decade"** is an interactive data visualization dashboard that explores **India’s GDP growth trends from 2014 to 2024**.  
It provides a visual journey through India’s economic rise — capturing the effects of reforms, global events like COVID-19, and post-pandemic recovery.

---

## 📂 Dataset Details

- **Source:** World Bank — World Development Indicators (API)
- **Fetched Using:** `requests` library in Python  
- **Years Covered:** 2014–2024  
- **Indicators Used:**
  | Indicator Code | Description |
  |----------------|-------------|
  | NY.GDP.MKTP.CD | GDP (current US$) |
  | NY.GDP.MKTP.KD | GDP (constant 2015 US$) |
  | NY.GDP.MKTP.KD.ZG | GDP growth (%) |
  | NY.GDP.PCAP.CD | GDP per capita (current US$) |
  | SP.POP.TOTL | Total population |

After fetching, the dataset was **cleaned and interpolated** for missing years using `pandas`, and exported as  
👉 `india_gdp_2014_2024.csv`

---

## 🧰 Tools & Technologies

| Category | Tools Used |
|-----------|-------------|
| Programming | Python |
| Data Handling | Pandas |
| Visualization | Plotly Express, Matplotlib |
| Dashboard Framework | Streamlit |
| Dataset Source | World Bank API |
| Version Control | Git + GitHub |

---

## ⚙️ How to Run the Project

pip install -r requirements.txt

streamlit run gdp_dashboard.py

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/TejaswiniH123/india-gdp-visualization.git
cd india-gdp-visualization
