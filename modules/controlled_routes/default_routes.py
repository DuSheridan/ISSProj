#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify

import modules.kernel.default_functions as default_func

blueprint_default = Blueprint("blueprint_default", __name__)


@blueprint_default.route("/hello", methods=["GET"])
def r_hello():
    """This is an example route that you could remove.
    This route says "Hello World!"

    :return: Hello world!
    :rtype: :class:`flask.Response`
    """
    output = default_func.k_hello()
    return jsonify(output)
