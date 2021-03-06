from __future__ import absolute_import

from tornado import web

from ..views import BaseHandler
from ..models import TaskModel, WorkersModel


class TaskView(BaseHandler):
    def get(self, task_id):
        task = TaskModel.get_task_by_id(task_id)
        if task is None:
            raise web.HTTPError(404)

        self.render("task.html", task=task)


class TasksView(BaseHandler):
    def get(self):
        limit = self.get_argument('limit', None)
        worker = self.get_argument('worker', None)
        type = self.get_argument('type', None)

        limit = limit and int(limit)
        worker = worker if worker != 'All' else None
        type = type if type != 'All' else None

        tasks = TaskModel.iter_tasks(limit=limit, type=type, worker=worker)
        workers = WorkersModel.get_workers()
        seen_task_types = TaskModel.seen_task_types()

        self.render("tasks.html", tasks=tasks,
                                  task_types=seen_task_types,
                                  workers=workers,
                                  limit=limit,
                                  worker=worker,
                                  type=type)
