# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user, AnonymousUserMixin

from atss4po.extensions import login_manager
from atss4po.auth.forms import LoginForm
from atss4po.auth.forms import RegisterForm
from atss4po.user.models import User
from atss4po.utils import flash_errors
from flask import jsonify, g, current_app
from ..extensions import csrf_protect, auth
from ..summary import autosum
import base64
import time
import datetime
from atss4po.database import db

class ErrorType(object):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

class ErrorStatus(object):
    def __init__(self):
        self.success = ErrorType(0, 'success')
        self.format_error = ErrorType(1, 'json format error')
        self.unknown_error = ErrorType(2, 'unknown error')
        self.no_article = ErrorType(3, 'no unsummarized article')
        self.no_amount = ErrorType(4, 'upload to increase your use amount')

def encrypt(id):
    bytes_id = str(id).encode(encoding='utf-8')
    return base64.encodebytes(bytes_id).decode('utf-8')

def decrypt(str_id):
    bytes_id = str_id.encode(encoding='utf-8')
    return int(base64.decodebytes(bytes_id).decode('utf-8'))

def utc2local(utc_st):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st


def can_summary(user):
    last_use = user.last_use
    last_use = last_use.strftime('%Y%m%d')
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    if today==last_use:
        use = user.use
    else:
        user.use = 0
        use = 0
        db.session.add(user)
        db.session.commit()
    amount = user.uploads // 10 + 10
    if use < amount:
        return True
    else:
        return False


error_status = ErrorStatus()