import os
from urllib.parse import parse_qsl, urlparse

import serpapi
import streamlit as st


def fetch_all_local_results(client, query):
    start = 0
    local_results = []

    search_params = {
                            "engine": "google_maps",
                            "type": "search",
                            "q": query.strip(),
                            "ll": "@40.7455096,-74.0083012,14z",
                            "hl": "es",
                            "gl": "ar",
                            "start": start,
                        }

    while True:
        results = client.search(search_params)
        local_results.extend(results.get("local_results", []))
        pagination = results.get("serpapi_pagination", {})
        next_page = pagination.get("next", None)
        print(f"Next page: {next_page}")

        if next_page:
            search_params["start"] += 20
        else:
            break

    return local_results



st.title("Búsqueda local")
st.write("Busca negocios y servicios cercanos usando los resultados locales de Google.")

with st.form("serpapi_search"):
    query = st.text_input("Qué quieres buscar", value="Farmacias en Burzaco, Buenos Aires, Argentina")
    submitted = st.form_submit_button("Buscar", icon=":material/search:", type="primary")

if submitted:
    serpapi_key = os.getenv("SERPAPI_KEY", None)

    if not serpapi_key:
        st.error("Configura SERPAPI_KEY en las variables de entorno.")

    elif not query.strip():
        st.warning("Indica una búsqueda y una ubicación.")

    else:
        with st.spinner("Buscando resultados..."):
            try:
                client = serpapi.Client(api_key=serpapi_key)

                local_results = fetch_all_local_results(
                    client,
                    query=query,
                )

                if local_results:
#                    local_results
                    st.dataframe(
                        local_results,
                        width="stretch",
                        hide_index=True,
                        column_order=(
                            "place_id",
                            "title",
                            "address",
                            "phone",
                            "gps_coordinates",
                        ),
                    )

                else:
                    st.info("SerpAPI no devolvió resultados locales para esta búsqueda.")

            except Exception as error:
                st.error(f"Error al consultar SerpAPI: {error}")
