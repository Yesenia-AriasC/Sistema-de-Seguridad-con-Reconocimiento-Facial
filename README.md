# 🎥 Sistema de Seguridad con Reconocimiento Facial

Este proyecto implementa un sistema de seguridad en tiempo real basado en **reconocimiento facial**, utilizando una cámara web. Cuando una persona autorizada es detectada, el sistema muestra su información y registra su ingreso en un archivo `.csv` solo una vez por día.

## Características

- Detección de rostros en tiempo real con webcam
- Identificación mediante codificaciones faciales (`face_recognition`)
- Registro automático del ingreso (ID, nombre, fecha, hora)
- Interfaz gráfica con OpenCV (UI mínima + ícono de confirmación)
- Registro único por día para cada persona

---

## Requisitos

Este proyecto usa Python 3 y las siguientes librerías:

```bash
pip install opencv-python face_recognition numpy
