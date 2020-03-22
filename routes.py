from app import app
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/backend')
def backend():
    return render_template('Backend/index.html')

@app.route('/insertar')
def insertar():
    return render_template('Backend/insertar.html')

@app.route('/editar')
def editar():
    return render_template('Backend/editar.html')

@app.route('/update')
def update():
    return index()