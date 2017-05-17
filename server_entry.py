#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, request, static_file, error, response, template, redirect, abort
from passlib.hash import bcrypt
from utils import ConnectDB
import bottle, uuid, importlib, os, traceback, datetime, ConfigParser

def checkauth(fn):
    def check_uid(**kwargs):
        cookie_uid = request.cookies.get('token')

        if cookie_uid:
            db = ConnectDB()
            db.execute('SELECT * FROM users where session_key = %s',(cookie_uid,))

            row = db.fetchone()

            if row:
                return fn(**kwargs)
            else:
                abort(401, "Sorry, incorrect authentication, access denied.")
        else:
            abort(401, "Sorry no cookie found, access denied.")

    return check_uid


@route('/authenticate/<type>', method="POST")
def authenticate(type):
    try:
        Config = ConfigParser.ConfigParser()
        Config.read("config.ini")
        main_menu_path = Config.get("login", "main_menu_path")
        incorrect_login_path = Config.get("login", "incorrect_login_path")

        ts = datetime.datetime.now()+datetime.timedelta(days=1)
        token = str(uuid.uuid4())
        response.set_cookie("token", token, expires=ts, path="/")

        user = request.forms.get('user','')
        password = request.forms.get('password','')
        db = ConnectDB()
        db.execute('SELECT password from users where user = %s', (str(user),))
        row = db.fetchone()
        if row != None and bcrypt.verify(password, row['password']):
            db.execute('UPDATE users SET session_key = %s WHERE user = %s', (token,user))
            db.execute('COMMIT');
            if(type == 'background'):
                return {'result': 0}
            else:
                redirect(main_menu_path)
        else:
            if(type == 'background'):
                return {'result': 1}
            else:
                redirect(incorrect_login_path)
    except bottle.HTTPResponse, e:
        raise e
    except:
        return {'result' : 2, 'message': traceback.format_exc()}

@route('/web/<app>', method="GET")
@checkauth
def app_get(app):
    try:
        try:
            bottle.TEMPLATE_PATH.index('./app/'+app)
        except:
            bottle.TEMPLATE_PATH.append('./app/'+app)
        module = importlib.import_module(app)
        function = getattr(module, 'GET')
        return function(**request.params)
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@route('/web/<app>', method="POST")
@checkauth
def app_post(app):
    try:
        try:
            bottle.TEMPLATE_PATH.index('./app/'+app)
        except:
            bottle.TEMPLATE_PATH.append('./app/'+app)
        module = importlib.import_module(app)
        function = getattr(module, 'POST')
        return function(**request.params)
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@route('/web/<app>', method="PUT")
@checkauth
def app_put(app):
    try:
        try:
            bottle.TEMPLATE_PATH.index('./app/'+app)
        except:
            bottle.TEMPLATE_PATH.append('./app/'+app)
        module = importlib.import_module(app)
        function = getattr(module, 'PUT')
        return function(**request.params)
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@route('/web/<app>', method="DELETE")
@checkauth
def app_put(app):
    try:
        try:
            bottle.TEMPLATE_PATH.index('./app/'+app)
        except:
            bottle.TEMPLATE_PATH.append('./app/'+app)
        module = importlib.import_module(app)
        function = getattr(module, 'DELETE')
        return function(**request.params)
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@route('/web/<app>/<page>', method="GET")
@checkauth
def page_get(app, page):
    try:
        try:
            bottle.TEMPLATE_PATH.index('./app/'+app)
        except:
            bottle.TEMPLATE_PATH.append('./app/'+app)
        module = importlib.import_module(app)
        function = getattr(module, page+'_GET')
        return function(**request.params)
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@route('/web/<app>/<page>', method="POST")
@checkauth
def page_post(app, page):
    try:
        try:
            bottle.TEMPLATE_PATH.index('./app/'+app)
        except:
            bottle.TEMPLATE_PATH.append('./app/'+app)
        module = importlib.import_module(app)
        function = getattr(module, page+'_POST')
        return function(**request.params)
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@route('/web/<app>/<page>', method="PUT")
@checkauth
def page_put(app, page):
    try:
        try:
            bottle.TEMPLATE_PATH.index('./app/'+app)
        except:
            bottle.TEMPLATE_PATH.append('./app/'+app)
        module = importlib.import_module(app)
        function = getattr(module, page+'_PUT')
        return function(**request.params)
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@route('/web/<app>/<page>', method="DELETE")
@checkauth
def page_delete(app, page):
    try:
        try:
            bottle.TEMPLATE_PATH.index('./app/'+app)
        except:
            bottle.TEMPLATE_PATH.append('./app/'+app)
        module = importlib.import_module(app)
        function = getattr(module, page+'_DELETE')
        return function(**request.params)
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@route('/web/<app>/static/<filename:path>')
@checkauth
def server_static_app_file(app, filename):
    try:
        return static_file(filename, root='app/'+app+'/static')
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@error(404)
def error404(*error):
    return '<h1>Pagina no encontrada</h1>'

#@error(500)
#def error500(error):
#    return 'Error procesando pagina. Detalle Error:'+str(error)

@route('/api/<api>', method="GET")
@checkauth
def api_request(api):
    try:
        module = importlib.import_module(api)
        return module.GET(**request.params)
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@route('/api/<api>', method="POST")
@checkauth
def api_post(api):
    try:
        module = importlib.import_module(api)
        return module.POST(**request.params)
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@route('/api/<api>', method="PUT")
@checkauth
def api_put(api):
    try:
        module = importlib.import_module(api)
        return module.PUT(**request.params)
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@route('/api/<api>', method="DELETE")
@checkauth
def api_delete(api):
    try:
        module = importlib.import_module(api)
        return module.DELETE(**request.params)
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@route('/api/<api>/<method>', method="GET")
@checkauth
def api_method_request(api,method):
    try:
        module = importlib.import_module(api)
        function = getattr(module, method+'_GET')
        return function(**request.params)
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@route('/api/<api>/<method>', method="POST")
@checkauth
def api_method_post(api,method):
    try:
        module = importlib.import_module(api)
        function = getattr(module, method+'_POST')
        return function(**request.params)
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@route('/api/<api>/<method>', method="PUT")
@checkauth
def api_method_put(api,method):
    try:
        module = importlib.import_module(api)
        function = getattr(module, method+'_PUT')
        return function(**request.params)
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@route('/api/<api>/<method>', method="DELETE")
@checkauth
def api_method_delete(api,method):
    try:
        module = importlib.import_module(app)
        function = getattr(module, method+'_DELETE')
        return function(**request.params)
    except bottle.HTTPResponse, e:
        raise e
    except:
        abort(500, traceback.format_exc())

@route('/.well-known/<filename:path>')
def serve_ssl_certificate_validation(filename):
    return static_file(filename, root='www/.well-known')


@route('/static/<filename:path>')
def server_static_file(filename):
    return static_file(filename, root='static')


@route('/')
def server_main_page():
    return template("main_index.html", title="perez")
