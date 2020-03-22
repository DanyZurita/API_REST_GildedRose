from mongoengine import *


# Cada Item ira a la coleccion Item
class Item(Document):

    name = StringField(required=True)
    sell_in = IntField()
    quality = IntField()
