# cython: language_level=3
import re
import uuid
import hashlib
import requests
from functools import wraps
from flask_mail import Message
from threading import Thread, Lock
from itsdangerous import URLSafeTimedSerializer
from flask import request, jsonify, current_app as app, render_template, url_for, session

from project import mail

_port_allocation_lock = Lock()
_port_allocated = set()


def hash_file(filename):
    """"

    This function returns the SHA-1 hash
   of and audio file passed into it

   """
    h = hashlib.md5()
    with open(filename, 'rb') as file:
        # loop till the end of the file
        print(file)
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)
    return h.hexdigest()


def authenticate(f):
    """
    authentication wrapper function
    :param f:
    :return: return user id if authentication is successful invalid auth token if not.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify(response_object), 403
        auth_token = auth_header.split(" ")[1]
        resp, exp = User.decode_auth_token(auth_token)
        if isinstance(resp, int):
            response_object['message'] = resp
            return jsonify(response_object), 401
        user = User.query.filter_by(id=resp).first()
        if not user or not user.active:
            return jsonify(response_object), 401
        return f(resp, *args, **kwargs)
    return decorated_function


def is_active(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user.active


def generate_confirmation_token(email):
    """

    Confirmation email token.

    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_SALT'])


def confirm_token(token, expiration=3600):
    """

    Plausibility check of confirmation token.

    """
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_SALT'], max_age=expiration)
    except Exception as ex:
        return False
    return email


def send_email(to, subject, template):
    """

    Send an email.
    ocm.digitalcenter@orange.com

    """
    msg = Message(subject, sender=app.config['MAIL_SENDER'], recipients=[to], html=template,
                  bcc='rfetcheping@caysti.com')
    mail.send(msg)


def send_confirmation_email(to, login_url, password):
    """

    Send a confirmation email to the registered user.

    """
    html = render_template('confirmation.html', login_url=login_url, password=password)
    send_email(to, 'Your supercodeur acciount credentials.', html)
