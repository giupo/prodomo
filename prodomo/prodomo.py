# -*- coding: utf-8 -*-

import os
import glob
import tornado.httpserver
import tornado.auth
import tornado.escape
import tornado.options
import tornado.ioloop
import tornado.web

import facebook

from pkg_resources import Requirement, resource_filename
import logging
import mimetypes

from switch import Session, Switch


log = logging.getLogger(__name__)
content_path = resource_filename(Requirement.parse("prodomo"), "public")
settings = {
    # 'static_path': content_path,
    'autoreload': True,
    'debug': True
}

def is_access_token_valid(access_token):
    try:
        graph = facebook.GraphAPI(acces_token)
        graph.get_object("/me")

    except:
        return False

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        "Provides the user from the access_token posted and checks for autorization"
        scheme, _, acces_token= self.request.headers.get('Authorization', '').partition(' ')
        log.debug("Access Token: %s" % token)

        try:
            graph = facebook.GraphAPI(acces_token)
            me = graph.get_object("/me")
        except Exception as e:
            log.error(e)
            raise tornado.web.HTTPError(500, "Auth")

        # TODO: verify that me is in the local database
        return tornado.escape.json_decode(me)


class AuthLoginHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
        my_url = (self.request.protocol + "://" + self.request.host +
                  "/auth/login?next=" +
                  tornado.escape.url_escape(self.get_argument("next", "/")))
        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri=my_url,
                client_id=self.settings["facebook_api_key"],
                client_secret=self.settings["facebook_secret"],
                code=self.get_argument("code"),
                callback=self._on_auth)
            return
        self.authorize_redirect(redirect_uri=my_url,
                                client_id=self.settings["facebook_api_key"],
                                extra_params={"scope": "public_profile"})

class Application(tornado.web.Application):
    "Main Application Instance"
    def __init__(self):

        handlers = [
            (r'/api/v1/switch', SwitchHandler),
            (r'/api/v1/switch/(.*)', SwitchHandler),
            (r'/(.*)', MainHandler),
            (r"/", MainHandler),
            (r"/auth/login", AuthLoginHandler),
        ]

        settings = dict(
            cookie_secret="TheBigBrownFoxJumpsOverTheLazyDog",
            login_url="/auth/login",
            xsrf_cookies=False,
            facebook_api_key=os.environ['FACEBOOK_API_KEY'],
            facebook_secret=os.environ['FACEBOOK_SECRET'],
            autoescape=None,
            autoreload=True,
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)



class MainHandler2(BaseHandler, tornado.auth.FacebookGraphMixin):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        self.facebook_request("/me/home", self._on_stream,
                              access_token=self.current_user["access_token"])

    def _on_stream(self, stream):
        if stream is None:
            # Session may have expired
            self.redirect("/auth/login")
            return
        self.render("stream.html", stream=stream)

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Facebook auth failed")
        self.set_secure_cookie("prodomo_user", tornado.escape.json_encode(user))
        self.redirect(self.get_argument("next", "/"))


class SwitchHandler(BaseHandler):
    "Handler degli switch"
    def get(self, switch=None):
        log.debug(switch)
        session = Session()
        if switch == '' or switch is None:
            data = session.query(Switch).all()
            data = [x.as_dict() for x in data]
        else:
            data = session.query(Switch).filter_by(pin=str(switch)).first()
            if data is None:
                raise tornado.web.HTTPError(404)
            data = data.as_dict()

        self.write(tornado.escape.json_encode(data))

    def post(self):
        session = Session()
        try:
            switch = Switch()
            switch.pin = int(self.get_argument("pin"))
            switch.description = self.get_argument("description")
            session.add(switch)
            session.commit()
        except Exception as e:
            #log.exception(e)
            session.rollback()
            raise tornado.web.HTTPError(500)


    def put(self, switch):
        session = Session()
        data = session.query(Switch).filter_by(pin=switch).first()
        if data is None:
            raise tornado.web.HTTPError(404)
        data.description = self.get_argument("description")
        try:
            session.commit()
        except Exception as e:
            #log.exception(e)
            session.rollback()
            raise tornado.web.HTTPError(500)

    def delete(self, switch):
        session = Session()
        data = session.query(Switch).filter_by(pin=switch).first()
        if data is None:
            raise tornado.web.HTTPError(404)

        try:
            session.delete(data)
            session.commit()
        except Exception as e:
            #log.exception(e)
            session.rollback()
            raise tornado.web.HTTPError(500)


static_content = glob.glob(content_path + '/*')
log.debug("here your static content: " + str(static_content))


class MainHandler(tornado.web.RequestHandler):
    def get(self, what="index.html"):
        if what is None or len(what) == 0:
            what = 'index.html'

        if what.endswith(".html") or "." not in what:
            what = "index.html"

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

application = Application()

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
