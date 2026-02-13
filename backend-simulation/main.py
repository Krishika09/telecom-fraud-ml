from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio
import json
from simulator import FraudSimulator
from websocket_manager import ConnectionManager

app = FastAPI(title="Satark Fraud Simulation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()
simulator = FraudSimulator()

@app.get("/")
async def root():
    return {"message": "Satark Intelligence Grid Online"}

@app.websocket("/ws/threat-stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Simulate fetching a batch of events
            events = simulator.generate_batch(size=5)
            await manager.broadcast(json.dumps(events))
            await asyncio.sleep(1) # Send every second
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(websocket)

@app.get("/api/campaigns")
def get_campaigns():
    return simulator.get_active_campaigns()

@app.get("/api/stats")
def get_stats():
    return simulator.get_global_stats()

class NumberLookupRequest(BaseModel):
    number: str

@app.post("/api/check-number")
def check_number(request: NumberLookupRequest):
    """Lookup phone number risk using ML predictions"""
    return simulator.lookup_number(request.number)

class CDRRequest(BaseModel):
    caller_id: Optional[str] = None
    source: Optional[str] = None
    destination: str
    duration: float
    timestamp: float
    origin_region: str
    target_region: str

@app.post("/api/cdr")
def ingest_cdr(cdr: CDRRequest):
    """
    Ingest CDR (Call Detail Record) for processing
    Processes through: Feature Extraction → ML → Cluster Detection → Alert Generation
    """
    cdr_data = {
        "caller_id": cdr.caller_id or cdr.source,
        "destination": cdr.destination,
        "duration": cdr.duration,
        "timestamp": cdr.timestamp,
        "origin_region": cdr.origin_region,
        "target_region": cdr.target_region
    }
    
    result = simulator.process_cdr(cdr_data)
    return {
        "success": True,
        "caller_id": result["caller_id"],
        "risk_score": result["risk_score"],
        "is_fraud": result["is_fraud"],
        "cluster_id": result.get("cluster_id"),
        "fraud_type": result.get("fraud_type"),
        "alerts_generated": len(result.get("alerts", []))
    }

@app.get("/api/alerts")
def get_alerts(severity: Optional[str] = None, status: Optional[str] = None, limit: int = 50):
    """Get alerts with optional filtering"""
    alerts = simulator.alert_generator.get_alerts(severity, status, limit)
    return alerts

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)