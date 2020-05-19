from flask import Flask
from config.config import Config
from flask_restful import Api
from config.db import db
from flask_jwt import JWT
from config.security import authenticate, identity

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)