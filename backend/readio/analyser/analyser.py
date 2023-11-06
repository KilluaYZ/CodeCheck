# 对项目进行分析
# 使用该类默认项目的目录已经建立，相关的json文件和压缩文件或者源码链接已经准备好了，且项目的信息已经写在数据库中了
import os
from concurrent.futures import ThreadPoolExecutor
from readio.analyser.compressor import Compressor
import json
from readio.database.sqls.task_sqls import *
from readio.database.sqls.file_sqls import file_sqls_get_zip_file_path_by_project_id, file_sqls_get_project_root_src_path, file_sqls_insert_file, file_sqls_get_json_file_path_by_project_id
from readio.database.sqls.problem_sqls import problem_sql_insert_problem_json_obj
from readio.database.sqls.trace_sqls import trace_sqls_insert_trace_by_trace_obj
class Analyzer:
    def __init__(self, max_workers = 8):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)


    def run(self, project_id: str, task_id: str):
        trans = SqlTransaction(pooldb)
        trans.begin()
        try:
            print(f'[DEBUG] args: project_id = {project_id}, task_id = {task_id}')
            print(f'[DEBUG] 1')
            # 获取压缩包路径
            zip_file_path = file_sqls_get_zip_file_path_by_project_id(project_id)
            print(f'[DEBUG] 1.1')
            src_dir_path = file_sqls_get_project_root_src_path(project_id)
            print(f'[DEBUG] 1.2')
            task_sqls_update_task_status(task_id, 'unzipping')
            # 申明一个Compressor实例，并解压
            cmr = Compressor(zip_file_path, src_dir_path)
            cmr.uncompress()
            print(f'[DEBUG] 1.3')
            # 拿到解压后的目标文件夹
            target_src_path = cmr.file_path
            target_src_path = target_src_path[target_src_path.index("src"):]
            target_src_dir_name = cmr.current_file_name_without_suffix
            # 将解压后的源码目录根目录加入到file_info表中
            file_sqls_insert_file(target_src_dir_name, target_src_path, 'directory', project_id, trans)
            print(f'[DEBUG] 2')
            task_sqls_update_task_status(task_id, 'analysing')
            json_path = file_sqls_get_json_file_path_by_project_id(project_id)
            json_file_text = ''
            print(f'[DEBUG] 2.1')
            with open(json_path, "r") as jf:
                json_file_text = jf.read()
                json_obj = json.loads(json_file_text)
                for problem in json_obj:
                    problem_id = problem_sql_insert_problem_json_obj(problem, project_id, trans)
                    traces_list = problem["trace"]
                    if traces_list is not None:
                        for trace_obj in traces_list:
                            trace_sqls_insert_trace_by_trace_obj(trace_obj, project_id, problem_id, trans)

            print(f'[DEBUG] 3')
            trans.commit()
            task_sqls_update_task_status(task_id, 'success')

        except Exception as e:
            print("[ERROR] 运行analyser::run出错")
            print(e)
            task_sqls_update_task_status(task_id, 'error')
            trans.rollback()
            raise e


    # 提交处理该项目
    def submit(self, project_id: str):
        tasks_list = task_sqls_get_tasks_list_by_project_id(project_id)

        # 检查该项目是否正在执行任务
        if len(tasks_list) > 0:
            task = tasks_list[0]
            if task['status'] in ['unzipping', 'pulling', 'analysing']:
                raise Exception(f"Analyzer::commit，项目{project_id}的状态为{task['status']}，正在执行任务，无法提交")

        # 项目没有执行任何任务，可以加入到队列中
        # 先向表中加入一个task记录
        task_id = task_sqls_init_task(project_id)
        task_sqls_update_task_status(task_id, 'waiting')
        self.executor.submit(self.run, project_id, task_id)

CodeAnalyzer = Analyzer()

