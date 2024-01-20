from flask_apscheduler import APScheduler
from flask import Flask

class TaskHandler:
    def __init__(self, flask_app: Flask) -> None:
        self.flask_app = flask_app

        self.scheduler = APScheduler()
        self.scheduler.init_app(self.flask_app)

        # Example task
        @self.scheduler.task("interval", id="do_test_task", seconds=30, misfire_grace_time=900)
        def test_task():
            print("test task executed")

        self.scheduler.start()