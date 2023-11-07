"""
项目管理
"""
from flask import Blueprint, request, send_file
import codecheck.database.connectPool
from typing import BinaryIO
from codecheck.database.SQLUtils import *
from codecheck.utils.buildResponse import *
from codecheck.utils.auth import *
import codecheck.utils.check as check
from codecheck.database.sqls.project_sqls import *
from codecheck.database.sqls.task_sqls import *
from codecheck.database.sqls.problem_sqls import *
from codecheck.analyser.analyser import CodeAnalyzer
bp = Blueprint('projectManage', __name__, url_prefix='/project')
pooldb = codecheck.database.connectPool.pooldb


@bp.route('/get/list', methods=['GET'])
def get_project_list():
    try:
        user = check_user_before_request(request)
        userId = user['id']
        rows = project_sqls_query_project_sql({"userId": userId})

        for i in range(len(rows)):
            project_id = rows[i]['projectId']
            tasks = task_sqls_get_tasks_list_by_project_id(project_id)
            if tasks is None or len(tasks) == 0:
                rows[i]['projectStatus'] = 'created'
            else:
                rows[i]['projectStatus'] = tasks[0]['status']

            problemNum = problem_sql_get_problem_cnt_by_project_id(project_id)
            rows[i]['problemNum'] = problemNum['problemNum']


        return build_success_response(data=rows)

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')


@bp.route('/get/list/public', methods=['GET'])
def get_project_list_public():
    try:
        rows = project_sqls_query_project_sql({"isPublic": True})
        for i in range(len(rows)):
            tasks = task_sqls_get_tasks_list_by_project_id(rows['projectId'])
            if tasks is None or len(tasks) == 0:
                rows['projectStatus'] = 'created'
            else:
                rows['projectStatus'] = tasks[0]['status']

        return build_success_response(data=rows)

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

@bp.route('/del', methods=['POST'])
def del_project():
    trans = SqlTransaction(pooldb)
    trans.begin()
    try:
        project_id = request.json.get("projectId")

        check.checkFrontendArgsIsNotNone([
            {"key": "projectId", "val": project_id},
        ])
        user = check_user_before_request(request)
        userId = user['id']
        if not project_sqls_check_if_project_belong_to_user_id(project_id, userId):
            raise NetworkException(403, '您没有权限执行该操作')

        project_sqls_del_by_project_id(project_id, trans)
        trans.commit()
        return build_success_response()

    except NetworkException as e:
        if trans is not None:
            trans.rollback()
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        if trans is not None:
            trans.rollback()
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

@bp.route('/problem/get', methods=['POST'])
def get_porject_problem():
    try:
        projectId = request.json.get('projectId')
        check.checkFrontendArgsIsNotNone([
            {"key": "projectId", "val": projectId},
        ])
        user = check_user_before_request(request)
        userId = user['id']
        if not project_sqls_check_if_project_belong_to_user_id(projectId, userId):
            raise NetworkException(403, '您没有权限执行该操作')

        rows = problem_sql_get_problem_json_obj_list_by_project_id(projectId)

        return build_success_response(rows)

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')


