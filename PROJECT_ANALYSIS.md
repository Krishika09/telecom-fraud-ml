# Complete Project Analysis: Telecom Fraud ML - Satark Intelligence Grid

## 📋 Executive Summary

This is a **real-time fraud detection system** for telecom networks that combines machine learning, real-time WebSocket streaming, and an interactive dashboard. The system simulates a national-level fraud detection infrastructure capable of processing millions of calls and identifying fraudulent patterns in real-time.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Dashboard  │  │   Campaigns  │  │   Lookup     │    │
│  │   Page       │  │   Analysis   │  │   Service    │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │                  │                  │            │
│         └──────────────────┼──────────────────┘            │
│                            │                                │
│                    ┌───────▼────────┐                       │
│                    │ SocketContext  │                       │
│                    │  (WebSocket)   │                       │
│                    └───────┬────────┘                       │
└────────────────────────────┼────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   WebSocket     │
                    │   HTTP REST     │
                    └────────┬────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│              BACKEND (FastAPI)                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  FastAPI Server (main.py)                            │ │
│  │  - REST Endpoints                                    │ │
│  │  - WebSocket Handler                                 │ │
│  │  - CORS Middleware                                   │ │
│  └──────────────┬───────────────────────────────────────┘ │
│                 │                                          │
│  ┌──────────────▼──────────┐  ┌──────────────────────┐  │
│  │  FraudSimulator         │  │  ConnectionManager    │  │
│  │  - generate_batch()    │  │  - WebSocket Pool     │  │
│  │  - get_campaigns()     │  │  - Broadcast          │  │
│  │  - get_stats()         │  │                       │  │
│  └────────────────────────┘  └──────────────────────┘  │
└───────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│              ML PIPELINE (Offline Training)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │ generate_data│  │   feature_   │  │  train_model  │    │
│  │   .py        │→ │ engineering  │→ │     .py       │    │
│  │              │  │     .py      │  │               │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
│         │                  │                  │            │
│    Raw Call Data    Feature Extraction   Model Training   │
│    (CSV)            (Aggregated)         (IsolationForest) │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 FRONTEND ANALYSIS

### Technology Stack
- **Framework**: Next.js 14.2.16 (App Router)
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 3.4.1
- **UI Components**: Custom components (shadcn/ui style)
- **Charts**: Recharts 2.12.0
- **Animations**: Framer Motion 11.0.0
- **Icons**: Lucide React 0.344.0
- **WebSocket**: Native WebSocket API

### Application Structure

#### 1. **Landing Page** (`/`)
- **File**: `src/app/page.tsx`
- **Components**:
  - `Navbar`: Navigation bar
  - `HeroSection`: Marketing/landing content
  - `LiveThreatCounter`: Real-time call counter with WebSocket
- **Purpose**: Public-facing landing page with live statistics

#### 2. **Dashboard** (`/dashboard`)
- **File**: `src/app/dashboard/page.tsx`
- **Layout**: `src/app/dashboard/layout.tsx` (includes Sidebar + SocketProvider)
- **Key Features**:
  - **Threat Index**: National threat level indicator (0-10 scale)
  - **Suspicious Signals**: Count of flagged calls
  - **Victims Saved**: Estimated protected users
  - **Network Load**: System capacity indicator
  - **Call Ingestion Chart**: Real-time line chart of calls/second
  - **Active Campaigns**: List of detected fraud clusters
  - **Region Heatmap**: Geographic distribution visualization
  - **Emerging Anomalies**: Real-time alerts

#### 3. **Campaign Analysis** (`/dashboard/campaigns`)
- **File**: `src/app/dashboard/campaigns/page.tsx`
- **Features**:
  - **Network Graph**: Interactive visualization of fraud clusters
  - **Cluster List**: Sidebar with identified fraud patterns
  - **Metrics Overlay**: Node count, density, velocity
  - **Export/Control**: Pause stream, export reports

#### 4. **Number Lookup** (`/dashboard/lookup`)
- **File**: `src/app/dashboard/lookup/page.tsx`
- **Functionality**:
  - Phone number search interface
  - Risk assessment display
  - Status categories: SAFE, SUSPICIOUS, DANGEROUS
  - Detailed metrics: Risk score, category, reports, carrier, last active
  - Visual indicators with color-coded badges

#### 5. **Explainability** (`/dashboard/explainability`)
- **File**: `src/app/dashboard/explainability/page.tsx`
- **Features**:
  - **SHAP Values Visualization**: Feature importance bar chart
  - **Decision Logic**: Rule-based explanations for fraud detection
  - **Key Features**:
    - Call Duration < 3s (85% importance)
    - High Frequency Outbound (78%)
    - New Number Activation (65%)
    - International Destination (45%)
    - Non-Contact Ratio (40%)

#### 6. **Alerts** (`/dashboard/alerts`)
- **File**: `src/app/dashboard/alerts/page.tsx`
- **Features**: Alert management interface with severity levels

### State Management

#### WebSocket Context (`src/context/SocketContext.tsx`)
- **Purpose**: Centralized WebSocket connection management
- **Connection**: `ws://127.0.0.1:8000/ws/threat-stream`
- **State**:
  - `data`: Parsed WebSocket messages
  - `isConnected`: Connection status
- **Usage**: Provides real-time data to all dashboard components

### Component Architecture

#### Reusable Components
1. **UI Components** (`src/components/ui/`):
   - `button.tsx`: Styled button component
   - `card.tsx`: Card container with header/content
   - `badge.tsx`: Status badges

2. **Dashboard Components** (`src/components/dashboard/`):
   - `ThreatIndex.tsx`: Threat level indicator
   - `CallIngestionChart.tsx`: Real-time call volume chart
   - `ActiveCampaigns.tsx`: Campaign list with API integration
   - `RegionHeatmap.tsx`: Geographic visualization

3. **Campaign Components** (`src/components/campaign/`):
   - `NetworkGraph.tsx`: Fraud cluster network visualization

4. **Shared Components**:
   - `Navbar.tsx`: Navigation bar
   - `Sidebar.tsx`: Dashboard sidebar navigation
   - `LiveThreatCounter.tsx`: Real-time counter with WebSocket
   - `HeroSection.tsx`: Landing page hero

### Data Flow (Frontend)

```
WebSocket Stream → SocketContext → Components
     ↓
{ events: [...], stats: {...} }
     ↓
┌─────────────────┬─────────────────┬─────────────────┐
│ LiveThreatCounter│ CallIngestionChart│ ThreatIndex     │
│ (uses stats)    │ (uses stats)     │ (uses isConnected)│
└─────────────────┴─────────────────┴─────────────────┘

HTTP REST API → Components
     ↓
┌─────────────────┬─────────────────┐
│ ActiveCampaigns │ LookupPage      │
│ GET /api/campaigns│ POST /api/check-number│
└─────────────────┴─────────────────┘
```

---

## ⚙️ BACKEND ANALYSIS

### Technology Stack
- **Framework**: FastAPI 0.129.0
- **Server**: Uvicorn 0.35.0
- **WebSocket**: Native FastAPI WebSocket support
- **Data Generation**: Faker 40.4.0 (Indian locale)
- **Data Processing**: Pandas, NumPy

### API Structure

#### 1. **Main Application** (`backend-simulation/main.py`)

**REST Endpoints**:
- `GET /`: Health check
  - Returns: `{"message": "Satark Intelligence Grid Online"}`
  
- `GET /api/campaigns`: Get active fraud campaigns
  - Returns: Array of campaign objects
  - Updates: Randomly increments affected_users for realism
  
- `GET /api/stats`: Get global statistics
  - Returns: `{total_calls, blocked_threats, active_campaigns_count}`
  
- `POST /api/check-number`: Check phone number risk
  - Input: `{"number": "string"}`
  - Logic: Deterministic based on last digit
    - Last digit > 7: DANGEROUS (95 risk score)
    - Last digit > 4: SUSPICIOUS (65 risk score)
    - Otherwise: SAFE (5 risk score)
  - Returns: Status, risk_score, category, reports, carrier, last_active

**WebSocket Endpoint**:
- `WS /ws/threat-stream`: Real-time threat data stream
  - Broadcasts every 1 second
  - Format: `{events: [...], stats: {...}}`
  - Events include: id, timestamp, source, destination, duration, risk_score, type, location

#### 2. **Fraud Simulator** (`backend-simulation/simulator.py`)

**Class: FraudSimulator**

**Initialization**:
- Creates 5 persistent fraud campaigns
- Initializes global stats (1,420,310 total calls, 1,240 blocked threats)
- Campaign types: Wangiri, IRS Impersonation, Lottery Fraud, KYC Phishing

**Methods**:
- `generate_batch(size=5)`: Generates batch of call events
  - 15% fraud probability
  - Fraud events: risk_score 80-99
  - Legitimate events: risk_score 0-10
  - Updates global stats
  
- `get_active_campaigns()`: Returns active campaigns with dynamic updates
  
- `get_global_stats()`: Returns current statistics

**Data Generation**:
- Uses Faker with Indian locale (`en_IN`)
- Generates Indian phone numbers
- Random cities, timestamps, durations

#### 3. **WebSocket Manager** (`backend-simulation/websocket_manager.py`)

**Class: ConnectionManager**

**Purpose**: Manages multiple WebSocket connections

**Methods**:
- `connect(websocket)`: Accepts and stores connection
- `disconnect(websocket)`: Removes connection
- `broadcast(message)`: Sends message to all connected clients

**Architecture**: Simple list-based connection pool

### Backend Data Flow

```
FraudSimulator.generate_batch()
         ↓
    {events, stats}
         ↓
ConnectionManager.broadcast()
         ↓
    All WebSocket Clients
         ↓
    Frontend Components
```

---

## 🤖 ML PIPELINE ANALYSIS

### 1. **Data Generation** (`src/generate_data.py`)

**Purpose**: Create synthetic telecom call dataset

**Configuration**:
- Total Callers: 800
- Fraud Ratio: 5% (40 fraud callers, 760 normal)
- Simulation Period: 30 days
- Regions: Delhi, Mumbai, Kolkata, Chennai, Bangalore, Hyderabad

**Normal Caller Behavior**:
- Calls per day: 1-10 (random)
- Call duration: Normal distribution (μ=180s, σ=40s, min=20s)
- Time pattern: 95% day calls (8-21h), 5% night calls (22-23h)
- Regional pattern: 70% same region, 30% different region

**Fraud Caller Behavior**:
- Calls per day: 50-150 (much higher volume)
- Call duration: Exponential distribution (scale=20s) - short calls
- Time pattern: 50% night calls (22-5h), 50% day calls
- Regional pattern: Random (no preference)

**Output**: `data/call_data.csv`
- Columns: caller_id, receiver_id, call_duration, timestamp, origin_region, target_region, true_label

### 2. **Feature Engineering** (`src/feature_engineering.py`)

**Purpose**: Extract behavioral features per caller

**Features Extracted**:
1. **avg_call_duration**: Mean call duration
2. **total_calls**: Total number of calls made
3. **night_call_ratio**: Proportion of calls during night (22:00-05:00)
4. **unique_origin_regions**: Number of distinct origin regions
5. **unique_target_regions**: Number of distinct target regions
6. **true_label**: Ground truth (preserved for evaluation)

**Aggregation**: Grouped by `caller_id` with various aggregations

**Output**: `data/caller_features.csv`
- One row per caller
- Ready for ML model training

### 3. **Model Training** (`src/train_model.py`)

**Algorithm**: Isolation Forest (Unsupervised Anomaly Detection)

**Configuration**:
- `n_estimators`: 200 trees
- `contamination`: 0.05 (expects 5% anomalies)
- `random_state`: 42 (reproducibility)

**Training Process**:
1. Load feature data
2. Separate features (X) from labels
3. Train Isolation Forest
4. Predict anomalies (-1 = anomaly, 1 = normal)
5. Convert to binary (0 = normal, 1 = fraud)
6. Generate risk scores using decision function

**Risk Score Generation**:
- Uses `decision_function()` to get anomaly scores
- Negative scores = more anomalous
- Normalized to 0-100 scale using MinMaxScaler
- Higher score = higher fraud risk

**Evaluation Metrics**:
- True Positives (TP): Correctly identified fraud
- False Positives (FP): Legitimate calls flagged as fraud
- False Negatives (FN): Fraud calls missed
- True Negatives (TN): Correctly identified legitimate calls

**Metrics Calculated**:
- Detection Rate (Recall): TP / (TP + FN) × 100
- Precision: TP / (TP + FP) × 100
- False Positive Rate: FP / (FP + TN) × 100

### ML Pipeline Data Flow

```
generate_data.py
    ↓
call_data.csv (Raw call records)
    ↓
feature_engineering.py
    ↓
caller_features.csv (Aggregated features)
    ↓
train_model.py
    ↓
Trained Isolation Forest Model
    ↓
Risk Scores & Predictions
```

**Note**: The trained model is NOT currently integrated into the backend. The backend uses simulated data. Integration would require:
1. Loading the trained model (joblib)
2. Real-time feature extraction from incoming calls
3. Model inference for risk scoring
4. Updating the simulator to use model predictions

---

## 🔄 INTEGRATION ANALYSIS

### Current Integration Status

#### ✅ **Fully Integrated**:
1. **Frontend ↔ Backend (WebSocket)**
   - Real-time threat streaming
   - Live statistics updates
   - Connection status monitoring

2. **Frontend ↔ Backend (REST API)**
   - Campaign fetching
   - Number lookup
   - Statistics retrieval

#### ⚠️ **Partially Integrated**:
1. **ML Model ↔ Backend**
   - Model is trained but NOT loaded in backend
   - Backend uses deterministic simulation instead of ML predictions
   - Risk scores are randomly generated, not from model

#### ❌ **Not Integrated**:
1. **Real Call Data → Backend**
   - System uses simulated data only
   - No actual telecom network integration

2. **ML Model → Real-time Inference**
   - Model predictions not used in live system
   - Would require feature extraction pipeline in backend

### Integration Points

```
┌─────────────────────────────────────────────────────────┐
│                    INTEGRATION MAP                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ML Model (Offline)                                      │
│       ↓                                                  │
│  [NOT CONNECTED]                                         │
│       ↓                                                  │
│  Backend Simulator (Uses Random Logic)                  │
│       ↓                                                  │
│  WebSocket Stream / REST API                             │
│       ↓                                                  │
│  Frontend Dashboard (Fully Connected)                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### How to Integrate ML Model

**Step 1**: Save trained model
```python
# In train_model.py, add:
joblib.dump(model, "models/fraud_detector.pkl")
joblib.dump(scaler, "models/scaler.pkl")
```

**Step 2**: Load in backend
```python
# In main.py or new ml_service.py
import joblib
model = joblib.load("models/fraud_detector.pkl")
scaler = joblib.load("models/scaler.pkl")
```

**Step 3**: Real-time feature extraction
```python
# Extract features from incoming call
features = extract_features(call_data)
features_scaled = scaler.transform([features])
risk_score = model.decision_function(features_scaled)[0]
```

**Step 4**: Update simulator
```python
# Use model prediction instead of random
is_fraud = model.predict(features_scaled)[0] == -1
```

---

## 📊 DATA FLOW DIAGRAM

### Real-time Processing Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    REAL-TIME FLOW                             │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  1. FraudSimulator.generate_batch()                          │
│     ↓                                                         │
│  2. Creates 5 call events (15% fraud probability)            │
│     ↓                                                         │
│  3. Updates global_stats (total_calls, blocked_threats)      │
│     ↓                                                         │
│  4. Returns {events: [...], stats: {...}}                    │
│     ↓                                                         │
│  5. ConnectionManager.broadcast()                             │
│     ↓                                                         │
│  6. WebSocket sends to all connected clients                  │
│     ↓                                                         │
│  7. Frontend SocketContext receives data                     │
│     ↓                                                         │
│  8. Components update:                                        │
│     - LiveThreatCounter: Updates count & threats              │
│     - CallIngestionChart: Adds data point                     │
│     - ActiveCampaigns: (Separate HTTP call)                   │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### HTTP Request Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    HTTP REQUEST FLOW                          │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Frontend Component                                           │
│     ↓                                                         │
│  fetch("http://127.0.0.1:8000/api/...")                       │
│     ↓                                                         │
│  FastAPI Route Handler                                        │
│     ↓                                                         │
│  FraudSimulator method                                        │
│     ↓                                                         │
│  Returns JSON response                                        │
│     ↓                                                         │
│  Frontend updates UI                                          │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎯 KEY FEATURES

### 1. **Real-time Monitoring**
- WebSocket-based live updates
- Sub-second latency
- Multiple concurrent connections

### 2. **Fraud Detection Simulation**
- Multiple fraud types (Wangiri, IRS, Lottery, KYC)
- Realistic behavioral patterns
- Dynamic campaign tracking

### 3. **Interactive Dashboard**
- Real-time charts and visualizations
- Geographic heatmaps
- Network graph for cluster analysis

### 4. **Number Lookup Service**
- Instant risk assessment
- Detailed fraud reports
- Carrier information

### 5. **Explainability**
- SHAP values visualization
- Rule-based decision logic
- Feature importance ranking

### 6. **ML Pipeline**
- Synthetic data generation
- Feature engineering
- Isolation Forest model
- Performance metrics

---

## 🔧 TECHNOLOGY DECISIONS

### Why Isolation Forest?
- **Unsupervised**: Works without labeled data in production
- **Anomaly Detection**: Perfect for fraud (rare events)
- **Scalable**: Handles high-dimensional features
- **Interpretable**: Decision function provides risk scores

### Why FastAPI?
- **Async Support**: Handles WebSocket efficiently
- **Fast**: High performance for real-time systems
- **Type Safety**: Pydantic validation
- **Auto Docs**: OpenAPI/Swagger support

### Why Next.js?
- **Server Components**: Better performance
- **App Router**: Modern routing
- **TypeScript**: Type safety
- **SSR/SSG**: SEO and performance

### Why WebSocket?
- **Real-time**: Low latency updates
- **Bidirectional**: Server can push data
- **Efficient**: Lower overhead than polling

---

## 📈 PERFORMANCE CHARACTERISTICS

### Backend
- **Throughput**: ~5 events/second (configurable)
- **Latency**: <100ms for WebSocket broadcasts
- **Concurrent Connections**: Unlimited (limited by server resources)
- **Memory**: Low (simulated data, no database)

### Frontend
- **Initial Load**: ~140KB (First Load JS)
- **Updates**: Real-time via WebSocket
- **Rendering**: React 18 with optimizations
- **Charts**: Recharts with animation disabled for performance

### ML Model
- **Training Time**: ~seconds (800 callers, 5 features)
- **Inference Time**: <1ms per prediction
- **Memory**: ~few MB (200 trees)
- **Scalability**: Can handle millions of callers

---

## 🚀 DEPLOYMENT CONSIDERATIONS

### Current State
- **Development**: Local only
- **Backend**: Single instance, no load balancing
- **Frontend**: Development server
- **Database**: None (in-memory only)
- **ML Model**: Not deployed

### Production Requirements
1. **Backend**:
   - Redis for WebSocket connection management
   - PostgreSQL for campaign/statistics storage
   - Load balancer for multiple instances
   - Model serving (TensorFlow Serving or similar)

2. **Frontend**:
   - Next.js production build
   - CDN for static assets
   - Environment variables for API URLs

3. **ML Pipeline**:
   - Model versioning
   - A/B testing framework
   - Monitoring and retraining pipeline

---

## 🔍 AREAS FOR IMPROVEMENT

### 1. **ML Integration**
- [ ] Load trained model in backend
- [ ] Real-time feature extraction
- [ ] Model inference for risk scoring
- [ ] Model versioning and updates

### 2. **Data Persistence**
- [ ] Database for campaigns
- [ ] Historical statistics storage
- [ ] User lookup history
- [ ] Audit logging

### 3. **Real-time Features**
- [ ] Real call data ingestion
- [ ] Stream processing (Kafka/RabbitMQ)
- [ ] Distributed WebSocket management
- [ ] Rate limiting and throttling

### 4. **Security**
- [ ] Authentication/Authorization
- [ ] API rate limiting
- [ ] Input validation
- [ ] HTTPS/WSS encryption

### 5. **Monitoring**
- [ ] Application metrics (Prometheus)
- [ ] Logging (ELK stack)
- [ ] Alerting system
- [ ] Performance monitoring

### 6. **Testing**
- [ ] Unit tests (backend)
- [ ] Integration tests
- [ ] E2E tests (frontend)
- [ ] ML model validation

---

## 📝 CONCLUSION

This is a **well-architected prototype** of a telecom fraud detection system with:

✅ **Strengths**:
- Clean separation of concerns
- Modern tech stack
- Real-time capabilities
- Comprehensive ML pipeline
- Professional UI/UX

⚠️ **Gaps**:
- ML model not integrated into live system
- No data persistence
- Simulated data only
- Missing production features (auth, monitoring, etc.)

🎯 **Use Case**: Perfect for:
- Proof of concept demonstrations
- ML research and experimentation
- UI/UX development
- System architecture design
- Educational purposes

The foundation is solid for scaling to a production system with the improvements listed above.
