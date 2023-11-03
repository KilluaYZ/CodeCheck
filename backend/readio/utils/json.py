# -*- coding: utf-8 -*-
# 配置自己的Json， 针对date和datetime格式进行特殊处理

# 已经在flask2.3中被取代######################################
# from flask.json import JSONEncoder

# class CustomJSONEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime):
#             return obj.strftime('%Y-%m-%d %H:%M:%S')
#         elif isinstance(obj, date):
#             return obj.strftime('%Y-%m-%d')
#         else:
#             return JSONEncoder.default(self, obj)
############################################################

# flask2.3之后用新的这个
from datetime import datetime, date
from flask.json.provider import DefaultJSONProvider


class UpdatedJsonProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return super().default(obj)
