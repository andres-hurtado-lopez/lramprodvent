#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import template, redirect
import utils

def GET(**params):
    return template('security_index.html', title="Seguridad")

def users_GET(**params):
    filter = '%'+params.get('filter','')+'%'
    table = utils.RenderTable(\
        'SELECT user, full_name FROM users WHERE user like %s ORDER BY user',\
        (filter,),\
        '<tr><td>Usuario</td><td>Nombre</td><td>Eliminar</td</tr>',\
        '<tr><td><a href="/web/security/user_detail?user={user}">{user}</td><td>{full_name}</td><td><a href="#" onclick="delete_record(\'{user}\');">Eliminar</a></td></tr>',\
        'table table-bordered',\
        5,\
        int(params.get('table_usuarios_page','1'))\
    )

    return template('users_list.html', table=table)

def user_detail_GET(**params):
    db = utils.ConnectDB()
    user = params.get('user')
    new = params.get('new')
    if user:
        db.execute('SELECT user, full_name FROM users WHERE user = %s',(user,))
        rowdata = db.fetchone()
    else:
        rowdata = {'user':'','full_name':''}

    return template("user_detail.html", title='Formulario', userdata=rowdata, create=('true' if new else 'false'))

    redirect('/web/security/users')