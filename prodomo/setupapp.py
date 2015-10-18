import os
import json
import logging.config
import logging
from logging import getLogger
import tornado.autoreload

def buildStaticContent():
    os.system("npm run build")

def setupTornadoHook():
    tornado.autoreload.add_reload_hook(buildStaticContent)

def setupLogging(level=logging.DEBUG):
  "Configura il logging per l'applicazione"
  logging.basicConfig(level=level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
