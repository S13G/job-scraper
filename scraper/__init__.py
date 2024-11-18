from flask import Flask


def create_app():
    app = Flask(__name__)  # noqa
    app.config.from_object("scraper.config.Config")
    return app


app = create_app()
