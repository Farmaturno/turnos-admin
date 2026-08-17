import streamlit as st
import boto3

st.set_page_config(page_title="Gestión de Turnos de Farmacias",
                   page_icon="🏪",
                   layout="wide")

# Inicializar el cliente de DynamoDB
@st.cache_resource
def init_dynamodb():
    return boto3.resource('dynamodb')

dynamodb = init_dynamodb()
table = dynamodb.Table('farmaturno-farmacias-dev')

@st.cache_data(ttl=60)
def fetch_all_data():
    try:
        response = table.scan()
        return response.get('Items', [])
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

st.title("🏪 Gestión de Turnos de Farmacias")

# Fetch and visualize data inside an interactive table widget
data = fetch_all_data()

if data:
    farmacia = st.dataframe(data,
                 selection_mode="single-row",
                 on_select="rerun",
                 column_order=("name", "compound_code"),
                 height=200,
                 )
else:
    st.info("No records found in the DynamoDB table.")

if len(farmacia.selection.rows):
    index = farmacia.selection.rows[0]
    detalles = data[index]  # This is the selected row data

    col_detalles, col_turnos = st.columns(2)

    with col_detalles:
        st.subheader("Detalles de la Farmacia Seleccionada")
        detalles_summary = detalles.copy()
        del detalles_summary["turnos"]  # Remove turnos for summary display
        st.json(detalles_summary)

    with col_turnos:
        st.subheader("Gestión de Turnos")

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
            options=detalles.get("turnos", []),
            default=detalles.get("turnos", []),
            accept_new_options=True
        )

        # 3. Botón final para guardar en AWS
        if st.button("💾 Guardar"):
            st.success(f"Guardando en DynamoDB: {fechas_actualizadas}")