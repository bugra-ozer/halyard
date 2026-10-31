from fastapi import FastAPI
from app.constant import constant as con
from app.core import logger
import logging

app=FastAPI()
log_handler=logger.LogHandler()
logger=logging.getLogger(__name__)

@app.get(con.HEALTH_ROUTE)
def health():
    return {con.KEY_STATUS: con.KEY_OK}

