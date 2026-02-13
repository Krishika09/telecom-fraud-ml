# Integration Analysis - Current State

## 📊 Existing Project Structure

```
telecom-fraud-ml/
├── backend-simulation/          # FastAPI Backend
│   ├── main.py                  # API routes + WebSocket
│   ├── simulator.py             # FraudSimulator class (MOCK DATA)
│   └── websocket_manager.py     # ConnectionManager
├── src/                         # ML Pipeline (Offline)
│   ├── generate_data.py         # Creates synthetic CDR data
│   ├── feature_engineering.py   # Extracts features from CDR
│   └── train_model.py           # Trains Isolation Forest
└── web-platform/                # Next.js Frontend
    └── src/
        ├── app/dashboard/       # Dashboard pages
        └── components/          # React components
```

## 🔧 Frameworks Being Used

### Backend
- **Framework**: FastAPI 0.129.0
- **Server**: Uvicorn
- **WebSocket**: Native FastAPI WebSocket
- **Data Processing**: Pandas, NumPy
- **ML**: scikit-learn (Isolation Forest)
- **Storage**: **NONE** (in-memory only, no database)

### Frontend
- **Framework**: Next.js 14.2.16 (App Router)
- **Language**: TypeScript
- **State**: React Context (SocketContext)
- **Charts**: Recharts
- **Styling**: Tailwind CSS

### ML Stack
- **Algorithm**: Isolation Forest
- **Features**: 5 behavioral features per caller
- **Training**: Offline (not integrated)
- **Model Format**: Not saved (needs joblib)

## 🔌 Current Working Endpoints

### REST API
1. `GET /` - Health check ✅
2. `GET /api/campaigns` - Returns mock campaigns ✅
3. `GET /api/stats` - Returns mock stats ✅
4. `POST /api/check-number` - **MOCK LOGIC** (deterministic based on last digit) ⚠️

### WebSocket
1. `WS /ws/threat-stream` - Streams mock events every 1 second ✅

### Frontend Calls
1. `GET /api/campaigns` - Used by ActiveCampaigns component ✅
2. `POST /api/check-number` - Used by LookupPage ✅
3. `WS /ws/threat-stream` - Used by SocketContext, LiveThreatCounter ✅

## ❌ Missing/Unconnected Components

1. **ML Model**: Trained but NOT loaded in backend
2. **Feature Engineering**: Only in offline script, not real-time
3. **CDR Ingestion**: No endpoint to receive real CDR data
4. **Cluster Detection**: Mock campaigns, no real clustering
5. **Alert System**: No API endpoint, frontend uses hardcoded data
6. **Data Storage**: No persistence, all in-memory
7. **Real-time ML Inference**: Not implemented

## 🔄 Current Data Flow (MOCK)

```
FraudSimulator.generate_batch()
    ↓ (random data)
WebSocket Broadcast
    ↓
Frontend Components
```

**Missing**: CDR → Features → ML → Clusters → Alerts

## 🎯 Integration Plan

### Phase 1: Data Storage Layer
- Create in-memory data structures (dicts/lists) to store:
  - CDR records
  - Caller features (rolling window)
  - ML predictions
  - Clusters
  - Alerts

### Phase 2: ML Integration
- Save trained model (joblib)
- Load model in backend startup
- Create feature extraction service
- Implement real-time inference

### Phase 3: CDR Processing Pipeline
- Create CDR ingestion endpoint
- Real-time feature extraction
- ML scoring
- Update caller profiles

### Phase 4: Cluster Detection
- Implement clustering logic (DBSCAN or similar)
- Track clusters over time
- Update campaigns endpoint

### Phase 5: Alert Generation
- Create alert generation logic
- Connect to alerts API endpoint
- Update frontend to fetch from API

### Phase 6: Endpoint Updates
- Update check-number: Use ML + stored data
- Update campaigns: Use real clusters
- Update stats: Aggregate from stored data
- Update WebSocket: Use ML predictions

## 📝 Implementation Strategy

**Key Principle**: Extend existing code, don't replace

1. **Extend FraudSimulator** class with:
   - Data storage (dicts for CDR, features, predictions)
   - ML model reference
   - Feature extraction methods
   - Cluster detection methods
   - Alert generation methods

2. **Create new services** (separate files):
   - `ml_service.py`: Model loading and inference
   - `feature_extractor.py`: Real-time feature extraction
   - `cluster_detector.py`: Cluster detection logic

3. **Add new endpoints**:
   - `POST /api/cdr`: CDR ingestion
   - `GET /api/alerts`: Alert retrieval

4. **Update existing endpoints**:
   - Use real data instead of mocks
   - Maintain same response structure
