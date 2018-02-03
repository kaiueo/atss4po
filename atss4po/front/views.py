# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from atss4po.extensions import login_manager
from atss4po.public.forms import LoginForm
from atss4po.user.models import User
from atss4po.utils import flash_errors


blueprint = Blueprint('summary', __name__, url_prefix='/summary', static_folder='../static')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """Home page."""
    if request.method=='POST':
        print(request.data)
    return render_template('summary/summary.html')

@blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('summary/uploads.html')


