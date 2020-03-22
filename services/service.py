
from flask import Response, g
from flask_restful import fields, marshal_with, abort
# from repository.models import Item
from mongoengine.queryset.visitor import Q
from repository.db_atlas import get_db

from repository.repo import Factory


class Service():

    resource_fields = {
            'name': fields.String,
            'sell_in': fields.Integer,
            'quality': fields.Integer
    }

    @staticmethod
    @marshal_with(resource_fields)
    def inventario():
        db = get_db()
        # devuelve db = g.db = connect() y g.Item = Item
        # Al invocar Item() encuentra a db, la referencia
        # a la conexión a la bbdd, en el contexto global
        listItems = []
        for item in g.Item.objects():
            listItems.append(item)
        return listItems

    @staticmethod
    def updateQuality():
        db = get_db()
        for item in g.Item.objects():
            itemObject = Factory.crearObjetoItem(
                [item.name, item.sell_in, item.quality])
            itemObject.update_quality()
            item.sell_in = itemObject.sell_in
            item.quality = itemObject.quality
            item.save()

        # los documentos en la bbdd tienen un id
        # creado de manera automatica
        # En la salida no aparece porque al
        # marshalizar el documento no he tenido
        # en cuenta este campo

        return Service.inventario()

    @staticmethod
    @marshal_with(resource_fields)
    def getItem(itemName):
        # Hay que resolver el tema del espacio
        # en blanco en la url en Aged%20Brie
        # De momento usar %20 como espacio

        # objects(name="Aged Brie") = QuerySet that will
        # only iterate over items =>
        # devuelve una coleccion => recogerla en lista
        # antes de devolver
        db = get_db()
        items = g.Item.objects(name=itemName)
        if not items:
            abort(404, message="El item {} no existe".format(itemName))
        return list(items)

    @staticmethod
    def postItem(args):
        db = get_db()
        item = g.Item(name=args['name'])
        item.sell_in = args['sell_in']
        item.quality = args['quality']
        item.save()

    @staticmethod
    def deleteItem(args):
        db = get_db()
        item = g.Item.objects(Q(name=args['name'])
                              & Q(sell_in=args['sell_in'])
                              & Q(quality=args['quality'])).first()
        if not item:
            abort(404, message="No existe el item")
        else:
            item.delete()

    @staticmethod
    @marshal_with(resource_fields)
    def filterQuality(itemQuality):
        db = get_db()
        items = g.Item.objects(quality=itemQuality)
        return Service.check(items)

    @staticmethod
    @marshal_with(resource_fields)
    def filterSellIn(itemSellIn):
        db = get_db()
        items = g.Item.objects(sell_in__lte=itemSellIn)
        return Service.check(items)

    @staticmethod
    def check(items):
        if not items:
            abort(404, message="No existen items que satisfagan el criterio")
        return list(items)
