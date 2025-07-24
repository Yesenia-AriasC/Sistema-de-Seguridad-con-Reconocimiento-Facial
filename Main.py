import cv2
import face_recognition
import numpy as np
import os
import csv
import time
from datetime import datetime

#------------RECUERDA ACTIVAR EN VSCODE EL ENTORNO py310env-------------#

# --- Configuración e inicio ---
RUTA_IMAGENES = '/Users/nayibeyeseniaariascortez/Desktop/surveillance_entry_system/Persona_imagenes'
ARCHIVO_DATOS = '/Users/nayibeyeseniaariascortez/Desktop/surveillance_entry_system/Persona_data.csv'
ICONO_CHULO = '/Users/nayibeyeseniaariascortez/Desktop/surveillance_entry_system/checkmark.png'
ARCHIVO_REGISTRO = 'registro_log.csv'  # Archivo de registro de asistencia
FACTOR_REDUCCION = 4  # Factor de reducción para procesar imágenes más rápido
TIEMPO_ESPERA_EXITO = 5  # Tiempo de espera (en segundos) antes de volver a registrar asistencia
TOLERANCIA_COINCIDENCIA = 0.45  # Nivel de precisión para comparar rostros

# --- Funciones auxiliares ---

def cargar_datos_personas():
    """
    IMPLEMENTACIÓN DEL MÉTODO 2:
    Carga los datos de los estudiantes desde el archivo CSV y codifica (encodindg) 
    MÚLTIPLES imágenes por estudiante. Busca todos los archivos de imagen
    en la carpeta persona_imagenes que comiencen con el nombre base
    del archivo listado en el CSV (por ejemplo: 'Muhammad_Bilal').
    
    La primera parte lee los datos del csv student data y exrtae los datos de cada persona.
    La segunda parte busca en la carpeta de imágenes todas las imágenes que comiencen con el nombre base
    del archivo y las codifica. Si encuentra imágenes, las codifica y las almacena
    en la lista known_face_encodings. Si no encuentra imágenes, muestra una advertencia.
    Si no encuentra el archivo CSV, muestra un mensaje de error y retorna listas vacías.     
    """
    codificaciones_conocidas = []
    nombres_conocidos = []
    mapa_datos_persona = {}

    print("Cargando datos de personas y codificando rostros...")
    try:
        with open(ARCHIVO_DATOS, mode='r', newline='') as archivo_csv:
            lector = csv.DictReader(archivo_csv)
            for fila in lector:
                nombre_persona = fila['Name']
                nombre_base = os.path.splitext(fila['ImageFile'])[0]
                mapa_datos_persona[nombre_persona] = fila

                imagenes_encontradas = 0
                for archivo in os.listdir(RUTA_IMAGENES):
                    if archivo.startswith(nombre_base):
                        ruta_imagen = os.path.join(RUTA_IMAGENES, archivo)
                        try:
                            imagen = face_recognition.load_image_file(ruta_imagen)
                            codificaciones = face_recognition.face_encodings(imagen) # (podriamos usar HOG o CNN para hacer codificaciones) face_encodings devuelve una lista de codificaciones llamando internamente a face_locations(imagen) que usa HOG  Histogram of oriented gradients.
                            print("Codificación exitosa")
                            if codificaciones:
                                codificaciones_conocidas.append(codificaciones[0])
                                nombres_conocidos.append(nombre_persona)
                                imagenes_encontradas += 1
                            else:
                                print(f"Advertencia: No se encontró rostro en {archivo}. Se omitirá.")
                        except Exception as e:
                            print(f"Error procesando {archivo}: {e}")
                if imagenes_encontradas == 0:
                    print(f"Advertencia: No se encontraron imágenes para {nombre_persona} que comiencen con '{nombre_base}'")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ARCHIVO_DATOS}.")
        return [], [], {}

    print(f"...Carga completa. Se codificaron {len(codificaciones_conocidas)} imágenes.")
    return codificaciones_conocidas, nombres_conocidos, mapa_datos_persona

def registrar_ingreso(id_persona, nombre_persona):
    '''sirve para registrar la asistencia en el archivo registro.csv
    Esta función verifica si el estudiante ya está registrado hoy. Si no, lo agrega al registro.
    La función toma el ID del estudiante y su nombre, y registra la fecha y hora actuales.
    Si el archivo registro.csv no existe, lo crea y agrega los encabezados.
    Si el estudiante ya está registrado hoy, no hace nada.
    Si el estudiante no está registrado, agrega una nueva fila con el ID, nombre, fecha
    '''
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    hora_ahora = datetime.now().strftime('%H:%M:%S')
    try:
        with open(ARCHIVO_REGISTRO, 'r', newline='') as f:
            for fila in csv.reader(f):
                if len(fila) == 4 and fila[0] == id_persona and fila[2] == fecha_hoy:
                    return
    except FileNotFoundError:
        pass
    with open(ARCHIVO_REGISTRO, 'a', newline='') as f:
        escritor = csv.writer(f)
        if f.tell() == 0:
            escritor.writerow(['ID', 'Nombre', 'Fecha', 'Hora'])
        escritor.writerow([id_persona, nombre_persona, fecha_hoy, hora_ahora])
        print(f"¡Hola, {nombre_persona}! Tu ingreso ha sido registrado exitosamente.") # no se muestra en el UI

def superponer_transparente(fondo, superposicion, x, y): #para poner el icono de exito de registro de ingreso al csv
    '''Superpone una imagen con transparencia sobre otra imagen en una posición específica.
    Esta función toma una imagen de fondo y una imagen de superposición (overlay) con un canal alfa.
    La imagen de superposición se coloca en la posición (x, y) del fondo.
    Si la posición está fuera de los límites del fondo, no se realiza ninguna superposición.
    La función devuelve la imagen de fondo con la superposición aplicada.
    Los parámetros son: 
    - background: La imagen de fondo sobre la que se superpone la imagen.
    - overlay: La imagen de superposición que contiene un canal alfa (transparencia).
    - x: La coordenada x donde se coloca la imagen de superposición.
    - y: La coordenada y donde se coloca la imagen de superposición.
    La función calcula el área de interés (ROI) en el fondo donde se superpondrá la imagen.
    Si la imagen de superposición está fuera de los límites del fondo, no se realiza ninguna acción.
    La imagen de superposición se aplica al fondo utilizando el canal alfa para manejar la transparencia.
    La función devuelve la imagen de fondo modificada con la superposición aplicada.
    '''
    alto_f, ancho_f, _ = fondo.shape
    alto, ancho, _ = superposicion.shape
    imagen_super = superposicion[:, :, :3]
    mascara = superposicion[:, :, 3:] / 255.0
    if x >= ancho_f or y >= alto_f:
        return fondo
    alto, ancho = min(alto, alto_f - y), min(ancho, ancho_f - x)
    region = fondo[y:y+alto, x:x+ancho]
    fondo[y:y+alto, x:x+ancho] = (1.0 - mascara[:alto, :ancho]) * region + mascara[:alto, :ancho] * imagen_super[:alto, :ancho]
    return fondo

def dibujar_perfil(canvas, info_persona, foto_perfil):
    '''''Dibuja un perfil de usuario en el canvas.
    Esta función toma un canvas, la información de una persona y una foto de perfil.
    Dibuja un rectángulo para el perfil, coloca la foto redimensionada y muestra el nombre, ID y carrera de la persona.
    Los parámetros son:
    - canvas: La imagen donde se dibuja el perfil.
    - info_persona: Un diccionario que contiene la información de la persona (Name, ID, Major).
    - foto_perfil: La imagen de perfil de la persona.
    La función calcula la posición y el tamaño del rectángulo del perfil en el canvas.
    Si se proporciona una foto de perfil, la redimensiona a 150x150 píxeles y la coloca en el canvas.
    Luego, dibuja el nombre, ID y carrera de la persona en el canvas.
    La función utiliza la fuente FONT_HERSHEY_DUPLEX para el texto.
    El rectángulo del perfil se dibuja con un color de fondo blanco y un borde de color púrpura.
    El nombre se coloca debajo de la foto, y el ID y la carrera se muestran en rectángulos separados debajo del nombre.
    '''
    ancho_canvas = canvas.shape[1]
    x, y, w, h = ancho_canvas - 320, 80, 300, 380
    cv2.rectangle(canvas, (x, y), (x + w, y + h), (255, 255, 255), cv2.FILLED)
    cv2.rectangle(canvas, (x, y), (x + w, y + h), (224, 200, 80), 3) # (128, 80, 224)

    if foto_perfil is not None:
        foto_redimensionada = cv2.resize(foto_perfil, (150, 150))
        pos_y = y + 20
        pos_x = x + (w - 150) // 2
        canvas[pos_y : pos_y + 150, pos_x : pos_x + 150] = foto_redimensionada

    fuente = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(canvas, info_persona['Name'], (x + 20, y + 210), fuente, 0.8, (0, 0, 0), 1)
    cv2.rectangle(canvas, (x + 20, y + 240), (x + w - 20, y + 270), (128, 80, 224), cv2.FILLED)
    cv2.putText(canvas, f"ID: {info_persona['ID']}", (x + 30, y + 262), fuente, 0.6, (255, 255, 255), 1)
    cv2.rectangle(canvas, (x + 20, y + 280), (x + w - 20, y + 310), (128, 80, 224), cv2.FILLED)
    cv2.putText(canvas, f"Carrera: {info_persona['Major']}", (x + 30, y + 302), fuente, 0.6, (255, 255, 255), 1)

def dibujar_ui_predeterminada(canvas):
    '''Hace una interfaz grafica que aparece cuando el sistema está esperando por reconocer o no un rostro.
    Esta función dibuja una tarjeta de interfaz de usuario en el lienzo (canvas) que invita al usuario a escanear su rostro.
    La tarjeta tiene un fondo blanco y un borde morado, y muestra un mensaje de texto.
    Los parámetros son:         
    - canvas: La imagen en la que se dibuja la tarjeta de interfaz de usuario.
    La función calcula la posición y el tamaño de la tarjeta en función del ancho del lienzo
    y dibuja un rectángulo blanco para el fondo. Luego, dibuja un borde morado alrededor de la tarjeta.
    Finalmente, muestra un mensaje de texto invitando al usuario a escanear su rostro.
    Esta tarjeta se utiliza como una interfaz de usuario predeterminada cuando
    el sistema está esperando que el usuario escanee su rostro.
    '''
    ancho = canvas.shape[1]
    x, y, w, h = ancho - 320, 80, 300, 380
    cv2.rectangle(canvas, (x, y), (x + w, y + h), (255, 255, 255), cv2.FILLED)
    cv2.rectangle(canvas, (x, y), (x + w, y + h), (224, 200, 80), 3) # 128, 80, 224
    cv2.putText(canvas, "Esperando...", (x + 40, y + 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1)

def main():
    '''Función principal que inicia el sistema de vigilancia IA.
    Esta función carga los datos de las personas desde un archivo CSV, configura la cámara,
    y entra en un bucle para capturar frames de video. Procesa cada frame para detectar rostros,
    codifica los rostros y compara las codificaciones con las conocidas. Si se detecta un rostro conocido,
    actualiza el estado del sistema a "EXITO" y registra el ingreso de la persona.
    La función también maneja la interfaz de usuario, mostrando mensajes y superponiendo iconos de éxito.
    Los parámetros son:
    - No recibe parámetros, ya que es la función principal del programa.
    La función comienza cargando los datos de las personas y configurando la cámara.
    Si no se cargan los datos correctamente, termina la ejecución.
    Luego, entra en un bucle infinito donde captura frames de video y los procesa.
    Dependiendo del estado del sistema (ESPERANDO o EXITO), realiza diferentes acciones:
    - En el estado "ESPERANDO", reduce el tamaño del frame, convierte el color a RGB,
      detecta rostros y codifica los rostros encontrados. Si se encuentra un rostro conocido,
      actualiza el estado a "EXITO" y registra el ingreso.
    - En el estado "EXITO", superpone un icono de éxito, muestra un mensaje de éxito,
      y muestra la información del perfil de la persona reconocida. Después de un tiempo de espera,
      vuelve al estado "ESPERANDO".
    La función también maneja la visualización del canvas con los frames procesados y la interfaz de usuario.
    Finalmente, libera la cámara y cierra todas las ventanas al finalizar.
    '''
    # Cargar datos de personas y codificaciones
    codificaciones, nombres, mapa_datos = cargar_datos_personas()
    if not codificaciones: return

    # Configuración de la cámara y canvas
    camara = cv2.VideoCapture(0)
    ancho_cam = int(camara.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto_cam = int(camara.get(cv2.CAP_PROP_FRAME_HEIGHT))
    ancho_canvas, alto_canvas = ancho_cam + 340, alto_cam + 60

    try:
        icono_chulo = cv2.imread(ICONO_CHULO, cv2.IMREAD_UNCHANGED)
        icono_chulo = cv2.resize(icono_chulo, (128, 128))
    except Exception:
        icono_chulo = None

    estado = "ESPERANDO"
    tiempo_exito = 0
    datos_ultimo = None
    procesar_frame = True
    ubicaciones_rostros = []

    while True:
        ret, frame = camara.read()
        if not ret: break

        canvas = np.full((alto_canvas, ancho_canvas, 3), (240, 235, 216), np.uint8)
        cv2.rectangle(canvas, (0, 0), (ancho_canvas, 60), (224, 200, 80), cv2.FILLED) # (128, 80, 224)
        cv2.putText(canvas, "Sistema de Vigilancia IA", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        canvas[60:60+alto_cam, 20:20+ancho_cam] = frame

        if estado == "ESPERANDO":
            if procesar_frame:
                # 🔹 Paso 1: Reducción de tamaño para acelerar el procesamiento
                frame_pequeno = cv2.resize(frame, (0, 0), fx=1.0/FACTOR_REDUCCION, fy=1.0/FACTOR_REDUCCION)
                # 🔹 Paso 2: Convertir de BGR (OpenCV) a RGB (lo que espera face_recognition)
                rgb = cv2.cvtColor(frame_pequeno, cv2.COLOR_BGR2RGB)
                # 🔹 Paso 3: 🔥 Uso del modelo preentrenado para detectar caras - usa HOG (Histogram of oriented gradients) aunque podriamos usar CNN pero exige GPU
                ubicaciones_rostros = face_recognition.face_locations(rgb)
                # 🔹 Paso 4: 🔥 Uso del modelo preentrenado para generar codificaciones faciales (vectores de 128 números)
                codificaciones_rostros = face_recognition.face_encodings(rgb, ubicaciones_rostros)

                # 🔹 Paso 5: Comparar las codificaciones de los rostros detectados con las codificaciones conocidas usando distancia euclidiana
                if codificaciones_rostros:
                    distancias = face_recognition.face_distance(codificaciones, codificaciones_rostros[0])
                    # 🔹 Paso 6: Si la distancia es suficientemente baja, el rostro es reconocido, y el sistema actualiza el estado a "EXITO".
                    if len(distancias) > 0:
                        mejor_indice = np.argmin(distancias)
                        if distancias[mejor_indice] < TOLERANCIA_COINCIDENCIA:
                            nombre = nombres[mejor_indice]
                            datos_ultimo = mapa_datos[nombre]
                            estado = "EXITO"
                            tiempo_exito = time.time()
                            registrar_ingreso(datos_ultimo['ID'], datos_ultimo['Name'])

            procesar_frame = not procesar_frame
            if ubicaciones_rostros:
                top, right, bottom, left = ubicaciones_rostros[0]
                top *= FACTOR_REDUCCION; right *= FACTOR_REDUCCION
                bottom *= FACTOR_REDUCCION; left *= FACTOR_REDUCCION
                cv2.rectangle(canvas, (left + 20, top + 60), (right + 20, bottom + 60), (0, 255, 0), 3)
            dibujar_ui_predeterminada(canvas)

        elif estado == "EXITO":
            overlay = canvas[60:60+alto_cam, 20:20+ancho_cam].copy()
            cv2.rectangle(overlay, (0, 0), (ancho_cam, alto_cam), (0, 180, 0), -1) # crea un rectángulo verde
            cv2.addWeighted(overlay, 0.3, canvas[60:60+alto_cam, 20:20+ancho_cam], 0.7, 0, canvas[60:60+alto_cam, 20:20+ancho_cam]) # Crea la transparencia
            if icono_chulo is not None: #tamaño del icono
                x_icono = 20 + (ancho_cam - 128) // 2
                y_icono = 60 + (alto_cam - 128) // 2 - 30
                superponer_transparente(canvas, icono_chulo, x_icono, y_icono) #superponer el icono
            mensaje = "Tu ingreso ha sido registrado"
            cv2.putText(canvas, mensaje, (20 + ancho_cam // 2 - 180, 60 + alto_cam // 2 + 80), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255, 255, 255), 2)
            if datos_ultimo:
                ruta_foto = os.path.join(RUTA_IMAGENES, datos_ultimo['ImageFile'])
                foto_perfil = cv2.imread(ruta_foto)
                dibujar_perfil(canvas, datos_ultimo, foto_perfil)
            if time.time() - tiempo_exito > TIEMPO_ESPERA_EXITO:
                estado = "ESPERANDO"
                datos_ultimo = None
                ubicaciones_rostros = []

        cv2.imshow('Sistema de Vigilancia IA', canvas)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camara.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
