from flask import current_app, Flask, request
from flask_socketio import join_room, leave_room, SocketIO, disconnect, emit
import random
import string
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('dmcode-socketio')

