from flask import Flask

from .database import Database, database_instance
from .tasks import TaskHandler
from .routes import (
    user_endpoints,
    nation_endpoints
)

BLUEPRINTS: list = [
    user_endpoints,
    nation_endpoints
]

class FlaskConfig:
    SCHEDULER_API_ENABLED = True

class FlaskServer:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.app.config.from_object(FlaskConfig())

        self.task_handler = TaskHandler(flask_app=self.app)
        self.database: Database = database_instance

    def _register_blueprints(self):
        for blueprint in BLUEPRINTS:
            self.app.register_blueprint(blueprint)
    
    def run_app(self) -> None:
        self._register_blueprints()
        self.app.run()

    def get_database(self) -> Database:
        return self.database


flask_server: FlaskServer = FlaskServer()