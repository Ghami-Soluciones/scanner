import mysql.connector
import cv2

# Conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",        # Cambia esto si usas otro servidor
        user="root",             # Usuario de MySQL
        password="", # Contraseña del usuario
        database="reconocimiento"# Tu base de datos
    )

# Función para cargar imágenes en la base de datos
def cargar_imagen(nombre, ruta_imagen):
    # Leer la imagen
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print(f"No se pudo leer la imagen en {ruta_imagen}")
        return

    # Convertir la imagen a bytes para almacenarla
    _, buffer = cv2.imencode('.jpg', imagen)
    imagen_bytes = buffer.tobytes()

    # Conexión a la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insertar datos en la tabla
    sql = "INSERT INTO rostros (nombre, foto) VALUES (%s, %s)"
    cursor.execute(sql, (nombre, imagen_bytes))

    conn.commit()
    print(f"Imagen de {nombre} cargada correctamente.")
    conn.close()

# Subir imágenes con nombres
if __name__ == "__main__":
    cargar_imagen("Shadow", "img/shadow.jpg")
    cargar_imagen("Sonic", "img/sonic.jpg")
