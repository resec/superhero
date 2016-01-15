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

class IndexInfoHandler(BaseHandler):

    @not_need_login
    def prepare(self):
        BaseHandler.prepare(self)    

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.write(self.index)
        
        
    index = { 'domain': 'jsgen.org',
  'beian': '',
  'title': 'jsGen',
  'url': 'http://www.jsgen.org',
  'logo': '/static/img/logo.png',
  'description': 'You can generate a beautiful website or blog with javascript!',
  'metatitle': 'jsGen',
  'metadesc': 'You can generate a beautiful website or blog with javascript!',
  'keywords': 'jsGen,Node.js,MongoDB',
  'date': 1452827445323,
  'onlineNum': 2,
  'onlineUsers': 2,
  'maxOnlineNum': 2,
  'maxOnlineTime': 1452836161181,
  'ArticleTagsMax': 5,
  'UserTagsMax': 10,
  'TitleMinLen': 12,
  'TitleMaxLen': 90,
  'SummaryMaxLen': 420,
  'ContentMinLen': 24,
  'ContentMaxLen': 20480,
  'UserNameMinLen': 5,
  'UserNameMaxLen': 15,
  'register': True,
  'upload': False,
  'cloudDomian': '',
  'tagsList': ['为什么','你','这么','叼'],
  'user': None }