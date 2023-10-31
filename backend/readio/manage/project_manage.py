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
from readio.database.sqls.project_sqls import *
from readio.database.sqls.task_sqls import *
from readio.analyser.analyser import CodeAnalyzer
bp = Blueprint('projectManage', __name__, url_prefix='/project')
pooldb = readio.database.connectPool.pooldb


@bp.route('/get/list', methods=['GET'])
def get_project_list():
    try:
        user = check_user_before_request(request)
        userId = user['id']
        rows = project_sqls_query_project_sql({"userId":userId})
        build_success_response(data=rows)

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')


@bp.route('/get/list/public', methods=['GET'])
def get_project_list_public():
    try:
        rows = project_sqls_query_project_sql({"isPublic": True})
        build_success_response(data=rows)

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')

@bp.route('/get/profile', methods=['GET'])
def get_project_profile():
    pass

@bp.route('/add', methods=['POST'])
def add_project():
    try:
        project_name = request.json.get('projectName')
        is_public = request.json.get('isPublic')

        check.checkFrontendArgsIsNotNone([
            {"key": "projectName", "val": project_name},
            {"key": "isPublic", "val": is_public},
        ])
        user = check_user_before_request(request)
        userId = user['id']
        project_id = project_sqls_insert(project_name, is_public, userId)
        return build_success_response(data={"projectId":project_id})

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')

@bp.route('/del', methods=['GET'])
def del_project():
    try:
        project_id = request.args.get("projectId")

        check.checkFrontendArgsIsNotNone([
            {"key": "projectId", "val": project_id},
        ])
        user = check_user_before_request(request)
        userId = user['id']
        if not project_sqls_check_if_project_belong_to_user_id(project_id, userId):
            raise NetworkException(403, '您没有权限执行该操作')

        project_sqls_

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')


@bp.route('/submit', methods=['POST'])
def submit_project():
    try:
        projectId = request.json.get('projectId')
        check.checkFrontendArgsIsNotNone([
            {"key": "projectId", "val": projectId},
        ])
        user = check_user_before_request(request)
        userId = user['id']
        if not project_sqls_check_if_project_belong_to_user_id(projectId, userId):
            raise NetworkException(403, '您没有权限执行该操作')

        CodeAnalyzer.submit(projectId)

        return build_success_response()

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')
