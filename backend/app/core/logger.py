from logging import handlers
from app.constant import constant as con
import logging, pathlib as pl

class LogHandler():
    """Class for configuring logs shape and internal"""

    def __init__(self, directory='core', filename='log.log'):
        self.filename=filename
        self.path=pl.Path(__file__).parent.parent / directory / filename
        pl.Path.mkdir(self.path.parent, parents=True, exist_ok=True)
        logging.basicConfig(level=logging.INFO, format=con.LOG_FORMAT)
        self.logger=logging.getLogger()
        self.handler=logging.handlers.RotatingFileHandler(self.path, maxBytes=1000000, backupCount=5)
        self.handler.setFormatter(logging.Formatter(con.LOG_FORMAT))
        self.logger.addHandler(self.handler)