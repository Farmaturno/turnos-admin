import streamlit as st

from database import fetch_all_data

st.title("Farmacias")
st.write("Consulta las farmacias registradas y selecciona una para gestionar sus turnos.")

data = fetch_all_data()

if not data:
    st.info("No hay farmacias registradas en la tabla de DynamoDB.")
else:
    selected = st.dataframe(
        data,
        selection_mode="single-row",
        on_select="rerun",
        column_order=("name", "formatted_address"),
        height=320,
        width="stretch",
    )

    if selected.selection.rows:
        st.session_state.selected_pharmacy = data[selected.selection.rows[0]]
        st.switch_page("app_pages/turnos.py")
