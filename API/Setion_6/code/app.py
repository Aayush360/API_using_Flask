from flask import Flask
from flask_restful import Api
from flask_jwt  import JWT


from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store,StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '$AAYUSH123'
api = Api(app)



@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app,authenticate, identity) # creates a new endpoint /auth


# class students inherits from the class Resources
# inheriting some stuff from Resource class


api.add_resource(Store, '/store/<string:name>') # http://127.0.0.1:5000/student/aayush
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/student/aayush
api.add_resource(ItemList, '/items') # http://127.0.0.1:5000/items/
api.add_resource(UserRegister,'/register')
api.add_resource(StoreList, '/stores') # http://127.0.0.1:5000/items/



# prevent running app if this file is imported from another file
# only run if we run python app.py


# only the file that you run is __main

if __name__=="__main__":
    from db import db
    db.init_app(app)

    app.run(port=5000,debug=True)


