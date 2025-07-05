from flask import jsonify

def create_response(msg, status="ok", code=200):
    response = {
        "statusCode": code,
        "statusMsg": status,
        "msg": msg
    }
    return jsonify(response)
