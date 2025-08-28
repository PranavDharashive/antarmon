from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Dict, Any, Optional
import database as db
import sqlite3
import auth
import secrets

app = FastAPI()

# Initialize the database on startup
db.initialize_database()

class Metrics(BaseModel):
    metrics: Dict[str, Any]

class User(BaseModel):
    email: str
    password: str

class Agent(BaseModel):
    name: str

class Alert(BaseModel):
    metric_name: str
    threshold: float

def get_db_connection():
    conn = db.create_connection()
    try:
        yield conn
    finally:
        conn.close()

async def verify_api_key(x_api_key: str = Header(...), conn: sqlite3.Connection = Depends(get_db_connection)):
    agent = db.get_agent_by_api_key(conn, x_api_key)
    if not agent:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return agent

@app.post("/register")
def register_user(user: User, conn: sqlite3.Connection = Depends(get_db_connection)):
    db_user = db.get_user_by_email(conn, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    db.create_user(conn, (user.email, hashed_password))
    return {"message": "User created successfully"}

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), conn: sqlite3.Connection = Depends(get_db_connection)):
    user = db.get_user_by_email(conn, form_data.username)
    if not user or not auth.verify_password(form_data.password, user[2]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(
        data={"sub": user[1]}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"message": "AntarMon Server is running"}

@app.post("/metrics")
def receive_metrics(metrics: Metrics, agent: Agent = Depends(verify_api_key), conn: sqlite3.Connection = Depends(get_db_connection)):
    metric_data = metrics.metrics
    db.insert_metric(conn, (metric_data['hostname'], metric_data['cpu_percent'], metric_data['memory_percent'], metric_data['disk_percent']))
    
    # Check for alerts
    alerts = db.get_all_alerts(conn)
    for alert in alerts:
        metric_name = alert[1]
        threshold = alert[2]
        if metric_name in metric_data and metric_data[metric_name] >= threshold:
            print(f"ALERT: {metric_data['hostname']} - {metric_name} ({metric_data[metric_name]}%) has exceeded the threshold of {threshold}%")

    return {"status": "success", "data_received": metrics.dict()}

@app.get("/metrics/all")
def get_all_metrics(conn: sqlite3.Connection = Depends(get_db_connection), current_user: str = Depends(auth.get_current_user)):
    rows = db.get_all_metrics(conn)
    return {"metrics": rows}

@app.post("/agents")
def register_agent(agent: Agent, conn: sqlite3.Connection = Depends(get_db_connection), current_user: str = Depends(auth.get_current_user)):
    api_key = secrets.token_hex(32)
    user = db.get_user_by_email(conn, current_user)
    db.create_agent(conn, (agent.name, api_key, user[0]))
    return {"agent_name": agent.name, "api_key": api_key}

@app.get("/agents")
def get_agents(conn: sqlite3.Connection = Depends(get_db_connection), current_user: str = Depends(auth.get_current_user)):
    user = db.get_user_by_email(conn, current_user)
    agents = db.get_agents_by_user_id(conn, user[0])
    return {"agents": agents}

@app.post("/alerts")
def create_alert(alert: Alert, conn: sqlite3.Connection = Depends(get_db_connection), current_user: str = Depends(auth.get_current_user)):
    user = db.get_user_by_email(conn, current_user)
    db.create_alert(conn, (alert.metric_name, alert.threshold, user[0]))
    return {"message": "Alert created successfully"}

@app.get("/alerts")
def get_alerts(conn: sqlite3.Connection = Depends(get_db_connection), current_user: str = Depends(auth.get_current_user)):
    user = db.get_user_by_email(conn, current_user)
    alerts = db.get_alerts_by_user_id(conn, user[0])
    return {"alerts": alerts}

@app.delete("/alerts/{alert_id}")
def delete_alert(alert_id: int, conn: sqlite3.Connection = Depends(get_db_connection), current_user: str = Depends(auth.get_current_user)):
    # In a real app, you should verify that the user owns the alert before deleting it
    db.delete_alert(conn, alert_id)
    return {"message": "Alert deleted successfully"}
