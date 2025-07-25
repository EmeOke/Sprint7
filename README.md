Dashboard Interactivo de Anuncios de Vehículos 🚗📊
Este proyecto es una aplicación web interactiva desarrollada con Streamlit que permite explorar un conjunto de datos de anuncios de vehículos en EE.UU.
La aplicación ofrece visualizaciones dinámicas para analizar precios, años de modelos, condiciones y otras características de los vehículos.

Funcionalidades ✨
Filtros interactivos por año del modelo, condición y marca del vehículo.

Visualización de histogramas de precios con colores según categorías seleccionadas.

Gráfico de dispersión animado que muestra la relación entre kilómetro recorrido y precio a lo largo de los años del modelo.

Información detallada al pasar el cursor sobre cada punto en los gráficos.

Instalación ⚙️
Clona este repositorio:

git clone https://github.com/EmeOke/Sprint7.git
cd Sprint7

Crea un entorno virtual y actívalo:

python -m venv vehicles_env
source vehicles_env/bin/activate (Linux/Mac)
vehicles_env\Scripts\activate (Windows)

Instala las dependencias:

pip install -r requirements.txt

Uso 🚀
Para ejecutar la aplicación localmente, usa:

streamlit run app.py

Esto abrirá la app en tu navegador en http://localhost:8501

Estructura del proyecto 🗂️
.
├── README.md
├── app.py
├── vehicles_us.csv
├── requirements.txt
└── notebooks
  └── EDA.ipynb

Despliegue ☁️
La aplicación está preparada para ser desplegada en Render.com o cualquier servicio similar que soporte Python y Streamlit.

Licencia 📄
Este proyecto es para fines educativos.

¡Disfruta explorando los datos de vehículos! 🚗📈
