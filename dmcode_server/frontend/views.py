import sys
from flask import Blueprint, redirect, request, url_for, render_template, abort
from dmcode_server import db
from dmcode_server.files.models import Files, Pastes
from werkzeug import secure_filename, exceptions
from time import time
from flask import current_app as app

bp = Blueprint('frontend', __name__, url_prefix='/', template_folder='templates')

@bp.route("all_public", methods=['GET'])
def all_public():
   pastes = Pastes.query.order_by(Pastes.updatetime.desc()).all()
   return render_template('public.html', pastes=pastes)

def _get_paste(id):
    paste = Pastes.query.get_or_404(id)
    if not paste:
        abort(404)
    return paste

@bp.route("paste/<id>")
def one_paste(id):
    paste = _get_paste(id)
    return render_template('files.html', paste=paste)

