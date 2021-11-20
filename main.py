from altair.vegalite.v4.api import value
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title='Financial Tool', page_icon = "🧊")

st.title("🪙 Financial Tool")

entry = st.number_input('Ingresos:',0,value=1500000)
col1,col2 = st.columns(2)
with col1.expander('Tipos de Obligaciones'):
    st.markdown("""
    1. Renta.
    2. Celular.
    3. Matricula estudiantil.
    4. Transporte.
    5. Seguro Medico.
    6. Deuda.
    """
    )
fixed = col2.slider('Obligaciones',0,100,value=60)
col1.write(entry*fixed*0.01)

col1,col2 = st.columns(2)

with col1.expander('Tipos de Inversión'):
    st.markdown("""
    1. Pensión.
    2. CDT.
    3. Acciones.
    4. Bonos.
    """
    )
investment = col2.slider('Inversion',0,100,value=10)
col1.write(entry*investment*0.01)

col1,col2 = st.columns(2)

with col1.expander('Motivos de Ahorro'):
    st.markdown("""
    1. Vacaciones.
    2. Regalos.
    3. Pagar una casa.
    4. Fondo de emergencias.
    5. Estudios.
    6. Boda.
    """
    )
savings = col2.slider('Ahorros',0,100,value=10)
col1.write(entry*savings*0.01)

with col1.expander('Gustos'):
    st.markdown("""
    1. Comer por fuera.
    2. Salir de fiesta.
    3. Peliculas.
    4. Ropa y Zapatos.
    5. Videojuegos.
    7. Etc...
    """
    )
spending = col2.slider('Gustos',0,100,value=20)
col1.write(entry*spending*0.01)


if fixed+investment+savings+spending != 100:
    st.error(
        """
        La suma de los porcentajes es distinta a 100.
        Intenta ajustar los valores
        """
        )

st.write('## Evolución de Ahorros e Inversiones')
c1,c2,c3 = st.columns(3)
years = c1.number_input('Años',0,value=5)
time = np.arange(1,1+years*12)
investment_array = np.zeros(len(time))
saving_array = np.zeros(len(time))

inversion_input = entry*investment*0.01
saving_input = entry*savings*0.01

investment_array[0] = inversion_input
saving_array[0] = saving_input

inv_return = c2.number_input('Retorno de Inversión Anual (%)', value=10)
inflation = c3.number_input('Inflación Anual (%)',value=3)
inf_ad = st.checkbox('Ingresos ajustados a la inflación (Devaluación del Ingreso por Inflación)',value=True)
if inf_ad:
    ad = 1
else:
    ad=0
for i in range(1,len(time)):
    #Valor actual es el valor del mes pasado más el retorno
    investment_array[i] = inversion_input*(1-(ad* i*inflation/(12*100))) + investment_array[i-1]*(1-(inflation/(12*100))+(inv_return/(12*100))) 
    saving_array[i] = saving_input*(1-(ad*i*inflation/(12*100))) + saving_array[i-1]*(1-(inflation/(12*100)))

df = pd.DataFrame({
    'Tiempo':time,
    'Inversion':investment_array,
    'Ahorro':saving_array
})
df = df.set_index('Tiempo')
st.markdown('##### Dinero vs Tiempo (Meses)')
st.area_chart(df)

diff = np.abs(saving_array[-1] - investment_array[-1])
sum = np.abs(saving_array[-1] + investment_array[-1])

col1,col2 = st.columns(2)

col1.write(f'Sumando Ahorros e Inversión, en {years} años tendremos:')
col1.markdown(f'**{round(sum)}** aproximadamente')

col2.write(f'La diferencia entre las inversiones y los ahorros a los {years} años es de:')
col2.write(f"**{round(diff)}** aproximadamente")




