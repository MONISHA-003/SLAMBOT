from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import random
import json
import psycopg2

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
conn = psycopg2.connect("dbname=slam_db user=postgres password=yourpassword host=localhost")
cur = conn.cursor()

# Fleet simulation
fleet = [
    {"id": 1, "lat": 40.7128, "lng": -74.0060, "status": "Idle", "path": []},
    {"id": 2, "lat": 40.7138, "lng": -74.0050, "status": "Moving", "path": []},
]

clients = []

async def send_fleet_data():
    while True:
        for robot in fleet:
            robot["lat"] += (random.random() - 0.5) * 0.001
            robot["lng"] += (random.random() - 0.5) * 0.001
            robot["path"].append([robot["lat"], robot["lng"]])

        data = json.dumps({"robots": fleet})
        for client in clients:
            await client.send_text(data)

        await asyncio.sleep(3)

@app.websocket("/fleet")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        clients.remove(websocket)

@app.post("/assign")
async def assign_task(data: dict):
    robot_id = data.get("robotId")
    task = data.get("task", "Inspect Field")
    
    for robot in fleet:
        if robot["id"] == robot_id:
            robot["status"] = f"Assigned: {task}"
            return {"message": "Task assigned", "robot": robot}
    
    return {"error": "Robot not found"}, 404

@app.get("/soil-data")
async def get_soil_data():
    cur.execute("SELECT timestamp, level FROM soil_nutrients ORDER BY timestamp DESC LIMIT 10;")
    soil_data = [{"timestamp": row[0], "level": row[1]} for row in cur.fetchall()]
    return soil_data

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(send_fleet_data())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
