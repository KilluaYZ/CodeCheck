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


def __query_project_sql(query_param: dict) -> list:
    sql_select = (' select distinct projects.id as projectId, '
                  ' projects.name as projectName, '
                  ' projects.isPublic as isPublic, '
                  ' projects.userId as userId, '
                  ' users.name as userName '
                  ' projects.createTime as createTime, '
                  'from projects, users where projects.userId = users.id ')

    args_str_list = []
    args_val_list = []

    if 'id' in query_param:
        args_str_list.append(f' and projects.id = %s ')
        args_val_list.append(query_param['id'])
    if 'exact_name' in query_param:
        args_str_list.append(f' and projects.name = %s ')
        args_val_list.append(query_param['exact_name'])
    if 'fuzz_name' in query_param:
        args_str_list.append(f' and name like %s ')
        args_val_list.append(f'%{query_param["fuzz_name"]}%')
    if 'isPublic' in query_param:
        args_str_list.append(f' and projects.isPublic = %s ')
        args_val_list.append(query_param['isPublic'])
    if 'userId' in query_param:
        args_str_list.append(f' and projects.userId = %s ')
        args_val_list.append(query_param['userId'])

    sql = sql_select

    for item in args_str_list:
        sql += item

    sql += ' order by projects.createTime desc '

    rows = execute_sql_query(pooldb, sql, tuple(args_val_list))
    return rows

@bp.route('/get/list', methods=['GET'])
def get_project_list():
    try:
        user = check_user_before_request(request)
        userId = user['id']
        rows = __query_project_sql({"userId":userId})
        build_success_response(data=rows)

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')


@bp.route('/get/list/public', methods=['GET'])
def get_project_list_public():
    try:
        rows = __query_project_sql({"isPublic": True})
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
    request.files.get()

@bp.route('/del', methods=['GET'])
def add_project():
    pass