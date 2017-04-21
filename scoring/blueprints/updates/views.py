import json
from flask import (
    jsonify,
    Blueprint,
    redirect,
    request,
    flash,
    url_for,
    render_template)


updates = Blueprint('update', __name__, template_folder='templates')


@updates.route('/ping', methods=['GET'])
def ping():
    return jsonify({'msg': "Hello World"})
