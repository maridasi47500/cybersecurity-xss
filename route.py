from directory import Directory
from render_figure import RenderFigure
from myscript import Myscript
from user import User
from myrecording import Myrecording
from gagnant import Gagnant
from ad import Ad


from song import Song
from mypic import Pic
from javascript import Js
from stylesheet import Css
import re
import traceback
import sys

class Route():
    def get_routes(self):
        routes={
                    '^/get_my_cookie$': self.get_my_cookie,
                    '^/welcome$': self.welcome,
                    '^/new$': self.newshop,
                    '^/newad$': self.new1,
                    '^/list$': self.list,
                    "^/list/(\d+)$":self.seead,
                    '^/thanks$': self.thanks,
                    '^/shops$': self.shops,
                    '^/signin$': self.signin,
                    '^/logmeout$':self.logout,
                                        '^/save_user$':self.save_user,
                                                            '^/update_user$':self.update_user,
                    "^/seeuser/([0-9]+)$":self.seeuser,
                                        "^/edituser/([0-9]+)$":self.edit_user,
                                                            "^/deleteuser/([0-9]+)$":self.delete_user,
                                                                                '^/login$':self.login,

                                                                                                    '^/users$':self.myusers,
                    '^/$': self.hello

                    }
        return routes
    def __init__(self):
        self.dbUsers=User()
        self.Program=Directory("premiere radio")
        self.Program.set_path("./")
        self.mysession={"notice":None,"email":None,"name":None}
        self.dbScript=Myscript()
        self.dbAd = Ad()
        self.render_figure=RenderFigure(self.Program)
        self.getparams=("id",)

    def set_post_data(self,x):
        self.post_data=x
    def get_post_data(self):
        return self.post_data
    def set_my_session(self,x):
        print("set session",x)
        self.Program.set_my_session(x)
        self.render_figure.set_session(self.Program.get_session())
    def set_redirect(self,x):
        self.Program.set_redirect(x)
        self.render_figure.set_redirect(self.Program.get_redirect())
    def render_some_json(self,x):
        self.Program.set_json(True)
        return self.render_figure.render_some_json(x)
    def render_my_json(self,x):
        self.Program.set_json(True)
        return self.render_figure.render_my_json(x)
    def set_json(self,x):
        self.Program.set_json(x)
        self.render_figure.set_json(self.Program.get_json())
    def set_notice(self,x):
        print("set session",x)
        self.Program.set_session_params({"notice":x})
        self.render_figure.set_session(self.Program.get_session())
    def set_session(self,x):
          print("set session",x)
          self.Program.set_session(x)
          self.render_figure.set_session(self.Program.get_session())
    def get_this_get_param(self,x,params):
          print("set session",x)
          hey={}
          for a in x:
              hey[a]=params[a][0]
          return hey
          
    def get_this_route_param(self,x,params):
          print("set session",x)
          return dict(zip(x,params["routeparams"]))
          
    def logout(self,search):
        self.Program.logout()
        self.set_redirect("/")
        return self.render_figure.render_redirect()
    def welcome(self,search):
        hi=self.dbScript.getall()
        self.render_figure.set_param("scripts",hi)
        return self.render_figure.render_figure("welcome/index.html")
    def shops(self,search):
        print("hello action")
        self.render_figure.set_param("shops",self.dbAd.getall())
        return self.render_some_json("welcome/shops.json")
    def hello(self,search):
        print("hello action")
        return self.render_figure.render_figure("welcome/index.html")
    def get_my_cookie(self,hey):
        print("hello action")
        self.render_figure.set_param("cookie",str(self.Program.get_session()))
        return self.render_some_json("welcome/get_cookie.json")
    def newshop(self,search):
        print("hello action")
        return self.render_figure.render_figure("welcome/newshop.html")
    def new1(self,search):
        print("hello action")
        getparams=("title","pic","text",)
        myparam=self.post_data(getparams)
        self.dbAd.create(myparam)
        return self.render_some_json("welcome/created.json")
    def delete_user(self,params={}):
        getparams=("id",)
        myparam=self.post_data(self.getparams)
        self.render_figure.set_param("user",User().deletebyid(myparam["id"]))
        self.set_redirect("/")
        return self.render_figure.render_redirect()
    def edit_user(self,params={}):
        getparams=("id",)

        myparam=self.get_this_route_param(getparams,params)
        print("route params")
        self.render_figure.set_param("user",User().getbyid(myparam["id"]))
        return self.render_figure.render_figure("user/edituser.html")
    def seead(self,params={}):
        getparams=("id",)
        print("get param, action see my new",getparams)
        myparam=self.get_this_route_param(getparams,params)
        self.render_figure.set_param("ad",self.dbAd.getbyid(myparam["id"]))
        return self.render_figure.render_figure("welcome/seead.html")
    def seeuser(self,params={}):
        getparams=("id",)
        print("get param, action see my new",getparams)
        myparam=self.get_this_route_param(getparams,params)
        self.render_figure.set_param("user",User().getbyid(myparam["id"]))
        return self.render_figure.render_figure("user/showuser.html")
    def thanks(self,params={}):
        return self.render_figure.render_figure("welcome/merci.html")
    def list(self,params={}):
        self.render_figure.set_param("ads",self.dbAd.getall())
        return self.render_figure.render_figure("welcome/list.html")
    def myusers(self,params={}):
        self.render_figure.set_param("users",User().getall())
        return self.render_figure.render_figure("user/users.html")
    def update_user(self,params={}):
        myparam=self.post_data(self.getparams)
        self.user=self.dbUsers.update(params)
        self.set_session(self.user)
        self.set_redirect(("/seeuser/"+params["id"][0]))
    def login(self,s):
        search=self.get_post_data()(params=("email","password"))
        self.user=self.dbUsers.getbyemailpw(search["email"],search["password"])
        print("user trouve", self.user)
        if self.user["email"]:
            self.set_session(self.user)
            self.set_session(self.user)
            if self.Program.get_session_param("jeu_id") and self.Program.get_session_param("user_id"):
                self.set_json("{\"redirect\":\"/welcome\"}")
            elif self.get_session("user_id"):
                self.set_json("{\"redirect\":\"/welcome\"}")
            else:
                self.set_json("{\"redirect\":\"/chat\"}")

        else:
            self.set_json("{\"redirect\":\"/signin\"}")
            print("session login",self.Program.get_session())
        return self.render_figure.render_json()
    def signin(self,search):
        return self.render_figure.render_figure("user/signin.html")

    def save_user(self,params={}):
        myparam=self.get_post_data()(params=("businessaddress","gender","profile","metier", "otheremail", "password","zipcode", "email", "mypic","postaladdress","nomcomplet","password_confirmation"))
        self.user=self.dbUsers.create(myparam)
        if self.user["email"]:
            if self.Program.get_session_param("jeu_id") and self.Program.get_session_param("user_id"):
                self.set_json("{\"redirect\":\"/welcome\"}")
            else:
                self.set_json("{\"redirect\":\"/chat\"}")
        else:
            self.set_json("{\"redirect\":\"/signin\"}")
        return self.render_figure.render_json()
    def run(self,redirect=False,redirect_path=False,path=False,session=False,params={},url=False,post_data=False):
        if post_data:
            print("post data")
            self.set_post_data(post_data)
            print("post data set",post_data)
        if url:
            print("url : ",url)
            self.Program.set_url(url)
        self.set_my_session(session)

        if redirect:
            self.redirect=redirect
        if redirect_path:
            self.redirect_path=redirect
        if not self.render_figure.partie_de_mes_mots(balise="section",text=self.Program.get_title()):
            self.render_figure.ajouter_a_mes_mots(balise="section",text=self.Program.get_title())
        if path and path.endswith("png"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith("gif"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith("svg"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith("jpg"):
            self.Program=Pic(path)
            self.Program.set_path("./")
        elif path and path.endswith(".jfif"):
            self.Program=Pic(path)
        elif path and path.endswith(".css"):
            self.Program=Css(path)
        elif path and path.endswith(".js"):
            self.Program=Js(path)
        elif path:
            path=path.split("?")[0]
            print("link route ",path)
            ROUTES=self.get_routes()

            REDIRECT={"/save_user": "/welcome"}
            for route in ROUTES:
               print("pattern=",route)
               mycase=ROUTES[route]
               x=(re.match(route,path))
               print(True if x else False)
               if x:
                   params["routeparams"]=x.groups()
                   self.Program.gagnant()
                   try:
                       self.Program.set_html(html=mycase(params))


                   except Exception:  
                       self.Program.set_html(html="<p>une erreur s'est produite "+str(traceback.format_exc())+"</p><a href=\"/\">retour à l'accueil</a>")
                   self.Program.redirect_if_not_logged_in()

                   return self.Program
               else:
                   self.Program.set_html(html="<p>la page n'a pas été trouvée</p><a href=\"/\">retour à l'accueil</a>")
        return self.Program
