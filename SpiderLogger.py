import logging
import datetime
import time
from csimulate import getLineFileFunc
class SpiderLogger:
    def debug(self, message):
        self.objLogger.debug(message + getLineFileFunc())
    def info(self,message):
        self.objLogger.info(message + getLineFileFunc())
    def warning(self, message):
        self.objLogger.warning(message + getLineFileFunc())
    def error(self, message):
        self.objLogger.critical(message + getLineFileFunc())
    def __init__(self, strLogfile):
        self.objLogger = logging.getLogger(None)
        self.objLogger.setLevel(logging.DEBUG)
        self.objHterm = logging.StreamHandler()
        self.objHterm.setLevel(logging.ERROR)
        self.objFile = logging.FileHandler(strLogfile)
        self.objFile.setLevel(logging.INFO)
        self.objFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.objHterm.setFormatter(self.objFormatter)
        self.objFile.setFormatter(self.objFormatter)
        self.objLogger.addHandler(self.objHterm)
        self.objLogger.addHandler(self.objFile)

strLogfile = time.strftime('%Y-%m-%d %H:%M:%S') + '.log'
strLogfile = strLogfile.replace(':','-').replace(' ', '-')
logger = SpiderLogger(strLogfile = strLogfile)

