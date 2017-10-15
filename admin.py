#!/usr/bin/env python
# coding=utf8 check git update

import sys
import logging
import tornado.web
import tornado.ioloop
from tornado.httpserver import HTTPServer
from tornado.options import  parse_command_line
from lib.bootloader import settings, jinja_environment, memcachedb
from lib.filter import register_filters
from lib.route import Route
from lib.session import MemcacheSessionStore
from handler import AdminPageNotFoundHandler, admin


class Application(tornado.web.Application):
    def __init__(self):
        self.jinja_env = jinja_environment
        self.jinja_env.filters.update(register_filters())
        # self.jinja_env.tests.update({})
        self.jinja_env.globals['settings'] = settings

        self.memcachedb = memcachedb
        self.session_store = MemcacheSessionStore(memcachedb)

        handlers = Route.routes() + [
            tornado.web.url(r"/style/(.+)", tornado.web.StaticFileHandler, dict(path=settings['static_path']), name='static_path'),
            tornado.web.url(r"/upload/(.+)", tornado.web.StaticFileHandler, dict(path=settings['upload_path']), name='upload_path'),
            (r".*", AdminPageNotFoundHandler)
        ]

        tornado.web.Application.__init__(self, handlers, **settings)


def runserver():
    parse_command_line()    # 解析命令行，输出logging日志
    app = Application()
    http_server = HTTPServer(app, xheaders=True)
    port = 8890
    if len(sys.argv) >= 2:
        port = int(sys.argv[1])
    http_server.listen(port)
    loop = tornado.ioloop.IOLoop.instance()
    logging.info('Admin Server running on http://127.0.0.1:%d/admin' % port)
    loop.start()


if __name__ == '__main__':
    runserver()

