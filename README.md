# 🍬 Nassau Candy Distributor — Shipping Route Efficiency Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-purple?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 🚚 Factory-to-Customer Shipping Route Efficiency Analysis

This project analyzes **Nassau Candy Distributor’s shipping operations** to understand delivery performance, identify delay-prone routes, and improve logistics decision-making.

The dashboard converts raw order and shipment data into interactive insights such as **lead time, delayed shipments, route efficiency, geographic bottlenecks, ship mode performance, and executive recommendations**.

---

## 🌐 Live Dashboard

🔗 **Streamlit App:** https://supply-chain-shipping-analysis-nmveh3kpdjkmjztn73ks3n.streamlit.app

---

## 📌 Project Objective

The main goal of this project is to answer one important business question:

> **Which factory-to-customer shipping routes are efficient, and which routes are causing delays or logistics bottlenecks?**

By analyzing shipment records, this project helps logistics teams make data-driven decisions to reduce delays, improve route planning, and optimize shipping performance.

---

## ❗ Business Problem

Nassau Candy Distributor ships products from multiple factories to customers across different states and regions. Without proper route-level visibility, the company may struggle to identify:

- 🚧 Delay-prone routes
- 🗺️ Geographic bottlenecks
- 🚚 Slow shipping modes
- 🏭 Underperforming factory routes
- 📦 High-volume routes with poor delivery performance

This dashboard solves that problem by providing a clear, interactive view of shipping efficiency.

---

## 📊 Key Performance Indicators

| KPI | Description |
|---|---|
| ⏱️ **Average Lead Time** | Average number of days between order date and ship date |
| 📦 **Total Shipments** | Total number of shipment records analyzed |
| ⚠️ **Delayed Shipments** | Shipments crossing the selected delay threshold |
| 💰 **Total Sales** | Total sales generated from filtered shipments |
| 📈 **Gross Profit** | Total gross profit from shipments |
| 🏆 **Efficiency Score** | Normalized score used to compare route performance |

---

## ✨ Dashboard Features

### 🏆 Route Efficiency
- Top 10 fastest shipping routes
- Bottom 10 slowest shipping routes
- Lead time distribution by factory
- Monthly lead time trend in detailed mode

### 🗺️ Geographic Map
- US state-level shipping heatmap
- Factory location markers
- Map views by average lead time, shipment volume, and delay percentage

### 🚚 Ship Mode Analysis
- Lead time comparison by ship mode
- Delay rate by shipping method
- Shipment volume by ship mode
- Division × Ship Mode performance heatmap

### 🔍 Route Drill-Down
- State-level shipment performance
- Product-wise lead time analysis
- Ship mode mix by selected state
- Order-level shipment timeline

### 🚧 Bottleneck Detection
- Identifies high-volume states with long lead times
- Helps prioritize logistics improvement areas

### 📋 Executive Summary
- Automated business summary
- Best and worst routes
- Best and worst states
- Ship mode recommendations
- Actionable logistics improvement suggestions

---

## 🧠 Methodology

### 1️⃣ Data Cleaning
- Converted order and ship dates into datetime format
- Removed invalid date records
- Removed negative lead times
- Prepared clean shipment records for analysis

### 2️⃣ Feature Engineering
- Created **Lead Time** using:

```text
Lead Time = Ship Date - Order Date
```

- Mapped each product to its respective factory
- Created route labels using factory and destination information
- Extracted monthly order trends

### 3️⃣ Analysis
- Grouped data by route, factory, state, division, and ship mode
- Calculated average lead time, shipment count, delay count, and delay percentage
- Created route efficiency scores and bottleneck indicators

### 4️⃣ Dashboard Development
- Built an interactive Streamlit dashboard
- Added filters for date, ship mode, region, division, state, and delay threshold
- Used Plotly visualizations for charts, maps, and drill-down analysis

---

## 📈 Key Insights

- 🚚 Delivery performance varies significantly across factory-to-state routes.
- 🗺️ Some states show higher average lead times and act as bottleneck zones.
- ⚠️ Routes with both high shipment volume and high lead time require immediate attention.
- 🚛 Ship mode strongly impacts delivery speed and delay percentage.
- 🏭 Factory-level performance comparison helps identify operational inefficiencies.

---

## 💡 Business Recommendations

- Optimize high-delay, high-volume shipping routes first.
- Use expedited shipping only for priority or delay-prone destinations.
- Monitor state-level bottlenecks regularly.
- Compare factories using lead time and delay rate metrics.
- Improve logistics planning using route-level performance trends.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python** | Data processing and analysis |
| **Pandas** | Data cleaning and transformation |
| **NumPy** | Numerical operations |
| **Plotly** | Interactive charts and maps |
| **Streamlit** | Web dashboard development |
| **Jupyter Notebook** | Exploratory data analysis |

---

## 📂 Project Structure

```text
Nassau-Candy-Shipping-Analysis/
│
├── candy_app.py                         # Streamlit dashboard application
├── candy_train_data.ipynb          # Data analysis notebook
├── Nassau Candy Distributor.csv    # Dataset
├── requirements.txt                # Required Python packages
├── Research_paper.pdf              # Project report / research paper
└── README.md                       # Project documentation
```

---

## 🚀 How to Run Locally

### 1️⃣ Clone the Repository

```bash
git clone <your-github-repository-link>
cd <your-project-folder>
```

### 2️⃣ Install Required Libraries

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Streamlit App

```bash
streamlit run app.py
```

---

## 📦 Required Packages

```text
streamlit
pandas
numpy
plotly
```

---

## 📊 Dashboard Preview

> Add your dashboard screenshot here after deployment.

```markdown
![Dashboard Preview](your-screenshot-link-here)
```

---

## 🔮 Future Enhancements

- Predict delivery delay using machine learning
- Add distance-based route optimization
- Include real-time shipment tracking
- Add cost vs delivery speed optimization
- Deploy advanced forecasting for route delays

---

## 📌 Conclusion

This project demonstrates how data analytics can improve logistics and supply chain performance. By analyzing shipping lead time, delay frequency, route efficiency, and geographic bottlenecks, the dashboard helps identify where delivery operations are strong and where improvements are needed.

The final dashboard provides a clear, interactive, and business-friendly solution for monitoring shipping performance and making smarter logistics decisions.

---

## 👩‍💻 Author

**Prasanna rani**  
Data Science / Data Analytics Project

---

## ⭐ If you found this project useful

Give this repository a ⭐ and connect with me on LinkedIn.
