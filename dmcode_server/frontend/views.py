import sys
import os
from flask import Blueprint, redirect, request, url_for, render_template, \
    abort, jsonify, send_file
from dmcode_server import db
from dmcode_server.files.models import Files, Pastes
from werkzeug import secure_filename, exceptions
from time import time
from datetime import datetime
from flask import current_app as app

bp = Blueprint('frontend', __name__, url_prefix='/',
               template_folder='templates')


@app.template_filter('strftime')
def _jinja2_filter_datetime(unixtime, fmt="%Y-%m-%d %H:%M:%s"):
    return datetime.utcfromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')


@bp.route("all_public", methods=['GET'])
def all_public():
    pastes = Pastes.query.order_by(Pastes.updatetime.desc()).all()
    return render_template('public.html', pastes=pastes)


def _get_paste(id):
    paste = Pastes.query.get_or_404(id)
    if not paste or not paste.files:
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
    files = {}
    for file in paste.files:
        if file.filepath not in files:
            files[file.filepath] = []
        files[file.filepath].append(file)
    return render_template('files.html', dirs=files, paste_name=paste.name)


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


@bp.route('dl/<id>', methods=['GET'])
def dl(id):
    from random import seed
    from random import random
    seed(1)
    file = _get_file(id)
    randname = random()
    tmp_dir = os.path.join(app.config['TMP_STORAGE'], 'dl_{}_{}_{}'.format(
        int(time()), file.filehash, randname))
    os.makedirs(tmp_dir, exist_ok=False)

    dl_file = os.path.join(tmp_dir, str(randname) + file.fileext)
    with open(dl_file, 'w') as f:
        f.write(file.filecontent)

    return send_file(dl_file, as_attachment=True)
