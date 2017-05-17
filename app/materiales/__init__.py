#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import template, redirect
import utils

def GET(**params):
    return template('materiales_index.html')


def crear_entrada_material_GET(**params):
    return template('crear_entrada_material.html')

def crear_entrada_material_POST(**params):
    db = utils.ConnectDB()
    user = params.get('user')
    new = params.get('new')
    if user:
        db.execute('SELECT user, full_name FROM users WHERE user = %s',(user,))
        rowdata = db.fetchone()
    else:
        rowdata = {'user':'','full_name':''}

    redirect('crear_entrada_material')
