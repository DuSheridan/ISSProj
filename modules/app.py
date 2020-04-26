#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib
import logging

from flask import Flask, Blueprint, jsonify
from os import chdir, getcwd, listdir
from os.path import isfile, join, splitext
from modules.lib import db
from modules.exceptions.api_error_exception import ApiErrorException


ALIAS = {
    "PROD": "modules.flask_settings.ProdConfig",
    "DEV": "modules.flask_settings.DevConfig",
    "STAGING": "modules.flask_settings.StagingConfig",
    "LOCAL": "modules.flask_settings.LocalConfig",
}


def create_app(application_name, env):

    app = Flask(__name__)
    app.config.from_object(ALIAS[env])

    # Update configuration with the name of the application
    app.config["APP_NAME"] = application_name
    app.config["BASE_DIR"] = join(app.config["BASE_DIR"], application_name)
    db.init_app(app)

    # Logger configured here
    if app.config.get("LOG_DIR"):
        logging.basicConfig(
            filename="{}/{}.log".format(app.config.get("LOG_DIR"), application_name),
            format="%(asctime)s [%(threadName)-10s] - %(levelname)s - "
                   "%(module)s.%(funcName)s(%(lineno)d): %(message)s",
            level=logging.DEBUG if app.config.get("DEBUG") else logging.INFO
        )
    else:
        logging.basicConfig(
            format="%(asctime)s [%(threadName)-10s] - %(levelname)s - "
                   "%(module)s.%(funcName)s(%(lineno)d): %(message)s",
            level=logging.DEBUG if app.config.get("DEBUG") else logging.INFO
        )
    #
    # logger_flask_app = logging.getLogger("flask_app")
    # app.logger.addHandler(logger_flask_app)
    
    # No-cache configured here after each request
    @app.after_request
    def no_cache(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
    
    # Custom exception handler ApiErrorException
    @app.errorhandler(ApiErrorException)
    def handle_exception(error):
        output = jsonify(error.to_dict())
        # Real http status code
        output.status_code = error.status_code
        return output

    import sys
    app.logger.info(sys.version_info)
    
    auto_register_blueprint_from_directory(app, "modules/controlled_routes")
    return app


def auto_register_blueprint_from_directory(app, path):
    previous_directory = getcwd()
    chdir(app.config["BASE_DIR"])
    files = [
        splitext(f)[0]
        for f in listdir(path)
        if isfile(join(path, f)) and f.lower().endswith(".py")
    ]
    path = path.replace("/", ".")
    path = path.replace("\\", ".")
    for file in files:
        module = importlib.import_module(path + "." + file)
        for item in dir(module):
            blueprint = getattr(module, item)
            if isinstance(blueprint, Blueprint):
                app.register_blueprint(blueprint)
    chdir(previous_directory)


if __name__ == "__main__":  # code to execute if called from command-line
    pass  # do nothing
