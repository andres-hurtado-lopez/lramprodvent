#!/usr/bin/env python
# -*- coding: utf-8 -*-

def GET(**params):
    return {'data': [{'value':str(i),'id':str(i*2)} for i in [1,2,3,4,5,6,7,8,10,11] if i > int(params.get('query','0'))]}