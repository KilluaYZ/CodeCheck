import json
# from dbtest.showdata10 import db # 引入其他蓝图
import re
from typing import Dict, Tuple, Optional

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, url_for, g
from flask_cors import CORS  # 跨域

# app
from readio.auth import appAuth
from readio.database.init_db import init_db
from readio.manage.fileManage import getFilePathById
from readio.monitor.monitor import monitor
from readio.manage import file_manage as fileManage , userManage
from readio.utils.json import UpdatedJsonProvider

test_cnt = 0

# 创建flask app
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.json_encoder = UpdatedJsonProvider(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # 在应用中注册init_db
    @app.cli.command('init-db')
    def init_db_command():
        """删除现有的所有数据，并新建关系表"""
        init_db()

    app.register_blueprint(monitor, url_prefix='/monitor')
    app.register_blueprint(userManage.bp)
    app.register_blueprint(appAuth.bp)
    app.register_blueprint(fileManage.bp)

    # 配置定时任务
    # 该任务作用是每个一个小时检查一次user_token表，将超过1天未活动的token删掉（随便定的，后面改
    from readio.manage.userManage import checkSessionsAvailability
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=checkSessionsAvailability,
                      id='checkSessionsAvailability',
                      trigger='interval',
                      seconds=3600,
                      replace_existing=True
                      )
    # 该任务作用是每一个小时检查一次check_code_session_key表，删除超过10分钟的过期令牌
    from readio.auth.appAuth import checkCheckCodeSessionKeysAvailability
    scheduler.add_job(func=checkCheckCodeSessionKeysAvailability,
                      id='checkCheckCodeSessionKeysAvailability',
                      trigger='interval',
                      seconds=3600,
                      replace_existing=True
                      )
    # 启动任务列表
    scheduler.start()

    return app


