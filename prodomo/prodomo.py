# -*- coding: utf-8 -*-

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from pkg_resources import Requirement, resource_filename
import logging

log = logging.getLogger(__name__)
content_path = resource_filename(Requirement.parse("prodomo"), "public")
settings = {
    # 'static_path': content_path,
    'autoreload': True,
    'debug': True
}

class ProdomoAPIHandler(tornado.web.RequestHandler):
    pass

class MainHandler(tornado.web.RequestHandler):
    def get(self, what):

        if what is None or len(what) == 0:
            what = 'index.html'

        log.debug("serving %s" % what)

        try:
            with open(os.path.join(content_path, what)) as f:
                self.write(f.read())
        except IOError as e:
            self.write("404: Not Found")

application = tornado.web.Application([
    (r'/api/v1/*', ProdomoAPIHandler),
    (r'/(.*)', MainHandler),
], **settings)


def startServer(certfile, keyfile, address=None, port=8443):
    http_server = tornado.httpserver.HTTPServer(application, ssl_options={
        "certfile": certfile,
        "keyfile": keyfile,
    })
    http_server.listen(port, address=address)
    log.info("Content path: %s" % content_path)
    log.info("starting server...")
    tornado.ioloop.IOLoop.instance().start()
