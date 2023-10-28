import readio.database.connectPool

pooldb = readio.database.connectPool.pooldb
from readio.database.SQLUtils import *


def __get_project_by_project_id(project_id: str) -> dict:
    return execute_sql_query_by_property_unique(pooldb, 'projects', 'id', project_id)

def __get_user_by_project_id(project_id: str) -> dict:
    return execute_sql_query_one(pooldb,
    ' select users.id as id, userName, email, createTime from users, projects '
    ' where projects.id = %s '
    ' and users.id=projects.id ',
    project_id)

def __check_if_project_is_public_by_project_id(project_id: str) -> bool:
    project = __get_project_by_project_id(project_id)
    if project is None:
        return False
    if not project['isPublic']:
        return False
    return True

