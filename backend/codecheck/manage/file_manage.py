"""
文件管理层，用于向上层提供透明的存储服务
"""
import os.path

from flask import Blueprint, request
import codecheck.database.connectPool
from codecheck.utils.buildResponse import *
from codecheck.utils.auth import *
from codecheck.database.SQLUtils import *
import codecheck.utils.check as check
from codecheck.utils.SourceCodeReader import SourceCodeReader
from codecheck.database.sqls.project_sqls import project_sqls_check_if_project_is_public_by_project_id, project_sqls_get_project_by_project_id
from codecheck.database.sqls.file_sqls import *
from codecheck.database.sqls.problem_sqls import *
from codecheck.database.sqls.trace_sqls import *
import base64
bp = Blueprint('fileManage', __name__, url_prefix='/file')
pooldb = codecheck.database.connectPool.pooldb



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
        print(f'[DEBUG] 1')
        project_id = request.json.get("projectId")
        file_path = request.json.get("filePath")
        file_name = request.json.get("fileName")
        check.checkFrontendArgsIsNotNone([
            {"key": "projectId", "val": project_id},
            {"key": "filePath", "val": file_path},
            {"key": "fileName", "val": file_name},
        ])
        if file_path == '/':
            file_path = ''
        print(f'[DEBUG] 2')
        if not project_sqls_check_if_project_is_public_by_project_id(project_id):
            # 如果此项目不是公开的, 则需要检查权限
            print(f'[DEBUG] 2.1')
            user = check_user_before_request(request)
            project_obj = project_sqls_get_project_by_project_id(project_id)
            print(f'[DEBUG] user = {user}')
            print(f'[DEBUG] project_obj = {project_obj}')
            if project_obj['userId'] != user['id']:
                raise NetworkException(403, "您没有权限访问该文件")
        print(f'[DEBUG] 3')
        project_source_code_dir = file_sqls_get_dir_file_path_by_project_id(project_id)
        source_code_file_relative_path = f"{file_path}/{file_name}"

        print(f'[DEBUG] project_source_code_dir = {project_source_code_dir}')
        print(f'[DEBUG] source_code_file_relative_path = {source_code_file_relative_path}')

        my_reader = SourceCodeReader(project_source_code_dir)
        response_content = my_reader.read(source_code_file_relative_path)

        if response_content['fileCategory'] == "text":
            problem_objs = problem_sql_get_problem_json_objs_by_project_id_and_file_path(project_id, source_code_file_relative_path)
            if problem_objs is not None:
                for problem_obj in problem_objs:
                    problemDetailObj = json.loads(problem_obj["problemDetail"])
                    problem_line = problemDetailObj["line"]
                    if "problem" not in response_content["content"][problem_line - 1]:
                        response_content["content"][problem_line - 1]["problem"] = []
                    problemDetailObj['problemId'] = problem_obj["problemId"]
                    response_content["content"][problem_line - 1]["problem"].append(problemDetailObj)
                    # trace_obj_list = problemDetailObj["trace"]
                    # if trace_obj_list is not None:
                    #     for trace_obj in trace_obj_list:
                    #         trace_line = trace_obj["line"]
                    #         response_content["content"][trace_line - 1]["trace"] = trace_obj
            trace_obj_list = trace_sqls_get_trace_by_project_id_and_file_path(project_id, source_code_file_relative_path)
            if trace_obj_list is not None:
                for trace_obj in trace_obj_list:
                    trace_line = trace_obj['line']
                    if "trace" not in response_content["content"][trace_line - 1]:
                        response_content["content"][trace_line - 1]["trace"] = []
                    response_content["content"][trace_line - 1]["trace"].append(trace_obj)
        return build_success_response(data=response_content)

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')


@bp.route('/upload', methods=['POST'])
def upload_file():
    try:
        project_id = request.json.get("projectId")
        fileName = request.json.get('fileName')
        fileContent = request.json.get('fileContent')
        print(f'[DEBUG] 1')
        check.checkFrontendArgsIsNotNone([
            {"key": "projectId", "val": project_id},
            {"key": "fileName", "val": fileName},
            {"key": "fileContent", "val": fileContent},
        ])

        # 检查文件格式
        fileName = fileName.strip()
        fileName_lowercase = fileName.lower()
        fileSuffix = file_sqls_get_file_suffix(fileName_lowercase)
        if fileSuffix == 'json':
            filePath = 'json'
            fileCategory = 'text'
        else:
            filePath = 'zip'
            fileCategory = 'zip'

        __mkdir_project_directory_if_not_exist(project_id)
        # file.save(os.path.join(BASE_FILE_STORE_DIR, filePath))
        write_path = f'{BASE_FILE_STORE_DIR}/{project_id}/{filePath}/{fileName}'

        fileContentBinary = base64.b64decode(fileContent)
        with open(write_path, "wb") as fw:
            fw.write(fileContentBinary)
        # fileContent.save(write_path)

        file_sqls_insert_file(fileName, filePath, fileCategory, project_id, fileSuffix)

        return build_success_response(msg='上传成功')

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')
