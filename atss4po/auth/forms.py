# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email
from ..user.models import User


class LoginForm(Form):
    """Login form."""

    username = StringField('账号', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登录')

class PasswordForm(Form):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    new_password = PasswordField('新密码', validators=[DataRequired()])
    confirm_password = PasswordField('确认密码', validators=[DataRequired(), EqualTo('new_password', message='两次密码不同')])
    submit = SubmitField('修改')

class RegisterForm(Form):
    """Register form."""

    username = StringField('用户名',
                           validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('邮箱',
                        validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('密码',
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('确认密码',
                            [DataRequired(), EqualTo('password', message='两次密码不一致')])
    biography = TextAreaField('个人简介', default="这家伙很懒，没有介绍")
    submit = SubmitField('注册')

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('用户名已被使用')
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('邮箱已被注册')
            return False
        return True
