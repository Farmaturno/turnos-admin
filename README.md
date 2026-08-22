# Turnos Admin 🏪

Aplicación web para la gestión centralizada de turnos de farmacias. Interfaz interactiva que permite visualizar, editar y sincronizar datos de turnos de farmacias en AWS DynamoDB.

## Características

- 📋 **Listado de farmacias**: Visualiza todas las farmacias registradas en una tabla interactiva
- 🔍 **Selección rápida**: Selecciona una farmacia para ver sus detalles completos
- 📅 **Gestión de turnos**: Añade, edita y elimina fechas de turno
- 💾 **Sincronización en tiempo real**: Los cambios se guardan directamente en AWS DynamoDB
- ⚡ **Caché inteligente**: Optimización con ttl para reducir llamadas a la base de datos
- 📱 **Interfaz responsiva**: Diseño adaptado para múltiples dispositivos
- 🔎 **Búsqueda local**: Consulta y visualiza negocios mediante SerpAPI

## Stack Tecnológico

- **Frontend**: [Streamlit](https://streamlit.io/) - Framework Python para aplicaciones web
- **Backend**: Python 3.12
- **Base de datos**: AWS DynamoDB
- **AWS SDK**: boto3
- **Gestor de dependencias**: Pipenv

## Requisitos

- Python 3.12
- Pipenv
- Credenciales de AWS configuradas (para acceso a DynamoDB)

## Instalación

1. Clona este repositorio:
```bash
git clone <repository-url>
cd turnos-admin
```

2. Instala las dependencias con Pipenv:
```bash
pipenv install
```

3. Configura tus credenciales de AWS:
```bash
aws configure
```
O establece las variables de entorno:
```bash
export AWS_ACCESS_KEY_ID=tu_access_key
export AWS_SECRET_ACCESS_KEY=tu_secret_key
export AWS_DEFAULT_REGION=tu_region
```

Configura también tu clave de SerpAPI como variable de entorno:
```bash
export SERPAPI_API_KEY=tu_serpapi_api_key
```
También puedes guardarla en `.streamlit/secrets.toml`:
```toml
SERPAPI_API_KEY = "tu_serpapi_api_key"
```

## Uso

Inicia la aplicación con:
```bash
pipenv run streamlit run src/app.py
```

La aplicación se abrirá en `http://localhost:8501`

### Flujo de uso:

1. **Ver farmacias**: Se carga automáticamente el listado de farmacias desde DynamoDB
2. **Seleccionar farmacia**: Haz clic en una fila para ver sus detalles
3. **Gestionar turnos**: 
   - Usa el selector de fecha para añadir nuevas fechas
   - Usa el campo multiselect para editar fechas existentes
   - Elimina fechas haciendo clic en la "X" junto a cada una
   - Las fechas deben estar en el formato "YYYYMMDD". Ej. "20260817" para el 17 de Agosto de 2026.
4. **Guardar cambios**: Haz clic en el botón "Guardar" para sincronizar con DynamoDB
5. **Buscar negocios locales**: Abre **Búsqueda local**, indica el servicio y la ubicación, y pulsa **Buscar**

## Estructura del Proyecto

```
turnos-admin/
├── src/
│   ├── app.py              # Entrada y navegación principal
│   ├── database.py         # Acceso compartido a DynamoDB
│   └── app_pages/          # Páginas de la aplicación
│       └── busqueda_serpapi.py # Resultados locales de SerpAPI
├── Pipfile                 # Definición de dependencias
├── Pipfile.lock            # Lock file de dependencias
├── README.md               # Este archivo
└── LICENSE
```

## Licencia

Ver archivo [LICENSE](LICENSE) para más detalles.
