import os
from flask import Blueprint, request, render_template, abort, Response
from dmcode_server import db
from dmcode_server.files.models import Files, Pastes
from dmcode_server.rooms.views import _check_auth
from time import time
from datetime import datetime
from flask import current_app as app
from pygments import highlight
from pygments.formatters import HtmlFormatter
import pygments.lexers

bp = Blueprint('frontend', __name__, url_prefix='/',
               template_folder='templates')


def _get_paste(id):
    paste = Pastes.query.get_or_404(id)
    if not paste or not paste.files:
        abort(404)
    return paste

def _get_paste_by_hash(hash):
    paste = Pastes.query.filter_by(hash=hash).first()
    if not paste or not paste.files:
        abort(404)
    return paste

def _get_file_by_hash(hash):
    file = Files.query.filter_by(hash=hash).first()
    if not file:
        abort(404)
    return file

def _get_file(id):
    file = Files.query.get_or_404(id)
    if not file:
        abort(404)
    return file

@app.template_filter('highlighter')
def _jinja2_filter_highlighter(filename, code):
    lexer = pygments.lexers.get_lexer_for_filename(filename)
    return highlight(code, lexer, HtmlFormatter(linenos=True))

@app.template_filter('check_room_sess')
def _jinja2_filter_check_room_sess():
    return _check_auth() 

@app.template_filter('len')
def _jinja2_filter_len(arr):
    return len(arr)


@app.template_filter('strftime')
def _jinja2_filter_datetime(unixtime, fmt="%Y-%m-%d %H:%M:%s"):
    return datetime.utcfromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')


@bp.route('/', methods=['GET'])
def lanfing():
    return render_template('landing.html')


@bp.route("all", methods=['GET'])
def all_public():
    pastes = Pastes.query.order_by(Pastes.updatetime.desc()).all()
    return render_template('public.html', pastes=pastes)


@bp.route("paste/<hash>", methods=['GET'])
def one_paste(hash):
    paste = _get_paste_by_hash(hash)
    files = {}
    for file in paste.files:
        if file.filepath not in files:
            files[file.filepath] = []
        files[file.filepath].append(file)
    return render_template('files.html', dirs=files, paste_name=paste.name)


@bp.route('fetch_file_info', methods=['POST'])
def fetch_file_info():
    if 'hash' not in request.values:
        return {'error': True}

    file = Files.query.filter_by(hash=request.values['hash']).first()

    if not file:
        return {'error': True, 'message': 'File not found'}

    return {'error': False, 'file': {
        'id': file.hash,
        'filesize': file.filesize,
        'fileext': file.fileext,
        'filehash': file.filehash,
        'createtime': file.createtime,
        'updatetime': file.updatetime,
        'fileview': file.fileview}}


@bp.route('file/<hash>', methods=['GET'])
def file(hash):
    file = _get_file_by_hash(hash)
    file.fileview += 1
    db.session.add(file)
    db.session.commit()
    return render_template('file.html', file=file)


@bp.route('file/dl/<hash>', methods=['GET'])
def dl(hash):
    file = _get_file_by_hash(hash)
    headers = {
        "Content-Disposition": "attachment;filename={}".format(file.filename)}
    return Response(file.filecontent, mimetype="txt/plain", headers=headers)


@bp.route('file/raw/<hash>', methods=['GET'])
def raw(hash):
    return render_template('raw_file.html', file=_get_file_by_hash(hash))


@bp.route('file/edit/<hash>', methods=['GET'])
def edit(hash):
    return render_template('edit.html', file=_get_file_by_hash(hash))
