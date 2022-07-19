from flask_restful import Resource, Api, reqparse
from flask_jwt  import JWT, jwt_required
import sqlite3


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

        item = self.get_by_name(name)
        if item:
            return item


        return {'message':'item not found'},404

    @classmethod
    def get_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items where name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {
                'name': row[0],
                'price': row[1]
            }}

    def post(self,name):
        if self.get_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        #
        # if next(filter(lambda x: x['name']==name,items ),None):
        #     return {'message':"An item with name '{}' already exists.".format(name)},400

        # force=True --this ensures you do not need content type header
        # just look in the content and format it even if the
        # content type header is not set to be application/json

        # without it, if the header is not set correctly you do nothing
        # you will always do preocessing of the tect even if it is incorrect
        # silent=True , it does not give error, just returns none
        data = Item.parser.parse_args()
        item = {'name':name,
                'price':data['price']}
        try:
            self.insert(item)
        except:
            return {"message":
                        "An error occured inserting the item."
                    },500 # internal server error
        # items.append(item)
        return item, 201

    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    def delete(self,name):
        # global items
        # items = list(filter(lambda x: x['name']!=name,items))
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message':'Item Deleted'}

    def put(self,name):

        data = Item.parser.parse_args()
        # item = next(filter(lambda x: x['name']==name,items),None)
        # print(data['another'])

        # if item is None:
        #     item = {'name':name, 'price':data['price']}
        #     items.append(item)
        # else:
        #     item.update(data)
        item = self.get_by_name(name)
        updated_item = {'name':name,'price':data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message":"An error occured inserting the item."},500


        else:
            try:
                self.update(updated_item)
            except:
                return {"message":"An error occured updating the item."},500


        
        # item = {'name': name,
        #         'price': data['price']}
        return updated_item


    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items set price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()



class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({"name":row[0],
                          "price":row[1]})
        # connection.commit()
        connection.close()

        return {'items':items},200
