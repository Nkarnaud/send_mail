import os

from flask import Flask
from flask_cors import CORS
from flask_mail import Mail


# instantiate the extensions
mail = Mail()
UPLOAD_FOLDER = '/usr/src/app/project/audio_files/'
ALLOWED_EXTENSIONS = {'csv'}
MAIL_SENDER = 'mycaysti.supercodeurs@gmail.com'


# App initialisation
def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)
    # enable CORS
    CORS(app)
    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.config['MAIL_SENDER'] = MAIL_SENDER

    # setting the smtp server
    app.config.update(dict(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True,
        MAIL_USERNAME='softwaresmart20@gmail.com',
        MAIL_PASSWORD='codeur.caysti12'
    ))

    # set up extensions
    mail.init_app(app)

    # register endpoints
    from project.api.users import user_blueprint
    app.register_blueprint(user_blueprint)

    # shell context for flask cli
    app.shell_context_processor({'app': app})
    return app
