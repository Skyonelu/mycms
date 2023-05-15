# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/4/4
@description: 
"""
import os

import uvicorn
from core.server import create_app
from uvicorn.supervisors.watchgodreload import CustomWatcher

#忽略文件
ignored = {
    "templates",
    "static",
    "staticfiles",
    "compose",
    ".ipython",
    "bin",
    ".pytest_cache",
    ".idea",
    "media",
    "htmlcov",
    "logs",
    "locale",
    "requirements",
}


class WatchgodWatcher(CustomWatcher):
    def __init__(self, *args, **kwargs):
        self.ignored_dirs.update(ignored)
        super(WatchgodWatcher, self).__init__(*args, **kwargs)


uvicorn.supervisors.watchgodreload.CustomWatcher = WatchgodWatcher
app = create_app()

print("当前路径",os.getcwd())
if __name__ == '__main__':
    # 输出所有的路由
    print(os.cpu_count())
    for route in app.routes:
        if hasattr(route, "methods"):
            print({'path': route.path, 'name': route.name, 'methods': route.methods})
    # uvicorn.run(app='run:app', host='0.0.0.0', port=8000, reload=True,timeout_keep_alive=20)
    uvicorn.run(app='run:app', host='0.0.0.0', port=8081, reload=True,workers=9)