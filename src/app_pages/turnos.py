import streamlit as st

from database import update_turnos

st.title("Gestión de turnos")

pharmacy = st.session_state.get("selected_pharmacy")
if pharmacy is None:
    st.info("Selecciona una farmacia desde la página Farmacias para gestionar sus turnos.")
    st.page_link("app_pages/farmacias.py", label="Ir a Farmacias", icon=":material/store:")
else:
    col_details, col_shifts = st.columns(2)

    with col_details:
        st.subheader(pharmacy.get("name", "Farmacia seleccionada"))
        details = pharmacy.copy()
        details.pop("turnos", None)
        st.json(details)

    with col_shifts:
        st.subheader("Turnos asignados")
        turnos = st.multiselect(
            "Fechas de turno",
            options=pharmacy.get("turnos", []),
            default=pharmacy.get("turnos", []),
            accept_new_options=True,
        )

        col_save, col_back = st.columns(2)
        with col_save:
            if st.button("Guardar cambios", icon=":material/save:", type="primary", use_container_width=True):
                with st.spinner("Guardando cambios..."):
                    try:
                        update_turnos(pharmacy["place_id"], turnos)
                        st.session_state.selected_pharmacy = {**pharmacy, "turnos": turnos}
                        st.success("Cambios guardados correctamente.")
                    except Exception as error:
                        st.error(f"Error al guardar los cambios: {error}")

        with col_back:
            if st.button("Volver", icon=":material/arrow_back:", use_container_width=True):
                st.session_state.selected_pharmacy = None
                st.switch_page("app_pages/farmacias.py")
