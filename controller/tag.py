#coding=utf-8
__author__ = 'phithon'
import tornado.web
from controller.base import BaseHandler
from tornado import gen
import pymongo
from bson.objectid import ObjectId
from util.function import not_need_login, intval

class TagHandler(BaseHandler):


    def initialize(self):
        BaseHandler.initialize(self)
        self.topbar = ""
    
    
    @not_need_login
    def prepare(self):
        BaseHandler.prepare(self)  
    
    
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        tagid = args[0]
        limit = 15
        
        try:        
            page = intval(args[2])
            if page <= 0 : page = 1
        except:
            page = 1
            
        tag = yield self.db.tag.find_one({
            "_id": ObjectId(tagid)
        })
        if not tag:
            self.custom_error("标签不存在")
        cursor = self.db.article.find({
            "tag._id": ObjectId(tagid)
        })
        count = yield cursor.count()
        cursor.sort([('time', pymongo.DESCENDING)]).limit(limit).skip((page - 1) * limit)
        posts = yield cursor.to_list(length = limit)
        self.render("tag.html", posts = posts, page = page, tag = tag, count = count, each = limit)
            
            
class TagListHandler(BaseHandler):


    def initialize(self):
        BaseHandler.initialize(self)
        self.topbar = ""
    
    
    @not_need_login
    def prepare(self):
        BaseHandler.prepare(self)  


    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        limit = 15
        
        try:        
            page = intval(args[2])
            if page <= 0 : page = 1
        except:
            page = 1
            
        cursor = self.db.tag.find()
        count = yield cursor.count()
        cursor.sort([('time', pymongo.DESCENDING)]).limit(limit).skip((page - 1) * limit)
        tags = yield cursor.to_list(length = limit)
        self.write(dict(tags = tags, page = page, count = count, each = limit))