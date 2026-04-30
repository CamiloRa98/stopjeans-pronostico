"""
Dashboard de Pronóstico de Ventas — STOP JEANS
Especialización Inteligencia de Negocios | UPB
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ─── Paleta de colores: definida dinámicamente tras selección de marca ──
# (ver bloque debajo de marca_sel)
BLANCO = "#FFFFFF"
POSITIVO = "#2E7D32"   # Verde crecimiento (igual para ambas marcas)

# ─── Logo SVG inline — STOP JEANS ────────────────────────────────────
LOGO_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 127 20" height="28" width="180">
<g clip-path="url(#clip0_2_2)">
<path fill="black" d="M3.82904 19.1096C2.96143 18.7637 2.26795 18.2519 1.74934 17.5748C1.22998 16.897 0.957111 16.08 0.928467 15.1267H4.80972C4.86626 15.6659 5.05922 16.077 5.38637 16.3607C5.71276 16.6445 6.1394 16.7859 6.66555 16.7859C7.19169 16.7859 7.63266 16.6652 7.94548 16.423C8.25755 16.1807 8.41509 15.8459 8.41509 15.417C8.41509 15.0585 8.28996 14.76 8.04121 14.5252C7.79246 14.2896 7.48642 14.097 7.12385 13.9445C6.76203 13.7919 6.24644 13.6193 5.57708 13.4252C4.61072 13.1356 3.82075 12.8445 3.20943 12.5541C2.59811 12.263 2.07272 11.8348 1.63175 11.2674C1.19003 10.7007 0.970679 9.96001 0.970679 9.04668C0.970679 7.69186 1.47421 6.62964 2.48504 5.86223C3.49436 5.09482 4.80897 4.71112 6.43112 4.71112C8.05327 4.71112 9.40933 5.09482 10.4194 5.86223C11.4287 6.62964 11.9692 7.69779 12.0401 9.06742H8.09398C8.06533 8.59779 7.88744 8.22816 7.5618 7.95779C7.23466 7.68816 6.81555 7.55334 6.30297 7.55334C5.86276 7.55334 5.50622 7.66816 5.23712 7.89556C4.96651 8.12445 4.83233 8.4526 4.83233 8.88075C4.83233 9.35186 5.05998 9.71779 5.51451 9.98075C5.96905 10.2437 6.68062 10.5267 7.64773 10.8311C8.61409 11.1496 9.39954 11.4533 10.0041 11.7437C10.6086 12.0348 11.131 12.4563 11.5712 13.0104C12.0114 13.563 12.2323 14.2748 12.2323 15.1467C12.2323 16.0185 12.0159 16.7304 11.5825 17.4074C11.1491 18.0852 10.5189 18.6252 9.69427 19.0259C8.87038 19.4274 7.89573 19.6274 6.77259 19.6274C5.64944 19.6274 4.69665 19.4541 3.8298 19.1082"></path>
<path fill="black" d="M24.6027 4.91852V7.76074H20.6355V19.4837H16.9879V7.76074H13.0208V4.91852H24.6027Z"></path>
<path fill="black" d="M29.0062 18.6741C27.8333 18.0385 26.9016 17.1504 26.2127 16.0089C25.523 14.8674 25.1777 13.5844 25.1777 12.16C25.1777 10.7356 25.523 9.4563 26.2127 8.32148C26.9016 7.18741 27.8333 6.30222 29.0062 5.66593C30.1799 5.03037 31.4704 4.71185 32.8777 4.71185C34.285 4.71185 35.5755 5.03037 36.7491 5.66593C37.922 6.30222 38.8454 7.18741 39.5216 8.32148C40.197 9.4563 40.5347 10.7363 40.5347 12.16C40.5347 13.5837 40.1939 14.8681 39.511 16.0089C38.8288 17.1504 37.9047 18.0385 36.7386 18.6741C35.5725 19.3104 34.2858 19.6289 32.8784 19.6289C31.4711 19.6289 30.1806 19.3104 29.007 18.6741M35.7466 15.2304C36.4642 14.4556 36.8238 13.4326 36.8238 12.1593C36.8238 10.8859 36.4642 9.84593 35.7466 9.07852C35.0275 8.31111 34.0724 7.92593 32.8777 7.92593C31.6829 7.92593 30.7053 8.30741 29.9877 9.06741C29.2685 9.82815 28.9105 10.8593 28.9105 12.1593C28.9105 13.4593 29.2685 14.4726 29.9877 15.2407C30.7053 16.0082 31.6686 16.3919 32.8777 16.3919C34.0868 16.3919 35.0275 16.0052 35.7466 15.2296"></path>
<path fill="black" d="M52.734 11.9207C52.3367 12.6193 51.7247 13.183 50.9 13.6119C50.0761 14.04 49.0517 14.2548 47.8291 14.2548H45.567V19.483H41.9209V4.91852H47.8291C49.0231 4.91852 50.0324 5.11926 50.8578 5.51926C51.6817 5.92148 52.2998 6.47407 52.7129 7.17926C53.1252 7.88444 53.3317 8.69482 53.3317 9.60667C53.3317 10.4504 53.132 11.2215 52.734 11.92M49.1083 10.9563C49.4497 10.6378 49.6193 10.1889 49.6193 9.60815C49.6193 9.02741 49.4497 8.57778 49.1083 8.26C48.7668 7.94148 48.2474 7.78222 47.5509 7.78222H45.5677V11.4341H47.5509C48.2474 11.4341 48.7668 11.2748 49.1083 10.9563Z"></path>
<path fill="black" d="M67.8564 4.91853V14.8356C67.8564 16.3719 67.4117 17.5541 66.523 18.3837C65.6342 19.2133 64.4365 19.6289 62.9296 19.6289C61.4228 19.6289 60.0856 19.1926 59.1321 18.3215C58.1793 17.4496 57.7029 16.2119 57.7029 14.6074H61.3294C61.3294 15.217 61.4568 15.6756 61.713 15.9874C61.9678 16.2978 62.3387 16.4541 62.8226 16.4541C63.2628 16.4541 63.6035 16.3156 63.8455 16.0385C64.0875 15.763 64.2081 15.3615 64.2081 14.8348V4.91779H67.8557L67.8564 4.91853Z"></path>
<path fill="black" d="M73.806 7.76074V10.7074H78.6906V13.4459H73.806V16.6407H79.3305V19.483H70.1584V4.91852H79.3305V7.76074H73.806Z"></path>
<path fill="black" d="M90.3783 16.9111H84.7905L83.8942 19.483H80.077L85.4937 4.91852H89.7172L95.1339 19.483H91.2745L90.3783 16.9111ZM89.4398 14.1719L87.584 8.84L85.75 14.1719H89.4398Z"></path>
<path fill="black" d="M109.532 19.483H105.884L99.7846 10.4993V19.483H96.1378V4.91779H99.7846L105.884 13.943V4.91779H109.532V19.483Z"></path>
<path fill="black" d="M114.01 19.1096C113.142 18.7637 112.449 18.2519 111.931 17.5748C111.411 16.897 111.138 16.08 111.109 15.1267H114.99C115.047 15.6659 115.24 16.077 115.567 16.3607C115.893 16.6445 116.32 16.7859 116.846 16.7859C117.372 16.7859 117.813 16.6652 118.126 16.423C118.439 16.1807 118.595 15.8459 118.595 15.417C118.595 15.0585 118.47 14.76 118.222 14.5252C117.973 14.2896 117.667 14.097 117.305 13.9445C116.942 13.7919 116.426 13.6193 115.758 13.4252C114.791 13.1356 114.001 12.8445 113.39 12.5541C112.778 12.263 112.252 11.8348 111.812 11.2674C111.37 10.7007 111.151 9.96001 111.151 9.04668C111.151 7.69186 111.656 6.62964 112.665 5.86223C113.675 5.09482 114.989 4.71112 116.611 4.71112C118.234 4.71112 119.59 5.09482 120.6 5.86223C121.609 6.62964 122.149 7.69779 122.22 9.06742H118.274C118.246 8.59779 118.068 8.22816 117.742 7.95779C117.415 7.68816 116.996 7.55334 116.483 7.55334C116.043 7.55334 115.687 7.66816 115.417 7.89556C115.147 8.12445 115.013 8.4526 115.013 8.88075C115.013 9.35186 115.24 9.71779 115.695 9.98075C116.149 10.2437 116.861 10.5267 117.828 10.8311C118.794 11.1496 119.58 11.4533 120.184 11.7437C120.789 12.0348 121.311 12.4563 121.752 13.0104C122.192 13.563 122.413 14.2748 122.413 15.1467C122.413 16.0185 122.196 16.7304 121.763 17.4074C121.329 18.0852 120.7 18.6252 119.875 19.0259C119.051 19.4274 118.076 19.6274 116.953 19.6274C115.83 19.6274 114.877 19.4541 114.01 19.1082"></path>
<path fill="black" d="M124.244 0.371094C124.749 0.371094 125.208 0.571835 125.537 0.895538C125.87 1.2185 126.071 1.66813 126.071 2.15998C126.071 2.65184 125.869 3.10517 125.537 3.42887C125.208 3.75628 124.749 3.95184 124.244 3.95184C123.738 3.95184 123.279 3.75554 122.95 3.42887C122.617 3.10517 122.413 2.6548 122.413 2.15998C122.413 1.66517 122.618 1.21776 122.95 0.895538C123.279 0.571835 123.738 0.371094 124.244 0.371094ZM125.257 1.17332C124.999 0.916279 124.642 0.759983 124.244 0.759983C123.846 0.759983 123.487 0.915538 123.227 1.17332C122.971 1.42295 122.807 1.7748 122.807 2.15998C122.807 2.54517 122.971 2.90146 123.227 3.15406C123.487 3.40813 123.849 3.56739 124.244 3.56739C124.639 3.56739 124.999 3.40813 125.257 3.15406C125.52 2.90146 125.676 2.54813 125.676 2.15998C125.676 1.77184 125.52 1.42295 125.257 1.17332Z"></path>
<path fill="black" d="M123.592 3.01035V1.29553H124.479C124.683 1.29553 124.831 1.35775 124.926 1.47998C124.992 1.57035 125.028 1.66887 125.028 1.77998C125.028 1.87775 125.001 1.96442 124.955 2.03257C124.906 2.10664 124.841 2.15998 124.757 2.18812C124.841 2.22072 124.893 2.26146 124.922 2.30664C124.959 2.36738 124.976 2.47479 124.976 2.62516C124.976 2.76146 124.978 2.84738 124.987 2.87553C124.999 2.91998 125.018 2.95257 125.055 2.96516V3.00961H124.654C124.626 2.92812 124.611 2.80887 124.611 2.6659C124.611 2.53479 124.598 2.45331 124.571 2.41627C124.534 2.36294 124.455 2.33924 124.331 2.33924H123.95V3.00961H123.592V3.01035ZM123.95 2.05331H124.38C124.571 2.05331 124.665 1.97183 124.665 1.81553C124.665 1.66812 124.575 1.59405 124.409 1.59405H123.95V2.05331Z"></path>
</g>
<defs><clipPath id="clip0_2_2"><rect fill="white" height="20" width="127"></rect></clipPath></defs>
</svg>'''

# ─── Logo SVG inline — YOYO JEANS ─────────────────────────────────────
LOGO_SVG_YOYO = '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 181 59" height="40" width="130">
<path fill="black" d="M10.2704 0.839844L20.0668 18.06L29.8557 0.839844H40.1863L24.6339 26.5825V42.8679H15.4921V26.5825L0 0.839844H10.2704Z"></path>
<path fill="black" d="M66.3025 0.0219116C79.1838 0.0219116 88.6792 9.71284 88.6792 21.8502C88.6792 33.9876 79.244 43.6785 66.3025 43.6785C53.361 43.6785 43.9258 34.1045 43.9258 21.8502C43.9258 9.59599 53.361 0.0219116 66.3025 0.0219116ZM66.3025 35.4555C74.0222 35.4555 79.4772 29.3868 79.4772 21.8575C79.4772 14.3283 74.0147 8.25956 66.3025 8.25956C58.5903 8.25956 53.1278 14.3867 53.1278 21.8575C53.1278 29.3284 58.5903 35.4555 66.3025 35.4555Z"></path>
<path fill="black" d="M102.554 0.817932L112.35 18.0381L122.146 0.817932H132.477L116.925 26.5606V42.846H107.783V26.5606L92.2832 0.817932H102.554Z"></path>
<path fill="black" d="M158.623 0C171.505 0 181 9.69093 181 21.8283C181 33.9657 171.565 43.6566 158.623 43.6566C145.682 43.6566 136.247 34.0826 136.247 21.8283C136.247 9.57408 145.682 0 158.623 0ZM158.623 35.4336C166.343 35.4336 171.798 29.3649 171.798 21.8356C171.798 14.3063 166.336 8.23765 158.623 8.23765C150.911 8.23765 145.449 14.3648 145.449 21.8356C145.449 29.3065 150.911 35.4336 158.623 35.4336Z"></path>
<path fill="black" d="M130.589 58.8905V57.1743C130.747 57.2035 130.905 57.2181 131.1 57.2181C131.672 57.2181 131.928 56.9114 131.928 56.2906V47.9361H134.11V56.5681C134.11 58.2186 133.312 58.9927 131.582 58.9927C131.236 58.9927 130.852 58.9635 130.596 58.8832L130.589 58.8905ZM131.913 44.7959H134.125V46.8334H131.913V44.7959Z"></path>
<path fill="black" d="M141.453 47.7609C144.079 47.7609 145.449 49.5793 145.449 51.9162V52.4274H139.437C139.52 53.6324 140.264 54.5452 141.536 54.5452C142.552 54.5452 143.094 54.0852 143.364 53.479H145.336C144.952 55.0711 143.477 56.1665 141.551 56.1665C138.895 56.1665 137.353 54.3262 137.353 51.9673C137.353 49.6085 139.038 47.7682 141.453 47.7682V47.7609ZM143.364 50.9595C143.221 49.959 142.537 49.258 141.453 49.258C140.37 49.258 139.685 49.9809 139.497 50.9595H143.364Z"></path>
<path fill="black" d="M151.701 51.0983L153.703 50.9449V50.6528C153.703 49.8495 153.244 49.3383 152.288 49.3383C151.415 49.3383 150.874 49.8203 150.776 50.4337H148.707C148.962 48.8417 150.332 47.7609 152.288 47.7609C154.628 47.7609 155.87 48.9658 155.87 50.7843V55.9693H153.77V54.8739C153.454 55.5676 152.544 56.1519 151.302 56.1519C149.549 56.1519 148.421 55.166 148.421 53.6324C148.421 52.0988 149.549 51.237 151.694 51.0837L151.701 51.0983ZM151.889 54.7205C153.003 54.7205 153.703 54.0413 153.703 52.8802V52.3398L152.13 52.4639C151.144 52.5442 150.52 52.8218 150.52 53.574C150.52 54.2531 151.016 54.7132 151.889 54.7132V54.7205Z"></path>
<path fill="black" d="M159.451 47.9434H161.55V49.1776C161.934 48.3159 162.694 47.7609 163.935 47.7609C165.892 47.7609 166.892 49.09 166.892 51.0618V55.9693H164.71V51.3393C164.71 50.3242 164.266 49.5793 163.228 49.5793C162.19 49.5793 161.618 50.2438 161.618 51.3393V55.9693H159.436V47.9434H159.451Z"></path>
<path fill="black" d="M169.932 53.3768H171.918C172.076 54.1509 172.663 54.6913 173.717 54.6913C174.672 54.6913 175.259 54.275 175.259 53.6543C175.259 53.1942 174.943 52.8948 174.161 52.7779L172.377 52.4858C170.835 52.2375 170.067 51.5584 170.067 50.2804C170.067 48.7833 171.452 47.7609 173.491 47.7609C175.53 47.7609 176.832 48.7321 176.975 50.3388H174.988C174.875 49.7034 174.416 49.2433 173.491 49.2433C172.633 49.2433 172.046 49.5501 172.046 50.1051C172.046 50.536 172.317 50.7039 173.002 50.8135L174.8 51.091C176.455 51.3393 177.253 52.0915 177.253 53.4352C177.253 55.1149 175.711 56.1519 173.724 56.1519C171.61 56.1519 170.18 55.1149 169.94 53.3695L169.932 53.3768Z"></path>
</svg>'''

# ─── Configuración de página ───────────────────────────────────────────
st.set_page_config(
    page_title="STOP JEANS — Pronóstico de Ventas",
    page_icon="👖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Rutas de archivos (relativas al repo) ─────────────────────────────
BASE_DIR = Path(__file__).parent

ARCHIVOS_MARCA = {
    "STOP JEANS": {
        "historico":  BASE_DIR / "data" / "Ventas_linea_stopjeans.csv",
        "pronostico": BASE_DIR / "data" / "pronostico_ventas_stop_jeans.csv",
        "cierre":     BASE_DIR / "data" / "cierre_mes_curso_stop_jeans.csv",
    },
    "YOYO JEANS": {
        "historico":  BASE_DIR / "data" / "Ventas_linea_yoyojeans.csv",
        "pronostico": BASE_DIR / "data" / "pronostico_ventas_yoyo_jeans.csv",
        "cierre":     BASE_DIR / "data" / "cierre_mes_curso_yoyo_jeans.csv",
    },
}


# ─── Selector de marca (sidebar anticipado) ────────────────────────────
marca_sel = st.sidebar.selectbox(
    "Marca",
    list(ARCHIVOS_MARCA.keys()),
    index=0,
)
RUTAS = ARCHIVOS_MARCA[marca_sel]

# ─── Paleta de colores dinámica por marca ──────────────────────────────
if marca_sel == "YOYO JEANS":
    NEGRO          = "#1A001A"    # near-black violeta
    SIDEBAR_BG     = "#6A0062"    # violeta medio (sidebar)
    GRIS_OSCURO    = "#1A1A1A"    # neutro (texto)
    GRIS_MEDIO     = "#4A4A4A"    # neutro (texto secundario)
    GRIS_CLARO     = "#8C8C8C"    # neutro (captions)
    GRIS_MUY_CLARO = "#FCE4F0"    # rosa muy claro (fondos suaves)
    ACENTO         = "#C2006E"    # fucsia YOYO
    ACENTO_SUAVE   = "#E91E8C"    # magenta
    NEGATIVO       = "#C2006E"
    ESCALA_MARCA   = ["#FCE4F0", "#F472B6", "#E91E8C", "#880050", "#1A001A"]
    ESCALA_BARRAS  = ["#FCE4F0", "#1A001A"]
    PALETA_LINEAS  = [
        "#1A001A", "#3D003A", "#880050", "#C2006E", "#E91E8C",
        "#F472B6", "#FF80BC", "#FFD6EC", "#4A004A", "#6B0050",
    ]
    FILL_INTERVALO = "rgba(194,0,110,0.12)"
else:  # STOP JEANS
    NEGRO          = "#1A0000"    # near-black rojo
    SIDEBAR_BG     = "#6A0000"    # rojo medio (sidebar)
    GRIS_OSCURO    = "#1A1A1A"    # neutro (texto)
    GRIS_MEDIO     = "#4A4A4A"    # neutro (texto secundario)
    GRIS_CLARO     = "#8C8C8C"    # neutro (captions)
    GRIS_MUY_CLARO = "#FFE4E4"    # rosa muy claro (fondos suaves)
    ACENTO         = "#C8102E"    # rojo STOP
    ACENTO_SUAVE   = "#EF5350"    # rojo suave
    NEGATIVO       = "#C8102E"
    ESCALA_MARCA   = ["#FFE4E4", "#EF5350", "#D32F2F", "#B30000", "#1A0000"]
    ESCALA_BARRAS  = ["#FFE4E4", "#1A0000"]
    PALETA_LINEAS  = [
        "#1A0000", "#3D0000", "#6B0000", "#B30000", "#C8102E",
        "#D32F2F", "#EF5350", "#FF8A80", "#8B0000", "#555555",
    ]
    FILL_INTERVALO = "rgba(200,16,46,0.12)"


# ─── Carga de datos (cacheada) ─────────────────────────────────────────
@st.cache_data(ttl=60)
def cargar_historico(path):
    df = pd.read_csv(path, sep=";")
    df["fecha"] = pd.to_datetime(df["fecha"], format="%d/%m/%Y")
    return df


@st.cache_data(ttl=60)
def cargar_pronostico(path):
    df = pd.read_csv(path)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["Cantidad_Pronosticada"] = df["Cantidad_Pronosticada"].clip(lower=0)
    if "Limite_Inferior" not in df.columns:
        df["Limite_Inferior"] = df["Cantidad_Pronosticada"]
    if "Limite_Superior" not in df.columns:
        df["Limite_Superior"] = df["Cantidad_Pronosticada"]
    df["Limite_Inferior"] = df["Limite_Inferior"].clip(lower=0)
    df["Limite_Superior"] = df["Limite_Superior"].clip(lower=0)
    return df


if not RUTAS["pronostico"].exists() or not RUTAS["historico"].exists():
    st.warning(f"Los datos de **{marca_sel}** aún no están disponibles. Ejecuta el notebook con `MARCA_ACTIVA = '{marca_sel}'` y sube los CSV al repositorio.")
    st.stop()

hist = cargar_historico(str(RUTAS["historico"]))
pron = cargar_pronostico(str(RUTAS["pronostico"]))

# ─── Líneas problemáticas ──────────────────────────────────────────────
LINEAS_ADVERTENCIA = set()
for linea in pron["Linea"].unique():
    vals = pron.loc[pron["Linea"] == linea, "Cantidad_Pronosticada"]
    pct_ceros = (vals == 0).sum() / len(vals)
    if pct_ceros > 0.5 or vals.sum() < 500:
        LINEAS_ADVERTENCIA.add(linea)

# Orden oficial de líneas de producto (recategorización 2026)
ORDEN_LINEAS = [
    "JEANS", "CAMISETA", "BLUSA-CAMISA", "CORTOS", "SOBRETODOS", "CALZADO",
    "DEPORTIVOS", "CORPORATIVOS", "PANTALONES", "ACCESORIOS", "PRENDAS DE MODA",
    "ROPA INTERIOR", "BOLSAS", "TEJIDO", "TOP-BODY", "COMPLEMENTOS", "BEAUTY",
]

def ordenar_lineas(lista):
    """Ordena una lista de líneas según ORDEN_LINEAS; las no listadas van al final."""
    orden_map = {l: i for i, l in enumerate(ORDEN_LINEAS)}
    return sorted(lista, key=lambda x: orden_map.get(x, 999))

LINEAS_ACTIVAS = ordenar_lineas([l for l in pron["Linea"].unique() if l not in LINEAS_ADVERTENCIA])
TODAS_LINEAS = ordenar_lineas(list(pron["Linea"].unique()))

# ─── Datos agregados ───────────────────────────────────────────────────
hist_mensual = hist.groupby(["fecha", "Linea"])["Cantidad"].sum().reset_index()
hist_total = hist.groupby("fecha")["Cantidad"].sum().reset_index()

pron_activo = pron[pron["Linea"].isin(LINEAS_ACTIVAS)]
pron_total = pron_activo.groupby("fecha").agg(
    Cantidad_Pronosticada=("Cantidad_Pronosticada", "sum"),
    Limite_Inferior=("Limite_Inferior", "sum"),
    Limite_Superior=("Limite_Superior", "sum"),
).reset_index()

fecha_max_hist = hist["fecha"].max()
primer_mes_pron = pron_activo["fecha"].min()

# ─── Cierre mes en curso (global para todas las páginas) ───────────────
CIERRE_CSV = RUTAS["cierre"]
df_cierre_nb = pd.read_csv(CIERRE_CSV) if CIERRE_CSV.exists() else None

# ─── Estilos CSS — Paleta STOP JEANS ──────────────────────────────────
st.markdown(f"""
<style>
    .main-header {{
        font-size: 2rem;
        font-weight: 700;
        color: {NEGRO};
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }}
    .sub-header {{
        font-size: 1rem;
        color: {GRIS_MEDIO};
        margin-bottom: 1.5rem;
    }}
    .warning-box {{
        background: #FFF3CD;
        border-left: 4px solid #FFC107;
        padding: 0.8rem 1rem;
        border-radius: 4px;
        margin: 0.5rem 0;
    }}
    .logo-container {{
        text-align: center;
        padding: 1rem 0 0.5rem 0;
    }}
    [data-testid="stSidebar"] {{
        background-color: {SIDEBAR_BG};
        border-right: 3px solid {ACENTO};
    }}
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] *,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {{
        color: rgba(255,255,255,0.92) !important;
    }}
    [data-testid="stSidebar"] hr {{
        border-color: rgba(255,255,255,0.15);
    }}
    [data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {{
        background-color: rgba(255,255,255,0.08);
        border-color: rgba(255,255,255,0.2);
        color: white;
    }}
    [data-testid="stSidebar"] .stAlert,
    [data-testid="stSidebar"] .stAlert *,
    [data-testid="stSidebar"] [data-testid="stNotification"],
    [data-testid="stSidebar"] [data-testid="stNotification"] *,
    [data-testid="stSidebar"] [role="alert"],
    [data-testid="stSidebar"] [role="alert"] * {{
        background: none !important;
        background-color: transparent !important;
        color: white !important;
        border: none !important;
        box-shadow: none !important;
    }}
    [data-testid="stMetric"] {{
        background-color: {BLANCO};
        border: 1px solid {GRIS_MUY_CLARO};
        border-left: 4px solid {NEGRO};
        padding: 0.8rem;
        border-radius: 4px;
    }}
    [data-testid="stMetricLabel"] {{
        color: {GRIS_MEDIO};
        font-weight: 600;
    }}
    [data-testid="stMetricValue"] {{
        color: {NEGRO};
        font-weight: 700;
    }}
</style>
""", unsafe_allow_html=True)

# ─── Layout para gráficos Plotly (tema STOP JEANS) ────────────────────
PLOTLY_LAYOUT = dict(
    font=dict(family="Arial, sans-serif", color=NEGRO),
    plot_bgcolor=BLANCO,
    paper_bgcolor=BLANCO,
    xaxis=dict(gridcolor=GRIS_MUY_CLARO, zerolinecolor=GRIS_MUY_CLARO),
    yaxis=dict(gridcolor=GRIS_MUY_CLARO, zerolinecolor=GRIS_MUY_CLARO),
)

# ─── Sidebar: Navegación ───────────────────────────────────────────────
logo_base = LOGO_SVG if marca_sel == "STOP JEANS" else LOGO_SVG_YOYO
logo_activo = logo_base.replace('fill="black"', 'fill="white"')
st.sidebar.markdown(f'<div class="logo-container">{logo_activo}</div>', unsafe_allow_html=True)
st.sidebar.markdown(f'<p style="text-align:center; color:rgba(255,255,255,0.6); font-size:0.85rem; margin-top:-0.5rem;">{marca_sel} — Pronóstico de Ventas</p>', unsafe_allow_html=True)
st.sidebar.markdown("---")
pagina = st.sidebar.radio(
    "Navegación",
    ["📊 Resumen Ejecutivo", "📈 Pronóstico por Línea", "🏢 Visión Total", "📆 Mes en Curso"],
    index=0,
)
st.sidebar.markdown("---")
st.sidebar.caption(f"Datos históricos hasta: **{fecha_max_hist.strftime('%B %Y')}**")
st.sidebar.caption(f"Pronóstico desde: **{primer_mes_pron.strftime('%B %Y')}**")
if LINEAS_ADVERTENCIA:
    st.sidebar.warning(f"Líneas excluidas: {', '.join(sorted(LINEAS_ADVERTENCIA))}")
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Actualizar datos"):
    st.cache_data.clear()
    st.rerun()


# ═══════════════════════════════════════════════════════════════════════
# PÁGINA 1: RESUMEN EJECUTIVO
# ═══════════════════════════════════════════════════════════════════════
if pagina == "📊 Resumen Ejecutivo":
    st.markdown('<p class="main-header">Resumen Ejecutivo — Pronóstico de Ventas</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">Proyección a 12 meses desde {primer_mes_pron.strftime("%B %Y")} | Líneas activas: {len(LINEAS_ACTIVAS)}</p>', unsafe_allow_html=True)

    # Filtro de mes
    fechas_pron = sorted(pron_activo["fecha"].unique())
    opciones_mes = {f.strftime("%B %Y"): f for f in pd.to_datetime(fechas_pron)}
    mes_sel_label = st.selectbox("Seleccione un mes:", list(opciones_mes.keys()), index=0)
    mes_sel = opciones_mes[mes_sel_label]

    total_12m = pron_activo["Cantidad_Pronosticada"].sum()
    total_mes_sel = pron_activo[pron_activo["fecha"] == mes_sel]["Cantidad_Pronosticada"].sum()
    total_q1 = pron_activo[pron_activo["fecha"].isin(fechas_pron[:3])]["Cantidad_Pronosticada"].sum()

    mes_ant = mes_sel - pd.DateOffset(years=1)
    real_mes_ant = hist_mensual[
        (hist_mensual["fecha"] == mes_ant) & (hist_mensual["Linea"].isin(LINEAS_ACTIVAS))
    ]["Cantidad"].sum()
    delta_pct = ((total_mes_sel - real_mes_ant) / real_mes_ant * 100) if real_mes_ant > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label=f"Pronóstico {mes_sel.strftime('%b %Y')}",
            value=f"{total_mes_sel:,.0f} uds",
            delta=f"{delta_pct:+.1f}% vs {mes_ant.strftime('%b %Y')}",
        )
    with col2:
        st.metric(label="Próximo Trimestre", value=f"{total_q1:,.0f} uds")
    with col3:
        st.metric(label="Total 12 Meses", value=f"{total_12m:,.0f} uds")
    with col4:
        promedio_mensual = total_12m / 12
        st.metric(label="Promedio Mensual", value=f"{promedio_mensual:,.0f} uds")

    st.markdown("---")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader(f"Volumen por Línea — {mes_sel.strftime('%B %Y')}")
        df_mes_sel = pron_activo[pron_activo["fecha"] == mes_sel][["Linea", "Cantidad_Pronosticada"]].copy()
        # Orden fijo de líneas (invertido para barras horizontales)
        orden_activas_rev = list(reversed(LINEAS_ACTIVAS))
        df_mes_sel["Linea"] = pd.Categorical(df_mes_sel["Linea"], categories=orden_activas_rev, ordered=True)
        df_mes_sel = df_mes_sel.sort_values("Linea")
        fig = px.bar(
            df_mes_sel, x="Cantidad_Pronosticada", y="Linea",
            orientation="h",
            color="Cantidad_Pronosticada",
            color_continuous_scale=ESCALA_BARRAS,
            text="Cantidad_Pronosticada",
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig.update_layout(
            height=400, showlegend=False, coloraxis_showscale=False,
            xaxis_title="Unidades Pronosticadas", yaxis_title="",
            margin=dict(l=10, r=80, t=10, b=30),
            **PLOTLY_LAYOUT,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader(f"Participación por Línea — {mes_sel.strftime('%B %Y')}")
        df_part = pron_activo[pron_activo["fecha"] == mes_sel].groupby("Linea")["Cantidad_Pronosticada"].sum().reset_index()
        # Orden fijo
        df_part["Linea"] = pd.Categorical(df_part["Linea"], categories=LINEAS_ACTIVAS, ordered=True)
        df_part = df_part.sort_values("Linea")
        fig2 = px.pie(
            df_part, values="Cantidad_Pronosticada", names="Linea",
            color_discrete_sequence=PALETA_LINEAS,
            hole=0.4,
        )
        fig2.update_traces(textposition="inside", textinfo="percent+label")
        fig2.update_layout(height=400, showlegend=False, margin=dict(l=10, r=10, t=10, b=10),
                           paper_bgcolor=BLANCO)
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader(f"Detalle por Línea — {mes_sel.strftime('%B %Y')}")
    df_detalle_mes = pron_activo[pron_activo["fecha"] == mes_sel][["Linea", "Modelo", "Cantidad_Pronosticada", "Limite_Inferior", "Limite_Superior"]].copy()
    df_detalle_mes["Linea"] = pd.Categorical(df_detalle_mes["Linea"], categories=LINEAS_ACTIVAS, ordered=True)
    df_detalle_mes = df_detalle_mes.sort_values("Linea")
    df_detalle_mes_disp = df_detalle_mes.rename(columns={
        "Cantidad_Pronosticada": "Pronóstico",
        "Limite_Inferior": "Lím. Inferior",
        "Limite_Superior": "Lím. Superior",
    })
    total_det = pd.DataFrame([{
        "Linea": "TOTAL", "Modelo": "",
        "Pronóstico": df_detalle_mes_disp["Pronóstico"].sum(),
        "Lím. Inferior": df_detalle_mes_disp["Lím. Inferior"].sum(),
        "Lím. Superior": df_detalle_mes_disp["Lím. Superior"].sum(),
    }])
    df_detalle_mes_disp = pd.concat([df_detalle_mes_disp, total_det], ignore_index=True)
    st.dataframe(
        df_detalle_mes_disp.style.format({
            "Pronóstico": "{:,.0f}",
            "Lím. Inferior": "{:,.0f}",
            "Lím. Superior": "{:,.0f}",
        }),
        use_container_width=True, hide_index=True, height=494,
    )

    st.markdown("---")
    st.subheader("Resumen Anual por Línea")
    resumen = pron_activo.groupby("Linea").agg(
        Modelo=("Modelo", "first"),
        Total_12M=("Cantidad_Pronosticada", "sum"),
    ).reset_index()
    # Separar por año
    fechas_2026 = pron_activo[pron_activo["fecha"].dt.year == 2026]
    fechas_2027 = pron_activo[pron_activo["fecha"].dt.year == 2027]
    res_2026 = fechas_2026.groupby("Linea")["Cantidad_Pronosticada"].sum().rename("Total_2026")
    res_2027 = fechas_2027.groupby("Linea")["Cantidad_Pronosticada"].sum().rename("Total_2027")
    resumen = resumen.merge(res_2026, on="Linea", how="left").merge(res_2027, on="Linea", how="left")
    resumen["Total_2026"] = resumen["Total_2026"].fillna(0).astype(int)
    resumen["Total_2027"] = resumen["Total_2027"].fillna(0).astype(int)
    resumen["Linea"] = pd.Categorical(resumen["Linea"], categories=LINEAS_ACTIVAS, ordered=True)
    resumen = resumen.sort_values("Linea")
    total_res = pd.DataFrame([{
        "Linea": "TOTAL", "Modelo": "",
        "Total_2026": resumen["Total_2026"].sum(),
        "Total_2027": resumen["Total_2027"].sum(),
        "Total_12M": resumen["Total_12M"].sum(),
    }])
    resumen_disp = pd.concat([resumen[["Linea", "Modelo", "Total_2026", "Total_2027", "Total_12M"]], total_res], ignore_index=True)
    st.dataframe(
        resumen_disp.rename(columns={"Total_2026": "Total 2026", "Total_2027": "Total 2027", "Total_12M": "Total 12M"}).style.format({
            "Total 2026": "{:,.0f}", "Total 2027": "{:,.0f}", "Total 12M": "{:,.0f}",
        }),
        use_container_width=True, hide_index=True, height=494,
    )
    if LINEAS_ADVERTENCIA:
        st.markdown(f'<div class="warning-box">Las líneas <b>{", ".join(sorted(LINEAS_ADVERTENCIA))}</b> fueron excluidas del resumen por tener datos insuficientes o pronósticos con mayoría de ceros.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# PÁGINA 2: PRONÓSTICO POR LÍNEA
# ═══════════════════════════════════════════════════════════════════════
elif pagina == "📈 Pronóstico por Línea":
    st.markdown('<p class="main-header">Pronóstico por Línea de Producto</p>', unsafe_allow_html=True)

    linea_sel = st.selectbox("Seleccione una línea:", TODAS_LINEAS, index=0)

    if linea_sel in LINEAS_ADVERTENCIA:
        st.warning(f"La línea **{linea_sel}** tiene datos insuficientes o ventas cercanas a cero. El pronóstico puede no ser confiable.")

    hist_linea = hist_mensual[hist_mensual["Linea"] == linea_sel].sort_values("fecha")
    pron_linea = pron[pron["Linea"] == linea_sel].sort_values("fecha")

    modelo_usado = pron_linea["Modelo"].iloc[0] if len(pron_linea) > 0 else "N/A"

    col1, col2, col3, col4 = st.columns(4)
    total_pron_linea = pron_linea["Cantidad_Pronosticada"].sum()
    prom_hist = hist_linea["Cantidad"].mean() if len(hist_linea) > 0 else 0
    prom_pron = pron_linea["Cantidad_Pronosticada"].mean()

    with col1:
        st.metric("Total Pronóstico 12M", f"{total_pron_linea:,.0f} uds")
    with col2:
        st.metric("Promedio Histórico/Mes", f"{prom_hist:,.0f} uds")
    with col3:
        st.metric("Promedio Pronóstico/Mes", f"{prom_pron:,.0f} uds")
    with col4:
        st.metric("Modelo Seleccionado", modelo_usado)

    st.markdown("---")

    meses_recientes = st.slider("Meses históricos a mostrar:", 6, len(hist_linea), min(18, len(hist_linea)))
    hist_reciente = hist_linea.tail(meses_recientes)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist_reciente["fecha"], y=hist_reciente["Cantidad"],
        mode="lines+markers", name="Histórico",
        line=dict(color=NEGRO, width=2.5),
        marker=dict(size=5, color=NEGRO),
        hovertemplate="<b>%{x|%b %Y}</b><br>Cantidad: %{y:,.0f}<extra></extra>",
    ))
    if len(hist_linea) > 0 and len(pron_linea) > 0:
        fig.add_trace(go.Scatter(
            x=[hist_linea["fecha"].iloc[-1], pron_linea["fecha"].iloc[0]],
            y=[hist_linea["Cantidad"].iloc[-1], pron_linea["Cantidad_Pronosticada"].iloc[0]],
            mode="lines", showlegend=False,
            line=dict(color=ACENTO, width=1.5, dash="dot"),
        ))
    # Intervalo de confianza (área sombreada)
    tiene_intervalo = not (pron_linea["Limite_Inferior"] == pron_linea["Limite_Superior"]).all()
    if tiene_intervalo:
        fig.add_trace(go.Scatter(
            x=pron_linea["fecha"], y=pron_linea["Limite_Superior"],
            mode="lines", name="Límite Superior",
            line=dict(width=0), showlegend=False,
            hovertemplate="<b>%{x|%b %Y}</b><br>Límite superior: %{y:,.0f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=pron_linea["fecha"], y=pron_linea["Limite_Inferior"],
            mode="lines", name="Intervalo 80%",
            line=dict(width=0),
            fill="tonexty", fillcolor=FILL_INTERVALO,
            hovertemplate="<b>%{x|%b %Y}</b><br>Límite inferior: %{y:,.0f}<extra></extra>",
        ))
    fig.add_trace(go.Scatter(
        x=pron_linea["fecha"], y=pron_linea["Cantidad_Pronosticada"],
        mode="lines+markers", name="Pronóstico",
        line=dict(color=ACENTO, width=2.5, dash="dash"),
        marker=dict(size=7, symbol="diamond", color=ACENTO),
        hovertemplate="<b>%{x|%b %Y}</b><br>Pronóstico: %{y:,.0f}<extra></extra>",
    ))
    fig.add_vline(x=fecha_max_hist, line_dash="dot", line_color=GRIS_CLARO, opacity=0.7)
    fig.update_layout(
        title=f"Línea: {linea_sel}",
        xaxis_title="", yaxis_title="Unidades",
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=20, t=60, b=30),
        hovermode="x unified",
        **PLOTLY_LAYOUT,
    )
    st.plotly_chart(fig, use_container_width=True)

    col_tabla, col_comp = st.columns([3, 2])
    with col_tabla:
        st.subheader("Pronóstico Mensual")
        tabla_pron = pron_linea[["fecha", "Cantidad_Pronosticada", "Limite_Inferior", "Limite_Superior"]].copy()
        tabla_pron["Mes"] = tabla_pron["fecha"].dt.strftime("%B %Y")
        tabla_pron = tabla_pron.rename(columns={
            "Cantidad_Pronosticada": "Pronóstico",
            "Limite_Inferior": "Lím. Inferior",
            "Limite_Superior": "Lím. Superior",
        })
        fmt = {"Pronóstico": "{:,.0f}", "Lím. Inferior": "{:,.0f}", "Lím. Superior": "{:,.0f}"}
        cols_mostrar = ["Mes", "Pronóstico", "Lím. Inferior", "Lím. Superior"]
        if marca_sel == "STOP JEANS" and "Ajuste_Venta_Perdida_Pct" in pron_linea.columns:
            tabla_pron["Ajuste VP"] = (pron_linea["Ajuste_Venta_Perdida_Pct"].values * 100).round(1)
            fmt["Ajuste VP"] = "{:.1f}%"
            cols_mostrar = ["Mes", "Pronóstico", "Lím. Inferior", "Lím. Superior", "Ajuste VP"]

        for anio in sorted(tabla_pron["fecha"].dt.year.unique()):
            bloque = tabla_pron[tabla_pron["fecha"].dt.year == anio][cols_mostrar].copy()
            subtotal = pd.DataFrame([{
                "Mes": f"TOTAL {anio}",
                "Pronóstico": bloque["Pronóstico"].sum(),
                "Lím. Inferior": bloque["Lím. Inferior"].sum(),
                "Lím. Superior": bloque["Lím. Superior"].sum(),
            }])
            bloque = pd.concat([bloque, subtotal], ignore_index=True)
            st.caption(f"**{anio}**")
            st.dataframe(bloque.style.format(fmt), use_container_width=True, hide_index=True, height=494)

    with col_comp:
        st.subheader("Comparativa Interanual")
        st.markdown("<div style='height:36px'></div>", unsafe_allow_html=True)
        ultimo_ano_hist = hist_linea[hist_linea["fecha"] >= (fecha_max_hist - pd.DateOffset(months=11))]
        if len(ultimo_ano_hist) > 0:
            comp = pd.DataFrame({
                "Mes": [f.strftime("%b") for f in ultimo_ano_hist["fecha"]],
                f"Real {ultimo_ano_hist['fecha'].dt.year.iloc[0]}": ultimo_ano_hist["Cantidad"].values,
            })
            st.dataframe(comp.style.format({col: "{:,.0f}" for col in comp.columns if col != "Mes"}),
                         use_container_width=True, hide_index=True, height=494)


# ═══════════════════════════════════════════════════════════════════════
# PÁGINA 3: VISIÓN TOTAL
# ═══════════════════════════════════════════════════════════════════════
elif pagina == "🏢 Visión Total":
    st.markdown('<p class="main-header">Visión Total — Todas las Líneas</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">Serie agregada (líneas activas: {len(LINEAS_ACTIVAS)})</p>', unsafe_allow_html=True)

    hist_total_activo = hist_mensual[hist_mensual["Linea"].isin(LINEAS_ACTIVAS)].groupby("fecha")["Cantidad"].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist_total_activo["fecha"], y=hist_total_activo["Cantidad"],
        mode="lines", name="Histórico",
        line=dict(color=NEGRO, width=2),
        fill="tozeroy", fillcolor="rgba(0,0,0,0.05)",
        hovertemplate="<b>%{x|%b %Y}</b><br>Real: %{y:,.0f}<extra></extra>",
    ))
    if len(hist_total_activo) > 0 and len(pron_total) > 0:
        fig.add_trace(go.Scatter(
            x=[hist_total_activo["fecha"].iloc[-1], pron_total["fecha"].iloc[0]],
            y=[hist_total_activo["Cantidad"].iloc[-1], pron_total["Cantidad_Pronosticada"].iloc[0]],
            mode="lines", showlegend=False,
            line=dict(color=ACENTO, width=1.5, dash="dot"),
        ))
    # Intervalo de confianza agregado
    tiene_intervalo_total = not (pron_total["Limite_Inferior"] == pron_total["Limite_Superior"]).all()
    if tiene_intervalo_total:
        fig.add_trace(go.Scatter(
            x=pron_total["fecha"], y=pron_total["Limite_Superior"],
            mode="lines", name="Límite Superior", line=dict(width=0), showlegend=False,
            hovertemplate="<b>%{x|%b %Y}</b><br>Límite superior: %{y:,.0f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=pron_total["fecha"], y=pron_total["Limite_Inferior"],
            mode="lines", name="Intervalo 80%", line=dict(width=0),
            fill="tonexty", fillcolor=FILL_INTERVALO,
            hovertemplate="<b>%{x|%b %Y}</b><br>Límite inferior: %{y:,.0f}<extra></extra>",
        ))
    fig.add_trace(go.Scatter(
        x=pron_total["fecha"], y=pron_total["Cantidad_Pronosticada"],
        mode="lines+markers", name="Pronóstico",
        line=dict(color=ACENTO, width=2.5, dash="dash"),
        marker=dict(size=6, symbol="diamond", color=ACENTO),
        hovertemplate="<b>%{x|%b %Y}</b><br>Pronóstico: %{y:,.0f}<extra></extra>",
    ))
    fig.add_vline(x=fecha_max_hist, line_dash="dot", line_color=GRIS_CLARO, opacity=0.7)
    fig.update_layout(
        title="Ventas Totales: Histórico + Pronóstico 12 Meses",
        xaxis_title="", yaxis_title="Unidades Totales",
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=20, t=60, b=30),
        hovermode="x unified",
        **PLOTLY_LAYOUT,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pronóstico Mensual Total")
        pron_total_disp = pron_total.copy()
        pron_total_disp["Mes"] = pron_total_disp["fecha"].dt.strftime("%B %Y")
        pron_total_disp = pron_total_disp.rename(columns={"Cantidad_Pronosticada": "Unidades"})

        fig_bar = px.bar(
            pron_total_disp, x="Mes", y="Unidades",
            color="Unidades",
            color_continuous_scale=ESCALA_BARRAS,
            text="Unidades",
        )
        fig_bar.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig_bar.update_layout(
            height=400, showlegend=False, coloraxis_showscale=False,
            xaxis_title="", yaxis_title="Unidades",
            margin=dict(l=50, r=20, t=10, b=80),
            xaxis_tickangle=-45,
            **PLOTLY_LAYOUT,
        )
        avg = pron_total_disp["Unidades"].mean()
        fig_bar.add_hline(y=avg, line_dash="dash", line_color=ACENTO,
                          annotation_text=f"Promedio: {avg:,.0f}", annotation_position="top right")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("Distribución por Línea (Treemap)")
        df_tree = pron_activo.groupby("Linea")["Cantidad_Pronosticada"].sum().reset_index()
        fig_tree = px.treemap(
            df_tree, path=["Linea"], values="Cantidad_Pronosticada",
            color="Cantidad_Pronosticada",
            color_continuous_scale=ESCALA_MARCA,
        )
        fig_tree.update_layout(height=400, margin=dict(l=10, r=10, t=10, b=10),
                               coloraxis_showscale=False, paper_bgcolor=BLANCO)
        fig_tree.update_traces(
            textinfo="label+value+percent root",
            texttemplate="<b>%{label}</b><br>%{value:,.0f}<br>%{percentRoot:.1%}",
        )
        st.plotly_chart(fig_tree, use_container_width=True)

    st.subheader("Composición del Pronóstico por Línea")
    st.caption("Real (meses cerrados) · Proyección (mes en curso) · Pronóstico (meses futuros)")
    orden_idx = {l: i for i, l in enumerate(LINEAS_ACTIVAS)}

    # ── Construir tabla combinada: Real + Proyección mes curso + Pronóstico ──
    anio_pron = primer_mes_pron.year  # año de inicio del pronóstico (2026)

    # Meses reales: solo meses completamente cerrados (antes del mes en curso)
    mes_curso_dt = fecha_max_hist.replace(day=1)
    meses_cerrados = hist_mensual[
        (hist_mensual["fecha"].dt.year == anio_pron) &
        (hist_mensual["fecha"] < mes_curso_dt) &
        (hist_mensual["Linea"].isin(LINEAS_ACTIVAS))
    ]["fecha"].unique()
    cols_real = {}
    for f in sorted(meses_cerrados):
        lbl = pd.Timestamp(f).strftime("%b %Y") + " ✓"
        cols_real[lbl] = hist_mensual[
            (hist_mensual["fecha"] == f) & (hist_mensual["Linea"].isin(LINEAS_ACTIVAS))
        ].set_index("Linea")["Cantidad"]

    # Mes en curso: solo proyección (sin parcial)
    cols_curso = {}
    if df_cierre_nb is not None and "Pronostico_Modelo" in df_cierre_nb.columns:
        lbl_curso = mes_curso_dt.strftime("%b %Y") + " ~"
        cols_curso[lbl_curso] = df_cierre_nb.set_index("Linea")["Pronostico_Modelo"]

    # Pronóstico (meses futuros) separado por año
    fechas_ord = sorted(pron_activo["fecha"].unique())

    for anio in sorted(set(pd.to_datetime(fechas_ord).year)):
        fechas_anio = [f for f in pd.to_datetime(fechas_ord) if f.year == anio]
        pron_anio = pron_activo[pron_activo["fecha"].isin(fechas_anio)]
        comp = pron_anio.pivot_table(
            index="Linea", columns=pron_anio["fecha"].dt.strftime("%b %Y"),
            values="Cantidad_Pronosticada", aggfunc="sum",
        )
        cols_anio_ord = [f.strftime("%b %Y") for f in fechas_anio]
        comp = comp[[c for c in cols_anio_ord if c in comp.columns]]

        # Agregar columnas reales y proyección al primer año en orden cronológico
        if anio == anio_pron:
            for lbl, serie in {**cols_real, **cols_curso}.items():
                comp[lbl] = serie.reindex(comp.index).fillna(0).astype(int)
            # Reordenar: reales (Jan, Feb...) + proyección (Mar~) + pronósticos (Apr...)
            cols_ordenadas = (
                [c for c in comp.columns if "✓" in c] +
                [c for c in comp.columns if "~" in c] +
                [c for c in comp.columns if "✓" not in c and "~" not in c]
            )
            comp = comp[cols_ordenadas]

        comp["TOTAL"] = comp.sum(axis=1)
        comp["_orden"] = comp.index.map(lambda x: orden_idx.get(x, 999))
        comp = comp.sort_values("_orden").drop(columns=["_orden"])
        total_row = comp.sum(numeric_only=True)
        total_row.name = "TOTAL"
        comp = pd.concat([comp, total_row.to_frame().T])
        st.caption(f"**{anio}** — ✓ Real  · ~ Proyección cierre  · resto Pronóstico modelo")
        st.dataframe(comp.style.format("{:,.0f}"), use_container_width=True, height=494)

        # ── Tabla de crecimiento vs año anterior (solo para el año de pronóstico) ──
        if anio == anio_pron:
            st.markdown("---")
            st.subheader(f"Crecimiento vs {anio_pron - 1}")

            fechas_real = [pd.Timestamp(f) for f in sorted(meses_cerrados)]
            fechas_curso = [mes_curso_dt] if cols_curso else []
            fechas_pron_anio = [f for f in pd.to_datetime(fechas_ord) if f.year == anio_pron]
            todos_meses_2026 = sorted(set(fechas_real + fechas_curso + fechas_pron_anio))
            crec_data = {}
            totales_2026 = {}
            totales_2025 = {}
            for f_2026 in todos_meses_2026:
                f_2025 = f_2026 - pd.DateOffset(years=1)
                lbl = f_2026.strftime("%b %Y")
                if f_2026 < primer_mes_pron:
                    val_2026 = hist_mensual[
                        (hist_mensual["fecha"] == f_2026) & (hist_mensual["Linea"].isin(LINEAS_ACTIVAS))
                    ].groupby("Linea")["Cantidad"].sum()
                elif f_2026 == mes_curso_dt and cols_curso:
                    val_2026 = df_cierre_nb.set_index("Linea")["Pronostico_Modelo"].reindex(LINEAS_ACTIVAS).fillna(0)
                else:
                    val_2026 = pron_activo[pron_activo["fecha"] == f_2026].set_index("Linea")["Cantidad_Pronosticada"].reindex(LINEAS_ACTIVAS).fillna(0)
                val_2025 = hist_mensual[
                    (hist_mensual["fecha"] == f_2025) & (hist_mensual["Linea"].isin(LINEAS_ACTIVAS))
                ].groupby("Linea")["Cantidad"].sum().reindex(LINEAS_ACTIVAS).fillna(0)
                crec = ((val_2026 - val_2025) / val_2025.replace(0, 1) * 100).round(1)
                crec_data[lbl] = crec
                totales_2026[lbl] = val_2026.sum()
                totales_2025[lbl] = val_2025.sum()

            if crec_data:
                df_crec = pd.DataFrame(crec_data)
                df_crec["_orden"] = df_crec.index.map(lambda x: orden_idx.get(x, 999))
                df_crec = df_crec.sort_values("_orden").drop(columns=["_orden"])
                total_crec = pd.Series({
                    col: round((totales_2026[col] - totales_2025[col]) / totales_2025[col] * 100, 1)
                    if totales_2025[col] > 0 else 0
                    for col in df_crec.columns
                }, name="TOTAL")
                df_crec = pd.concat([df_crec, total_crec.to_frame().T])

                def color_crec(val):
                    try:
                        v = float(val)
                        return f"color: {POSITIVO}" if v > 0 else f"color: {NEGATIVO}"
                    except:
                        return ""

                st.dataframe(
                    df_crec.style.format("{:+.1f}%").applymap(color_crec),
                    use_container_width=True,
                    height=494,
                )
            st.markdown("---")


# ═══════════════════════════════════════════════════════════════════════
# PÁGINA 4: MES EN CURSO
# ═══════════════════════════════════════════════════════════════════════
elif pagina == "📆 Mes en Curso":
    mes_curso = fecha_max_hist.replace(day=1)
    mes_curso_fin = mes_curso + pd.offsets.MonthEnd(0)
    dias_mes = mes_curso_fin.day

    # df_cierre_nb ya cargado globalmente
    dia_corte_default = 15
    if df_cierre_nb is not None and "Dias_Transcurridos" in df_cierre_nb.columns:
        dia_corte_default = int(df_cierre_nb["Dias_Transcurridos"].iloc[0])

    # Input: día de corte
    dia_corte = st.number_input(
        "Día de corte (día del mes hasta el que tienes datos):",
        min_value=1, max_value=dias_mes, value=dia_corte_default, step=1,
    )
    pct_mes = dia_corte / dias_mes

    st.markdown(f'<p class="main-header">Mes en Curso: {mes_curso.strftime("%B %Y")}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">Datos reales al día {dia_corte} de {dias_mes} ({pct_mes:.0%} del mes transcurrido)</p>', unsafe_allow_html=True)

    # Ventas parciales del mes en curso y año anterior
    hist_mes_curso = hist_mensual[
        (hist_mensual["fecha"] == mes_curso) & (hist_mensual["Linea"].isin(LINEAS_ACTIVAS))
    ].copy()
    mes_ant_ano = mes_curso - pd.DateOffset(years=1)
    hist_mes_ant = hist_mensual[
        (hist_mensual["fecha"] == mes_ant_ano) & (hist_mensual["Linea"].isin(LINEAS_ACTIVAS))
    ].copy()
    col_real_ant = f"Real_{mes_ant_ano.strftime('%b_%Y')}"

    # DataFrame base
    df_curso = pd.DataFrame({"Linea": LINEAS_ACTIVAS})
    df_curso = df_curso.merge(
        hist_mes_curso[["Linea", "Cantidad"]].rename(columns={"Cantidad": "Venta_Parcial"}),
        on="Linea", how="left",
    )
    df_curso = df_curso.merge(
        hist_mes_ant[["Linea", "Cantidad"]].rename(columns={"Cantidad": col_real_ant}),
        on="Linea", how="left",
    )
    df_curso["Venta_Parcial"] = df_curso["Venta_Parcial"].fillna(0).astype(int)
    df_curso[col_real_ant] = df_curso[col_real_ant].fillna(0).astype(int)

    # Proyección Cierre: regla de 3 según dia_corte del usuario
    df_curso["Proyeccion_Cierre"] = (
        (df_curso["Venta_Parcial"] / pct_mes).round(0).astype(int)
        if pct_mes > 0 else df_curso["Venta_Parcial"]
    )

    # Pronóstico del Modelo y Cierre Estimado (desde cierre_mes_curso.csv)
    tiene_modelo = df_cierre_nb is not None and "Pronostico_Modelo" in df_cierre_nb.columns
    if tiene_modelo:
        df_curso = df_curso.merge(
            df_cierre_nb[["Linea", "Pronostico_Modelo"]].copy(),
            on="Linea", how="left",
        )
        df_curso["Pronostico_Modelo"] = df_curso["Pronostico_Modelo"].fillna(0).astype(int)
        df_curso["Cierre_Estimado"] = (
            ((df_curso["Proyeccion_Cierre"] + df_curso["Pronostico_Modelo"]) / 2).round(0).astype(int)
        )
    else:
        df_curso["Cierre_Estimado"] = df_curso["Proyeccion_Cierre"]

    # Crecimiento vs año anterior (sobre Cierre Estimado)
    df_curso["Crecimiento_%"] = (
        (df_curso["Cierre_Estimado"] - df_curso[col_real_ant])
        / df_curso[col_real_ant].replace(0, 1) * 100
    ).round(1)
    df_curso["Linea"] = pd.Categorical(df_curso["Linea"], categories=LINEAS_ACTIVAS, ordered=True)
    df_curso = df_curso.sort_values("Linea")

    # Totales para KPIs
    total_parcial   = df_curso["Venta_Parcial"].sum()
    total_proy      = df_curso["Proyeccion_Cierre"].sum()
    total_modelo    = df_curso["Pronostico_Modelo"].sum() if tiene_modelo else 0
    total_cierre    = df_curso["Cierre_Estimado"].sum()
    total_real_ant  = df_curso[col_real_ant].sum()
    crec_total      = ((total_cierre - total_real_ant) / total_real_ant * 100) if total_real_ant > 0 else 0

    # KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Venta Parcial", f"{total_parcial:,.0f} uds", f"Al día {dia_corte} de {dias_mes}")
    with col2:
        st.metric("Proyección de Cierre", f"{total_proy:,.0f} uds")
    with col3:
        st.metric("Pronóstico del Modelo", f"{total_modelo:,.0f} uds" if tiene_modelo else "N/D")
    with col4:
        st.metric("Cierre Estimado", f"{total_cierre:,.0f} uds")
    with col5:
        st.metric(f"Real {mes_ant_ano.strftime('%b %Y')}", f"{total_real_ant:,.0f} uds",
                  f"{crec_total:+.1f}% vs año anterior")

    st.markdown("---")

    col_g1, col_g2 = st.columns([3, 2])

    with col_g1:
        st.subheader("Comparativa por Línea")
        fig_curso = go.Figure()
        fig_curso.add_trace(go.Bar(
            y=df_curso["Linea"], x=df_curso["Venta_Parcial"],
            name=f"Venta al día {dia_corte}",
            orientation="h", marker_color=GRIS_MUY_CLARO,
            text=df_curso["Venta_Parcial"].apply(lambda x: f"{x:,.0f}"),
            textposition="inside",
        ))
        fig_curso.add_trace(go.Bar(
            y=df_curso["Linea"], x=df_curso[col_real_ant],
            name=f"Real {mes_ant_ano.strftime('%b %Y')}",
            orientation="h", marker_color=GRIS_MEDIO,
            text=df_curso[col_real_ant].apply(lambda x: f"{x:,.0f}"),
            textposition="inside",
        ))
        fig_curso.add_trace(go.Scatter(
            y=df_curso["Linea"], x=df_curso["Proyeccion_Cierre"],
            name="Proyección Cierre",
            mode="markers",
            marker=dict(size=10, symbol="diamond", color=GRIS_OSCURO, line=dict(width=1, color=BLANCO)),
            hovertemplate="<b>%{y}</b><br>Proyección: %{x:,.0f}<extra></extra>",
        ))
        if tiene_modelo:
            fig_curso.add_trace(go.Scatter(
                y=df_curso["Linea"], x=df_curso["Cierre_Estimado"],
                name="Cierre Estimado",
                mode="markers",
                marker=dict(size=13, symbol="star", color=ACENTO, line=dict(width=1, color=BLANCO)),
                hovertemplate="<b>%{y}</b><br>Cierre estimado: %{x:,.0f}<extra></extra>",
            ))
        fig_curso.update_layout(
            barmode="group", height=420,
            margin=dict(l=10, r=20, t=10, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_title="Unidades",
            **PLOTLY_LAYOUT,
        )
        st.plotly_chart(fig_curso, use_container_width=True)

    with col_g2:
        st.subheader("Crecimiento vs Año Anterior")
        df_crec_curso = df_curso[["Linea", "Crecimiento_%"]].sort_values("Crecimiento_%", ascending=True)
        colores_crec = [POSITIVO if v > 0 else NEGATIVO for v in df_crec_curso["Crecimiento_%"]]
        fig_crec = go.Figure(go.Bar(
            y=df_crec_curso["Linea"], x=df_crec_curso["Crecimiento_%"],
            orientation="h", marker_color=colores_crec,
            text=df_crec_curso["Crecimiento_%"].apply(lambda x: f"{x:+.1f}%"),
            textposition="outside",
        ))
        fig_crec.update_layout(
            height=420, xaxis_title="% Crecimiento",
            margin=dict(l=10, r=60, t=10, b=30),
            **PLOTLY_LAYOUT,
        )
        st.plotly_chart(fig_crec, use_container_width=True)

    # Tabla detallada
    st.subheader("Detalle por Línea")
    cols_tabla = ["Linea", "Venta_Parcial", "Proyeccion_Cierre"]
    nombres_tabla = {
        "Venta_Parcial":    f"Venta al día {dia_corte}",
        "Proyeccion_Cierre": "Proyección Cierre",
        col_real_ant:        f"Real {mes_ant_ano.strftime('%b %Y')}",
        "Crecimiento_%":    "Crecimiento %",
    }
    fmt_tabla = {
        f"Venta al día {dia_corte}": "{:,.0f}",
        "Proyección Cierre":         "{:,.0f}",
        f"Real {mes_ant_ano.strftime('%b %Y')}": "{:,.0f}",
        "Crecimiento %":             "{:+.1f}%",
    }
    if tiene_modelo:
        cols_tabla += ["Pronostico_Modelo", "Cierre_Estimado"]
        nombres_tabla["Pronostico_Modelo"] = "Pronóstico Modelo"
        nombres_tabla["Cierre_Estimado"]   = "Cierre Estimado"
        fmt_tabla["Pronóstico Modelo"]     = "{:,.0f}"
        fmt_tabla["Cierre Estimado"]       = "{:,.0f}"
    cols_tabla += [col_real_ant, "Crecimiento_%"]

    st.dataframe(
        df_curso[cols_tabla].rename(columns=nombres_tabla).style.format(fmt_tabla),
        use_container_width=True, hide_index=True, height=494,
    )

    nota_dia = f"día {dia_corte_default}" if df_cierre_nb is not None else f"día {dia_corte}"
    st.markdown(
        f'<div class="warning-box">'
        f'<b>Proyección Cierre</b>: regla de 3 proporcional sobre la venta parcial al día {dia_corte}. '
        f'<b>Pronóstico Modelo</b>: calculado por el modelo ML con datos al {nota_dia} (requiere re-ejecutar celda 35 del notebook para actualizar). '
        f'<b>Cierre Estimado</b>: promedio de ambos métodos.'
        f'</div>',
        unsafe_allow_html=True,
    )


# ─── Footer ────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f'<p style="text-align:center; color:{GRIS_CLARO}; font-size:0.8rem;">Proyecto Final — Especialización Inteligencia de Negocios | UPB | Pronóstico con skforecast + scikit-learn</p>', unsafe_allow_html=True)
