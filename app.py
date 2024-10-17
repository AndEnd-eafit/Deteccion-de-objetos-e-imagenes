import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import paho.mqtt.client as paho
import json
from googletrans import Translator

# Función de callback cuando se publica un mensaje
def on_publish(client, userdata, result):
    print("El dato ha sido publicado \n")
    pass

# Función de callback para la recepción de mensajes
def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

# Configuración de MQTT
broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

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

st.title("INTERFACES MULTIMODALES")
st.subheader("CONTROL POR VOZ")

# Mostrar imagen centrada
image = Image.open('voice_ctrl.jpg')
st.markdown('<div class="center-img">', unsafe_allow_html=True)
st.image(image, width=200)
st.markdown('</div>', unsafe_allow_html=True)

# Botón y reconocimiento de voz
st.write("Toca el Botón y habla")

stt_button = Button(label="Inicio", width=200)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
"""))

# Resultado de la voz capturada
result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
        client1.on_publish = on_publish
        client1.connect(broker, port)

        # Publicar el mensaje de voz en el topic MQTT
        message = json.dumps({"Act1": result.get("GET_TEXT").strip()})
        ret = client1.publish("voice_ctrl", message)

    # Crear un directorio temporal si no existe
    try:
        os.mkdir("temp")
    except FileExistsError:
        pass
        
        # Agrupar los datos por la columna "Categoría" y sumar las cantidades
        df_sum = data2.groupby('Categoría')['Cantidad'].sum().reset_index() 
        st.dataframe(df_sum)  # Mostrar DataFrame en la interfaz
