import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import plotly.express as px
import time

# Configuración de la conexión
user = 'root'
password = 'Infersito21'
host = 'localhost'
database = 'supermarketsales'
connection_string = f'mysql+mysqlconnector://{user}:{password}@{host}/{database}'
engine = create_engine(connection_string)

# Función para cargar datos
def load_data():
    return pd.read_sql('SELECT * FROM `supermarketsales`', con=engine)

# Título de la aplicación
st.title('Análisis de ventas de supermercados') 

# Contenedor para la tabla y gráficos
table_placeholder = st.empty()
chart_placeholder = st.empty()

# Función para dibujar gráficos
def draw_charts(df):
    chart_placeholder.empty()  # Limpiar el contenedor de gráficos
    
    # Gráfico de distribución de precios unitarios
    with chart_placeholder.container():
        st.title('Análisis de Ventas')
        st.subheader('Distribución de Ventas Totales por Línea de Producto')
        total_sales = df.groupby('Product line')['Total'].sum().reset_index()
        fig = px.pie(total_sales, names='Product line', values='Total', 
               title='',
               hole=0.3,  # Si quieres un gráfico de dona, puedes usar este parámetro
               color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig)
        st.markdown("""
                        Este gráfico de pastel representa la distribución de las ventas totales 
                        según la línea de producto. Cada sección del pastel ilustra la proporción 
                        de ventas que cada línea contribuye al total. Esto permite identificar 
                        visualmente cuál línea de producto tiene mayor participación en las ventas.
                        """)

    # grafico ventas totales por genero
        st.subheader('Ventas Totales por Género')
        total_sales_by_gender = df.groupby('Gender')['Total'].sum().reset_index()
        fig2 = px.bar(total_sales_by_gender, x='Gender', y='Total', 
               title='', 
               color='Gender', 
               color_discrete_sequence=px.colors.sequential.Viridis)
        st.plotly_chart(fig2)
        st.markdown("""
                        Esta gráfica muestra la distribución de las ventas totales por género. 
                        Los datos se agrupan por género y se suman las ventas, lo que permite observar 
                        cuál género ha generado más ingresos en total. 
                        Los colores utilizados representan diferentes géneros.
                        """)
        
        st.subheader('Distribución de Ventas Totales por Método de Pago')
        total_sales_by_payment = df.groupby('Payment')['Total'].sum().reset_index()
        fig3 = px.pie(total_sales_by_payment, names='Payment', values='Total',
               title='',
               hole=0.3,  
               color_discrete_sequence=px.colors.qualitative.Set2,
               )  
        st.plotly_chart(fig3)
        st.markdown("""
                        En este gráfico de pastel se puede apreciar cómo todos los porcentajes 
                        están distribuidos casi iguales entre los diferentes métodos de pago. 
                        Esto indica que no hay un método de pago que predomine significativamente 
                        sobre los demás en las ventas totales.
                        """)

        st.subheader('Ventas Totales por Día de la Semana')
        total_sales_by_day = df.groupby('Day_Name')['Total'].sum().reset_index()
        fig4 = px.line(total_sales_by_day, x='Day_Name', y='Total', 
                        title='', 
                        markers=True)
        st.plotly_chart(fig4)
        st.markdown("""
                        En este gráfico se resalta que el sábado es el día con mejor rendimiento en 
                        ventas, seguido por el martes, que también presenta un desempeño ligeramente 
                        superior. Por otro lado, los lunes son los peores días en términos de ventas. 
                        Esto sugiere patrones de comportamiento en la compra según el día de la semana.
                            """)
        
        st.subheader('Distribución de Tipos de Productos Comprados por Género')

# Crear la figura de barras
        fig5 = px.histogram(df, x='Product line', color='Gender', 
                            title='Distribution of Product Types Purchased by Gender',
                            barmode='group',  # Cambiar a 'group' para barras separadas
                            color_discrete_sequence=px.colors.qualitative.Set2)

        # Personalización de etiquetas y diseño
        fig5.update_layout(
            xaxis_title='Product Line',
            yaxis_title='Count',
            xaxis_tickangle=-45,  # Rotar las etiquetas del eje x
            legend_title='Gender',
            height=600  # Ajustar altura para mejor visualización
        )

        # Mostrar la figura en Streamlit
        st.plotly_chart(fig5)

        # Añadir una breve descripción debajo del gráfico
        st.markdown("""
        Este gráfico muestra la distribución de los tipos de productos comprados 
        según el género. Se observa cómo cada género contribuye a la compra de 
        cada tipo de producto, permitiendo identificar patrones en las preferencias 
        de los clientes. 
        Los colores utilizados corresponden a los diferentes géneros.
        """)

# Función para mostrar la tabla
def show_table(df):
    table_placeholder.empty()  # Limpiar el contenedor de la tabla
    with table_placeholder.container():
        st.subheader('Datos de la Tabla')
        st.write(f'Cantidad de registros: {len(df)}')  # Mostrar cantidad de datos
        st.write(df.head())  # Mostrar los primeros registros

# Botón para actualizar los datos
if st.button('Actualizar gráficos y tabla'):
    df = load_data()  # Cargar los datos actualizados
    show_table(df)  # Mostrar la tabla actualizada
    draw_charts(df)  # Dibujar gráficos actualizados

# Refresco automático
while True:
    df = load_data()
    show_table(df)  # Mostrar la tabla actualizada
    draw_charts(df)  # Dibujar gráficos actualizados
    time.sleep(10)  # Esperar 10 segundos antes de actualizar
