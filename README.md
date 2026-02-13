# Telecom Fraud ML - Satark Intelligence Grid

A real-time fraud detection system for telecom networks using machine learning and behavioral analysis.

## Project Structure

```
telecom-fraud-ml/
├── backend-simulation/    # FastAPI backend with WebSocket support
│   └── package.json       # ❌ NO - This is Python, not Node.js!
├── web-platform/          # Next.js frontend dashboard
│   └── package.json       # ✅ YES - npm commands go here!
└── package.json           # Root package.json (helper scripts only)
```

## ⚠️ Common Error: npm install in wrong directory

**ERROR:**
```
npm error enoent Could not read package.json: Error: ENOENT: no such file or directory
```

**CAUSE:** Running `npm install` or `npm i` from the root directory instead of `web-platform/`

**SOLUTION:**
```powershell
# ❌ WRONG - Don't run npm from root
cd D:\DEV\Projects\telecom-fraud-ml
npm install  # This will fail!

# ✅ CORRECT - Run npm from web-platform directory
cd D:\DEV\Projects\telecom-fraud-ml\web-platform
npm install  # This will work!

# OR use the helper script
cd D:\DEV\Projects\telecom-fraud-ml
.\install.ps1  # Installs both backend and frontend dependencies
```

## Quick Start

### Option 1: Use PowerShell Scripts (Recommended for Windows)

1. **Install all dependencies:**
   ```powershell
   .\install.ps1
   ```

2. **Start both servers:**
   ```powershell
   .\start-all.ps1
   ```
   This will open two separate windows - one for backend and one for frontend.

3. **Start servers individually:**
   ```powershell
   # Backend only
   .\start-backend.ps1
   
   # Frontend only
   .\start-frontend.ps1
   ```

4. **Stop all servers:**
   ```powershell
   .\stop-all.ps1
   ```

### Option 2: Manual Start

#### Backend (FastAPI)

```powershell
cd backend-simulation
pip install -r requirements.txt
python main.py
```

The backend will start on `http://127.0.0.1:8000`

#### Frontend (Next.js)

```powershell
# ⚠️ IMPORTANT: Must be in web-platform directory!
cd web-platform
npm install
npm run dev
```

The frontend will start on `http://localhost:3000`

## Troubleshooting

### npm Error: ENOENT - package.json not found

**Problem:** Running npm commands from the wrong directory.

**Solution:**
- Always run `npm install`, `npm run dev`, etc. from the `web-platform/` directory
- Or use the provided PowerShell scripts which handle this automatically
- The root `package.json` is only for helper scripts, not for npm install

### Port Already in Use

If you get a port conflict error:
- **Port 8000 (Backend)**: The `start-backend.ps1` script will automatically kill existing processes
- **Port 3000 (Frontend)**: The `start-frontend.ps1` script will automatically kill existing processes
- Or use `.\stop-all.ps1` to stop all servers

### Python/Node Not Found

Make sure Python and Node.js are installed and added to your PATH:
```powershell
python --version  # Should show Python 3.x
node --version    # Should show v18.x or higher
```

## API Endpoints

- `GET /` - Health check
- `GET /api/campaigns` - Get active fraud campaigns
- `GET /api/stats` - Get global statistics
- `POST /api/check-number` - Check a phone number for fraud risk
- `WS /ws/threat-stream` - WebSocket stream for real-time threats

## ML Training

To train the fraud detection model:

```powershell
# Generate synthetic call data
cd src
python generate_data.py

# Extract features
python feature_engineering.py

# Train model
python train_model.py
```

## License

MIT
