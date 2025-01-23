from flask import Flask, request, jsonify, render_template
import mysql.connector
import face_recognition
import numpy as np
import cv2
import base64
import io
from PIL import Image

app = Flask(__name__)

# Función para conectar a la base de datos MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="sql103.infinityfree.com",        # Cambia a la IP del servidor MySQL si no es local
        user="if0_38121950",             # Usuario de MySQL
        password="220FEl78h41",            # Contraseña del usuario
        database="if0_38121950_reconocimiento" # Nombre de la base de datos
    )

# Función para cargar los rostros registrados desde MySQL
def cargar_rostros():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, foto FROM rostros")
    data = cursor.fetchall()
    rostros = []
    nombres = []
    for nombre, foto in data:
        # Convierte la foto almacenada en la base de datos a un encoding de rostro
        foto_array = np.frombuffer(foto, dtype=np.uint8)
        imagen = cv2.imdecode(foto_array, cv2.IMREAD_COLOR)
        encoding = face_recognition.face_encodings(imagen)[0]
        rostros.append(encoding)
        nombres.append(nombre)
    conn.close()
    return rostros, nombres

# Ruta para la página principal que carga index.html
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar la imagen enviada desde el cliente
@app.route('/reconocer', methods=['POST'])
def reconocer():
    data = request.json
    image_data = base64.b64decode(data['image'].split(",")[1])
    image = Image.open(io.BytesIO(image_data))
    image = np.array(image)

    # Cargar rostros registrados
    rostros_registrados, nombres_registrados = cargar_rostros()

    # Detectar y reconocer rostros
    unknown_encoding = face_recognition.face_encodings(image)
    if len(unknown_encoding) > 0:
        results = face_recognition.compare_faces(rostros_registrados, unknown_encoding[0])
        if True in results:
            index = results.index(True)
            return jsonify({"nombre": nombres_registrados[index]})
    return jsonify({"nombre": "No encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
