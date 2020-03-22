from flask_restful import Resource, Api, reqparse
from repository.models import Item
from services.service import Service


class Items(Resource):

    # /items/name/<itemName>
    def get(self, itemName):
        # curl http://localhost:5000/items/name/"Aged%20Brie"
        return Service.getItem(itemName), 200

    def post(self):
        # curl -d name="Conjured Mana Cake" -d sell_in=3 -d quality=6
        # http://127.0.0.1:5000/items -X POST
        args = self.parseRequest()

        # 201 response: request has succeeded and
        # a new resource has been created as a result.
        Service.postItem(args)
        return '', 201

    def delete(self):
        # curl -d name="Conjured Mana Cake" -d sell_in=3 -d quality=6
        # http://127.0.0.1:5000/items -X DELETE
        args = self.parseRequest()
        Service.deleteItem(args)
        return '', 204

    def parseRequest(self):
        # Validar el objeto flask.Request.values
        # o flask.Request.json
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', type=str, required=True,
                            help='name required')
        parser.add_argument('sell_in', type=int, required=True,
                            help='sellIn required')
        parser.add_argument('quality', type=int, required=True,
                            help='quality required')
        # args = parser.parse_args()
        # es un diccionario con los argumentos
        # especificados como keys
        return parser.parse_args()
