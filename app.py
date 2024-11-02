import cv2
import yolov5
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Detección de Objetos en Imágenes",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilo CSS para tipografías y ajuste visual
st.markdown(
    """
    <style>
        /* Fuentes personalizadas */
        @import url('https://fonts.googleapis.com/css2?family=Inter&family=Lexend:wght@600&display=swap');
        /* Configuración de títulos */
        h1, h2, h3 {
            font-family: 'Lexend', sans-serif;
        }
        /* Configuración de párrafos */
        p, label, .stButton>button {
            font-family: 'Inter', sans-serif;
        }
        /* Imagen centrada al cargar */
        .centered-img {
            display: flex;
            align-items: center;
            justify-content: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Configuración de YOLOv5
model = yolov5.load('yolov5s.pt')
model.conf = 0.25  # Confianza mínima para detección
model.iou = 0.45  # Umbral de superposición
model.agnostic = False  # Detección sin clase específica
model.multi_label = False  # Múltiples etiquetas por cuadro
model.max_det = 1000  # Máximo de detecciones por imagen

# Título de la aplicación
st.title("Detección de Objetos en Imágenes")

# Parámetros en barra lateral
with st.sidebar:
    st.subheader('Parámetros de Configuración')
    model.iou = st.slider('Seleccione el IoU', 0.0, 1.0)
    model.conf = st.slider('Seleccione el Confidence', 0.0, 1.0)

# Imagen inicial
st.markdown("<div class='centered-img'>", unsafe_allow_html=True)
image_path = "Yoru - Deteccion de objetos e imagenes.png"  # Cambia por el nombre de tu archivo de imagen
image = Image.open(image_path)
st.image(image, caption="Imagen inicial", use_column_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Captura de imagen
picture = st.camera_input("Capturar foto", label_visibility='visible')

if picture:
    bytes_data = picture.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
  
    # Inferencia y visualización
    results = model(cv2_img)
    predictions = results.pred[0]
    boxes = predictions[:, :4] 
    scores = predictions[:, 4]
    categories = predictions[:, 5]

    col1, col2 = st.columns(2)

    with col1:
        results.render()
        st.image(cv2_img, channels='BGR')

    with col2:
        label_names = model.names
        category_count = {}
        for category in categories:
            category_count[category] = category_count.get(category, 0) + 1

        data = [{"Categoría": label_names[int(cat)], "Cantidad": count} for cat, count in category_count.items()]
        data2 = pd.DataFrame(data)
        
        df_sum = data2.groupby('Categoría')['Cantidad'].sum().reset_index()
        st.write(df_sum)
