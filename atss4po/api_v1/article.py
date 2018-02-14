# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user, AnonymousUserMixin

from atss4po.extensions import login_manager
from atss4po.auth.forms import LoginForm
from atss4po.auth.forms import RegisterForm
from atss4po.user.models import Article, SummarizedArticle
from atss4po.utils import flash_errors
from flask import jsonify, g, current_app
from ..extensions import csrf_protect, auth
from ..summary import autosum
import random
from .utils import error_status, encrypt, decrypt
from atss4po.database import db
import traceback

blueprint = Blueprint('api_v1_article', __name__, url_prefix='/api/v1/article',static_folder='../static')


@blueprint.route('/get')
@csrf_protect.exempt
@auth.login_required
def get_article():
    unsummarized_articles = Article.query.filter_by(summarized=False).limit(100).all()
    if len(unsummarized_articles):
        article = random.sample(unsummarized_articles, 1).pop()
        result = {}
        result['code'] = error_status.success.code
        result['msg'] = error_status.success.msg
        result['data'] = {'id': encrypt(article.id), 'text': autosum.read_article(article.filepath)}
        return jsonify(result)
    else:
        result = {}
        result['code'] = error_status.no_article.code
        result['msg'] = error_status.no_article.msg
        result['data'] = {}
    return jsonify(result)


@blueprint.route('/upload', methods=['POST'])
@csrf_protect.exempt
@auth.login_required
def upload_summary():
    try:
        article_id = decrypt(request.json['id'])
        text = request.json['text']
        summarization = request.json['summarization']
        summarized_article = SummarizedArticle(text, summarization)
        article = Article.query.filter_by(id=article_id).first()
        article.summarized = True
        g.current_user.uploads = g.current_user.uploads + 1
        db.session.add(g.current_user)
        db.session.add(article)
        db.session.add(summarized_article)
        db.session.commit()
        result = {}
        result['code'] = error_status.success.code
        result['msg'] = error_status.success.msg
        result['data'] = []
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
