import os

from datetime import datetime, timedelta
from flask import jsonify, request, Blueprint, current_app
from werkzeug.utils import secure_filename

from project.api.utils.utils import authenticate, confirm_token, send_confirmation_email

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/ping')
def test_connection():
    response_object = {
        'status': 'success',
        'message': 'Server is up and working'
    }
    return jsonify(response_object), 201


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@user_blueprint.route('/caysti/mailsender', methods=['POST'])
def load_email_and_send():
    """

    Upload one audio file and a test audion file in to the database
    :param resp: authenticated user id
    :return:

    """
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if 'file' not in request.files:
        return jsonify(response_object), 400
    file = request.files['file']
    if not file:
        response_object['message'] = 'No file selected.'
        return jsonify(response_object), 405
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        csv_file = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        with open(csv_file, 'r') as f:
            data = f.readlines()
        for line in data:
            elt = line.split(';')
            login_url = elt[0]
            password = elt[1]
            email = elt[2]
            send_confirmation_email(email, login_url, password)
        response_object['message'] = "Emails were send success fully."
        response_object['success'] = 'success.'
        return jsonify(response_object), 200
    else:
        response_object['message'] = 'Wrong file format.'
        return jsonify(response_object), 400

