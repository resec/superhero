#coding=utf-8
import tornado.web, time, json, xxtea, hashlib
from controller.base import BaseHandler
from util.function import not_need_login, hash
from tornado import gen
from tornado.escape import url_escape, utf8
from util.sendemail import Sendemail

class AjaxHandler(BaseHandler):
    @not_need_login
    def prepare(self):
        BaseHandler.prepare(self)

    def _json(self, status, info = ""):
        data = {
            "status": status,
            "info": info
        }
        self.write(data)
        raise tornado.web.Finish()

    def post(self, *args, **kwargs):
        method = args[0]
        if hasattr(self, "_%s_action" % method):
            getattr(self, "_%s_action" % method)()
        else:
            self._json("fail")

    @tornado.web.asynchronous
    @gen.coroutine
    def _checkusername_action(self):
        username = self.get_body_argument("username", default=None)
        user = {"username": username}
        user = yield self.db.member.find_one({
            "username": username
        })
        if user:
            self._json("fail", "用户名已存在")
        else:
            self._json("success")

class ForgetpwdHandler(BaseHandler):
    def initialize(self):
        BaseHandler.initialize(self)
        self.topbar = ''

    @not_need_login
    def prepare(self):
        BaseHandler.prepare(self)

    def get_byte_16(self, key):
        m = hashlib.md5()
        m.update(key)
        return m.digest()

    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        auth = self.get_query_argument("auth", default=None)
        # after users click url in their email, show the new password page
        if auth:
            try:
                svalue = xxtea.decrypt_hex(utf8(auth), self.get_byte_16(self.settings.get("cookie_secret")))
                (username, password, t) = svalue.split("|")
            except:
                self.custom_error("参数错误，请重新找回密码", jump="/forgetpwd")

            if time.time() - float(t) > 30 * 60:
                self.custom_error("链接已过期，请在30分钟内点击链接找回密码", jump="/forgetpwd")
            user = yield self.db.member.find_one({
                "username": username, "password": password
            })
            if user:
                self.render("renewpwd.html", auth = auth)
            else:
                self.custom_error("参数错误，请重新找回密码", jump="/forgetpwd")
        # first visit forgetpwd
        else:
            self.render("forgetpwd.html", success = None)

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        email = self.get_body_argument("email", default=None)
        auth = self.get_body_argument("auth", default=None)
        # after users submit their email
        if email:
            user = yield self.db.member.find_one({
                "email": email
            })
            if not user:
                self.custom_error("不存在这个Email")
            sign = "%s|%s|%s" % (user["username"], user["password"], time.time())
            svalue = xxtea.encrypt_hex(utf8(sign), self.get_byte_16(self.settings.get("cookie_secret")))
            url = self.settings.get("base_url") + "/forgetpwd?auth=%s" % url_escape(svalue, False)
            Sendemail(self.settings.get("email")).send(
                to=user["email"],
                orgin="root@waf.science",
                title=u"找回密码 - %s" % self.settings["site"]["webname"],
                content=u"点击链接找回你的密码：<br /><a href=\"%s\">%s</a><br />如果你没有找回密码，请忽视这封邮件" % (url, url)
            )
            self.render("forgetpwd.html", success = True)
        # after users click url in their email, and submit a new password
        elif auth:
            newpwd = self.get_body_argument("password")
            try:
                svalue = xxtea.decrypt_hex(utf8(auth), self.get_byte_16(self.settings.get("cookie_secret")))
                (username, password, t) = svalue.split("|")
            except:
                self.custom_error("参数错误，请重新找回密码", jump="/forgetpwd")
            if time.time() - float(t) > 30 * 60:
                self.custom_error("链接已过期，请在30分钟内点击链接找回密码", jump="/forgetpwd")
            newpwd = yield self.backend.submit(hash.get, newpwd)
            user = yield self.db.member.find_and_modify({
                "username": username, "password": password
            }, {
                "$set": {"password": newpwd}
            })
            if not user:
                self.custom_error("参数错误，请重新找回密码", jump="/forgetpwd")
            else:
                self.custom_error("密码修改成功", jump="/login", status = "success")
        else:
            self.custom_error("不存在这个Email")

class LoginHandler(BaseHandler):
    def initialize(self):
        BaseHandler.initialize(self)
        self.topbar = 'login'

    @not_need_login
    def prepare(self):
        BaseHandler.prepare(self)

    def get(self):
        file = open("static/template/login.html", "rb")
        self.write(file.read())

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        try:
            username = self.get_body_argument('logname', default="")
            password = self.get_body_argument('logpwd', default="")
            remember = self.get_body_argument('logauto', default=False)

            user = yield self.db.member.find_one({"username": username})
            check = password == user.get("password")
            if check and user["power"] >= 0:
                session = self.set_session(user)
                if remember:
                    cookie_json = json.dumps(session)
                    self.set_secure_cookie("user_info", cookie_json, expires_days = 30, httponly = True)
                yield self.db.member.find_and_modify({"username": username},{
                    "$set": {
                        "logintime": time.time(),
                        "loginip": self.get_ipaddress()
                    }
                })
                self.redirect("/")
            else:
                assert False
        except tornado.web.Finish:
            pass
        except:
            import traceback
            print(traceback.print_exc())
            self.custom_error("用户名或密码错误或账号被禁用", jump = "/login")


class RegisterHandler(BaseHandler):
    def initialize(self):
        BaseHandler.initialize(self)
        self.topbar = 'register'

    @not_need_login
    def prepare(self):
        BaseHandler.prepare(self)
        self.error = {
            "usernameused": "用户已经注册过啦",
        }

    def get(self, *args, **kwargs):
        error = self.get_argument("error", default = "")
        error = self.error.get(error)
        self.render("register.html", error = error, flash = self.flash,
                    method = self.settings["register"])

    @tornado.web.asynchronous
    @gen.coroutine
    def post(self):
        print(self.request.body)
        name = self.get_body_argument("name", default="")
        email = self.get_body_argument("email", default="")
        passwd = self.get_body_argument("passwd", default="")

        self.flash["user_reg"] = dict(name = name, email = email, passwd = passwd)

        member = yield self.db.member.find_one({'username': name})
        # 用户名已存在
        if member:
            self.redirect("/register?error=usernameused")
        #插入用户
        user = {
            "username": name,
            "password": passwd,
            "power": 0,
            "time": time.time(),
            "bookmark": [],
            "email": email,
            "qq": "",
            "website": "",
            "address": "",
            "signal": u"太懒，没有留下任何个人说明",
            "openwebsite": 1,
            "openqq": 1,
            "openemail": 1,
            "allowemail": 1,
            "logintime": None,
            "loginip": self.get_ipaddress()
        }
        result = yield self.db.member.insert(user)
        self.flash["user_reg"] = None
        self.redirect('/login')

