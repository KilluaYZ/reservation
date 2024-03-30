from flask import Flask
import flask
from flask_cors import CORS
import config
import reservation.user.user as user
import reservation.file.fileManage as fileManage
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    app.config.from_object(config)
    app.register_blueprint(user.bp)
    app.register_blueprint(fileManage.bp)

    return app

app = create_app()




