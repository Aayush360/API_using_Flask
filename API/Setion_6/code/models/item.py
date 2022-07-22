# import sqlite3
from db import db



class ItemModel(db.Model):
    __tablename__="items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))


    store = db.relationship('StoreModel')

    def __init__(self,name,price,store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name":self.name,"price":self.price}


    @classmethod
    def get_by_name(cls, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM items where name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        #
        # if row:
        #     # return {'item': {
        #     #     'name': row[0],
        #     #     'price': row[1]
        #     # }}
        #     # return cls(row[0],row[1])
        #     return cls(*row) #parameter unpacking
        return cls.query.filter_by(name=name).first()  #SELECT * FROM items where name=name ,, we can also chain failter_by
        # this will return an item model object

    @classmethod
    def get_all(cls):
        return cls.query.all()

    # def update(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "UPDATE items set price=? WHERE name=?"
    #     cursor.execute(query, (self.price, self.name))
    #     connection.commit()
    #     connection.close()


    # since it is inserting itself , saving model to the db
    # def insert(self):

    def save_to_db(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO items VALUES (?,?)"
        # cursor.execute(query, (self.name, self.price))
        # connection.commit()
        # connection.close()
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()