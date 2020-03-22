from flask_restful import Resource
# from repository.models import Item
from services.service import Service


class Inventario(Resource):

    def get(self):
        return Service.inventario(), 200

    def post(self):
        pass
