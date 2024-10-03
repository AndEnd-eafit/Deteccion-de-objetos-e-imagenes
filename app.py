import cv2
import yolov5
import streamlit as st
import numpy as np
import pandas as pd

# Cargar modelo preentrenado
model = yolov5.load('yolov5s.pt')

# Configurar parámetros del modelo
model.conf = 0.25  # Umbral de confianza para NMS
model.iou = 0.45   # Umbral de IoU para NMS
model.agnostic = False  # NMS clase-agnóstica
model.multi_label = False  # NMS múltiples etiquetas por caja
model.max_det = 1000  # Número máximo de detecciones por imagen

# Agregar estilo CSS para las fuentes
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@700&family=Inter:wght@400&display=swap');
        body {
            font-family: 'Inter', sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Lexend', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Detección de Objetos en Imágenes")

with st.sidebar:
    st.subheader('Parámetros de Configuración')
    model.iou = st.slider('Seleccione el IoU', 0.0, 1.0)
    st.write('IOU:', model.iou)

with st.sidebar:
    model.conf = st.slider('Seleccione el Confidence', 0.0, 1.0)
    st.write('Conf:', model.conf)

picture = st.camera_input("Capturar foto", label_visibility='visible')

if picture:
    bytes_data = picture.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
  
    # Realizar inferencia
    results = model(cv2_img)

    # Analizar resultados
    predictions = results.pred[0]
    boxes = predictions[:, :4] 
    scores = predictions[:, 4]
    categories = predictions[:, 5]

    col1, col2 = st.columns(2)

    with col1:
        # Mostrar cajas de detección en la imagen
        results.render()
        # Mostrar imagen con detecciones 
        st.image(cv2_img, channels='BGR')

    with col2:      
        # Obtener nombres de etiquetas
        label_names = model.names
        # Contar categorías
        category_count = {}
        for category in categories:
            if category in category_count:
                category_count[category] += 1
            else:
                category_count[category] = 1        

        data = []        
        # Imprimir conteos y etiquetas de categorías
        for category, count in category_count.items():
            label = label_names[int(category)]            
            data.append({"Categoría": label, "Cantidad": count})
        data2 = pd.DataFrame(data)
        
        # Agrupar los datos por la columna "Categoría" y sumar las cantidades
        df_sum = data2.groupby('Categoría')['Cantidad'].sum().reset_index() 
        st.dataframe(df_sum)  # Mostrar DataFrame en la interfaz
