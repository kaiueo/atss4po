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
from .utils import error_status, can_summary, utc2local
from ..user import identicon
import datetime as dt
from atss4po.database import db
import traceback

blueprint = Blueprint('api_v1_summary', __name__, url_prefix='/api/v1/summary',static_folder='../static')



@blueprint.route('/', methods=['POST'])
@csrf_protect.exempt
@auth.login_required
def get_summary():
    if can_summary(g.current_user):
        try:
            remote = request.json
            print(remote)
            type = remote['type']
            print('ccc')
            if type==0:
                text = remote['text']
                count = remote['count']
                article, summary = autosum.summary_from_text(text, count)
            elif type==1:
                url = remote['url']
                count = remote['count']
                article, summary = autosum.summary_from_url(url, count)
            g.current_user.use = g.current_user.use + 1
            g.current_user.last_use = utc2local(dt.datetime.utcnow())
            db.session.add(g.current_user)
            db.session.commit()
            result = {}
            result['code'] = error_status.success.code
            result['msg'] = error_status.success.msg
            result['data'] = {'article':article, 'summary': summary}
        except(KeyError):
            result = {}
            result['code'] = error_status.format_error.code
            result['msg'] = error_status.format_error.msg
            result['data'] = []
        except:
            traceback.print_exc()
            result = {}
            result['code'] = error_status.unknown_error.code
            result['msg'] = error_status.unknown_error.msg
            result['data'] = []
        return jsonify(result)
    else:
        result = {}
        result['code'] = error_status.no_amount.code
        result['msg'] = error_status.no_amount.msg
        result['data'] = []
        return jsonify(result)

#
# @blueprint.route('/url', methods=['POST'])
# @csrf_protect.exempt
# @auth.login_required
# def from_url():
#     try:
#         remote = request.json
#         url = remote['url']
#         count = remote['count']
#         summary = autosum.summary_from_url(url, count)
#         result = {}
#         result['code'] = error_status.success.code
#         result['msg'] = error_status.success.msg
#         result['data'] = summary
#     except(KeyError):
#         result = {}
#         result['code'] = error_status.format_error.code
#         result['msg'] = error_status.format_error.msg
#         result['data'] = []
#     except:
#         result = {}
#         result['code'] = error_status.unknown_error.code
#         result['msg'] = error_status.unknown_error.msg
#         result['data'] = []
#     return jsonify(result)

@blueprint.route('/weibos', methods=['POST'])
@csrf_protect.exempt
@auth.login_required
def from_weibos():
    try:
        remote = request.json
        weibos = remote['weibos']
        count = remote['count']
        summary = autosum.summary_from_weibos(weibos, count)
        result = {}
        result['code'] = error_status.success.code
        result['msg'] = error_status.success.msg
        result['data'] = summary
    except(KeyError):
        result = {}
        result['code'] = error_status.format_error.code
        result['msg'] = error_status.format_error.msg
        result['data'] = []
    except:
        result = {}
        result['code'] = error_status.unknown_error.code
        result['msg'] = error_status.unknown_error.msg
        result['data'] = []
    return jsonify(result)

@blueprint.route('/test')
@csrf_protect.exempt
@auth.login_required
def test():
    print(can_summary(g.current_user))
    return jsonify({"aaa":"bbb"})




