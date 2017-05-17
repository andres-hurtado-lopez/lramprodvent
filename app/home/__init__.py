#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import template, redirect
import utils

def GET(**params):
    return template('home_index.html')

def ejemplos_bootstrap_grid_GET(**params):
    return template("ejemplos_bootstrap_grid.html")

def ejemplos_bootstrap_fixed_GET(**params):
    return template("ejemplos_bootstrap_fixed.html")

def ejemplos_bootstrap_fluid_GET(**params):
    return template("ejemplos_bootstrap_fluid.html")

def ejemplos_bootstrap_responsive_GET(**params):
    return template("ejemplos_bootstrap_responsive.html")

def tabla_ejemplo_GET(**params):
    filter = '%'+params.get('filter','')+'%'
    table = utils.RenderTable(\
        'SELECT user, full_name FROM users WHERE user like %s ORDER BY user',\
        (filter,),\
        '<tr><td>Usuario</td><td>Nombre</td><td>Eliminar</td</tr>',\
        '<tr><td><a href="/web/menu_principal/formulario_ejemplo?user={user}">{user}</td><td>{full_name}</td><td><a href="#" onclick="delete_record(\'{user}\');">Eliminar</a></td></tr>',\
        'table table-bordered',\
        5,\
        int(params.get('table_usuarios_page','1'))\
    )

    return template('tabla_ejemplo.html', title='Listado Tablas', table=table)

def formulario_ejemplo_GET(**params):
    db = utils.ConnectDB()
    user = params.get('user')
    new = params.get('new')
    if user:
        db.execute('SELECT user, full_name FROM users WHERE user = %s',(user,))
        rowdata = db.fetchone()
        return template("formulario_ejemplo.html", title='Formulario', userdata=rowdata, create='false')
    elif new == 'true':
        return template("formulario_ejemplo.html", title='Formulario', userdata={'user':'','full_name':''}, create='true')

    redirect('/web/menu_principal/tabla_ejemplo')

def formulario_ejemplo_POST(**params):
    db = utils.ConnectDB()
    if params.get('create') == 'true':
        db.execute('INSERT INTO users (user, full_name) VALUES (%s, %s)',(params.get('user'),params.get('full_name')))
    else:
        db.execute('UPDATE users SET full_name = %s WHERE user = %s',(params.get('full_name'),params.get('user')))
    db.execute('COMMIT');
    redirect('/web/menu_principal/formulario_ejemplo')

def formulario_ejemplo_DELETE(**params):
    try:
        db = utils.ConnectDB()
        db.execute('DELETE FROM users WHERE user = %s',(params.get('user',''),))
        db.execute('COMMIT');
        message = 'ok'
    except Exception, e:
        message = repr(e)
    return {'response':True,'message':message}

def typeahead_GET(**params):
    return template('typeahead.html')

def ejemplo_escaneo_codigo_barras_GET(**params):
    return template("ejemplo_escaneo_codigo_barras.html")
