import streamlit as st

st.set_page_config(
    page_title="Gestión de turnos de farmacias",
    page_icon="🏪",
    layout="wide",
)

if "selected_pharmacy" not in st.session_state:
    st.session_state.selected_pharmacy = None

page = st.navigation(
    {
        "": [
            st.Page("app_pages/farmacias.py", title="Farmacias", icon=":material/store:"),
            st.Page("app_pages/turnos.py", title="Gestión de turnos", icon=":material/calendar_month:"),
        ]
    },
    position="sidebar",
)

page.run()