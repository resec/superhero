#!/usr/bin/python
import tornado.ioloop
import tornado.web, tornado.options, tornado.httpserver
import motor
import sys
import os
import yaml
from concurrent import futures
import controller

tornado.options.define("port", default=8765, help="Run server on a specific port", type=int)
tornado.options.define("host", default="localhost", help="Run server on a specific host")
tornado.options.define("url", default=None, help="Url to show in HTML")
tornado.options.define("config", default="./config.yaml", help="config file's full path")
tornado.options.parse_command_line()

if not tornado.options.options.url:
    tornado.options.options.url = "http://%s:%d" % (tornado.options.options.host, tornado.options.options.port)

setting = {
    "base_url": tornado.options.options.url,
    "template_path": "static/template",
    "cookie_secret": "s3cr3tk3y",
    "config_filename": tornado.options.options.config,
    "compress_response": True,
    "default_handler_class": controller.base.NotFoundHandler,
    #"xsrf_cookies": True,
    "static_path": "static",
    "download": "./download",
    "session": {
        "driver": "redis",
        "driver_settings": {
            "host": "localhost",
            "port": 6379,
            "db": 1
        },
        "force_persistence": False,
        "cache_driver": True,
        "cookie_config": {
            "httponly": True
        },
    },
    "thread_pool": futures.ThreadPoolExecutor(4),
}

# config file
config = {}
try:
    with open(setting["config_filename"], "r") as fin:
        config = yaml.load(fin)
    for k, v in config["global"].items():
        setting[k] = v
    if "session" in config:
        setting["session"]["driver_settings"] = config["session"]
except:
    print("cannot found config.yaml file")
    sys.exit(0)

# mongodb connection
# format: mongodb://user:pass@host:port/
# database name: minos

try:
    client = motor.MotorClient(config["database"]["config"])
    database = client[config["database"]["db"]]
    setting["database"] = database
except:
    print("cannot connect mongodb, check the config.yaml")
    sys.exit(0)


class DummyHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.write({})

application = tornado.web.Application([
    # (r"^/(page/(\d+))?", "controller.main.IndexHandler"),
    # (r"^/login", "controller.auth.LoginHandler"),
    # (r"^/register", "controller.auth.RegisterHandler"),
    # (r"^/nologin/([a-z]+)", "controller.auth.AjaxHandler"),
    # (r"^/forgetpwd", "controller.auth.ForgetpwdHandler"),
    # (r"^/captcha\.png", "controller.auth.CaptchaHanlder"),
    # (r"^/user/([a-z]+)(/(.*))?", "controller.user.UserHandler"),
    # (r"^/admin/([a-z]+)?", "controller.admin.AdminHandler"),
    # (r"^/publish", "controller.publish.PublishHandler"),
    # (r"^/edit/([a-f0-9]{24})", "controller.publish.EditHandler"),
    # (r"^/uploader", "controller.publish.UploadHandler"),
    # (r"^/post/([a-f0-9]{24})", "controller.post.PostHandler"),
    # (r"^/ajax/([a-z]+)", "controller.ajax.AjaxHandler"),
    # (r"^/sort/([a-f0-9]{24})(/(\d+))?", "controller.sort.SortHandler"),
    # (r"^/search(/(\d+))?", "controller.search.SearchHandler"),
    # (r"^/message(/(\d+))?", "controller.message.MessageHandler"),
    # (r"^/message/([a-f0-9]{24})", "controller.message.DetailHandler"),
    # (r"^/manage/([a-z]+)(/(.*))?", "controller.dashboard.AdminHandler"),
    # (r"^/download/(.*)", "controller.download.DownloadHandler", {"path": "./download/"})
    (r"/", controller.main.IndexHandler), #(GET) 获取网站全局配置文件、包括站点信息、部分站点参数
    (r"/index", controller.main.IndexHandler), #(GET) 获取网站全局配置文件、包括站点信息、部分站点参数
    (r"/admin", controller.admin.AdminHandler), #(GET POST) 设置网站全局参数
    (r"/user", controller.user.UserHandler), #(GET POST) 获取已登录用户信息，包括用户个人信息和用户关注而未读的文章列表
    (r"/user/index", controller.user.UserHandler),  #(GET POST)
    (r"/login", controller.auth.LoginHandler), #(POST) 登录
    (r"/logout", DummyHandler), #(GET) 退出登录
    (r"/register", controller.auth.RegisterHandler), #(POST) 用户注册
    (r"/reset", controller.auth.ForgetpwdHandler), #(GET POST) 用户邮箱验证、申请解锁、重置密码、修改邮箱等涉及邮箱验证的操作
    (r"/user/admin", controller.admin.AdminHandler), #(GET POST) 用户管理相关后台接口
    (r"/user/article", controller.user.UserHandler), #(GET) 获取已登录用户（自己）的文章列表
    (r"/user/comment", controller.user.UserHandler), #(GET) 获取已登录用户（自己）的评论列表
    (r"/user/mark", controller.user.UserHandler), #(GET) 获取已登录用户（自己）的标记文章列表
    (r"/user/fans", controller.user.UserHandler), #(GET) 获取已登录用户（自己）的粉丝列表
    (r"/user/follow", controller.user.UserHandler), #(GET) 获取已登录用户（自己）的关注列表
    (r"/user/(?P<uid>U[^/]+)", controller.user.UserHandler), #(GET POST) 获取用户Uxxxxx的用户信息，包括用户公开的个人信息和用户最新发表的文章列表
    (r"/user/(?P<uid>U[^/]+)/article", controller.user.UserHandler), #(GET) 获取用户Uxxxxx的文章列表
    (r"/user/(?P<uid>U[^/]+)/fans", controller.user.UserHandler), #(GET) 获取用户Uxxxxx的粉丝列表
    (r"/article", controller.post.PostHandler), #(GET POST) 获取最新文章列表，添加文章
    (r"/article/index", DummyHandler), #(GET POST)
    (r"/article/admin", controller.admin.AdminHandler), #(GET POST) 文章管理相关后台接口
    (r"/article/comment", DummyHandler), #(GET POST) 获取热门评论、批量获取指定ID的评论
    (r"/article/latest", controller.post.PostListHandler), #(GET) 获取最新文章列表（按发表时间排序）
    (r"/article/hots", controller.post.PostListHandler), #(GET) 获取最热文章列表（按文章热度排序）
    (r"/article/update", controller.post.PostListHandler), #(GET) 获取最近更新（按文章最后更新、最后评论时间排序）
    (r"/article/(?P<aid>A[^/]+)", controller.post.PostHandler), #(GET POST DELETE) 获取文章Axxx的相信内容
    (r"/article/(?P<aid>A[^/]+)/comment", controller.post.PostHandler), #(GET) 获取文章Axxx的更多评论
    (r"/tag", controller.tag.TagListHandler), #(GET POST) 获取热门标签列表
    (r"/tag/admin", controller.admin.AdminHandler), #(GET POST) 标签管理后台相关接口
    (r"/tag/(?P<tid>T[^/]+)", controller.tag.TagHandler), #(GET POST) 获取标签Txxx包含的文章列表（按照发表时间排序）
    (r"/message", DummyHandler),
    (r"/collection", DummyHandler),    
], **setting)




if __name__ == "__main__":
    try:
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(tornado.options.options.port)
        tornado.ioloop.IOLoop.instance().start()
    except:
        import traceback
        print(traceback.print_exc())
    finally:
        sys.exit(0)