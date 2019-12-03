import sys
from flask import Blueprint, redirect, request, url_for
from dmcode_server import db
from dmcode_server.files.models import Files, Apps
from werkzeug import secure_filename, exceptions
import uuid
import pickle
import os
import shutil
import hashlib
from time import time
from flask import current_app as app

bp = Blueprint('files', __name__, url_prefix='/files')


@bp.route("fetch_token", methods=['POST'])
def fetch_token():
    """check if not set project name for uploading files"""
    name_paste = request.values.get('name_paste').strip()
    if name_paste is None or name_paste.split() == "":
        return {'error': True, 'message': 'name project is not set'}

    app = Apps.query.filter_by(name=name_paste).first()
    if app:
        return {'error': False, 'id': app.id, 'token': app.token}

    app = Apps()
    app.name = name_paste
    app.token = str(uuid.uuid4())
    app.createtime = int(time())
    db.session.add(app)
    db.session.commit()

    return {'error': False, 'id': app.id, 'token': app.token}


@bp.route("paste_files", methods=["POST"])
def deploy():
    if 'DMTOKEN' not in request.headers:
        return {'error': True, 'message': 'upload token is required'}
    try:
        pkg = request.files['dmfiles']
    except exceptions.BadRequestKeyError:
        return {'error': True, 'message': 'package is empty'}

    token = request.headers['DMTOKEN']
    pkg.filename = "package.pickle"
    tmp_dir = os.path.join(
        app.config['TMP_STORAGE'], '{}_{}'.format(token, int(time())))
    os.makedirs(tmp_dir, exist_ok=True)
    """security reason"""
    pkg_filename = secure_filename(pkg.filename)
    pkg.save(os.path.join(tmp_dir, pkg_filename))

    """get app paste for files"""
    apps = Apps.query.filter_by(token=token).first()
    if not apps:
        return {'error': True, 'message': 'token is not found in db'}

    with open(os.path.join(tmp_dir, pkg_filename), 'rb') as f:
        data_load = pickle.load(f)
        for dl in data_load:
            if dl['content'] is not bytes:
                fn, fileext = os.path.splitext(dl['name'])
                """first check if file hash exists in db and update if need"""
                filehash = hashlib.md5(dl['content']).hexdigest()
                files = Files(
                    filename=dl['name'],
                    filesize=len(dl['content']),
                    fileext=fileext,
                    filecontent=dl['content'],
                    filehash=filehash,
                    createtime=int(time()),
                    app_id=apps.id
                )

                db.session.add(files)
                db.session.commit()

    shutil.rmtree(tmp_dir)

    return {'error': False, 'result': True}
