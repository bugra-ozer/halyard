from fastapi import FastAPI
from app.constant import constant as con
from app.core import logger
from app.api.flags import router as flags_router
import logging

app=FastAPI()
log_handler=logger.LogHandler()
logger=logging.getLogger(__name__)

@app.get(con.HEALTH_ROUTE)
def health():
    return {con.KEY_STATUS: con.KEY_OK}

app.include_router(flags_router)
