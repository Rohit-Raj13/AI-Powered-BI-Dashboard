# 🧠 AI-Powered BI Dashboard

An end-to-end interactive Business Intelligence dashboard built on real e-commerce data featuring:
- **Traditional Analytics** — KPI summary, time-series, category breakdowns
- **Anomaly Detection** — Z-score + Isolation Forest
- **Revenue Forecasting** — Prophet with 95% confidence intervals
- **AI Insights** — Rule-based natural-language summaries
- **Real-time Updates** — WebSocket live metrics feed

---

## 📁 Project Structure

```
bi_dashboard/
├── backend/
│   ├── main.py              ← FastAPI entry point
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── data/
│   │   └── ecommerce_dataset_updated.csv
│   └── app/
│       ├── config.py
│       ├── data_service.py  ← pandas data layer
│       ├── schemas.py       ← Pydantic models
│       ├── routers/
│       │   ├── metrics.py   ← /metrics/*
│       │   ├── anomaly.py   ← /anomaly/detect
│       │   ├── forecast.py  ← /forecast
│       │   ├── insights.py  ← /insights
│       │   └── websocket.py ← /ws/live
│       └── ml/
│           ├── anomaly_detector.py  ← Z-score + IsolationForest
│           ├── forecaster.py        ← Prophet + ETS fallback
│           └── insight_engine.py    ← Rule-based insights
│
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── Dockerfile
│   ├── nginx.conf
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css        ← Dark glassmorphism design system
│       ├── api/
│       │   ├── client.js    ← Axios calls
│       │   └── hooks.js     ← React Query hooks
│       ├── components/
│       │   ├── KPICard.jsx
│       │   ├── TimeSeriesChart.jsx
│       │   ├── AnomalyChart.jsx
│       │   ├── ForecastChart.jsx
│       │   ├── InsightsPanel.jsx
│       │   ├── CategoryBreakdown.jsx
│       │   └── Sidebar.jsx
│       └── pages/
│           └── Dashboard.jsx
│
└── docker-compose.yml
```

---

## 🚀 Local Setup

### Option A — Manual (Recommended for development)

#### 1. Backend

```bash
cd bi_dashboard/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn main:app --reload --port 8000
```

API docs available at: **http://localhost:8000/docs**

#### 2. Frontend

> Requires Node.js 18+ and npm

```bash
cd bi_dashboard/frontend

npm install
npm run dev
```

Dashboard available at: **http://localhost:5173**

---

### Option B — Docker Compose (One command)

```bash
cd bi_dashboard
docker compose up --build
```

- Backend: http://localhost:8000/docs
- Frontend: http://localhost:3000

---

## 🌐 API Endpoints

| Method | Endpoint               | Description                        |
|--------|------------------------|------------------------------------|
| GET    | `/health`              | Health check                       |
| GET    | `/metrics/summary`     | KPI totals + WoW/MoM changes       |
| GET    | `/metrics/timeseries`  | Daily/weekly/monthly revenue       |
| GET    | `/metrics/categories`  | Revenue breakdown by category      |
| GET    | `/metrics/payments`    | Order count by payment method      |
| GET    | `/anomaly/detect`      | Z-score + Isolation Forest results |
| GET    | `/forecast`            | 30-day revenue forecast with 95%CI |
| GET    | `/insights`            | AI-generated insight strings       |
| WS     | `/ws/live`             | Real-time metrics stream           |

### Common Query Parameters

| Param            | Example          | Description          |
|------------------|------------------|----------------------|
| `start_date`     | `2024-01-01`     | Filter start         |
| `end_date`       | `2024-06-30`     | Filter end           |
| `category`       | `Electronics`    | Filter by category   |
| `payment_method` | `UPI`            | Filter by payment    |
| `granularity`    | `monthly`        | daily/weekly/monthly |
| `periods`        | `30`             | Forecast days (7-90) |

---

## 🛠 Tech Stack

| Layer        | Technology              |
|--------------|-------------------------|
| Backend      | FastAPI + Uvicorn       |
| Data         | pandas (in-memory)      |
| Anomaly      | Z-score (scipy) + Isolation Forest (sklearn) |
| Forecasting  | Prophet + ETS fallback  |
| Frontend     | React 18 + Vite 5       |
| Charts       | Recharts 2              |
| Data Layer   | React Query v5          |
| HTTP Client  | Axios                   |
| Containers   | Docker + Docker Compose |

---

## ☁️ Cloud Deployment (Suggested)

### AWS
- **Backend**: ECS Fargate + ALB or AWS Lambda + API Gateway
- **Frontend**: S3 + CloudFront CDN
- **Database** (if added): RDS PostgreSQL

### GCP
- **Backend**: Cloud Run (serverless containers)
- **Frontend**: Firebase Hosting
- **Storage**: Cloud Storage

### Quick production checklist
- [ ] Set `CORS_ORIGINS` env var to your production domain
- [ ] Add authentication (OAuth2 / JWT)
- [ ] Replace in-memory data with PostgreSQL + SQLAlchemy
- [ ] Add Redis caching for ML results
- [ ] Configure `uvicorn` with multiple workers: `--workers 4`
