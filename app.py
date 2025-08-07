import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# --- 1. Cargar y Procesar Datos ---
# Cargar el dataset
try:
    df = pd.read_csv('ventas.csv')
except FileNotFoundError:
    print("Error: El archivo 'ventas.csv' no se encontró. Asegúrate de que esté en el mismo directorio.")
    exit()

# Convertir 'Fecha' a datetime y extraer el mes
df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Mes'] = df['Fecha'].dt.to_period('M').astype(str)

# --- 2. Preparar Datos para Visualizaciones ---
# KPIs
total_ingresos = df['TotalVenta'].sum()
clientes_unicos = df['IDCliente'].nunique()
ticket_promedio = df['TotalVenta'].mean()

# Gráfico 1: Ventas mensuales por categoría
ventas_categoria_mes = df.groupby(['Mes', 'Categoria'])['TotalVenta'].sum().reset_index()

# Gráfico 2: Evolución de ingresos mensuales
ingresos_mensuales = df.groupby('Mes')['TotalVenta'].sum().reset_index()

# Gráfico 3: Porcentaje de ventas por producto (Top 10)
ventas_por_producto = df.groupby('Producto')['TotalVenta'].sum().nlargest(10).reset_index()

# --- 3. Inicializar la App Dash ---
app = dash.Dash(__name__)
server = app.server

# --- 4. Diseño del Layout del Dashboard ---
app.layout = html.Div(children=[
    # Título del Dashboard
    html.H1(
        children='Dashboard de Ventas Mensuales',
        style={'textAlign': 'center', 'color': '#1E3A8A'}
    ),

    # Contenedor para KPIs
    html.Div(className='kpi-container', children=[
        html.Div(className='kpi-card', children=[
            html.H3("Total de Ingresos"),
            html.P(f"${total_ingresos:,.2f}")
        ]),
        html.Div(className='kpi-card', children=[
            html.H3("Clientes Únicos"),
            html.P(f"{clientes_unicos}")
        ]),
        html.Div(className='kpi-card', children=[
            html.H3("Ticket Promedio"),
            html.P(f"${ticket_promedio:,.2f}")
        ])
    ]),

    # Contenedor para Gráficas Principales
    html.Div(className='graph-container', children=[
        # Gráfico de Barras: Ventas por Categoría
        dcc.Graph(
            id='bar-ventas-categoria',
            figure=px.bar(
                ventas_categoria_mes,
                x='Mes',
                y='TotalVenta',
                color='Categoria',
                title='Ventas Mensuales por Categoría',
                barmode='group',
                labels={'TotalVenta': 'Ventas ($)', 'Mes': 'Mes', 'Categoria': 'Categoría'}
            )
        ),
        # Gráfico de Línea: Evolución de Ingresos
        dcc.Graph(
            id='line-ingresos-mensuales',
            figure=px.line(
                ingresos_mensuales,
                x='Mes',
                y='TotalVenta',
                title='Evolución de Ingresos Mensuales',
                markers=True,
                labels={'TotalVenta': 'Ingresos ($)', 'Mes': 'Mes'}
            )
        )
    ]),

    # Contenedor para Gráfico de Pastel
    html.Div(className='pie-container', children=[
        # Gráfico de Pastel: Ventas por Producto
        dcc.Graph(
            id='pie-ventas-producto',
            figure=px.pie(
                ventas_por_producto,
                names='Producto',
                values='TotalVenta',
                title='Top 10 Productos Más Vendidos (%)',
                labels={'TotalVenta': 'Ventas', 'Producto': 'Producto'}
            )
        )
    ])
], style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'})


# --- 5. Ejecutar la Aplicación ---
if __name__ == '__main__':
    app.run(debug=False) # <-- ESTA ES LA LÍNEA CORREGIDA