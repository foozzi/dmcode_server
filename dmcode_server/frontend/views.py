import sys
from flask import Blueprint, redirect, request, url_for, render_template, abort, jsonify
from dmcode_server import db
from dmcode_server.files.models import Files, Pastes
from werkzeug import secure_filename, exceptions
from time import time
from flask import current_app as app

bp = Blueprint('frontend', __name__, url_prefix='/',
               template_folder='templates')


@bp.route("all_public", methods=['GET'])
def all_public():
    pastes = Pastes.query.order_by(Pastes.updatetime.desc()).all()
    return render_template('public.html', pastes=pastes)


def _get_paste(id):
    paste = Pastes.query.get_or_404(id)
    if not paste:
        abort(404)
    return paste

def _get_file(id):
    file = Files.query.get_or_404(id)
    if not file:
        abort(404)
    return file

@bp.route("paste/<id>", methods=['GET'])
def one_paste(id):
    paste = _get_paste(id)
    return render_template('files.html', paste=paste)


@bp.route('fetch_file_info', methods=['POST'])
def fetch_file_info():
    if 'id' not in request.values:
        return {'error': True}

    file = Files.query.filter_by(id=request.values['id']).first()

    return {'error': False, 'file': {
        'id': file.id,
        'filesize': file.filesize,
        'fileext': file.fileext,
        'filehash': file.filehash,
        'createtime': file.createtime,
        'updatetime': file.updatetime,
        'fileview': file.fileview}}

@bp.route('file/<id>', methods=['GET'])
def file(id):
    return render_template('file.html', file=_get_file(id))
