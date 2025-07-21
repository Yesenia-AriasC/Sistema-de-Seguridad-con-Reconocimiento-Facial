# 🎥 Sistema de Seguridad con Reconocimiento Facial

Este proyecto implementa un sistema de seguridad en tiempo real basado en **reconocimiento facial**, utilizando una cámara web. Cuando una persona autorizada es detectada, el sistema muestra su información y registra su ingreso en un archivo `.csv` solo una vez por día.

## Características

- Detección de rostros en tiempo real con webcam
- Identificación mediante codificaciones faciales (`face_recognition`)
- Registro automático del ingreso (ID, nombre, fecha, hora)
- Interfaz gráfica con OpenCV (UI mínima + ícono de confirmación)

---

## Requisitos

### ⚙️ Configuración del entorno de trabajo

Para este proyecto utilicé **Python 3.10.0** y creé un entorno virtual en Visual Studio Code. Aquí te explico los pasos que seguí:

1. **Abrir la carpeta del proyecto en Visual Studio Code**

   * Abre la carpeta del proyecto en VS Code.
   * Luego abre una nueva terminal integrada (puedes guiarte con este video: [Cómo abrir terminal en VS Code](https://www.youtube.com/watch?v=F0V5AbxwzSE)).

2. **Instalar Python 3.10.0** (o usar una versión compatible que ya tengas instalada).

3. **Crear un entorno virtual con Python 3.10**
   En la terminal, ejecuta:

   ```bash
   python3.10 -m venv py310env
   ```

4. **Activar el entorno virtual**
   En sistemas Unix/MacOS:

   ```bash
   source py310env/bin/activate
   ```

   Para verificar que estás usando la versión correcta de Python, puedes ejecutar:

   ```bash
   python --version
   ```

5. **Instalar las librerías necesarias**

   ```bash
   pip install cmake
   pip install face_recognition
   ```

   ⚠️ **Nota sobre Dlib:** Esta librería puede presentar errores al instalarla directamente. En mi caso, la instalé manualmente así:

   ```bash
   git clone https://github.com/davisking/dlib.git
   cd dlib
   python setup.py install
   ```

   Luego, para asegurarme de que quedara bien integrada, también ejecuté:

   ```bash
   pip install dlib
   ```

   Esto generó una carpeta llamada `dlib` dentro de mi carpeta del proyecto, y funcionó correctamente.

6. **Verificar librerías instaladas**

   Puedes ver el listado de paquetes instalados con:

   ```bash
   pip list
   ```

![](https://raw.githubusercontent.com/Yesenia-AriasC/Sistema-de-Seguridad-con-Reconocimiento-Facial/refs/heads/main/Doc/•%20(py318env)%20(base)%20nayibeyeseniaariascortez%40192%20dlib%20%26%20pip%20list.png|500)


## Estructura del proyecto

```
surveillance_entry_system/
│
├── main.py                      # Script principal del sistema
├── Persona_data.csv             # Datos de las personas (ID, nombre, imagen, etc.)
├── registro_log.csv             # Registro de entradas exitosas
├── checkmark.png                # Ícono que se muestra si la persona es reconocida
├── Persona_imagenes/            # Carpeta con imágenes de las personas autorizadas
```

## Cómo usar

1. Coloca las imágenes de las personas en la carpeta `Persona_imagenes/`.
2. Asegúrate de que cada imagen esté asociada en `Persona_data.csv` con su nombre, ID, archivo de imagen y especialidad.
3. Ejecuta el archivo principal:

```bash
python main.py
```

4. Al detectar y reconocer una cara:

   * El sistema mostrará su nombre y datos en pantalla.
   * Se mostrará un fondo verde semitransparente con un ícono de check.
   * Se registrará en `registro_log.csv`.

> El sistema evita registrar múltiples veces a la misma persona el mismo día.



## Funcionamiento interno

* **Carga de datos:** Usa `csv.DictReader` para leer los datos desde `Persona_data.csv`, y codifica las imágenes con `face_recognition`.
* **Reconocimiento:** Se escalan los frames para eficiencia, se detecta y codifica la cara en tiempo real y se compara con las codificaciones conocidas.
* **Registro:** Se escribe una fila en el archivo `registro_log.csv` solo si la persona aún no ha sido registrada ese día.
* **Interfaz:** OpenCV muestra la cámara, dibuja la UI de escaneo y la tarjeta de perfil con el nombre, ID, especialidad e imagen de la persona.



##  Ejemplo de `registro_log.csv`

```csv
ID,Name,Date,Time
12345,Nayibe Yesenia,2025-07-20,08:45:12
```



##  Limitaciones actuales

* La UI es básica (solo OpenCV, sin botones ni menús).
* Solo funciona con una cámara.
* No maneja múltiples rostros por frame de forma simultánea.
* No se ha probado con grandes cantidades de datos.
* No hay autenticación ni cifrado del archivo de registro.



##  Posibles mejoras futuras

* Exportar los registros a una base de datos.
* Añadir soporte para múltiples cámaras.
* Usar una interfaz más amigable con `tkinter` o `PyQt`.
* Enviar notificaciones por correo o mensajes al registrar un ingreso.
* Crear un sistema de roles (estudiante, visitante, etc.).



## Vista previa

![Checkmark](checkmark.png)



## Créditos

Este proyecto está basado en un código original de código base disponible públicamente en GitHub.

Las modificaciones realizadas incluyen:
- Traducción completa al español
- Adaptación del sistema a un caso de seguridad con registro único en CSV
- Organización y documentación del proyecto

Modificado con fines de aprendizaje por una estudiante de Estadística de la Universidad Nacional de Colombia.




## 📜 Licencia

Este proyecto es de uso académico. Puedes modificarlo libremente para aprendizaje o desarrollo personal.

```


