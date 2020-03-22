from flask_restful import Resource, Api
# from repository.models import Item
from services.service import Service


class SellIn(Resource):

    # /items/sellin/<itemSellIn>
    # El nombre de este parametro <itemSellIn>
    # ha de ser igual que el del parametro del get()
    # get(self, itemSellIn)
    def get(self, itemSellIn):
        return Service.filterSellIn(itemSellIn), 200
