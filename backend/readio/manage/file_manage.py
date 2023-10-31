"""
文件管理层，用于向上层提供透明的存储服务
"""
import os.path

from flask import Blueprint, request
import readio.database.connectPool
from readio.utils.buildResponse import *
from readio.utils.auth import *
from readio.database.SQLUtils import *
import readio.utils.check as check
from readio.utils.SourceCodeReader import SourceCodeReader
from readio.database.sqls.project_sqls import project_sqls_check_if_project_is_public_by_project_id, project_sqls_get_project_by_project_id
from readio.database.sqls.file_sqls import *
bp = Blueprint('fileManage', __name__, url_prefix='/file')
pooldb = readio.database.connectPool.pooldb



def __mkdir_project_directory_if_not_exist(projectId: str):
    project_root_path = file_sqls_get_project_root_path(projectId)
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


@bp.route('/getFile', methods=['POST'])
def get_file():
    try:
        project_id = request.json.get("projectId")
        file_path = request.json.get("filePath")
        file_name = request.json.get("fileName")
        check.checkFrontendArgsIsNotNone([
            {"key": "projectId", "val": project_id},
            {"key": "filePath", "val": file_path},
            {"key": "fileName", "val": file_name},
        ])

        if not project_sqls_check_if_project_is_public_by_project_id(project_id):
            # 如果此项目不是公开的, 则需要检查权限
            user = check_user_before_request(request)
            project_obj = project_sqls_get_project_by_project_id(project_id)
            if project_obj['userId'] != user['id']:
                raise NetworkException(403, "您没有权限访问该文件")

        project_source_code_dir = file_sqls_get_dir_file_path_by_project_id(project_id)
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
