from flask import Blueprint, request
import readio.database.connectPool
from readio.utils.buildResponse import *
from readio.utils.auth import *
from readio.database.SQLUtils import *
import readio.utils.check as check
from readio.utils.SourceCodeReader import SourceCodeReader
from readio.database.sqls.project_sqls import project_sqls_check_if_project_is_public_by_project_id, project_sqls_get_project_by_project_id
from readio.database.sqls.file_sqls import *
from readio.database.sqls.problem_sqls import *
from readio.database.sqls.trace_sqls import *
from readio.ai.WenXinAi import chat

import base64
bp = Blueprint('AiChat', __name__, url_prefix='/ai')
pooldb = readio.database.connectPool.pooldb

@bp.route("/chat", methods=["POST"])
def chat():
    try:
        chat_history = request.json.get("chatHistory")
        check.checkFrontendArgsIsNotNone([
            {"key": "chatHistory", "val": chat_history},
        ])

        new_chat_history, reply = chat(chat_history)
        response = {
            "reply": reply
        }

        return build_success_response(data=response)

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')


