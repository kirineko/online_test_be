from flask import jsonify
from . import main


@main.app_errorhandler(403)
def forbidden(e):
    response = jsonify({
        'code': -1,
        'msg': 'forbidden'
    })
    response.status_code = 403
    return response


@main.app_errorhandler(404)
def page_not_found(e):
    response = jsonify({
        'code': -1,
        'msg': 'url error'
    })
    response.status_code = 404
    return response


@main.app_errorhandler(500)
def internal_server_error(e):
    response = jsonify({
        'code': -1,
        'msg': 'internal server error'
    })
    response.status_code = 500
    return response
