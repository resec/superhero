#coding=utf-8
__author__ = 'phithon'
import tornado.web, time, re
from controller.base import BaseHandler
from tornado import gen
import pymongo
from bson.objectid import ObjectId
from util.function import not_need_login, intval, humantime

class PostHandler(BaseHandler):
    
    @not_need_login
    def prepare(self):
        BaseHandler.prepare(self)    
    
    def initialize(self):
        BaseHandler.initialize(self)
        self.topbar = ""

    def is_edit(self, post):
        return post["user"] == self.current_user.get("username")

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.set_header("Content-Security-Policy", "default-src 'self'; script-src bdimg.share.baidu.com 'self' 'unsafe-eval'; "
                                                    "connect-src 'self'; img-src *.share.baidu.com nsclick.baidu.com 'self' data:; "
                                                    "style-src 'self' 'unsafe-inline'; font-src 'self'; frame-src 'self';")
        id = args[0]
        post = yield self.db.article.find_one({
            "_id": ObjectId(id)
        })
        if not post:
            self.custom_error("你找的文章并不存在", jump = "/")

        user = yield self.db.member.find_one({
            "username": post["user"]
        })
        yield self.db.article.find_and_modify({
            "_id": ObjectId(id)
        }, {
            "$inc": {"view": 1}
        })
        self.render("post.html", post = post, user = user, is_edit = self.is_edit)

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self, *args, **kwargs):
        content = self.get_body_argument("content")
        postid = self.get_body_argument("postid")
        _id = ObjectId()
        post = yield self.db.article.find_and_modify({
                "_id": ObjectId(postid)
            },{
                "$push": {
                    "comment": {
                        "_id": _id,
                        "content": content,
                        "user": {
                            "id": self.current_user["_id"],
                            "username": self.current_user["username"]
                        },
                        "time": time.time()
                    }
                },
                "$set": {
                    "lastcomment": time.time()
                }
            })
        if post:
            if self.current_user["username"] != post["user"]:
                self.message(fromuser=None, touser=post["user"],
                    content=u"%s 评论了你的文章《%s》" % (self.current_user["username"], post["title"]),
                    jump="/post/%s" % postid)
            self.at_user(content, post["title"], post["_id"], _id)
            self.redirect("/post/%s#%s" % (postid, _id))
        else:
            self.custom_error("不存在这篇文章")

    @gen.coroutine
    def at_user(self, content, title, postid, comid):
        at = []
        grp = re.findall(r"@([a-zA-Z0-9_\-\u4e00-\u9fa5]+)", content)
        for username in grp:
            try:
                user = yield self.db.member.find_one({
                    "username": username
                })
                assert type(user) is dict
                assert self.current_user["username"] != username
                assert username not in at
                yield self.message(fromuser=None, touser=username,
                    content=u"%s在文章《%s》中提到了你。" % (self.current_user["username"], title),
                    jump="/post/%s#%s" % (postid, comid))
                at.append(username)
            except:
                continue

    @gen.coroutine
    def get_user(self, username):
        user = yield self.db.member.find_one({
            "username": {"$eq": username}
        })
        raise gen.Return(user)


class PostListHandler(BaseHandler):
    
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
            page = intval(args[1])
            if page <= 0 : page = 1
        except:
            page = 1
                    
        cursor = self.db.article.find()
        cursor.sort([('top', pymongo.DESCENDING), ("lastcomment", pymongo.DESCENDING), ('time', pymongo.DESCENDING)]).limit(limit).skip((page - 1) * limit)
        count = yield cursor.count()
        posts = yield cursor.to_list(length = limit)
        tags = yield self.get_tag()
        
        self.write(dict(posts = posts, tags = tags, page = page,
            count = count, each = limit))
            
            
    @gen.coroutine
    def get_tag(self):
        tags = []
        cursor = self.db.tag.find()
        while (yield cursor.fetch_next):
            tags.append(cursor.next_object())
        raise gen.Return(tags)