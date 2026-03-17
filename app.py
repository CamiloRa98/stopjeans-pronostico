"""
Dashboard de Pronóstico de Ventas — STOP JEANS
Especialización Inteligencia de Negocios | UPB
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ─── Configuración de página ───────────────────────────────────────────
st.set_page_config(
    page_title="STOP JEANS — Pronóstico de Ventas",
    page_icon="👖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Rutas de archivos (relativas al repo) ─────────────────────────────
BASE_DIR = Path(__file__).parent

HISTORICO_CSV = BASE_DIR / "data" / "Ventas_linea.csv"
PRONOSTICO_CSV = BASE_DIR / "data" / "pronostico_ventas_por_linea.csv"


# ─── Carga de datos (cacheada) ─────────────────────────────────────────
@st.cache_data
def cargar_historico():
    df = pd.read_csv(HISTORICO_CSV, sep=";")
    df["fecha"] = pd.to_datetime(df["fecha"], format="%d/%m/%Y")
    return df


@st.cache_data
def cargar_pronostico():
    df = pd.read_csv(PRONOSTICO_CSV)
    df["fecha"] = pd.to_datetime(df["fecha"])
    # Eliminar valores negativos residuales
    df["Cantidad_Pronosticada"] = df["Cantidad_Pronosticada"].clip(lower=0)
    return df


hist = cargar_historico()
pron = cargar_pronostico()

# ─── Líneas problemáticas ──────────────────────────────────────────────
# Líneas con datos insuficientes o pronósticos poco confiables
LINEAS_ADVERTENCIA = set()
for linea in pron["Linea"].unique():
    vals = pron.loc[pron["Linea"] == linea, "Cantidad_Pronosticada"]
    pct_ceros = (vals == 0).sum() / len(vals)
    if pct_ceros > 0.5 or vals.sum() < 500:
        LINEAS_ADVERTENCIA.add(linea)

# Líneas activas (excluir las problemáticas del resumen principal)
LINEAS_ACTIVAS = sorted([l for l in pron["Linea"].unique() if l not in LINEAS_ADVERTENCIA])
TODAS_LINEAS = sorted(pron["Linea"].unique())

# ─── Datos agregados ───────────────────────────────────────────────────
hist_mensual = hist.groupby(["fecha", "Linea"])["Cantidad"].sum().reset_index()
hist_total = hist.groupby("fecha")["Cantidad"].sum().reset_index()

pron_activo = pron[pron["Linea"].isin(LINEAS_ACTIVAS)]
pron_total = pron_activo.groupby("fecha")["Cantidad_Pronosticada"].sum().reset_index()

# Fecha máxima del histórico y primer mes de pronóstico
fecha_max_hist = hist["fecha"].max()
primer_mes_pron = pron_activo["fecha"].min()

# ─── Estilos CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1B3A5C;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        margin-bottom: 1.5rem;
    }
    .warning-box {
        background: #FFF3CD;
        border-left: 4px solid #FFC107;
        padding: 0.8rem 1rem;
        border-radius: 4px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar: Navegación ───────────────────────────────────────────────
st.sidebar.markdown("## 👖 STOP JEANS")
st.sidebar.markdown("**Pronóstico de Ventas**")
st.sidebar.markdown("---")
pagina = st.sidebar.radio(
    "Navegación",
    ["📊 Resumen Ejecutivo", "📈 Pronóstico por Línea", "🏢 Visión Total", "📅 Próximo Mes"],
    index=0,
)
st.sidebar.markdown("---")
st.sidebar.caption(f"Datos históricos hasta: **{fecha_max_hist.strftime('%B %Y')}**")
st.sidebar.caption(f"Pronóstico desde: **{primer_mes_pron.strftime('%B %Y')}**")
if LINEAS_ADVERTENCIA:
    st.sidebar.warning(f"Líneas excluidas del resumen por datos insuficientes: {', '.join(sorted(LINEAS_ADVERTENCIA))}")


# ═══════════════════════════════════════════════════════════════════════
# PÁGINA 1: RESUMEN EJECUTIVO
# ═══════════════════════════════════════════════════════════════════════
if pagina == "📊 Resumen Ejecutivo":
    st.markdown('<p class="main-header">Resumen Ejecutivo — Pronóstico de Ventas</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">Proyección a 12 meses desde {primer_mes_pron.strftime("%B %Y")} | Líneas activas: {len(LINEAS_ACTIVAS)}</p>', unsafe_allow_html=True)

    # KPIs principales
    total_12m = pron_activo["Cantidad_Pronosticada"].sum()
    total_mes1 = pron_activo[pron_activo["fecha"] == primer_mes_pron]["Cantidad_Pronosticada"].sum()

    # Trimestre (primeros 3 meses del pronóstico)
    fechas_pron = sorted(pron_activo["fecha"].unique())
    total_q1 = pron_activo[pron_activo["fecha"].isin(fechas_pron[:3])]["Cantidad_Pronosticada"].sum()

    # Mismo mes del año anterior para delta
    mes_ant = primer_mes_pron - pd.DateOffset(years=1)
    real_mes_ant = hist_mensual[
        (hist_mensual["fecha"] == mes_ant) & (hist_mensual["Linea"].isin(LINEAS_ACTIVAS))
    ]["Cantidad"].sum()
    delta_pct = ((total_mes1 - real_mes_ant) / real_mes_ant * 100) if real_mes_ant > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label=f"Pronóstico {primer_mes_pron.strftime('%b %Y')}",
            value=f"{total_mes1:,.0f} uds",
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

    # Top líneas por volumen primer mes
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader(f"Volumen por Línea — {primer_mes_pron.strftime('%B %Y')}")
        df_mes1 = pron_activo[pron_activo["fecha"] == primer_mes_pron][["Linea", "Cantidad_Pronosticada"]].copy()
        df_mes1 = df_mes1.sort_values("Cantidad_Pronosticada", ascending=True)
        fig = px.bar(
            df_mes1, x="Cantidad_Pronosticada", y="Linea",
            orientation="h",
            color="Cantidad_Pronosticada",
            color_continuous_scale=["#B8D4E8", "#1B3A5C"],
            text="Cantidad_Pronosticada",
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig.update_layout(
            height=400,
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title="Unidades Pronosticadas",
            yaxis_title="",
            margin=dict(l=10, r=80, t=10, b=30),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Participación por Línea (12 meses)")
        df_part = pron_activo.groupby("Linea")["Cantidad_Pronosticada"].sum().reset_index()
        df_part = df_part.sort_values("Cantidad_Pronosticada", ascending=False)
        fig2 = px.pie(
            df_part, values="Cantidad_Pronosticada", names="Linea",
            color_discrete_sequence=px.colors.sequential.Blues_r,
            hole=0.4,
        )
        fig2.update_traces(textposition="inside", textinfo="percent+label")
        fig2.update_layout(height=400, showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig2, use_container_width=True)

    # Tabla resumen
    st.subheader("Resumen por Línea")
    resumen = pron_activo.groupby("Linea").agg(
        Modelo=("Modelo", "first"),
        Total_12M=("Cantidad_Pronosticada", "sum"),
        Promedio_Mes=("Cantidad_Pronosticada", "mean"),
        Mes_Max=("Cantidad_Pronosticada", "max"),
        Mes_Min=("Cantidad_Pronosticada", "min"),
    ).reset_index().sort_values("Total_12M", ascending=False)
    resumen["Promedio_Mes"] = resumen["Promedio_Mes"].round(0).astype(int)
    st.dataframe(
        resumen.style.format({
            "Total_12M": "{:,.0f}",
            "Promedio_Mes": "{:,.0f}",
            "Mes_Max": "{:,.0f}",
            "Mes_Min": "{:,.0f}",
        }),
        use_container_width=True,
        hide_index=True,
    )

    if LINEAS_ADVERTENCIA:
        st.markdown(f'<div class="warning-box">⚠️ Las líneas <b>{", ".join(sorted(LINEAS_ADVERTENCIA))}</b> fueron excluidas del resumen por tener datos insuficientes o pronósticos con mayoría de ceros.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# PÁGINA 2: PRONÓSTICO POR LÍNEA
# ═══════════════════════════════════════════════════════════════════════
elif pagina == "📈 Pronóstico por Línea":
    st.markdown('<p class="main-header">Pronóstico por Línea de Producto</p>', unsafe_allow_html=True)

    # Selector de línea
    linea_sel = st.selectbox("Seleccione una línea:", TODAS_LINEAS, index=TODAS_LINEAS.index(LINEAS_ACTIVAS[0]) if LINEAS_ACTIVAS else 0)

    if linea_sel in LINEAS_ADVERTENCIA:
        st.warning(f"⚠️ La línea **{linea_sel}** tiene datos insuficientes o ventas cercanas a cero. El pronóstico puede no ser confiable.")

    # Datos de la línea
    hist_linea = hist_mensual[hist_mensual["Linea"] == linea_sel].sort_values("fecha")
    pron_linea = pron[pron["Linea"] == linea_sel].sort_values("fecha")

    modelo_usado = pron_linea["Modelo"].iloc[0] if len(pron_linea) > 0 else "N/A"
    factor_usado = pron_linea["Factor_Peso"].iloc[0] if len(pron_linea) > 0 else "N/A"

    # KPIs de la línea
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

    # Gráfico principal: Histórico + Pronóstico
    meses_recientes = st.slider("Meses históricos a mostrar:", 6, len(hist_linea), min(18, len(hist_linea)))

    hist_reciente = hist_linea.tail(meses_recientes)

    fig = go.Figure()
    # Histórico
    fig.add_trace(go.Scatter(
        x=hist_reciente["fecha"], y=hist_reciente["Cantidad"],
        mode="lines+markers", name="Histórico",
        line=dict(color="#1B3A5C", width=2.5),
        marker=dict(size=5),
        hovertemplate="<b>%{x|%b %Y}</b><br>Cantidad: %{y:,.0f}<extra></extra>",
    ))
    # Línea de conexión
    if len(hist_linea) > 0 and len(pron_linea) > 0:
        fig.add_trace(go.Scatter(
            x=[hist_linea["fecha"].iloc[-1], pron_linea["fecha"].iloc[0]],
            y=[hist_linea["Cantidad"].iloc[-1], pron_linea["Cantidad_Pronosticada"].iloc[0]],
            mode="lines", showlegend=False,
            line=dict(color="#E74C3C", width=1.5, dash="dot"),
        ))
    # Pronóstico
    fig.add_trace(go.Scatter(
        x=pron_linea["fecha"], y=pron_linea["Cantidad_Pronosticada"],
        mode="lines+markers", name="Pronóstico",
        line=dict(color="#E74C3C", width=2.5, dash="dash"),
        marker=dict(size=7, symbol="diamond"),
        hovertemplate="<b>%{x|%b %Y}</b><br>Pronóstico: %{y:,.0f}<extra></extra>",
    ))
    # Línea vertical de separación
    fig.add_vline(x=fecha_max_hist, line_dash="dot", line_color="gray", opacity=0.7)

    fig.update_layout(
        title=f"Línea: {linea_sel}",
        xaxis_title="", yaxis_title="Unidades",
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=20, t=60, b=30),
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Tabla de pronóstico mensual
    col_tabla, col_comp = st.columns([3, 2])
    with col_tabla:
        st.subheader("Pronóstico Mensual")
        tabla_pron = pron_linea[["fecha", "Cantidad_Pronosticada"]].copy()
        tabla_pron["Mes"] = tabla_pron["fecha"].dt.strftime("%B %Y")
        tabla_pron = tabla_pron.rename(columns={"Cantidad_Pronosticada": "Unidades"})
        st.dataframe(
            tabla_pron[["Mes", "Unidades"]].style.format({"Unidades": "{:,.0f}"}),
            use_container_width=True, hide_index=True,
        )

    with col_comp:
        st.subheader("Comparativa Interanual")
        ultimo_ano_hist = hist_linea[hist_linea["fecha"] >= (fecha_max_hist - pd.DateOffset(months=11))]
        if len(ultimo_ano_hist) > 0 and len(pron_linea) > 0:
            comp = pd.DataFrame({
                "Mes": [f.strftime("%b") for f in ultimo_ano_hist["fecha"]],
                f"Real {ultimo_ano_hist['fecha'].dt.year.iloc[0]}": ultimo_ano_hist["Cantidad"].values,
            })
            comp2 = pd.DataFrame({
                "Mes": [f.strftime("%b") for f in pron_linea["fecha"]],
                f"Pronóstico {pron_linea['fecha'].dt.year.iloc[0]}": pron_linea["Cantidad_Pronosticada"].values,
            })
            st.dataframe(comp.style.format({col: "{:,.0f}" for col in comp.columns if col != "Mes"}),
                         use_container_width=True, hide_index=True)
            st.dataframe(comp2.style.format({col: "{:,.0f}" for col in comp2.columns if col != "Mes"}),
                         use_container_width=True, hide_index=True)


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
        line=dict(color="#1B3A5C", width=2),
        fill="tozeroy", fillcolor="rgba(27,58,92,0.1)",
        hovertemplate="<b>%{x|%b %Y}</b><br>Real: %{y:,.0f}<extra></extra>",
    ))
    if len(hist_total_activo) > 0 and len(pron_total) > 0:
        fig.add_trace(go.Scatter(
            x=[hist_total_activo["fecha"].iloc[-1], pron_total["fecha"].iloc[0]],
            y=[hist_total_activo["Cantidad"].iloc[-1], pron_total["Cantidad_Pronosticada"].iloc[0]],
            mode="lines", showlegend=False,
            line=dict(color="#E74C3C", width=1.5, dash="dot"),
        ))
    fig.add_trace(go.Scatter(
        x=pron_total["fecha"], y=pron_total["Cantidad_Pronosticada"],
        mode="lines+markers", name="Pronóstico",
        line=dict(color="#E74C3C", width=2.5, dash="dash"),
        marker=dict(size=6, symbol="diamond"),
        fill="tozeroy", fillcolor="rgba(231,76,60,0.08)",
        hovertemplate="<b>%{x|%b %Y}</b><br>Pronóstico: %{y:,.0f}<extra></extra>",
    ))
    fig.add_vline(x=fecha_max_hist, line_dash="dot", line_color="gray", opacity=0.7)
    fig.update_layout(
        title="Ventas Totales: Histórico + Pronóstico 12 Meses",
        xaxis_title="", yaxis_title="Unidades Totales",
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=20, t=60, b=30),
        hovermode="x unified",
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
            color_continuous_scale=["#B8D4E8", "#1B3A5C"],
            text="Unidades",
        )
        fig_bar.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig_bar.update_layout(
            height=400, showlegend=False, coloraxis_showscale=False,
            xaxis_title="", yaxis_title="Unidades",
            margin=dict(l=50, r=20, t=10, b=80),
            xaxis_tickangle=-45,
        )
        avg = pron_total_disp["Unidades"].mean()
        fig_bar.add_hline(y=avg, line_dash="dash", line_color="red",
                          annotation_text=f"Promedio: {avg:,.0f}", annotation_position="top right")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("Distribución por Línea (Treemap)")
        df_tree = pron_activo.groupby("Linea")["Cantidad_Pronosticada"].sum().reset_index()
        fig_tree = px.treemap(
            df_tree, path=["Linea"], values="Cantidad_Pronosticada",
            color="Cantidad_Pronosticada",
            color_continuous_scale="Blues",
        )
        fig_tree.update_layout(height=400, margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False)
        fig_tree.update_traces(
            textinfo="label+value+percent root",
            texttemplate="<b>%{label}</b><br>%{value:,.0f}<br>%{percentRoot:.1%}",
        )
        st.plotly_chart(fig_tree, use_container_width=True)

    # Tabla de composición
    st.subheader("Composición del Pronóstico por Línea")
    comp_linea = pron_activo.pivot_table(
        index="Linea", columns=pron_activo["fecha"].dt.strftime("%b %Y"),
        values="Cantidad_Pronosticada", aggfunc="sum",
    )
    fechas_ord = sorted(pron_activo["fecha"].unique())
    cols_ord = [f.strftime("%b %Y") for f in pd.to_datetime(fechas_ord)]
    comp_linea = comp_linea[[c for c in cols_ord if c in comp_linea.columns]]
    comp_linea["TOTAL"] = comp_linea.sum(axis=1)
    comp_linea = comp_linea.sort_values("TOTAL", ascending=False)

    st.dataframe(
        comp_linea.style.format("{:,.0f}"),
        use_container_width=True,
    )


# ═══════════════════════════════════════════════════════════════════════
# PÁGINA 4: PRÓXIMO MES
# ═══════════════════════════════════════════════════════════════════════
elif pagina == "📅 Próximo Mes":
    st.markdown(f'<p class="main-header">Próximo Mes: {primer_mes_pron.strftime("%B %Y")}</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Pronóstico detallado del mes más inmediato</p>', unsafe_allow_html=True)

    df_mes = pron_activo[pron_activo["fecha"] == primer_mes_pron].copy()
    df_mes = df_mes.sort_values("Cantidad_Pronosticada", ascending=False)

    mes_anterior_ano = primer_mes_pron - pd.DateOffset(years=1)
    hist_mes_ant = hist_mensual[
        (hist_mensual["fecha"] == mes_anterior_ano) & (hist_mensual["Linea"].isin(LINEAS_ACTIVAS))
    ]

    df_comp = df_mes[["Linea", "Cantidad_Pronosticada", "Modelo"]].merge(
        hist_mes_ant[["Linea", "Cantidad"]].rename(columns={"Cantidad": "Real_Año_Anterior"}),
        on="Linea", how="left",
    )
    df_comp["Real_Año_Anterior"] = df_comp["Real_Año_Anterior"].fillna(0)
    df_comp["Crecimiento_%"] = (
        (df_comp["Cantidad_Pronosticada"] - df_comp["Real_Año_Anterior"])
        / df_comp["Real_Año_Anterior"].replace(0, 1) * 100
    ).round(1)
    df_comp = df_comp.sort_values("Cantidad_Pronosticada", ascending=False)

    total_mes = df_comp["Cantidad_Pronosticada"].sum()
    total_ant = df_comp["Real_Año_Anterior"].sum()
    crec_total = ((total_mes - total_ant) / total_ant * 100) if total_ant > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            f"Total {primer_mes_pron.strftime('%b %Y')}",
            f"{total_mes:,.0f} uds",
            f"{crec_total:+.1f}% vs {mes_anterior_ano.strftime('%b %Y')}",
        )
    with col2:
        top_linea = df_comp.iloc[0]["Linea"] if len(df_comp) > 0 else "N/A"
        top_val = df_comp.iloc[0]["Cantidad_Pronosticada"] if len(df_comp) > 0 else 0
        st.metric("Línea Líder", f"{top_linea}", f"{top_val:,.0f} uds")
    with col3:
        n_crecen = (df_comp["Crecimiento_%"] > 0).sum()
        st.metric("Líneas en Crecimiento", f"{n_crecen} de {len(df_comp)}")

    st.markdown("---")

    col_g1, col_g2 = st.columns([3, 2])

    with col_g1:
        st.subheader(f"Comparativa: {primer_mes_pron.strftime('%b %Y')} vs {mes_anterior_ano.strftime('%b %Y')}")
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            y=df_comp["Linea"], x=df_comp["Real_Año_Anterior"],
            name=f"Real {mes_anterior_ano.strftime('%b %Y')}",
            orientation="h", marker_color="#B8D4E8",
            text=df_comp["Real_Año_Anterior"].apply(lambda x: f"{x:,.0f}"),
            textposition="inside",
        ))
        fig_comp.add_trace(go.Bar(
            y=df_comp["Linea"], x=df_comp["Cantidad_Pronosticada"],
            name=f"Pronóstico {primer_mes_pron.strftime('%b %Y')}",
            orientation="h", marker_color="#1B3A5C",
            text=df_comp["Cantidad_Pronosticada"].apply(lambda x: f"{x:,.0f}"),
            textposition="inside",
        ))
        fig_comp.update_layout(
            barmode="group", height=400,
            margin=dict(l=10, r=20, t=10, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_title="Unidades",
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    with col_g2:
        st.subheader("Crecimiento por Línea")
        df_crec = df_comp[["Linea", "Crecimiento_%"]].sort_values("Crecimiento_%", ascending=True)
        colores = ["#27AE60" if v > 0 else "#E74C3C" for v in df_crec["Crecimiento_%"]]
        fig_crec = go.Figure(go.Bar(
            y=df_crec["Linea"], x=df_crec["Crecimiento_%"],
            orientation="h", marker_color=colores,
            text=df_crec["Crecimiento_%"].apply(lambda x: f"{x:+.1f}%"),
            textposition="outside",
        ))
        fig_crec.update_layout(
            height=400, xaxis_title="% Crecimiento",
            margin=dict(l=10, r=60, t=10, b=30),
        )
        st.plotly_chart(fig_crec, use_container_width=True)

    # Tabla detallada
    st.subheader("Detalle por Línea")
    st.dataframe(
        df_comp[["Linea", "Modelo", "Real_Año_Anterior", "Cantidad_Pronosticada", "Crecimiento_%"]].rename(columns={
            "Real_Año_Anterior": f"Real {mes_anterior_ano.strftime('%b %Y')}",
            "Cantidad_Pronosticada": f"Pronóstico {primer_mes_pron.strftime('%b %Y')}",
            "Crecimiento_%": "Crecimiento %",
        }).style.format({
            f"Real {mes_anterior_ano.strftime('%b %Y')}": "{:,.0f}",
            f"Pronóstico {primer_mes_pron.strftime('%b %Y')}": "{:,.0f}",
            "Crecimiento %": "{:+.1f}%",
        }),
        use_container_width=True, hide_index=True,
    )

# ─── Footer ────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Proyecto Final — Especialización Inteligencia de Negocios | UPB | Pronóstico con skforecast + scikit-learn")
