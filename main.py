from flask import Flask, request, jsonify, Response
from consultas import *


app = Flask(__name__)


@app.route('/usuarios', methods=["GET"])
def obtener_usuarios():
    try:
        resultados = get_usuarios()
        if resultados:
            return jsonify(resultados), 200
    except UsuariosNoEncontrados:
        return jsonify({"Error": "No se pudo obtener a los usuarios."}), 404
    except ErrorDataBase:
        return jsonify({"Error": "Error interno del servidor."}), 500
 
 
    
@app.route('/usuarios/<int:id>', methods=["GET"])
def obtener_usuario_id(id):
    try:
        resultado = get_usuario_id(id)
        if resultado:
            return jsonify(resultado), 200
    except UsuariosNoEncontrados:
        return jsonify({"Error": "No se pudo obtener al usuario."}), 404
    except ErrorDataBase:
        return jsonify({"Error": "Error interno del servidor."}), 500
 
    
    
@app.route('/usuarios', methods=["POST"])
def insertar_usuario():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"Error": "JSON vacio o invalido."}), 400
    nombre = data.get('nombre')
    email = data.get('email')
    edad = data.get('edad')
    if not nombre or not email or not edad or edad < 0:
        return jsonify({"Error": "Faltan campos"}), 400
    try:
        crear_usuario(nombre, email, edad)
        return Response(status=201)
    except ErrorDataBase:
        return jsonify({"Error": "Error interno del servidor."}), 500
 
 
    
@app.route('/usuarios/<int:id>', methods=["PUT"])
def actualizar_usuario(id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"Error": "JSON vacio o invalido"}), 400
    nombre = data.get('nombre')
    email = data.get('email')
    edad = data.get('edad')
    if not nombre or not email or not edad or edad < 0:
        return jsonify({"Error": "Faltan campos"}), 400
    try:
        editar_usuario(id, nombre, email, edad)
        return Response(status=200)
    except ErrorDataBase:
        return jsonify({"Error": "Error interno del servidor."}), 500



@app.route('/usuarios/<int:id>', methods=["DELETE"])
def borrar_usuario(id):
    try:
        eliminar_usuario(id)
        return Response(status=204)
    except UsuariosNoEncontrados:
        return jsonify({"Error": "No se pudo obtener al usuario."}), 404
    except ErrorDataBase:
        return jsonify({"Error": "Error interno del servidor."}), 500   

if __name__ == "__main__":
    app.run(port=5000, debug=True)