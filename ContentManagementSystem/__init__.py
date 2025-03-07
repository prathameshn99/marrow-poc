import os 
from flask import Flask

def create_app(test_config= None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'ContentManagementSystem.sqlite'),
    )   

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from . import db

    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import cms
    app.register_blueprint(cms.cms)
    app.add_url_rule('/', endpoint='index')

    return app