from flask import Flask

from .tasks import CeleryTasks
from .routes import (
    # Reason for parenthesis is because there will be more later
    user_endpoints
)

BLUEPRINTS: list = [user_endpoints]


class FlaskServer:
    def __init__(self) -> None:
        self.app = Flask(__name__)

    def _register_blueprints(self):
        self.app.register_blueprint(user_endpoints)
    
    def run_app(self) -> None:
        self._register_blueprints()
        self.app.run()


flask_server: FlaskServer = FlaskServer()