#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import template, redirect
import utils

def GET(**params):
    return template('materiales_index.html')
