from flask_restful import Resource, Api, reqparse
from flask_jwt  import JWT, jwt_required
from models.item import  ItemModel
import sqlite3


class Item(Resource):
    # authenticate before we call the get mothod
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank"

                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="every item needs a store id."

                        )

    @jwt_required()
    def get(self,name):

        item = ItemModel.get_by_name(name)
        if item:
            return item.json()


        return {'message':'item not found'},404



    def post(self,name):
        if ItemModel.get_by_name(name):
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
        # item = {'name':name,
        #         'price':data['price']}

        item = ItemModel(name,data['price'],data['store_id'])
        try:
            item.save_to_db()
            # ItemModel.insert(item)
        except:
            return {"message":
                        "An error occured inserting the item."
                    },500 # internal server error
        # items.append(item)
        return item.json(), 201



    def delete(self,name):
        # # global items
        # # items = list(filter(lambda x: x['name']!=name,items))
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()
        # return {'message':'Item Deleted'}
        item=ItemModel.get_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "item has been deleted"}



    def put(self,name):

        data = Item.parser.parse_args()
        # item = next(filter(lambda x: x['name']==name,items),None)
        # print(data['another'])

        # if item is None:
        #     item = {'name':name, 'price':data['price']}
        #     items.append(item)
        # else:
        #     item.update(data)
        item = ItemModel.get_by_name(name)
        # updated_item = {'name':name,'price':data['price']}
        # updated_item = ItemModel(name,data['price'])

        if item is None:
            try:
                # ItemModel.insert(updated_item)
                # item = ItemModel(name,data['price'],data['store_id'])
                item = ItemModel(name,**data)

            except:
                return {"message":"An error occured inserting the item."},500


        else:
            try:
                # ItemModel.update(updated_item)
                item.price = data['price']
                item.store_id = data['store_id']
            except:
                return {"message":"An error occured updating the item."},500


        
        # item = {'name': name,
        #         'price': data['price']}
        # return updated_item.json()
        return item.json()






class ItemList(Resource):
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({"name":row[0],
        #                   "price":row[1]})
        # # connection.commit()
        # connection.close()
        items = ItemModel.get_all()
        # item_list =[]
        #
        # for i in items:
        #     item_list.append(i.json())


        # item_list = [i.json() for i in items]

        # or can direcly use
        # [i.json() for i in ItemModel.query.all()]

        # list(map(lambda x: x.json(), ItemModel.query.all()))
        # [i.json() for i in items]

        return {'items':list(map(lambda x: x.json(), ItemModel.query.all() ))},200
