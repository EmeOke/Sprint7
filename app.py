import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide")
st.title("🚗 Dashboard Interactivo de Anuncios de Vehículos")
# Cargar datos
df = pd.read_csv("vehicles_us.csv")
# Crear columna manufacturer si no existe (extraída de model)
df['manufacturer'] = df['model'].str.split().str[0].str.lower()

# Limpiar la columna model para mostrar nombres completos
df['model'] = df['model'].str.title()  # Capitalizar cada palabra
# Sidebar para filtros
st.sidebar.header("🔍 Filtros")
# Rango de año del modelo
year_min = int(df["model_year"].min())
year_max = int(df["model_year"].max())
year_range = st.sidebar.slider("Rango de año del modelo", year_min, year_max, (year_min, year_max))
# Condición del vehículo
condition_options = df["condition"].dropna().unique().tolist()
condition_selected = st.sidebar.multiselect("Condición del vehículo", options=condition_options, default=condition_options)
# Filtro por marca (manufacturer)
manufacturer_options = sorted(df["manufacturer"].dropna().unique().tolist())
manufacturer_selected = st.sidebar.multiselect("Marca del vehículo", options=manufacturer_options, default=manufacturer_options)
# Filtro de color para los gráficos
color_options = ["manufacturer", "model", "condition", "fuel", "type", "transmission", "paint_color"]
color_selected = st.sidebar.selectbox("Categoría para colorear gráficos:", options=color_options, index=0)  # manufacturer por defecto
# Filtrar DataFrame según filtros seleccionados
df_filtered = df[
    (df["model_year"] >= year_range[0]) &
    (df["model_year"] <= year_range[1]) &
    (df["condition"].isin(condition_selected)) &
    (df["manufacturer"].isin(manufacturer_selected))
]
# Mostrar primeras filas del dataframe filtrado
st.subheader("📄 Primeras filas del dataset filtrado:")
st.dataframe(df_filtered.head())
# Botón para histograma de precios
if st.button("📊 Mostrar histograma de precios"):
    fig = px.histogram(
        df_filtered,
        x="price",
        color=color_selected,
        nbins=50,
        title=f"Distribución de Precios por {color_selected.capitalize()}"
    )
    fig.update_layout(bargap=0.1)
    fig.update_traces(marker_line_width=0.5, opacity=0.8)
    st.plotly_chart(fig, use_container_width=True)
# Botón para gráfico de dispersión animado
if st.button("📈 Mostrar gráfico de dispersión animado"):
    # Limpiar datos para animación
    df_filtered_no_na = df_filtered.dropna(subset=["odometer", "model_year", "price", "model"])
    df_filtered_no_na = df_filtered_no_na[df_filtered_no_na["odometer"] > 0]
    df_filtered_no_na = df_filtered_no_na.sort_values("model_year")
    
    # Limitar cantidad de puntos para mejor rendimiento
    if len(df_filtered_no_na) > 3000:
        df_filtered_no_na = df_filtered_no_na.sample(3000, random_state=42)
        # Volver a ordenar después del sampling
        df_filtered_no_na = df_filtered_no_na.sort_values("model_year")
    
    # Convertir model_year a entero para asegurar orden numérico
    df_filtered_no_na["model_year"] = df_filtered_no_na["model_year"].astype(int)
    
    # Crear información adicional para hover
    df_filtered_no_na["info"] = df_filtered_no_na["model"] + " (" + df_filtered_no_na["manufacturer"].str.title() + ")"
    
    # Mostrar información sobre las marcas y modelos únicos
    if color_selected == "manufacturer":
        st.write(f"🏭 **Marcas únicas en los datos filtrados:** {df_filtered_no_na['manufacturer'].nunique()}")
        st.write(f"📈 **Primeras 10 marcas más frecuentes:**")
        top_items = df_filtered_no_na['manufacturer'].str.title().value_counts().head(10)
    else:
        st.write(f"📊 **{color_selected.capitalize()} únicos en los datos filtrados:** {df_filtered_no_na[color_selected].nunique()}")
        st.write(f"📈 **Primeros 10 {color_selected} más frecuentes:**")
        top_items = df_filtered_no_na[color_selected].value_counts().head(10)
    
    for item, count in top_items.items():
        st.write(f"• {item}: {count} anuncios")
    
    # Crear una columna para colorear que tenga formato consistente
    if color_selected == "manufacturer":
        df_filtered_no_na["color_column"] = df_filtered_no_na["manufacturer"].str.title()
    else:
        df_filtered_no_na["color_column"] = df_filtered_no_na[color_selected]
    
    fig = px.scatter(
        df_filtered_no_na,
        x="odometer",
        y="price",
        color="color_column",
        size="odometer",
        size_max=40,
        animation_frame="model_year",
        hover_data=["info", "condition", "fuel"],
        title=f"Precio vs Kilometraje animado por Año del Modelo - Coloreado por {color_selected.capitalize()}",
        color_discrete_sequence=px.colors.qualitative.Set1,  # Paleta con colores más distintivos para marcas
        opacity=0.8  # Hacer las burbujas semi-transparentes
    )
    
    # Personalizar hover template
    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>" +
                      "Kilometraje: %{x:,.0f}<br>" +
                      "Precio: $%{y:,.0f}<br>" +
                      "Condición: %{customdata[1]}<br>" +
                      "Combustible: %{customdata[2]}<br>" +
                      "<extra></extra>"
    )
    
    # Configurar el orden de la animación explícitamente
    fig.update_layout(
        showlegend=True,
        # Asegurar que los frames están en orden numérico
        sliders=[{
            "currentvalue": {"prefix": "Año: "},
            "steps": [
                {"args": [
                    [year],
                    {"frame": {"duration": 300, "redraw": True},
                     "mode": "immediate",
                     "transition": {"duration": 300}}
                ],
                "label": str(year),
                "method": "animate"}
                for year in sorted(df_filtered_no_na["model_year"].unique())
            ]
        }]
    )
    
    # Mejorar la apariencia de las burbujas
    fig.update_traces(
        marker=dict(
            line=dict(width=2, color='white'),  # Borde blanco más grueso para mejor distinción
            opacity=0.8  # Transparencia
        )
    )
    
    # Mejorar la leyenda para marcas
    fig.update_layout(
        legend=dict(
            title=f"{color_selected.capitalize()}",
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.01
        )
    )
    
    # Configurar los frames en orden
    fig.frames = [
        {"data": fig.frames[i].data, "name": str(year)}
        for i, year in enumerate(sorted(df_filtered_no_na["model_year"].unique()))
    ]
    
    st.plotly_chart(fig, use_container_width=True)