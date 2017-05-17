#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request
import utils, uuid, time

def get_actual_user():
    cookie_uid = request.cookies.get('token')

    if cookie_uid:
        db = ConnectDB()
        db.execute('SELECT user, type FROM users where session_key = %s',(cookie_uid,))
        row = db.fetchone()
        return row
    else:
        raise Exception(_("No se encontraron sesiones activas"))

def is_actual_user_sysop():
    return get_actual_user()['type'] == 'S'

def actual_user_datagroup_privileges(datagroup):
    db = utils.ConnectDB()
    count = db.query("SELECT `update`, `create`, `delete`, `view` FROM users_datagroup WHERE `user` = ? and `data_group` = ?",(get_actual_user()['user'], datagroup))
    row = db.fetchone()
    if count > 0:
        return row
    else
        return False

def check_secobj(secobj):
    if not is_actual_user_sysop():
        if not utils.secobjs.get(secobj,False):
            raise Exception("No tiene privilegios para realizar esta operación. Requiere objeto de seguridad {secobj}".format(secobj=secobj))


def actual_user_has_secobjs(secobjs):
    if not is_actual_user_sysop():
        found_secobjs = sum((1 for secobj in utils.secobjs if secobj in secobjs))
        if found_secobjs > 0:
            return True
        else
            return False
    else
        return True

def record_history(action, data):

    db = utils.ConnectDB()
    db.execute("""INSERT INTO user_history(log_id,
                                   user,
                                   action,
                                   data,
                                   `timestamp`)
                VALUES (:?,
                        :?,
                        :?,
                        :?,
                        :?);""",
                        (
                            str(uuid.uuid4()),
                            get_actual_user()['user']
                            action, \
                            data, \
                            time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                        )
    )
    db.execute('COMMIT')

def create_user(user, password, full_name, email, contact_address, telephone, notes, status, utype,data_group):

    check_secobj("A0001")

    db = utils.ConnectDB()
    db.execute("""INSERT INTO users(user,
                            password,
                            full_name,
                            email,
                            contact_address,
                            telephone,
                            notes,
                            status,
                            type)
                            VALUES (?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?)""",
                                    (user,\
                                    password,\
                                    full_name,\
                                    email,\
                                    contact_address,\
                                    telephone,\
                                    notes,\
                                    status,\
                                    utype))
    db.execute('COMMIT')

def delete_user(user):

    check_secobj("A0002")

    db = utils.ConnectDB()

    db.execute("SELECT * FROM user WHERE user = ?",(user,))
    row = db.fetchone()

    if row:
        privileges = actual_user_datagroup_privileges(row['data_group'])
        if !privileges or privileges['delete'] != 1:
            raise Exception(_("Eliminacion de usuario denegada, el usuario actual no tiene asignado el grupo de datos {data_group} o este grupo no tiene el privilegio de eliminacion").format(data_group=row['data_group']))
    else:
        raise Exception(_("El usuario {user} no fue encontrado".format(user=user)))

    db.execute('DELETE FROM users WHERE user = %s',(user,))
    db.execute('COMMIT')

def update_user(user,**fields):

    check_secobj("A0003")

    db = utils.ConnectDB()

    db.execute("SELECT * FROM user WHERE user = ?",(user,))
    row = db.fetchone()

    if row:
        privileges = actual_user_datagroup_privileges(row['data_group'])
        if !privileges or privileges['update'] != 1:
            raise Exception(_("Actualizacion de datos de usuario denegada, el usuario actual no tiene asignado el grupo de datos {data_group} o este grupo no tiene el privilegio de actualizacion").format(data_group=row['data_group']))
    else:
        raise Exception(_("El usuario {user} no fue encontrado".format(user=user)))

    db.execute('UPDATE users SET {updated_fields} WHERE user = %s'.format(updated_fields=", ".["{field} = '{value}'" for field, value in fields.iteritems()]),(user,))
    db.execute('COMMIT')

