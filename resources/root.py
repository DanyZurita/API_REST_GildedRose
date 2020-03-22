from flask_restful import Resource, Api
from services.service import Service
from repository.models import Item


class Root(Resource):

    def get(self):
        return {'Welcome!': 'Ollivanders'}
        # return Item.objects().to_json()
