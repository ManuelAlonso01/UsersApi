import sqlite3 as sql
from errors import *

def get_conexion():
    conexion = sql.connect('database.db')
    return conexion


def get_usuarios():
    conexion = get_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT id, nombre, email, edad FROM usuarios")
        resultados = cursor.fetchall()
        
        if not resultados:
            raise UsuariosNoEncontrados()
        
        return [
            {'id': r[0], 'nombre': r[1], 'email': r[2], 'edad':r[3]}
            for r in resultados
            ]
        
    except sql.Error:
        raise ErrorDataBase()
    finally:
        conexion.close()



def get_usuario_id(id_usuario):
    conexion = get_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT id, nombre, email, edad FROM usuarios WHERE id = ?", (id_usuario,))
        resultado = cursor.fetchone()
        if not resultado:
            raise UsuariosNoEncontrados()
        return {'id': resultado[0], 'nombre': resultado[1], 'email': resultado[2], 'edad': resultado[3]}
    except sql.Error:
        raise ErrorDataBase()
    finally:
        conexion.close()




def crear_usuario(nombre, email, edad):
    conexion = get_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO usuarios(nombre, email, edad) VALUES (?, ?, ?)",
                       (nombre, email, edad,))
        conexion.commit()
    except sql.Error:
        raise ErrorDataBase()
    finally:
        conexion.close()




def editar_usuario(id_usuario, nombre, email, edad):
    conexion = get_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("UPDATE usuarios SET nombre = ?, email = ?, edad = ? WHERE id = ?",
                       (nombre, email, edad, id_usuario))
        conexion.commit()
    except sql.Error:
        raise ErrorDataBase()
    finally:
        conexion.close()




def eliminar_usuario(id_usuario):
    conexion = get_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute('DELETE FROM usuarios WHERE id = ?', (id_usuario,))
        if cursor.rowcount == 0:
            raise UsuariosNoEncontrados()
        conexion.commit()    
    except sql.Error:
        raise ErrorDataBase()
    finally:
        conexion.close()
