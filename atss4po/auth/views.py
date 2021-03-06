# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for, session, make_response
from flask_login import login_required, login_user, logout_user, current_user

from atss4po.extensions import login_manager
from atss4po.auth.forms import LoginForm
from atss4po.auth.forms import RegisterForm
from atss4po.user.models import User
from atss4po.utils import flash_errors
from .utils import get_basic_auth_token


blueprint = Blueprint('auth', __name__, url_prefix='/auth',static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))



@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('您已经登出', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(username=form.username.data, email=form.email.data, password=form.password.data, biography=form.biography.data, active=True)
        flash('注册成功', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('auth/register.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)

@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None and user.check_password(form.password.data):
                login_user(user)
                token = user.generate_auth_token(expiration=3600)
                encrypt_token = get_basic_auth_token(token)
                redirect_url = url_for('public.home')
                response = redirect(redirect_url)
                response.set_cookie('token', encrypt_token)
                flash('您已成功登陆', 'success')
                return response
            else:
                flash('请输入正确的账号和密码', 'danger')
    return render_template('auth/login.html', form=form)

@blueprint.route('/detail/')
@login_required
def detail():
    return render_template('users/user.html', user=current_user)

