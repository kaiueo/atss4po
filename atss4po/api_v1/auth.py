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
from .utils import utc2local, error_status

blueprint = Blueprint('api_v1_auth', __name__, url_prefix='/api/v1/auth',static_folder='../static')

@auth.verify_password
def verify_password(username_or_token, password):
    print(username_or_token)
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.check_password(password):
            return False
    g.current_user = user
    return True

@blueprint.route('/token')
@auth.login_required
def get_auth_token():
    token = g.current_user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

@blueprint.route('/detail')
@csrf_protect.exempt
@auth.login_required
def get_detail():
    try:
        username = g.current_user.username
        created_at = utc2local(g.current_user.created_at).strftime('%Y-%m-%d %H:%M:%S')
        uploads = g.current_user.uploads
        avatar = url_for('static', filename=g.current_user.avatar)
        use = g.current_user.get_today_use()
        biography = g.current_user.biography
        data = {"username": username,
                        "created_at": created_at,
                        "uploads": uploads,
                        "avatar": avatar,
                        "use": use,
                "biography": biography}
        result = {}
        result["code"] = error_status.success.code
        result["msg"] = error_status.success.msg
        result["data"] = data
        return jsonify(result)
    except:
        result = {}
        result["code"] = error_status.unknown_error.code
        result["msg"] = error_status.unknown_error.msg
        result["data"] = []
        return jsonify(result)






