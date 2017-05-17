#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb, ConfigParser, json
from bottle import template

secobjs = \
{ \
    "A0001" : "Crear Usuario", \
    "A0002" : "Actualizar Usuario", \
    "A0003" : "Eliminar Usuario", \
}

def ConnectDB():
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")

    db = MySQLdb.connect(host=Config.get("database", "host"),\
                         user=Config.get("database", "user"),\
                         passwd=Config.get("database", "passwd"),\
                         db=Config.get("database", "db"))

    return db.cursor(MySQLdb.cursors.DictCursor)

def RenderTable(sql, params, head_template, row_template, table_class, page_size, page_cursor):
    db = ConnectDB()
    offset = page_size * ( page_cursor - 1 ) if page_cursor >= 0 else 0
    add_params = params if type(params) is tuple else ()
    db.execute(sql+' LIMIT %s, %s',add_params + (offset, page_size))
    record_count = db.rowcount

    if (record_count % page_size) > 0:
        max_pages = record_count / page_size + 1
    elif (record_count % page_size) == 0:
        max_pages = record_count / page_size
    else:
        max_pages = 1

    previous_page = page_cursor - 1 if (page_cursor - 1) > 0 else 1
    next_page = page_cursor + 1 if page_cursor < max_pages else max_pages

    table_render = '\
<div class="table-responsive">\n\
    <table class="'+table_class+'">\n\
        <thead>\n\
            '+head_template+'\n\
        </thead>\n\
        <tbody>'
    for row in db.fetchall():
        try:
            table_render += row_template.format(**row)
        except UnicodeDecodeError:
            pass
    table_render += '\n\
        </tbody>\n\
    </table>\n\
</div>\n\
<div class="text-center">\n\
<ul class="pagination">\n\
    <li><a href="?table_'+table_class+'_page='+str(previous_page)+'">&larr;</a></li>\n\
    <li><a href="#">'+str(page_cursor)+' / '+str(max_pages)+'</a></li>\n\
    <li><a href="?table_'+table_class+'_page='+str(next_page)+'">&rarr;</a></li>\n\
</ul>\n\
</div>\n\
'

    return template(table_render,**{})

def get_menu():
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")
    return Config.get('navbar','appserver_name'), Config.get('navbar','appserver_link'), json.load(open(Config.get('navbar','pages'))),