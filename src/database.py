import boto3
import streamlit as st

TABLE_NAME = "farmaturno-farmacias-dev"


@st.cache_resource
def get_table():
    return boto3.resource("dynamodb").Table(TABLE_NAME)


@st.cache_data(ttl=60)
def fetch_all_data():
    try:
        return get_table().scan().get("Items", [])
    except Exception as error:
        st.error(f"Error al consultar las farmacias: {error}")
        return []


def update_turnos(place_id, turnos):
    get_table().update_item(
        Key={"place_id": place_id},
        UpdateExpression="SET turnos = :turnos",
        ExpressionAttributeValues={":turnos": turnos},
    )
    fetch_all_data.clear()
