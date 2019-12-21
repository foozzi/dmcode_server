from flask import Blueprint, request, session
from dmcode_server import db

bp = Blueprint('rooms', __name__, url_prefix='/room')


def _check_auth(room_name):
    if not session.get('room_{}'.format(room_name)):
        return False
    return True

@bp.route('/join/<hash_paste>/<hash_file>')
def join_edit_room(hash_paste, hash_file):
    return True
