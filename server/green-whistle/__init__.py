from flask import Flask, request


def create_app():
    # create and configure the app
    app = Flask(__name__)

    @app.route('/hello')
    def hello():
        return 'Hello.'

    return app
