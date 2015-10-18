# -*- coding:utf-8 -*-
import argparse

from prodomo import startServer, startDevServer
from setupapp import setupLogging, setupTornadoHook
setupLogging()
setupTornadoHook()
import logging
log = logging.getLogger(__name__)

def dev_webapp():
    startDevServer()


def webapp():
    """Lancia il server stack per Prodomo"""
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('--certfile', dest='certfile', default='server.crt',
        help='specifica il file del certificato')

    parser.add_argument('--keyfile', dest='keyfile', default='server.key',
        help='specifica il file della chiave privata')

    parser.add_argument('--address', dest='address', default='',
        help="specifica l'indirizzo del server")

    parser.add_argument('--port', dest='port', default=8443, type=int,
        help="specifica l'indirizzo del server")


    args = parser.parse_args()

    log.debug("Certfile: %s" % args.certfile)
    log.debug("Keyfile: %s" % args.keyfile)
    log.debug("Listen address: %s" % args.address)
    log.debug("Listen port: %s" % args.port)


    startServer(args.certfile, args.keyfile,
                address=args.address, port=args.port)
