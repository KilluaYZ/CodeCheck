"""
文件管理层，用于向上层提供透明的存储服务
"""
import os.path

from flask import Blueprint, request, send_file, g, current_app
import readio.database.connectPool
from typing import BinaryIO
from readio.database.SQLUtils import *
from readio.utils.buildResponse import *
from readio.utils.auth import *
from readio.database.SQLUtils import *
import struct
import readio.utils.check as check
from readio.utils.SourceCodeReader import SourceCodeReader
from readio.utils.query_tools import query_tool_check_if_project_is_public_by_project_id, query_tool_get_project_by_project_id
bp = Blueprint('fileManage', __name__, url_prefix='/file')
pooldb = readio.database.connectPool.pooldb
BASE_FILE_STORE_DIR = './code_check_shower_server_data'

def __get_file_info_by_id(fileId: str) -> dict:
    """
    通过id唯一地找到对应的文件信息
    """
    return execute_sql_query_by_property_unique(pooldb, 'file_info', 'id', fileId)

def __get_file_info_by_sha256(sha256_str: str) -> dict:
    """
    通过sha256值唯一地找到对应的文件信息
    """
    return execute_sql_query_by_property_unique(pooldb, 'file_info', 'sha256', sha256_str)

def __query_file_info_sql(query_param: dict) -> list:
    sql = f'select * from file_info'
    arg_list = []
    if ('fileName' in query_param
            or 'fileType' in query_param
            or 'fileId' in query_param
            or 'sha256' in query_param
            or 'projectId' in query_param
    ):
        sql = sql + ' where 1=1 '
        if 'fileName' in query_param:
            sql += f' and fileName like %s '
            arg_list.append(f'%{query_param["fileName"]}%')
        if 'fileType' in query_param:
            sql += f' and fileType=%s '
            arg_list.append(query_param['fileType'])
        if 'fileId' in query_param:
            sql += f' and id=%s '
            arg_list.append(query_param['fileId'])
        if 'sha256' in query_param:
            sql += f' and sha256=%s '
            arg_list.append(query_param['sha256'])
        if 'projectId' in query_param:
            sql += f' and project_id=%s '
            arg_list.append(query_param['projectId'])


    if 'sortMode' in query_param:
        if query_param['sortMode'] == 'Old':
            sql += ' order by createTime asc '
        else:
            sql += ' order by createTime desc '
    else:
        sql += ' order by createTime desc '

    rows = execute_sql_query(pooldb, sql, tuple(arg_list))
    return rows

def __get_project_root_path(projectId: str):
    return os.path.join(BASE_FILE_STORE_DIR, projectId)

def __get_file_path_by_file_info(file_info) -> str:
    """
    根据fileInfo对象，获取该文件的文件路径
    """
    if file_info is None:
        raise Exception("__get_file_path_by_file_info::file_info为None")

    file_path = file_info['filePath']
    file_name = file_info['fileName']
    file_type = file_info['fileType']
    project_id = file_info['project_id']
    if file_type == 'directory':
        return f"{__get_project_root_path(project_id)}/{file_path}/{file_name}"
    else:
        return f"{__get_project_root_path(project_id)}/{file_path}/{file_name}.{file_type}"

def __get_file_path_by_id(fileId: str) -> str:
    """
    根据id获取文件的路径，如果是目录则获取根目录
    """
    file_info = __get_file_info_by_id(fileId)

    if file_info is None:
        return None

    return __get_file_path_by_file_info(file_info)


def __get_dir_file_path_by_project_id(project_id: str) -> str:
    """
    根据项目id获取源码根目录路径
    """
    file_info_list = __query_file_info_sql({"projectId": project_id, "fileType": "directory"})
    if file_info_list is None or len(file_info_list) == 0:
        return None

    file_info = file_info_list[0]
    file_path = __get_file_path_by_file_info(file_info)
    return file_path

def __get_text_file_content_by_id(fileId: str) -> str:
    """
    读取文本数据
    """
    file_path = __get_file_path_by_id(fileId)

def __mkdir_project_directory_if_not_exist(projectId: str):
    project_root_path = __get_project_root_path(projectId)
    src_path = os.path.join(project_root_path, 'src')
    json_path = os.path.join(project_root_path, 'json')
    zip_path = os.path.join(project_root_path, 'zip')

    if not os.path.exists(project_root_path):
        os.mkdir(project_root_path)
    if not os.path.exists(src_path):
        os.mkdir(src_path)
    if not os.path.exists(json_path):
        os.mkdir(json_path)
    if not os.path.exists(zip_path):
        os.mkdir(zip_path)


@bp.route('/getFile',methods=['POST'])
def get_file():
    try:
        project_id = request.json.get("projectId")
        file_path = request.json.get("filePath")
        file_name = request.json.get("fileName")
        check.checkFrontendArgsIsNotNone([
            {"key": "projectId", "val": project_id},
            {"key": "filePath", "val": file_path},
            {"key": "file_name", "val": file_name},
        ])

        if not query_tool_check_if_project_is_public_by_project_id(project_id):
            # 如果此项目不是公开的, 则需要检查权限
            user = check_user_before_request(request)
            project_obj = query_tool_get_project_by_project_id(project_id)
            if project_obj['userId'] != user['id']:
                raise NetworkException(403, "您没有权限访问该文件")

        project_source_code_dir = __get_dir_file_path_by_project_id(project_id)
        source_code_file_relative_path = f"{file_path}/{file_name}"
        my_reader = SourceCodeReader(project_source_code_dir)
        response_content = my_reader.read(source_code_file_relative_path)
        return build_success_response(data=response_content)

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')


@bp.route('/upload', methods=['POST'])
def upload_file():
    try:
        project_id = request.args.get("projectId")
        file = request.files.get('file')
        check.checkFrontendArgsIsNotNone([
            {"key": "projectId", "val": project_id},
            {"key": "file", "val": file},
        ])

        # 检查文件格式
        fileName = file.filename
        fileName = fileName.strip()
        fileName_lowercase = fileName.lower()
        if fileName_lowercase.endswith('json'):
            filePath = 'json'
        else:
            filePath = 'zip'

        __mkdir_project_directory_if_not_exist(project_id)

        file.save(os.path.join(BASE_FILE_STORE_DIR, filePath))

        return build_success_response(msg='上传成功')

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')
