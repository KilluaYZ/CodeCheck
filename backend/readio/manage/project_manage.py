"""
项目管理
"""
from flask import Blueprint, request, send_file
import readio.database.connectPool
from typing import BinaryIO
from readio.database.SQLUtils import *
from readio.utils.buildResponse import *
from readio.utils.auth import *
import readio.utils.check as check
bp = Blueprint('projectManage', __name__, url_prefix='/project')
pooldb = readio.database.connectPool.pooldb

@bp.route('/get/list', methods=['GET'])
def get_project_list():
    pass

@bp.route('/get/list/public', methods=['GET'])
def get_project_list_public():
    pass

@bp.route('/get/profile', methods=['GET'])
def get_project_profile():
    pass

@bp.route('/add', methods=['POST'])
def add_project():
    pass

@bp.route('/del', methods=['GET'])
def add_project():
    pass