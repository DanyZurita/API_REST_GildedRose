# Conectar la app a BBDD mongo local

from pymongo import MongoClient
from mongoengine import *
from repository.models import Item

# conectar con MongoDB
client = MongoClient()
# client = MongoClient('localhost', 27017)
# client = MongoClient('mongodb://localhost:27017/')

# obteniendo una bbdd
client.drop_database('ollivanders')
# db = client['ollivanders']
db = client.ollivanders

# Getting a Collection
collection = db['inventario']

# mongoengine: how to connect to our instance of mongod:
connect('ollivanders')


# adding data
def initdb():
    inventario = [["+5 Dexterity Vest", 10, 20],
                  ["Aged Brie", 2, 0],
                  ["Elixir of the Mongoose", 5, 7],
                  ["Sulfuras, Hand of Ragnaros", 0, 80],
                  ["Sulfuras, Hand of Ragnaros", -1, 80],
                  ["Backstage passes to a TAFKAL80ETC concert", 15, 20],
                  ["Backstage passes to a TAFKAL80ETC concert", 10, 49],
                  ["Backstage passes to a TAFKAL80ETC concert", 5, 49],
                  # ["Conjured Mana Cake", 3, 6]
                  ]

    for product in inventario:
        item = Item(name=product[0])
        item.sell_in = product[1]
        item.quality = product[2]
        item.save()


# initdb()
