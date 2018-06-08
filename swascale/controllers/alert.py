from flask import Blueprint, request, Response
import json
from config import cfg

alert = Blueprint('alert', 'alert')


@alert.route('', methods=['POST'])
def index():
    return 'ok'
