import streamlit as st
import cv2
import numpy as np
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model
import platform

# Agregar estilo CSS para las fuentes y centrar la imagen
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@700&family=Inter:wght@400&display=swap');
        body {
            font-family: 'Inter', sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Lexend', sans-serif;
        }
        .center-img {
            display: flex;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

# Muestra la versión de Python junto con detalles adicionales
st.write("Versión de Python:", platform.python_version())

# Cargar el modelo preentrenado
model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Título de la aplicación con la tipografía cambiada
st.title("Reconocimiento de Imágenes")

# Cargar y mostrar una imagen PNG centrada
image = Image.open('OIG5.jpg')
st.markdown('<div class="center-img">', unsafe_allow_html=True)
st.image(image, width=350)
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar para los detalles del modelo
with st.sidebar:
    st.subheader("Usando un modelo entrenado en Teachable Machine puedes usarlo en esta app para identificar")

# Obtener una imagen de la cámara
img_file_buffer = st.camera_input("Toma una Foto")

if img_file_buffer is not None:
    # Leer la imagen del buffer
    img = Image.open(img_file_buffer)

    # Redimensionar la imagen
    newsize = (224, 224)
    img = img.resize(newsize)

    # Convertir la imagen a un array numpy
    img_array = np.array(img)

    # Normalizar la imagen
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    # Cargar la imagen en el array de entrada
    data[0] = normalized_image_array

    # Ejecutar la inferencia
    prediction = model.predict(data)
    
    # Mostrar el resultado basado en la predicción
    if prediction[0][0] > 0.5:
        st.header('Izquierda, con Probabilidad: ' + str(prediction[0][0]))
    if prediction[0][1] > 0.5:
        st.header('Arriba, con Probabilidad: ' + str(prediction[0][1]))
    # Descomentar si tienes más categorías
    # if prediction[0][2] > 0.5:
    #     st.header('Derecha, con Probabilidad: ' + str(prediction[0][2]))
