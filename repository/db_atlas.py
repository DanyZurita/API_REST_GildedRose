from mongoengine import *
from repository.models import Item
from repository.repo import Factory
import dns  # mongo atlas, required for connecting with SRV
# Utileria de flask
import click
from flask.cli import with_appcontext
from flask import g

# Conectar con Mongo Atlas:
# Asegurarse de que el puerto 27017 está accesible:
# $ curl portquiz.net:27017
# proporciona además la ip pública desde la que
# te conectas al servicio de Atlas


def get_db():
    if 'db' not in g:
        # connect() devuelve una referencia en el contexto global
        # que ahora guardamos en el objeto global de flask g
        # Conectarse a Mongo Atlas con mongoengine
        # En la URI, /test? es la bbdd
        g.db = connect(
                    host='mongodb+srv://ollivander:gildedrose@pruebas-icv6e.mongodb.net/Ollivander?retryWrites=true&w=majority'
                )
        # Item necesita encontrar la referencia la conexión
        # devuelta por connect()
        # Parece ser que la encuentra tb al meterla en g
        # Guardo tb Item en g para evitar paso de parametros
        # entre resources y service (ver inventario)
        g.Item = Item
    return g.db


def close_db(e=None):
    # Si la conexión existe, se cierra.
    db = g.pop('db', None)

    if db is not None:
        db.close()


# Poblar la base de datos
def init_db():

    db = get_db()

    """
    inventario = [["+5 Dexterity Vest", 10, 20],
                  ["Aged Brie", 2, 0],
                  ["Elixir of the Mongoose", 5, 7],
                  ["Sulfuras, Hand of Ragnaros", 0, 80],
                  ["Sulfuras, Hand of Ragnaros", -1, 80],
                  ["Backstage passes to a TAFKAL80ETC concert", 15, 20],
                  ["Backstage passes to a TAFKAL80ETC concert", 10, 49],
                  ["Backstage passes to a TAFKAL80ETC concert", 5, 49],
                  # ["Conjured Mana Cake", 3, 6]
                  ] """

    # Cargamos los items del fichero de texto
    # con los casos test
    inventario = Factory.loadInventario()

    # Poblamos la bbdd
    # Item de mongoengine es la coleccion
    for product in inventario:
        Item(name=product[0], sell_in=product[1], quality=product[2]).save()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Define un comando para la linea de comandos
        llamado init-db que invoca a la función init_db,
        de modo que desacoplo la inicialización de la bbdd
        de la ejecución de la app."""
    init_db()
    click.echo('Base de datos inicializada en Mongo Atlas')


def init_app(app):
    # close_db se invoca tras cada request
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    # Now that init-db has been registered with the app,
    # it can be called using the flask command:
    # $ flask init-db
    # Antes set FLASK_APP and FLASK_ENV
    # export FLASK_APP=controller.py
    # export FLASK_ENV=development
