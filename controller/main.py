#coding=utf-8
__author__ = 'phithon'
import tornado.web
from controller.base import BaseHandler
from tornado import gen
from util.function import not_need_login

class IndexHandler(BaseHandler):

    @not_need_login
    def prepare(self):
        BaseHandler.prepare(self)    

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.render("index.html")

