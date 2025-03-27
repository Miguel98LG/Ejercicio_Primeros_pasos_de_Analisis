import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Leer archivos Excel con una ruta relativa
df = pd.read_excel('./proyecto1.xlsx')
df2 = pd.read_excel('./Catalogo_sucursal.xlsx')

# Conocer las ventas totales del comercio
ventas_totales = df['ventas_tot'].sum()
print(f'Ventas totales del comercio: {ventas_totales}')


# Contar socios con y sin adeudo
con_adeudo = (df['B_adeudo'] == 'Con adeudo').sum()
sin_adeudo = (df['B_adeudo'] == 'Sin adeudo').sum()
socios_totales = con_adeudo + sin_adeudo
porcentaje_con = (con_adeudo / socios_totales) * 100
porcentaje_sin = (sin_adeudo / socios_totales) * 100
print(f'Socios con adeudo: {con_adeudo} ({porcentaje_con:.2f}%)')
print(f'Socios sin adeudo: {sin_adeudo} ({porcentaje_sin:.2f}%)')

# Calcular la deuda total de los clientes
deuda_total = df['adeudo_actual'].sum()
print(f'Deuda total de los clientes: ${deuda_total}')

# Calcular el porcentaje de utilidad del comercio
porcentaje_utilidad = ((ventas_totales - deuda_total) / ventas_totales) * 100
print(f'Porcentaje de utilidad del comercio: {porcentaje_utilidad:.2f}%')

#3
# Grfica de barras de ventas totales a lo largo del tiempo 

# Convertir la columna de tiempo a formato datetime
df['fec_ini_cdto'] = pd.to_datetime(df['fec_ini_cdto'])

# Agrupar ventas por mes
df['mes'] = df['fec_ini_cdto'].dt.to_period('M')  # Extraer año y mes
ventas_mensuales = df.groupby('mes')['ventas_tot'].sum().reset_index()

# Convertir el periodo de mes a datetime para graficar correctamente
ventas_mensuales['mes'] = ventas_mensuales['mes'].astype(str)
ventas_mensuales['mes'] = pd.to_datetime(ventas_mensuales['mes'])

# Configurar la figura
plt.figure(figsize=(12, 6))
plt.bar(ventas_mensuales['mes'], ventas_mensuales['ventas_tot'], color='#5A9BD5', width=20)

# Formato de fecha en el eje X
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

# Personalización del gráfico
plt.title('Ventas Totales por Mes', fontsize=16, fontweight='bold')
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Ventas Totales', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Mostrar el gráfico
plt.show()

#4
# Gráfica de desviación estándar de pagos realizados respecto del tiempo

# Convertir la columna B_mes a formato datetime
df['B_mes'] = pd.to_datetime(df['B_mes'], format='%Y-%m')  # Asegurar formato YYYY-MM

# Hacer merge para obtener el nombre de la sucursal
df_merged = df.merge(df2, on='id_sucursal', how='left')

# Agrupar por mes y sucursal, calculando la desviación estándar de pagos
df_std = df_merged.groupby(['B_mes', 'suc'])['pagos_tot'].std().reset_index()

# Lista de colores para cada sucursal única
colores = plt.cm.Paired(np.linspace(0, 1, df_std['suc'].nunique()))

# Crear la gráfica
plt.figure(figsize=(12, 6))

# Graficar cada sucursal con un color diferente
for i, (sucursal, grupo) in enumerate(df_std.groupby('suc')):
    plt.bar(grupo['B_mes'], grupo['pagos_tot'], color=colores[i], label=f'Sucursal: {sucursal}', alpha=0.8, width=20)

# Formatear el eje X con fechas reales
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

# Personalización de la gráfica
plt.title('Desviación Estándar de los Pagos Realizados por Sucursal en el Tiempo', fontsize=16, fontweight='bold')
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Desviación Estándar de Pagos Totales', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Sucursal', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Mostrar la gráfica
plt.show()

#7
# Crear un gráfico circular de ventas por sucursal.

# Sumar las ventas por sucursal
ventas_por_sucursal = df_merged.groupby('suc')['ventas_tot'].sum()

# Crear la figura
plt.figure(figsize=(8, 8))

# Generar el gráfico de pastel
plt.pie(
    ventas_por_sucursal, 
    labels=ventas_por_sucursal.index, 
    autopct='%1.1f%%', 
    colors=plt.cm.Set2.colors, 
    startangle=140
)

# Agregar título
plt.title('Distribución de Ventas Totales por Sucursal', fontsize=16, fontweight='bold')

# Mostrar el gráfico
plt.show()

#8
# Presentar un gráfico de deudas totales por cada sucursal respecto del margen de utilidad.

# Calcular la deuda total y el margen de utilidad por sucursal
deuda_por_sucursal = df_merged.groupby('suc')['adeudo_actual'].sum()
ventas_por_sucursal = df_merged.groupby('suc')['ventas_tot'].sum()
utilidad_por_sucursal = ((ventas_por_sucursal - deuda_por_sucursal) / ventas_por_sucursal) * 100

# Crear el gráfico de barras
fig, ax1 = plt.subplots(figsize=(12, 6))

# Gráfico de deudas totales
color = 'tab:orange'
ax1.set_xlabel('Sucursal', fontsize=12)
ax1.set_ylabel('Deuda Total ($)', color=color, fontsize=12)
ax1.bar(deuda_por_sucursal.index, deuda_por_sucursal, color=color, alpha=0.7, label='Deuda Total')
ax1.tick_params(axis='y', labelcolor=color)

# Crear un segundo eje Y para el margen de utilidad
ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('Margen de Utilidad (%)', color=color, fontsize=12)
ax2.plot(utilidad_por_sucursal.index, utilidad_por_sucursal, color=color, marker='o', linestyle='-', linewidth=2, label='Margen de Utilidad')
ax2.tick_params(axis='y', labelcolor=color)

# Configurar el gráfico
plt.title('Deuda Total vs. Margen de Utilidad por Sucursal', fontsize=16, fontweight='bold')
fig.tight_layout()

# Agregar leyendas
ax1.legend(loc='upper left', fontsize=10)
ax2.legend(loc='upper right', fontsize=10)

# Mostrar el gráfico
plt.show()
