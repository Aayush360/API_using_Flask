from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt  import JWT, jwt_required


from security import authenticate,identity

app = Flask(__name__)

app.secret_key = '$AAYUSH123'
api = Api(app)


jwt = JWT(app,authenticate, identity) # creates a new endpoint /auth

items = []
# class students inherits from the class Resources
# inheriting some stuff from Resource class
class Item(Resource):
    # authenticate before we call the get mothod
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank"

                        )

    @jwt_required()
    def get(self,name):
        item = next(filter(lambda x: x['name']==name,items ),None)
        return {'item':item}, 200 if item else 404


    def post(self,name):

        if next(filter(lambda x: x['name']==name,items ),None):
            return {'message':"An item with name '{}' already exists.".format(name)},400

        # force=True --this ensures you do not need content type header
        # just look in the content and format it even if the
        # content type header is not set to be application/json

        # without it, if the header is not set correctly you do nothing
        # you will always do preocessing of the tect even if it is incorrect
        # silent=True , it does not give error, just returns none
        data = Item.parser.parse_args()
        item = {'name':name,
                'price':data['price']}
        items.append(item)
        return item, 201
    def delete(self,name):
        global items
        items = list(filter(lambda x: x['name']!=name,items))
        return {'message':'Item Deleted'}

    def put(self,name):

        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name']==name,items),None)
        # print(data['another'])

        if item is None:
            item = {'name':name, 'price':data['price']}
            items.append(item)
        else:
            item.update(data)

        return item


class ItemList(Resource):
    def get(self):
        return {'items':items},200



api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/student/aayush
api.add_resource(ItemList, '/items') # http://127.0.0.1:5000/items/



app.run(port=5000,debug=True)


