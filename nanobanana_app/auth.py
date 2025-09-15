from flask import Blueprint, redirect, url_for, flash
from flask_login import login_user, logout_user
from authlib.integrations.flask_client import OAuth
from . import db, login_manager
from .models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

oauth = OAuth()

def init_app(app):
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=app.config.get('GOOGLE_CLIENT_ID'),
        client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
        access_token_url='https://oauth2.googleapis.com/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={'scope': 'openid email profile'},
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
    )

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@bp.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('auth.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@bp.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    userinfo = token.get('userinfo')

    user = User.query.filter_by(email=userinfo['email']).first()
    if not user:
        user = User(
            id=userinfo['sub'],
            email=userinfo['email'],
            name=userinfo['name'],
            profile_pic=userinfo['picture']
        )
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('routes.index'))

@bp.route('/logout')
def logout():
    logout_user()
    flash('您已退出登录。')
    return redirect(url_for('routes.index'))