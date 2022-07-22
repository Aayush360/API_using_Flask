# import sqlite3
from db import db



class StoreModel(db.Model):
    __tablename__="stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')
    # whenever we access the json method , we will get error unless
    # when lazy='dynamic', self.items no longer creates list of items, now it is a query builder
    # that has ability to look into item tables

    def __init__(self,name):
        self.name = name


    def json(self):
        return {"name":self.name,"items":[item.json() for item in self.items.all()]}


    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  #SELECT * FROM items where name=name ,, we can also chain failter_by
        # this will return an item model object

    @classmethod
    def get_all(cls):
        return cls.query.all()


    def save_to_db(self):

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()