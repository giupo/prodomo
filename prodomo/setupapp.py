import os
import json
import logging.config
import logging
from logging import getLogger
import tornado.autoreload
import glob

def buildStaticContent():
    os.system("webpack")

def setupTornadoHook():
    root = "/Users/giupo/projects/prodomo/src"
    tornado.autoreload.watch("/Users/giupo/projects/prodomo/src")
    tornado.autoreload.add_reload_hook(buildStaticContent)

    for f in glob.glob(root+"/*.js"):
        tornado.autoreload.watch(f)
    for f in glob.glob(root+"/**/*.js"):
        tornado.autoreload.watch(f)
    for f in glob.glob(root+"/**/*.css"):
        tornado.autoreload.watch(f)

def setupLogging(level=logging.DEBUG):
  "Configura il logging per l'applicazione"
  logging.basicConfig(level=level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
