from domain.types import *
from domain.accesoCasosTexttest import *


class SingletonOllivander():

    instanciaTienda = None

    @staticmethod
    def crearTienda():
        if not SingletonOllivander.instanciaTienda:
            SingletonOllivander.instanciaTienda = Factory.initRepo()
        return SingletonOllivander.instanciaTienda


class Factory():

    rutaAccesoFichero = "domain/stdout_bug_conjured.gr"

    @staticmethod
    def loadInventario():
        matrizCasosTest = []

        matrizCasosTest = accesoCasosTexttest(
            matrizCasosTest, Factory.rutaAccesoFichero)

        items = Factory.extraerItemsIventario(matrizCasosTest)

        return items


    @staticmethod
    def initRepo():

        matrizCasosTest = []

        matrizCasosTest = accesoCasosTexttest(
            matrizCasosTest, Factory.rutaAccesoFichero)

        items = Factory.extraerItemsIventario(matrizCasosTest)

        inventario = []
        for item in items:
            objetoItem = Factory.crearObjetoItem(item)
            assert isinstance(objetoItem.sell_in, int)
            assert isinstance(objetoItem.quality, int)
            inventario.append(objetoItem)

        tienda = GildedRose(inventario)
        return tienda

    @staticmethod
    def extraerItemsIventario(matrizCasosTest):
        """
        Extrae los items y el estado en el que están el primer dia
        de los casos test y devuelve una lista de items:
        items = [ [item], [item], [item] ]

        Argumentos:
        matrizCasostest -> lista con los casos test. Cada elemento es un dia
        """
        return matrizCasosTest[0]

    @staticmethod
    def crearObjetoItem(item):
        """
        Devuelve un objeto de la clase Item.

        Es necesario convertir la segunda y tercera propiedad a int.

        Argumentos:
        item = ['Elixir of the Mongoose', ' 5', ' 7']
        """
        diccionarioClases = {"Sulfuras, Hand of Ragnaros": "Sulfuras",
                             "Aged Brie": "AgedBrie",
                             "Backstage passes to a TAFKAL80ETC concert": "Backstage",
                             "Conjured Mana Cake": "ConjuredItem",
                             "+5 Dexterity Vest": "ConjuredItem",
                             "Normal Item": "NormalItem"}

        try:
            nombreItem = item[0]
            clase = diccionarioClases[nombreItem]
        except KeyError:
            clase = diccionarioClases["Normal Item"]
        finally:
            return eval(clase + str(tuple(item)))

    @staticmethod
    def test(tienda, estadoInventario):

        nombrePropiedadesItem = ["name", "sell_in", "quality"]
        numeroPropiedadesItem = len(nombrePropiedadesItem)

        for (offset, item) in enumerate(tienda.items):
            print(item)
            for i in range(1, numeroPropiedadesItem):
                propiedad = nombrePropiedadesItem[i]
                valorPropiedadCasoTest = estadoInventario[offset][i]
                assert getattr(item, propiedad) == valorPropiedadCasoTest, \
                    "falla %s %s %s" % (
                        propiedad, estadoInventario[offset][i], item.__class__.__name__)
