from flask import Blueprint, request, send_file, Request
from bson import ObjectId
from codecheck.utils.Tools import *
from flask import Blueprint, request
from codecheck.utils.build_response import *
from codecheck.database.Mongo import Mongo
from codecheck.utils.myExceptions import *
from codecheck.utils.file import *
from codecheck.utils.Logger import logger
import datetime

bp = Blueprint('project', __name__, url_prefix='/project')
mongo = Mongo()

@bp.route('/add', methods=['POST'])
def add_project():
    try:
        name = request.json.get('name')
        container_id = request.json.get('container_id')
        checkFrontendArgsIsNotNone(
            [
                {"key":"name","val":name},
                {"key": "container_id", "val": container_id},
            ]
        )
        user = check_user_before_request(request)
        row = mongo.insert_one('Project',{"name":name, "container_id":container_id, "user_id": user['_id'], "status": "stop","create_time": datetime.datetime.now(), "last_start_time": datetime.datetime.now()})
        _id = row.inserted_id
        project = mongo.find_one('Project',{"_id": _id})
        return build_success_response(project)

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')

@bp.route('/del', methods=['POST'])
def del_project():
    try:
        project_id = request.json.get('project_id')
        checkFrontendArgsIsNotNone(
            [
                {"key":"project_id","val":project_id},
            ]
        )
        user = check_user_before_request(request)
        mongo.delete_one('Project',{"_id": ObjectId(project_id), "user_id": user['_id']})
        return build_success_response()

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')

@bp.route('/list', methods=['POST'])
def list_project():
    try:
        user = check_user_before_request(request)
        rows = mongo.find("Project", {"user_id": user['_id']}).sort("create_time", -1)
        return build_success_response(list(rows))

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')

@bp.route('/get', methods=['POST'])
def get_project():
    try:
        project_id = request.json.get('project_id')
        checkFrontendArgsIsNotNone(
            [
                {"key": "project_id", "val": project_id},
            ]
        )
        user = check_user_before_request(request)
        row = mongo.find_one("Project", {"user_id": user['_id'], "_id": ObjectId(project_id)})
        if row is None:
            raise NetworkException(404, f'project {project_id} 不存在')
        return build_success_response(row)

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        logger.logger.error(e)
        return build_error_response(code=500, msg='服务器内部错误')