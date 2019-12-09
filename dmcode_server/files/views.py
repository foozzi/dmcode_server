from flask import Blueprint, request
from dmcode_server import db
from dmcode_server.files.models import Files, Pastes
from werkzeug import secure_filename, exceptions
import uuid
import pickle
import os
import shutil
import hashlib
from time import time
from flask import current_app as app

bp = Blueprint('files', __name__, url_prefix='/files')

expire_types = {'10min': 600, '1hour': 3600,
                '1day': 86400, '1week': 604800, '1month': 2629746}


@bp.route("fetch_token", methods=['POST'])
def fetch_token():
    """check if not set project name for uploading files"""
    name_paste = request.values.get('name_paste').strip()
    expire_paste = request.values.get('expire_paste').strip()

    if name_paste is None or name_paste.strip() == "":
        return {'error': True, 'message': 'name project is not set'}
    elif expire_paste is None or expire_paste.strip() == "":
        """default expire time in sec"""
        expire_paste = expire_types['1month']
    elif expire_paste:
        if expire_paste not in expire_types:
            return {'error': True, 'message': 'error format expire paste `{}`'.format(expire_paste)}

    paste = Pastes.query.filter_by(name=name_paste).first()
    if paste:
        return {'error': False, 'id': paste.id, 'token': paste.token}

    paste = Pastes()
    paste.name = name_paste
    paste.token = str(uuid.uuid4())
    paste.expiretime = expire_types[expire_paste]
    paste.createtime = int(time())
    paste.updatetime = int(time())
    db.session.add(paste)
    db.session.commit()

    return {'error': False, 'id': paste.id, 'token': paste.token}


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
    paste = Pastes.query.filter_by(token=token).first()
    if not paste:
        return {'error': True, 'message': 'token is not found in db'}

    with open(os.path.join(tmp_dir, pkg_filename), 'rb') as f:
        data_load = pickle.load(f)
        for dl in data_load:
            if dl['content'] is not bytes:
                fn, fileext = os.path.splitext(dl['name'])
                """first check if file hash exists in db and update if need"""
                filehash = hashlib.md5(dl['content']).hexdigest()
                """check file and update if need"""
                skip = False
                db_paste = Pastes.query.filter_by(token=token).first()
                if db_paste:
                    for db_file in db_paste.files:
                        if db_file.filename == dl['name'] \
                                and db_file.filepath == dl['path']:
                            if db_file.filehash != filehash:
                                db_file.filecontent = dl['content'].decode(
                                    'utf-8')
                                db_file.updatetime = int(time())
                                db_paste.append(db_file)
                            skip = True
                    """update paste"""
                    db_paste.updatetime = int(time())
                    db.session.add(db_paste)
                    db.session.commit()

                """skip insert updated file"""
                if skip:
                    continue
                files = Files(
                    filename=dl['name'],
                    filepath=dl['path'],
                    filesize=len(dl['content']),
                    fileext=fileext,
                    filecontent=dl['content'].decode('utf-8'),
                    filehash=filehash,
                    createtime=int(time()),
                    updatetime=int(time())
                )

                paste.files.append(files)
                paste.updatetime = int(time())

                db.session.add(paste)
                db.session.commit()

    shutil.rmtree(tmp_dir)

    return {'error': False, 'link': request.host_url + 'paste/{}'.format(paste.id)}
