# 🚀 AI-Powered Business Intelligence Dashboard

> **An End-to-End Advanced Analytics & Machine Learning Platform**

Welcome to my portfolio project! This application demonstrates my ability as a **Senior Data Analyst & AI Engineer** to bridge the gap between raw data and actionable business strategy. 

Instead of building a traditional static dashboard, I Architected and developed a full-stack, AI-powered Business Intelligence platform that automatically surfaces anomalies, forecasts future revenue, and generates natural-language business insights.

---

## 🎯 Executive Summary & Impact

Modern businesses are drowning in data but starving for insights. Traditional BI tools require analysts to manually sift through charts to find drops in revenue or shifting consumer trends. 

**My Solution:** I built an intelligent system that does the heavy lifting:
- **Reduces Time-to-Insight:** Automated rule-based NLP engines instantly translate metrics into plain English (e.g., *"Revenue decreased by 48.0% compared to last week"*).
- **Proactive Anomaly Detection:** Utilizes statistical modeling to flag abnormal spikes or drops in revenue before they impact the bottom line.
- **Accurate Forecasting:** Employs advanced time-series modeling to project future performance with 95% confidence intervals, enabling proactive supply chain and marketing decisions.

---

## 🧠 Key Analytical & AI Features

### 1. Advanced Anomaly Detection (Machine Learning + Statistics)
I implemented a robust, ensemble approach to outlier detection:
- **Z-Score Analysis:** A statistical baseline that flags instances where daily revenue deviates by more than `2.5σ` from the moving average.
- **Isolation Forest Algorithm:** A machine learning model (via `scikit-learn`) that identifies complex, multi-dimensional anomalies that simple statistics might miss.
- **Severity Scoring:** Automatically categorizes anomalies into High, Medium, or Low severity based on standard deviation magnitude, helping stakeholders prioritize responses.

### 2. Time-Series Forecasting
To empower forward-looking strategy, I integrated predictive modeling:
- **Prophet Integration:** Uses Facebook's Prophet library for robust, daily-level forecasting that gracefully handles missing data and large outliers.
- **Statistical Fallback (ARIMA/ETS):** Engineered a highly resilient pipeline mapping to Exponential Smoothing if advanced dependencies are missing in production.
- **Confidence Intervals (95% CI):** Visualizes upper and lower bounds to communicate the statistical variance and risk to business stakeholders.

### 3. Automated NLP Insights Engine
Data is only valuable if it can be understood by non-technical teams. I designed an intelligence engine that programmatically traverses the dataset to generate contextual, natural-language insights:
- Evaluates Week-over-Week (WoW) and Month-over-Month (MoM) performance.
- Identifies the fastest-growing vs. highest-revenue product categories.
- Extracts hidden patterns, such as the most lucrative day of the week or optimal discount percentages.

---

## 🛠️ Technical Skills Showcased

This project was built from scratch, demonstrating my ability to architect and deploy production-ready applications across the entire data stack.

### Data Science & Analytics
- **Data Manipulation:** Advanced `pandas` & `NumPy` for in-memory data transformation, aggregation, and filtering.
- **Statistical Modeling:** Hypothesis testing, confidence intervals, moving averages, and standard deviation calculations.
- **Predictive Analytics:** Time-series forecasting (`Prophet`, `statsmodels`).
- **Machine Learning:** Unsupervised learning for anomaly detection (`scikit-learn` Isolation Forest).

### Full-Stack Engineering & Architecture
- **Backend (Python/FastAPI):** Built a highly modular, asynchronous RESTful API with strict data validation using `Pydantic`.
- **Frontend (React/Vite):** Developed an interactive, responsive UI leveraging `React Query` for data fetching and `Recharts` for complex data visualizations.
- **Real-Time Data (WebSockets):** Implemented a live WebSocket connection to continuously stream real-time metric snapshots to the client.
- **DevOps & Deployment:** Containerized the entire microservice architecture using `Docker` and `Docker Compose`, bundled with an `Nginx` reverse proxy.

---

## 📊 The Data

The dashboard is powered by an e-commerce dataset spanning 11 months of 2024. It processes thousands of transactional records mapping to user demographics, product hierarchies, pricing algorithms, and temporal metadata to synthesize the business's overall health.

---

## 📥 Want to see it in action?

To run this project locally, please refer to the technical [README.md](./README.md) for full setup instructions (Docker or manual startup).

---

*Thank you for reviewing my work! I am passionate about utilizing data to drive operational excellence and build AI-driven products that deliver measurable business value.*
