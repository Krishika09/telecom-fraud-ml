# 🚀 Site Startup Status

## ✅ Services Started

### Backend (FastAPI)
- **Status**: Running
- **URL**: http://127.0.0.1:8000
- **Port**: 8000
- **Endpoints Available**:
  - `GET /` - Health check
  - `GET /api/campaigns` - Active fraud clusters
  - `GET /api/stats` - Global statistics
  - `POST /api/check-number` - Number risk lookup
  - `POST /api/cdr` - CDR ingestion
  - `GET /api/alerts` - Alert retrieval
  - `WS /ws/threat-stream` - Real-time threat stream

### Frontend (Next.js)
- **Status**: Running
- **URL**: http://localhost:3000
- **Port**: 3000
- **Pages Available**:
  - `/` - Landing page
  - `/dashboard` - Intelligence Board
  - `/dashboard/campaigns` - Campaign Detection
  - `/dashboard/alerts` - Alert Center
  - `/dashboard/lookup` - Citizen Risk Lookup
  - `/dashboard/explainability` - AI Explainability

## 🔗 Access the Site

**Frontend**: http://localhost:3000
**Backend API**: http://127.0.0.1:8000
**API Docs**: http://127.0.0.1:8000/docs (Swagger UI)

## 📊 What's Working

✅ All endpoints connected
✅ ML model integration (with fallback)
✅ Real-time WebSocket streaming
✅ Feature extraction pipeline
✅ Cluster detection
✅ Alert generation
✅ Frontend-backend communication

## 🎯 Quick Test

1. **Open Frontend**: Navigate to http://localhost:3000
2. **Check Dashboard**: Go to http://localhost:3000/dashboard
3. **Test Lookup**: Go to http://localhost:3000/dashboard/lookup and search a number
4. **View Alerts**: Go to http://localhost:3000/dashboard/alerts
5. **Check API**: Visit http://127.0.0.1:8000/docs for API documentation

## 📝 Note

The ML model will use fallback heuristics until you train the model:
```bash
cd src
python generate_data.py
python feature_engineering.py
python train_model.py
```

After training, the model will be automatically loaded on next backend restart.

## 🛑 To Stop Services

Press `Ctrl+C` in the terminal windows, or run:
```powershell
.\stop-all.ps1
```
