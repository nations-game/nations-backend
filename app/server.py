from flask import Flask

from .tasks import CeleryTasks


class FlaskServer:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.celery = CeleryTasks(
            self.app.import_name,
            "solo://"
        )
    
    def run_app(self) -> None:
        self.app.run()