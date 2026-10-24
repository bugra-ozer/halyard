from fastapi import FastAPI
from app.constant import constant as con

app=FastAPI()

@app.get(con.HEALTH_ROUTE)
def health():
    return {con.KEY_STATUS: con.KEY_OK}

