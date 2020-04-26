#!/usr/bin/env python
# -*- coding: utf-8 -*-

# DON'T CHANGE THIS FILE WITHOUT CHECKING THE DOCUMENTATION
# http://flask.pocoo.org/docs/1.0/api/#configuration
import os


class Config(object):
    """Base configuration."""

    # If you want to set an maximum for uploaded file from the client,
    # uncomment and set the max size (bytes) :
    # MAX_CONTENT_LENGHT = 1024 * 1024

    # If you want to enable UTF-8 in json, uncomment :
    # JSON_AS_ASCII = False

    DB_CONNECTOR_TPL = """host=%(HOST)s dbname=%(NAME)s
                    user=%(USER)s password=%(PASSWORD)s"""
    DATABASE = {}
    BASE_DIR = "/opt/unit/"
    LOG_DIR = "/var/log/unit/services/"


class ProdConfig(Config):
    """Production configuration."""

    ENV = "production"
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""

    ENV = "development"

    # DEBUG mode : an interactive debugger will be shown for unhandled
    # exceptions, and the server will be reloaded when code changes.
    # VERY USEFUL.
    DEBUG = True

    DATABASE = {}
    DATABASE["db_test"] = {
        "HOST": "localhost",
        "USER": "postgres",
        "PASSWORD": "test1234",
        "NAME": "postgres",
        "PORT": 5432,
    }


class StagingConfig(Config):
    """Staging configuration."""

    ENV = "staging"
    DEBUG = True

    # TESTING mode : Enable the test mode of Flask extensions (later).
    TESTING = True

    DATABASE = {}
    DATABASE["db_test"] = {
        "HOST": "localhost",
        "USER": "postgres",
        "PASSWORD": "test1234",
        "NAME": "postgres",
        "PORT": 5432,
    }

    # If you need to set another database
    # Notice that, database should be different or you may have problem in
    # running test.

    # DATABASE["db_test_2"] = {
    # "HOST": "localhost",
    # "USER": "postgres",
    # "PASSWORD": "test1234",
    # "NAME": "postgres",
    # "PORT": 5432
    # }


class LocalConfig(Config):
    """Used to run flask locally"""
    ENV = "local"
    DEBUG = True
    BASE_DIR = os.path.dirname(os.getcwd())
    LOG_DIR = None
