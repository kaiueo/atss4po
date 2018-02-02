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

def encrypt(id):
    bytes_id = str(id).encode(encoding='utf-8')
    return base64.encodebytes(bytes_id).decode('utf-8')

def decrypt(str_id):
    bytes_id = str_id.encode(encoding='utf-8')
    return int(base64.decodebytes(bytes_id).decode('utf-8'))

error_status = ErrorStatus()