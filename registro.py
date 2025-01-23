import sqlite3
import cv2

def registrar_rostro(nombre, ruta_imagen):
    conn = sqlite3.connect('rostros.db')
    cursor = conn.cursor()

    # Cargar la imagen
    imagen = cv2.imread(ruta_imagen)
    _, buffer = cv2.imencode('.jpg', imagen)
    foto_blob = buffer.tobytes()

    cursor.execute("INSERT INTO rostros (nombre, foto) VALUES (?, ?)", (nombre, foto_blob))
    conn.commit()
    conn.close()

# Registrar ejemplos
registrar_rostro("Juan Pérez", "juan.jpg")
registrar_rostro("Ana López", "ana.jpg")
