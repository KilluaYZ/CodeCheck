# 对项目进行分析
# 使用该类默认项目的目录已经建立，相关的json文件和压缩文件或者源码链接已经准备好了，且项目的信息已经写在数据库中了
from concurrent.futures import ThreadPoolExecutor, as_completed
from readio.utils.query_tools import query_tool_get_project_by_project_id

class Analyzer:
    def __init__(self, max_workers = 8):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    # 提交处理该项目
    def commit(self, project_id: str):
        project = query_tool_get_project_by_project_id(project_id)
