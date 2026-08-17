import streamlit as st

# Inicializar el estado de la app para guardar las fechas temporalmente
if "fechas_turno" not in st.session_state:
    # Simulamos lo que vendría de DynamoDB
    st.session_state.fechas_turno = ["2026-05-09", "2026-05-24"]

st.title("🏪 Gestión de Turnos de Farmacias")

# 1. Selector de fecha individual
nueva_fecha = st.date_input("Selecciona una fecha para añadir:", format="YYYY-MM-DD")
str_fecha = nueva_fecha.strftime("%Y-%m-%d")

# Botón para agregar la fecha al array
if st.button("➕ Añadir Fecha"):
    if str_fecha not in st.session_state.fechas_turno:
        st.session_state.fechas_turno.append(str_fecha)
        st.rerun()

# 2. El "Carrito": Muestra y permite quitar fechas dispares fácilmente
fechas_actualizadas = st.multiselect(
    "Fechas de turno asignadas (puedes borrar con la X):",
    options=st.session_state.fechas_turno,
    default=st.session_state.fechas_turno
)

# Actualizar el estado si el usuario borra algo desde el multiselect
st.session_state.fechas_turno = fechas_actualizadas

# 3. Botón final para guardar en AWS
if st.button("💾 Guardar"):
    st.success(f"Guardando en DynamoDB: {st.session_state.fechas_turno}")