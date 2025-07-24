
# Sistema de Control de Acceso con Reconocimiento Facial

## Abstract

Este artículo presenta el diseño e implementación de un sistema de control de acceso automatizado mediante reconocimiento facial, basado en técnicas de inteligencia artificial y visión por computador. La solución propuesta utiliza la biblioteca `face_recognition` junto con OpenCV para el procesamiento en tiempo real de imágenes capturadas desde una cámara, permitiendo la detección, codificación y comparación de rostros frente a una base de datos previamente registrada. Cuando se identifica una coincidencia, el sistema registra el evento con los datos correspondientes (identidad, nombre, fecha y hora) en un archivo estructurado tipo CSV.

El sistema está orientado a escenarios que requieren autenticación biométrica confiable y no intrusiva, ofreciendo una alternativa de bajo costo, alto rendimiento y fácil implementación para entornos institucionales o corporativos.

## Palabras clave

**Reconocimiento facial**, **visión por computador**, **inteligencia artificial**, **codificación de imágenes**, **OpenCV**, **face_recognition**

---

## 1. Introducción

El reconocimiento facial basado en aprendizaje profundo ha demostrado ser una de las aplicaciones biométricas más efectivas para la autenticación de identidad en escenarios del mundo real. A diferencia de los métodos tradicionales, los enfoques modernos basados en redes neuronales convolucionales (CNN) permiten extraer representaciones latentes altamente discriminativas, incluso bajo variaciones significativas de iluminación, expresión facial, oclusiones parciales y pose [Parkhi et al., 2015; Schroff et al., 2015].

Este trabajo aborda la implementación de un sistema de control de acceso que, haciendo uso de redes preentrenadas, permita identificar en tiempo real si un individuo pertenece a una base autorizada y registrar automáticamente su ingreso. 

El objetivo del proyecto es desarrollar e implementar un pipeline de reconocimiento facial que integre:

- Captura de video  
- Detección de rostros  
- Extracción de embeddings  
- Verificación de identidad  

Utilizando bibliotecas como `face_recognition` (basada en `dlib`) y `OpenCV`. Se busca validar su desempeño en términos de precisión, robustez y viabilidad.

---

## 2. Metodología

El sistema se estructuró en módulos integrando visión por computador y aprendizaje profundo, usando herramientas open source. La metodología se divide en cinco etapas:

### 2.1 Descripción de los datos

Se recolectaron imágenes faciales de tres participantes en diferentes condiciones. Cada imagen fue almacenada como `.jpg` y etiquetada.

### 2.2 Preparación de datos

Las imágenes fueron:

- Redimensionadas  
- Convertidas a RGB  
- Procesadas con un detector HOG para localizar la región facial.

### 2.3 Codificación de rostros

Cada rostro se convierte en un vector de 128 dimensiones usando una red neuronal convolucional basada en ResNet-34 (dlib). Este vector representa un embedding facial.

### 2.4 Detección y reconocimiento

En tiempo real:

1. Se detecta el rostro usando HOG  
2. Se genera su codificación  
3. Se compara con vectores conocidos mediante distancia euclidiana  
4. Si la distancia < 0.6 → Coincidencia positiva

### 2.5 Registro de acceso

Al encontrar coincidencias:

- Se crea o actualiza un archivo `.csv`
- Se registra nombre, ID, fecha y hora
- Un usuario se registra solo una vez al día

### 2.6 Interfaz visual

- Visualización en tiempo real con `cv2.addWeighted`  
- Overlay con nombre y estado de acceso  

### Diagrama de flujo

```plaintext
Inicio
↓
Carga de datos e imágenes
↓
Inicialización de la cámara
↓
Captura de vídeo en tiempo real
↓
Reducción y conversión de imagen
↓
face_locations
↓
face_encodings
↓
Comparación con rostros conocidos
↓
¿Coincidencia?
→ Sí → Registrar ingreso → Mostrar UI de éxito
→ No → Estado de espera
```


## 3. Resultados

El sistema fue evaluado en condiciones controladas con tres participantes. Resultados:

* Reconocimiento > 90% en condiciones óptimas
* Reconocimiento > 80% con variaciones de luz y pose
* Tiempos de respuesta < 500 ms
* Cada usuario fue registrado solo una vez por día

El sistema resultó ser fluido y efectivo, actualizando correctamente el archivo `.csv` y proporcionando una buena experiencia de usuario.

---

## 4. Limitaciones

* El modelo inicial LBPH + Haarcascade fue reemplazado por CNN + HOG
* Dependencia de buena iluminación
* Menor precisión con rostros no frontales
* Reconoce solo una persona por frame
* No posee una interfaz gráfica amigable para usuarios no técnicos

---

## 5. Conclusiones

Se desarrolló un sistema de control de acceso robusto, preciso y de bajo costo, superando soluciones tradicionales como LBPH y Haarcascade. El sistema es escalable y aplicable en entornos reales. No obstante, su uso en ambientes no controlados requerirá mejoras en robustez y actualización de base de datos.

Este trabajo confirma la utilidad del deep learning para resolver tareas prácticas de reconocimiento facial de forma rápida y sin contacto.

---

## 6. Referencias

* **Cao et al. (2018):** VGGFace2, dataset para reconocimiento facial
* **King (2017):** Deep Metric Learning con dlib
* **OpenCV (n.d.):** Documentación oficial de `cv::detectionroi`
* **Parkhi et al. (2015):** DeepFace con modelos VGG
* **Schroff et al. (2015):** FaceNet y pérdida tipo triplete

