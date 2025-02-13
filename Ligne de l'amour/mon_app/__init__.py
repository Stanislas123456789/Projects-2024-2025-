from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ma_super_cle_secrete'

    from .routes import main
    app.register_blueprint(main)

    return app
