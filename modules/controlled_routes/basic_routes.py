#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify

import modules.kernel.basic_functions as basic_func

blueprint_basic = Blueprint("blueprint_basic", __name__)


@blueprint_basic.route("/locate", methods=["GET"])
def r_locate():
    """
    Give informations about app's location.
  
    .. :quickref: Location data
  
    **Request exemple**:
    
        .. sourcecode:: http
        
            GET /locate
            Content-Type: application/json

    :Return Data Fields:
    
        .. code-block:: yaml
        
            hostname:          # Server name
            location:
               service:        # Application directory
               logs:           # Logs directory
            type:
            environment:       # If DB exists
                db_key:
                    HOST:
                    NAME:
                    USER:
  
    :Status: 
    
        - 200: Success
        - 500: Error
    
    :Return Type: JSON
    
    :Return Data Structure:
        
        {    
            "environment": {
            "delivery-user_manager": {
              "HOST": "<SERVER_HOST>", 
              "NAME": "<DB_NAME>", 
              "USER": "<DB_USER>"
            }, 
            "hostname": "nginx-unit-dev", 
            "location": {
                "logs": "<LOG_DIRECTORY>", 
                "service": "<APPLICATION_DIRECTORY>"
              }, 
            "status": {
                "name": "success"
            }
        }
                    
    """
    output = basic_func.k_locate()
    return jsonify(output)


@blueprint_basic.route("/has_doc", methods=["GET"])
def r_has_doc():
    """
    Give informations about existence of doc
    
    .. :quickref: Existence of doc
  
    **Request exemple**:
    
        .. sourcecode:: http
        
            GET /has_doc
            Content-Type: application/json
    
    :Status: 
    
        - 200: Success
        - 500: Error
    
    :Return Data Fields:
    
        .. code-block:: yaml
    
            data:
                has_doc:
            status:
                message:
                name:
    
    :Return Type: JSON
    
    :Return Data Structure:
    
        .. code-block:: javascript
        
            {
              "data": {
                "has_doc": true
              }, 
              "status": {
                "message": "Documentation found for service nginx_unit_controller", 
                "name": "success"
              }
            }
    """
    output = basic_func.k_has_doc()
    return jsonify(output)


@blueprint_basic.route("/doc", methods=["GET"])
def r_doc():
    """
    Render the documentation from index.html .
    Only use /doc route

       .. :quickref: Render Documentation
       
    **Request exemple**:
    
        .. sourcecode:: http
        
            GET /doc
            Content-Type: text/html
            
    :Status: 
    
        - 200: Success
        - 500: Error
        - 404: Not found
    
    :Return Type: Web page
    
    """
    return basic_func.k_doc()


@blueprint_basic.route("/index.html", methods=["GET"])
@blueprint_basic.route("/_static/<string:name>", methods=["GET"])
@blueprint_basic.route(
    "/_static/<string:folder2>/<string:name>", methods=["GET"]
)
@blueprint_basic.route(
    "/_static/<string:folder1>/<string:folder2>/<string:name>", methods=["GET"]
)
def r_doc_ressources(name, folder2=None, folder1=None):
    """
    Render the ressources for documentation.
    Never use this route directly (use /doc)
    
    **Request exemple**:
    
        .. sourcecode:: http
        
            GET /<path_to_ressource>
            Content-Type: text/html
        
    :param name: file searched
    :type name: :class: `str`
    
    :param folder2: folder name 
    :type folder2: :class: `str`
    
    :param folder1: other folder name
    :type folder1: :class: `str`    
    
    :Status: 
    
        - 200: Success
        - 500: Error
        - 404: Not found
            
    :Return Type: Web page
            
    """

    return basic_func.k_doc_ressources(name, folder2, folder1)
