import streamlit as st
import boto3

st.set_page_config(page_title="Gestión de Turnos de Farmacias",
                   page_icon="🏪",
                   layout="wide")

# Inicializar el cliente de DynamoDB
@st.cache_resource
def init_dynamodb():
    print("Initializing DynamoDB resource...")
    return boto3.resource('dynamodb')

dynamodb = init_dynamodb()
table = dynamodb.Table('farmaturno-farmacias-dev')

@st.cache_data(ttl=60)
def fetch_all_data():
    print("Fetching all data from DynamoDB...")
    try:
        response = table.scan()
        return response.get('Items', [])
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

st.title("🏪 Gestión de Turnos de Farmacias")
st.markdown("Esta aplicación permite gestionar los turnos de las farmacias de manera interactiva. Selecciona una farmacia de la tabla para ver sus detalles y modificar sus turnos asignados.")

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

st.divider()

if len(farmacia.selection.rows):
    print(f"Selected row index: {farmacia.selection.rows[0]}")
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

        # 2. El "Carrito": Muestra y permite quitar fechas dispares fácilmente
        fechas_actualizadas = st.multiselect(
            "Fechas de turno asignadas (puedes borrar con la X):",
            options=detalles.get("turnos", []),
            default=detalles.get("turnos", []),
            accept_new_options=True
        )

        # 3. Botón final para guardar en AWS
        if st.button("💾 Guardar"):
            print(f"Saving updated turnos for place_id {detalles['place_id']}: {fechas_actualizadas}")
            with st.spinner("Guardando cambios..."):
                try:
                    # Actualizar el registro en DynamoDB
                    table.update_item(
                        Key={'place_id': detalles['place_id']},
                        UpdateExpression="SET turnos = :t",
                        ExpressionAttributeValues={':t': fechas_actualizadas}
                    )
                    st.success("Cambios guardados correctamente !")
                except Exception as e:
                    st.error(f"Error guardando cambios: {e}")