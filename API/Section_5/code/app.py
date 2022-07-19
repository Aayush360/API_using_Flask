from flask import Flask
from flask_restful import Api
from flask_jwt  import JWT


from security import authenticate,identity
from user import UserRegister
from item import Item,ItemList
app = Flask(__name__)

app.secret_key = '$AAYUSH123'
api = Api(app)


jwt = JWT(app,authenticate, identity) # creates a new endpoint /auth


# class students inherits from the class Resources
# inheriting some stuff from Resource class



api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/student/aayush
api.add_resource(ItemList, '/items') # http://127.0.0.1:5000/items/
api.add_resource(UserRegister,'/register')



# prevent running app if this file is imported from another file
# only run if we run python app.py


# only the file that you run is __main

if __name__=="__main__":
    app.run(port=5000,debug=True)


