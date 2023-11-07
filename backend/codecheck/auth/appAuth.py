from flask import Blueprint, request
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
# from codecheck.manage.userManage import __get_all_authorId_id_by_userid, __get_all_followerId_id_by_userid
from codecheck.utils.auth import *
import codecheck.database.connectPool
import codecheck.utils.check as check
from codecheck.database.SQLUtils import execute_sql_query
from codecheck.utils.buildResponse import build_error_response, build_success_response
from codecheck.emailSender.sendMyEmail import sendRegisterEmail, sendChangePasswdEmail

# appAuth = Blueprint('/auth/app', __name__)
bp = Blueprint('auth', __name__, url_prefix='/auth')

pooldb = codecheck.database.connectPool.pooldb

def authorizeEmailPassword(email, password):
    user = execute_sql_query_one(pooldb, 'select * from users where email=%s', email)
    if user is None:
        raise NetworkException(400, '该邮箱不存在')
    if not check_password_hash(user['password'], password):
        raise NetworkException(400, '密码不正确')
    # 验证正确，返回用户
    return user

def authorizeUserIdPassword(userId, password):
    user = execute_sql_query_one(pooldb, 'select * from users where id=%s', userId)
    if user is None:
        raise NetworkException(400, '该用户id不存在')
    if not check_password_hash(user['password'], password):
        raise NetworkException(400, '密码不正确')
    # 验证正确，返回用户
    return user


# 用户注册的sql语句, 默认的用户名随机生成，用户用phoneNumber和password注册
def register_user_sql(userName, password, email):
    execute_sql_write(pooldb, 'insert into users(username,password,email) values(%s,%s,%s)',
                      (userName, generate_password_hash(password), email))


# 检查email是不是唯一的，如果是则返回True，否则返回False
def checkEmailIsUnique(email: str) -> bool:
    rows = execute_sql_query(pooldb, 'select * from users where email=%s', (email))
    if (len(rows) == 0):
        return True
    return False


@bp.route('/register/check', methods=['POST'])
def checkRegisterEmailIsUnique():
    try:
        email = request.json.get('email')
        check.checkFrontendArgsIsNotNone(
            [{"key":"email","val":email}]
        )
        if checkEmailIsUnique(email):
            return build_success_response({"isExist": False})
        return build_success_response({"isExist": True})

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')


# 检查sessionKey和checkCode是否符合
def checkCheckCode(checkCode: str, sessionKey: str, deltaMinutes=10) -> bool:
    row = execute_sql_query_one(pooldb,
                                'select * from check_code_session_key where checkCode=%s and sessionKey=%s order by createTime desc',
                                (checkCode, sessionKey))

    # 检查该验证码是否存在
    if row is None:
        return False

    # 检查是否超过时限
    createTime = row['createTime']
    now_timestamp = datetime.datetime.now()
    if (now_timestamp - createTime > datetime.timedelta(minutes=deltaMinutes)):
        # 超过时限
        return False
    return True


# 生成一个sessionKey和checkCode
def createCheckCodeAndSession() -> tuple:
    # sessionKey和token生成方式一致，是一串随机的字符串
    sessionKey = buildSessionKey()
    # checkCode则是100000到999999之间的一个数字
    checkCode = str(random.randint(100000, 999999))
    # 将生成的sessionKey和checkCode加入到数据表中
    execute_sql_write(pooldb, 'insert into check_code_session_key(checkCode, sessionKey) values(%s, %s)',
                      (checkCode, sessionKey))
    # 返回两个数据
    return (checkCode, sessionKey)


def checkCheckCodeSessionKeysAvailability():
    execute_sql_write(pooldb,
                      'delete from check_code_session_key where timestampdiff(minute,createTime,CURRENT_TIMESTAMP) >= 10')


@bp.route('/getSessionKeyCheckCode', methods=['POST'])
def getSessionKeyCheckCode():
    try:
        type = request.json.get('type')
        email = request.json.get('email')
        check.checkFrontendArgsIsNotNone([{"key":"type", "val":type},{"key":"email", "val":email}])
        if type not in ['register', 'changePasswd']:
            raise NetworkException(400, '前端缺少参数type值不正确，type值只能为register, changePasswd')

        if type == 'register':
            userName = request.json.get('userName')
            check.checkFrontendArgsIsNotNone([{"key": "userName", "val": userName}])
            if not checkEmailIsUnique(email):
                raise NetworkException(400, '该邮箱已被注册')

            checkCode, sessionKey = createCheckCodeAndSession()
            sendRegisterEmail(userName, checkCode, email)
        elif type == 'changePasswd':
            user = execute_sql_query_by_property_unique(pooldb, 'users', 'email', email)
            if user is None:
                raise NetworkException(400, '该用户不存在')
            userName = user['userName']
            checkCode, sessionKey = createCheckCodeAndSession()
            sendChangePasswdEmail(userName, checkCode, email)
        return build_success_response(data={"sessionKey": sessionKey})

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')

@bp.route('/register', methods=['POST'])
def register():
    try:
        userName = request.json.get('userName')
        email = request.json.get('email')
        password = request.json.get('password')
        checkCode = request.json.get('checkCode')
        sessionKey = request.json.get('sessionKey')
        check.checkFrontendArgsIsNotNone(
            [
                {"key": "userName", "val": userName},
                {"key": "email", "val": email},
                {"key": "password", "val": password},
                {"key": "checkCode", "val": checkCode},
                {"key": "sessionKey", "val": sessionKey}
            ]
        )

        if not checkEmailIsUnique(email):
            raise NetworkException(400, '该邮箱已被注册')

        if not checkCheckCode(checkCode, sessionKey):
            raise NetworkException(400, '验证码错误')

        register_user_sql(userName, password, email)
        return build_success_response()

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')

def change_pwd_sql(email: str, password: str):
    user = execute_sql_query_one(pooldb, ' select * from users where email = %s ', email)
    if user is None:
        raise NetworkException(400, "此邮箱未注册")
    userId = user['id']
    return execute_sql_write(pooldb, ' update users set password=%s where id=%s ', (generate_password_hash(password), userId))

@bp.route('/updatePwd', methods=['POST'])
def update_pwd():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        checkCode = request.json.get('checkCode')
        sessionKey = request.json.get('sessionKey')
        check.checkFrontendArgsIsNotNone(
            [
                {"key": "email", "val": email},
                {"key": "password", "val": password},
                {"key": "checkCode", "val": checkCode},
                {"key": "sessionKey", "val": sessionKey}
            ]
        )

        if not checkCheckCode(checkCode, sessionKey):
            raise NetworkException(400, '验证码错误')

        change_pwd_sql(email, password)

        return build_success_response()

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')


# 收到用户名密码，返回会话对应的token
@bp.route('/login', methods=['POST'])
def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        check.checkFrontendArgsIsNotNone(
            [
                {"key": "email", "val": email},
                {"key": "password", "val": password},
            ]
        )
        user = authorizeEmailPassword(email, password)
        token = build_session(user['id'])
        print('[DEBUG] get token, token = ', token)
        # tokenList.append(token)
        return build_success_response({"token": token})

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')


# 退出登录，本质上就是删除与用户建立的对话
@bp.route('/logout', methods=['GET'])
def logout():
    try:
        token = request.headers.get('Authorization')
        if token is None:
            return build_success_response()
        execute_sql_write(pooldb, 'delete from user_token where token=%s', (token))
        return build_success_response()

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(code=500, msg='服务器内部错误')


# data里面应该有user的所有信息
def user_profile_update_user_sql(userId, data):
    try:
        conn, cursor = pooldb.get_conn()
        sql = 'update users set userName=%s,email=%s where id=%s'
        cursor.execute(sql, (data['userName'], data['email'], userId))
        conn.commit()
        pooldb.close_conn(conn, cursor)

    except Exception as e:
        pooldb.close_conn(conn, cursor) if conn is not None else None
        raise e


def __get_all_followerId_id_by_userid(userId) -> List[Dict]:
    """
    通过用户Id来获取该用户所有collect的pieces的id
    """
    sql = 'select followerId from user_subscribe where authorId=%s'
    rows = execute_sql_query(pooldb, sql, userId)
    rows = list(map(lambda x: int(x['followerId']), rows))
    return rows


def __get_all_authorId_id_by_userid(userId) -> List[Dict]:
    """
    通过用户Id来获取该用户所有collect的pieces的id
    """
    sql = 'select authorId from user_subscribe where followerId=%s'
    rows = execute_sql_query(pooldb, sql, userId)
    rows = list(map(lambda x: int(x['authorId']), rows))
    return rows


# 获取用户详细信息
@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    try:
        if request.method == 'GET':
            user = check_user_before_request(request)
            response = {
                "userInfo": {
                    "userId": user['id'],
                    "userName": user['userName'],
                    "email": user['email']
                }
            }

            return build_success_response(response)

        elif request.method == 'POST':
            token = request.headers.get('Authorization')
            if token is None:
                raise Exception('token不存在，无法修改信息')

            user = check_user_before_request(request)

            data = request.json
            user_profile_update_user_sql(user['id'], data)

            return build_success_response()

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response()


def user_profile_update_user_pwd(uid, pwd):
    try:
        sql = 'update users set password=%s where id=%s'
        conn, cursor = pooldb.get_conn()
        cursor.execute(sql, (generate_password_hash(pwd), uid))
        conn.commit()
        pooldb.close_conn(conn, cursor)
    except Exception as e:
        check.printException(e)
        pooldb.close_conn(conn, cursor) if conn is not None else None
        raise Exception(f'用户{uid}密码修改失败')


@bp.route('/profile/updatePwd', methods=['POST'])
def updatePwd():
    try:
        data = request.json
        if 'oldPassword' not in data or 'newPassword' not in data:
            raise NetworkException(400, '前端数据错误，不存在oldPassword或newPassword')

        user = check_user_before_request(request)

        res = authorizeUserIdPassword(user['id'], data['oldPassword'])
        if res is None:
            raise NetworkException(400, '密码不正确')

        user_profile_update_user_pwd(user['id'], data['newPassword'])

        return build_success_response()

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(500, "服务器内部错误")


def __user_avatar_add_sql(userId, fileId, trans=None):
    sql = 'insert into user_avatar_history(userId, fileId) values(%s, %s) '
    if trans is None:
        execute_sql_write(sql, (userId, fileId))
    else:
        trans.execute(sql, (userId, fileId))


def __user_avatar_query_sql(queryParam: dict) -> List[Dict]:
    sql = 'select * from user_avatar_history '
    value_list = []
    sql_list = []
    if 'fileId' in queryParam or 'userId' in queryParam:
        sql += ' where 1=1 '
        if 'fileId' in queryParam:
            value_list.append(queryParam['fileId'])
            sql_list.append(' and fileId = %s ')
        if 'userId' in queryParam:
            value_list.append(queryParam['userId'])
            sql_list.append(' and userId = %s ')

    for sql_str in sql_list:
        sql += sql_str
    sql += ' order by updateTime desc '
    rows = execute_sql_query(pooldb, sql, tuple(value_list))
    return rows


def __check_if_history_is_exist(userId, fileId) -> bool:
    queryParam = {}
    queryParam['fileId'] = fileId
    queryParam['userId'] = userId
    rows = __user_avatar_query_sql(queryParam)
    if rows is not None and len(rows) > 0:
        return True
    return False


def __update_user_avatar_updateTime(userId, fileId, trans=None):
    sql = 'update user_avatar_history set updateTime=now() where userId=%s and fileId=%s'
    if trans is None:
        execute_sql_write(pooldb, sql, (userId, fileId))
    else:
        trans.execute(sql, (userId, fileId))


def __update_user_avatar(userId, fileId, trans=None):
    sql = 'update users set avator=%s where id = %s'
    if trans is None:
        execute_sql_write(pooldb, sql, (fileId, userId))
    else:
        trans.execute(sql, (fileId, userId))


# 用户历史头像
@bp.route('/avatar/add', methods=['POST'])
def add_user_avatar():
    try:
        data = request.json
        if 'fileName' not in data or 'fileType' not in data or 'fileContent' not in data:
            return build_error_response(400, '上传错误，fileName,fileType,fileContent信息不全')

        user = check_user_before_request(request)
        trans = SqlTransaction(pooldb)
        trans.begin()
        fileId = __upload_file_binary_sql(data, trans)
        userId = user['id']
        if __check_if_history_is_exist(userId, fileId):
            # 如果存在了，就只更新一下时间
            __update_user_avatar_updateTime(userId, fileId, trans)
        else:
            # 否则就加进去
            __user_avatar_add_sql(userId, fileId, trans)

        __update_user_avatar(userId, fileId, trans)
        trans.commit()
        return build_success_response()

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(500, "服务器内部错误")


@bp.route('/avatar/get', methods=['GET'])
def get_user_avatar():
    try:
        user = check_user_before_request(request)
        queryParam = {}
        queryParam['userId'] = user['id']
        rows = __user_avatar_query_sql(queryParam)

        return build_success_response(data=rows, length=len(rows))

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(500, "服务器内部错误")


@bp.route('/avatar/update', methods=['POST'])
def update_user_avatar():
    try:
        data = request.json
        if 'fileId' not in data:
            return build_error_response(400, '上传错误，fileId缺失')

        fileId = data['fileId']
        user = check_user_before_request(request)
        trans = SqlTransaction(pooldb)
        trans.begin()
        userId = user['id']
        if __check_if_history_is_exist(userId, fileId):
            # 如果存在了，就只更新一下时间
            __update_user_avatar_updateTime(userId, fileId, trans)
        else:
            # 否则就加进去
            __user_avatar_add_sql(userId, fileId, trans)

        __update_user_avatar(userId, fileId, trans)
        trans.commit()
        return build_success_response()

    except NetworkException as e:
        return build_error_response(code=e.code, msg=e.msg)
    except Exception as e:
        check.printException(e)
        return build_error_response(500, "服务器内部错误")

# 每过一段时间，都会检查一遍user_token表，看createTime和visitTime之差，如果二者之差>=30min，说明该用户已经长时间未进行操作了，应该该会话关闭
def checkSessionsAvailability():
    execute_sql_write(pooldb, 'delete from user_token where timestampdiff(minute,visitTime,CURRENT_TIMESTAMP) >= 1440')
