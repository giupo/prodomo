# -*- coding: utf-8 -*-

import os
import glob
import tornado.httpserver
import tornado.ioloop
import tornado.web
from pkg_resources import Requirement, resource_filename
import logging
import mimetypes

log = logging.getLogger(__name__)
content_path = resource_filename(Requirement.parse("prodomo"), "public")
settings = {
    # 'static_path': content_path,
    'autoreload': True,
    'debug': True
}

class ProdomoAPIHandler(tornado.web.RequestHandler):
    pass

static_content = glob.glob(content_path + '/*')



class MainHandler(tornado.web.RequestHandler):
    def get(self, what):
        log.info("here your static content: " + str(static_content))
        if what is None or len(what) == 0:
            what = 'index.html'

        if not any(what in s for s in static_content):
            raise tornado.web.HTTPError(404)

        content_type = mimetypes.guess_type(what)
        log.debug("Content-Type: %s" % str(content_type))
        self.set_header("Content-Type", content_type[0])
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


def startDevServer(address=None, port=3000):
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port, address=address)
    log.info("Content path: %s" % content_path)
    log.info("starting server...")
    tornado.ioloop.IOLoop.instance().start()


def startServer(certfile, keyfile, address=None, port=8443):
    http_server = tornado.httpserver.HTTPServer(application, ssl_options={
        "certfile": certfile,
        "keyfile": keyfile,
    })
    http_server.listen(port, address=address)
    log.info("Content path: %s" % content_path)
    log.info("starting server...")
    tornado.ioloop.IOLoop.instance().start()
