#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket

from flask import current_app


def k_locate():
    """
    
    Give informations about app's location:
    - hostname
    - service's location
    - logs' location
    
    
    :return: App's informations
    :rtype: :class: `dict`
    
    """
    hostname = socket.gethostname()

    output = {}
    output["hostname"] = hostname
    output["location"] = {}
    output["location"]["service"] = current_app.config["BASE_DIR"]
    output["location"]["logs"] = current_app.config["LOG_DIR"]
    output["type"] = current_app.config["ENV"]
    output["environment"] = {}
    if "DATABASE" in current_app.config:
        for db_key in current_app.config["DATABASE"]:
            output["environment"][db_key] = {}
            output["environment"][db_key]["HOST"] = current_app.config[
                "DATABASE"
            ][db_key]["HOST"]
            output["environment"][db_key]["NAME"] = current_app.config[
                "DATABASE"
            ][db_key]["NAME"]
            output["environment"][db_key]["USER"] = current_app.config[
                "DATABASE"
            ][db_key]["USER"]
    return output


def k_has_doc():
    """
    
    :return: Static file
    :rtype: :class: dict
    
    """
    path = "/opt/unit"
    service = current_app.config["APP_NAME"]
    has_documentation_generated = os.path.exists(
        os.path.join(path, service, "modules", "static", "doc", "html")
    )
    current_app.logger.info(has_documentation_generated)
    if has_documentation_generated:
        output = {}
        output["status"] = {}
        output["status"]["name"] = "success"
        output["status"][
            "message"
        ] = "Documentation found for service {application_name}".format(
            application_name=service
        )
        output["data"] = {}
        output["data"]["has_doc"] = True
        return output
    else:
        output = {}
        output["status"] = {}
        output["status"]["name"] = "success"
        output["status"][
            "message"
        ] = "Documentation not found for service {application_name}".format(
            application_name=service
        )
        output["data"] = {}
        output["data"]["has_doc"] = False
        return output


def k_doc():
    """
    
    :return: Static file
    :rtype: :class: ?
    
    """

    try:
        return current_app.send_static_file("doc/html/index.html")
    except Exception as e:
        current_app.logger.exception(e)


def k_doc_ressources(name, folder2, folder1):
    """
    
    :param name: file searched
    :type name: :class: `str`
    
    :param folder2: folder name 
    :type folder2: :class: `str`
    
    :param folder1: other folder name
    :type folder1: :class: `str`
    
    :return: Static file
    :rtype: :class: ?
    
    """

    try:
        if name == "index.html":
            return current_app.send_static_file("doc/html/" + name)
        else:
            if folder2 is None:
                return current_app.send_static_file("doc/html/_static/" + name)
            elif folder1 is None:
                return current_app.send_static_file(
                    "doc/html/_static/" + folder2 + "/" + name
                )
            else:
                return current_app.send_static_file(
                    "doc/html/_static/" + folder1 + "/" + folder2 + "/" + name
                )
    except Exception as e:
        current_app.logger.exception(e)
    return None
