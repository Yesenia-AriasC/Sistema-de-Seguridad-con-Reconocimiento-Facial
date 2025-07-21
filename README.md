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

Explica acá lo de el environment

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
