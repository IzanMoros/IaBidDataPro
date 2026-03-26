# -*- coding: utf-8 -*-
"""
🎬 CineMatch — Recomendador Semántico de Películas
===================================================
Versión Profesional — Diseño Premium con IA Semántica
"""

import streamlit as st
import pandas as pd
import numpy as np
from embeddings_manager import EmbeddingsManager
from dataset import obtener_dataset_peliculas
from visualizacion import VisualizadorEmbeddings

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="CineMatch · Recomendador Semántico",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTILOS CSS PREMIUM
# ============================================================================

st.markdown("""
<style>
/* ─── FUENTES ─────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@400;600;700;900&display=swap');

/* ─── BASE & FONDO ────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0d1117 40%, #0a0f1e 100%);
    min-height: 100vh;
}

/* ─── SIDEBAR PREMIUM ─────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #161b27 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.2) !important;
}

section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* ─── HERO HEADER ─────────────────────────────────────────── */
.hero-container {
    background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(139,92,246,0.1) 50%, rgba(236,72,153,0.08) 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 24px;
    padding: 48px 40px;
    margin-bottom: 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(20px);
}

.hero-container::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at center, rgba(99,102,241,0.05) 0%, transparent 60%);
    animation: pulse 6s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.1); opacity: 1; }
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 12px;
    font-weight: 600;
    color: #a5b4fc !important;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.hero-title {
    font-family: 'Outfit', sans-serif !important;
    font-size: 3.2em !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 50%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 12px 0 !important;
    line-height: 1.1 !important;
    letter-spacing: -1px;
}

.hero-subtitle {
    font-size: 1.1em !important;
    color: #94a3b8 !important;
    font-weight: 400;
    max-width: 600px;
    margin: 0 auto !important;
    line-height: 1.7;
}

.hero-stats {
    display: flex;
    justify-content: center;
    gap: 32px;
    margin-top: 32px;
    flex-wrap: wrap;
}

.stat-item {
    text-align: center;
}

.stat-value {
    font-size: 1.8em;
    font-weight: 800;
    background: linear-gradient(135deg, #a5b4fc, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: block;
}

.stat-label {
    font-size: 0.75em;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 500;
}

/* ─── TARJETAS DE PELÍCULA ────────────────────────────────── */
.movie-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.movie-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    right: 0; height: 2px;
    background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.movie-card:hover::before { opacity: 1; }
.movie-card:hover {
    border-color: rgba(99,102,241,0.3);
    background: rgba(99,102,241,0.05);
    transform: translateY(-2px);
}

.movie-rank {
    position: absolute;
    top: 16px; right: 16px;
    background: linear-gradient(135deg, #6366f1, #a855f7);
    border-radius: 50%;
    width: 32px; height: 32px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 13px;
    color: white;
}

.movie-title {
    font-size: 1.15em;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 4px;
}

.movie-meta {
    font-size: 0.82em;
    color: #64748b;
    margin-bottom: 10px;
}

.movie-description {
    font-size: 0.9em;
    color: #94a3b8;
    line-height: 1.6;
    margin-bottom: 12px;
}

.similarity-bar-container {
    margin-top: 12px;
}

.similarity-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.8em;
    color: #64748b;
    margin-bottom: 4px;
}

.similarity-bar {
    height: 4px;
    border-radius: 2px;
    background: rgba(255,255,255,0.1);
    overflow: hidden;
}

.similarity-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.6s ease;
}

/* ─── BADGE DE GÉNERO ─────────────────────────────────────── */
.genre-badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 100px;
    padding: 3px 10px;
    font-size: 0.75em;
    font-weight: 600;
    color: #a5b4fc;
    margin-right: 6px;
    margin-bottom: 4px;
}

/* ─── SCORE BADGE ─────────────────────────────────────────── */
.score-excellent { background: rgba(34,197,94,0.15); border-color: rgba(34,197,94,0.4); color: #86efac; }
.score-good { background: rgba(234,179,8,0.15); border-color: rgba(234,179,8,0.4); color: #fde047; }
.score-mid { background: rgba(249,115,22,0.15); border-color: rgba(249,115,22,0.4); color: #fdba74; }
.score-low { background: rgba(239,68,68,0.15); border-color: rgba(239,68,68,0.4); color: #fca5a5; }

/* ─── GLASS PANEL ─────────────────────────────────────────── */
.glass-panel {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 24px;
    margin: 12px 0;
    backdrop-filter: blur(10px);
}

/* ─── COMPARISON RESULT ───────────────────────────────────── */
.comparison-result {
    text-align: center;
    padding: 40px;
    border-radius: 20px;
    margin: 20px 0;
}

/* ─── TABS STYLING ────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    gap: 4px !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: #64748b !important;
    font-weight: 500 !important;
    padding: 8px 18px !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1, #a855f7) !important;
    color: white !important;
}

/* ─── INPUTS STYLING ──────────────────────────────────────── */
.stTextInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    font-size: 1em !important;
    padding: 12px 16px !important;
}

.stTextInput input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}

/* ─── BUTTONS ─────────────────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    font-size: 0.95em !important;
    letter-spacing: 0.3px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.3) !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(99,102,241,0.4) !important;
}

/* ─── SLIDERS & METRICS ───────────────────────────────────── */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: linear-gradient(135deg, #6366f1, #a855f7) !important;
}

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
}

[data-testid="metric-container"] label {
    color: #64748b !important;
    font-size: 0.8em !important;
    font-weight: 500 !important;
}

[data-testid="metric-container"] [data-testid="metric-value"] {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
}

/* ─── EXPANDER ────────────────────────────────────────────── */
.stExpander {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
}

/* ─── SELECTBOX ───────────────────────────────────────────── */
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
}

/* ─── SUCCESS / INFO / WARNING ────────────────────────────── */
.stSuccess {
    background: rgba(34,197,94,0.1) !important;
    border: 1px solid rgba(34,197,94,0.3) !important;
    border-radius: 10px !important;
}

.stInfo {
    background: rgba(59,130,246,0.1) !important;
    border: 1px solid rgba(59,130,246,0.3) !important;
    border-radius: 10px !important;
}

.stWarning {
    background: rgba(234,179,8,0.1) !important;
    border: 1px solid rgba(234,179,8,0.3) !important;
    border-radius: 10px !important;
}

/* ─── SIDEBAR INFO ────────────────────────────────────────── */
.author-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 100px;
    padding: 6px 14px;
    margin: 4px 0;
    font-size: 0.85em;
    color: #a5b4fc;
}

.tech-tag {
    display: inline-block;
    background: rgba(168,85,247,0.1);
    border: 1px solid rgba(168,85,247,0.25);
    border-radius: 6px;
    padding: 3px 8px;
    font-size: 0.78em;
    color: #c4b5fd;
    margin: 2px;
}

/* ─── SECTION TITLE ───────────────────────────────────────── */
.section-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.5em;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 4px;
}

.section-subtitle {
    font-size: 0.9em;
    color: #64748b;
    margin-bottom: 20px;
    line-height: 1.6;
}

/* ─── SEARCH EXAMPLES ─────────────────────────────────────── */
.example-chip {
    display: inline-block;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 100px;
    padding: 5px 14px;
    font-size: 0.82em;
    color: #a5b4fc;
    margin: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.example-chip:hover {
    background: rgba(99,102,241,0.2);
    border-color: rgba(99,102,241,0.4);
}

/* ─── SCROLLBAR ───────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.5); }

/* hide streamlit branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

@st.cache_resource
def cargar_modelo():
    return EmbeddingsManager()

@st.cache_data
def cargar_datos():
    return obtener_dataset_peliculas()

@st.cache_data(ttl=300)
def generar_embeddings_dataset(_manager, descripciones):
    return _manager.generar_embeddings_batch(descripciones.tolist(), mostrar_progreso=False)


def get_similarity_color(sim):
    if sim >= 0.65: return "#22c55e", "score-excellent", "Excelente"
    elif sim >= 0.45: return "#eab308", "score-good", "Buena"
    elif sim >= 0.3: return "#f97316", "score-mid", "Moderada"
    else: return "#ef4444", "score-low", "Baja"


def render_movie_card(pelicula, similitud, rank, manager):
    color, score_class, label = get_similarity_color(similitud)
    pct = int(similitud * 100)
    fill_pct = min(100, int(similitud * 100 / 0.8 * 100))

    st.markdown(f"""
    <div class="movie-card">
        <div class="movie-rank">#{rank}</div>
        <div class="movie-title">{pelicula['titulo']}</div>
        <div class="movie-meta">📅 {pelicula['año']} &nbsp;·&nbsp; <span class="genre-badge">{pelicula['genero']}</span></div>
        <div class="movie-description">{pelicula['descripcion']}</div>
        <div class="similarity-bar-container">
            <div class="similarity-label">
                <span>Coincidencia semántica</span>
                <span class="genre-badge {score_class}">{label} · {pct}%</span>
            </div>
            <div class="similarity-bar">
                <div class="similarity-fill" style="width:{fill_pct}%; background: linear-gradient(90deg, {color}88, {color});"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_movie_card_simple(pelicula, rank, color_gradient, show_year=True):
    st.markdown(f"""
    <div class="movie-card" style="border-left: 3px solid; border-image: {color_gradient} 1;">
        <div class="movie-rank">#{rank}</div>
        <div class="movie-title">{pelicula['titulo']}{' (' + str(pelicula['año']) + ')' if show_year else ''}</div>
        <div class="movie-meta"><span class="genre-badge">{pelicula['genero']}</span></div>
        <div class="movie-description">{pelicula['descripcion']}</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 16px;">
        <div style="font-size: 2.5em;">🎬</div>
        <div style="font-family: 'Outfit', sans-serif; font-size: 1.4em; font-weight: 800;
                    background: linear-gradient(135deg, #a5b4fc, #f472b6);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    background-clip: text;">CineMatch</div>
        <div style="font-size: 0.75em; color: #4b5563; margin-top: 4px; letter-spacing: 1px; text-transform: uppercase;">
            Semantic AI Engine
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("**⚙️ Configuración de Búsqueda**")

    num_resultados = st.slider(
        "Número de recomendaciones",
        min_value=3, max_value=10, value=5,
        help="Cuántas películas mostrar como resultado"
    )

    metodo_viz = st.selectbox(
        "Método de visualización",
        options=['PCA', 't-SNE'],
        help="PCA es más rápido, t-SNE agrupa mejor"
    )

    dim_viz = st.radio(
        "Dimensión de visualización",
        options=['2D', '3D'],
        help="3D ofrece más perspectiva pero es más complejo"
    )

    st.divider()

    st.markdown("**👥 Equipo de Desarrollo**")
    for nombre in ["Cristian Rosa", "Izan Moros", "Samuel Fraca"]:
        initials = nombre.split()[0][0] + nombre.split()[1][0]
        st.markdown(f"""
        <div class="author-chip">
            <span style="background: linear-gradient(135deg,#6366f1,#a855f7);
                         border-radius: 50%; width:22px; height:22px;
                         display:inline-flex; align-items:center; justify-content:center;
                         font-size:0.7em; font-weight:700; color:white;">{initials}</span>
            {nombre}
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("**🛠️ Stack Tecnológico**")
    for tag in ["Python 3.12", "Streamlit", "Sentence-Transformers", "Scikit-learn", "Plotly", "NumPy", "Pandas"]:
        st.markdown(f'<span class="tech-tag">{tag}</span>', unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div style="font-size: 0.75em; color: #374151; text-align: center;">
        Proyecto 8 · IA para Desarrolladores<br>
        <span style="color: #4b5563;">Búsqueda semántica con embeddings</span>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# CARGA DE DATOS Y MODELO
# ============================================================================

with st.spinner("⚡ Iniciando motor de IA semántica..."):
    manager = cargar_modelo()
    df_peliculas = cargar_datos()
    embeddings_dataset = generar_embeddings_dataset(manager, df_peliculas['descripcion'])


# ============================================================================
# HERO SECTION
# ============================================================================

n_generos = df_peliculas['genero'].nunique()
st.markdown(f"""
<div class="hero-container">
    <div class="hero-badge">✨ &nbsp; IA Semántica · NLP · Embeddings</div>
    <div class="hero-title">Encuentra tu próxima película favorita</div>
    <p class="hero-subtitle">
        Describe <strong>cómo quieres sentirte</strong>, no el título. Nuestro motor de inteligencia artificial
        entiende el significado profundo de tus palabras para encontrar películas que realmente conecten contigo.
    </p>
    <div class="hero-stats">
        <div class="stat-item">
            <span class="stat-value">{len(df_peliculas)}</span>
            <span class="stat-label">Películas</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">{n_generos}</span>
            <span class="stat-label">Géneros</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">{manager.dimension_vector}</span>
            <span class="stat-label">Dimensiones</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">Ligero</span>
            <span class="stat-label">Ultra Rápido</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# TABS PRINCIPALES
# ============================================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 Buscador",
    "🆚 Comparador",
    "🎲 Sorpréndeme",
    "📊 Visualización",
    "🧬 Alquimia (NUEVO)",
    "🗄️ Dataset"
])

# ============================================================================
# TAB 1: BUSCADOR SEMÁNTICO
# ============================================================================

with tab1:
    st.markdown('<div class="section-title">🔍 Búsqueda Semántica</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-subtitle">
    Describe emociones, tonos y experiencias que buscas. El modelo convierte tu texto en un vector
    de alta dimensión y encuentra las películas con mayor similitud semántica.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-panel" style="margin-bottom: 16px;">
        <div style="font-size: 0.82em; color: #64748b; margin-bottom: 10px; font-weight: 600;">
            💡 EJEMPLOS DE BÚSQUEDA
        </div>
        <div>
            <span class="example-chip">Una película triste en el espacio</span>
            <span class="example-chip">Algo muy gracioso con superhéroes</span>
            <span class="example-chip">Terror psicológico perturbador</span>
            <span class="example-chip">Romance en Europa con final agridulce</span>
            <span class="example-chip">Ciencia ficción filosófica y lenta</span>
            <span class="example-chip">Thriller de suspense con giros</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    consulta = st.text_input(
        "¿Qué tipo de película buscas hoy?",
        placeholder="Describe emociones, ambientación, tono... ej: drama familiar conmovedor con esperanza",
        label_visibility="collapsed"
    )

    col_btn, col_clear = st.columns([4, 1])
    with col_btn:
        buscar = st.button("🚀 Buscar con IA semántica", type="primary", use_container_width=True, key="btn_buscar")

    if buscar:
        if consulta.strip():
            with st.spinner("🧠 Procesando consulta con embeddings..."):
                resultados = manager.buscar_similares_optimizada(
                    consulta, embeddings_dataset, top_k=num_resultados
                )

            st.session_state['ultimos_resultados'] = [r[0] for r in resultados]
            st.session_state['ultima_consulta'] = consulta

            st.markdown(f"""
            <div style="margin: 20px 0 12px;">
                <span style="color: #64748b; font-size: 0.85em;">
                    {len(resultados)} resultados para
                </span>
                <span style="color: #a5b4fc; font-weight: 600; font-size: 0.9em;">"{consulta}"</span>
            </div>
            """, unsafe_allow_html=True)

            for i, (idx, similitud) in enumerate(resultados, 1):
                pelicula = df_peliculas.iloc[idx]
                render_movie_card(pelicula, similitud, i, manager)

            with st.expander("🎓 ¿Cómo funciona la búsqueda semántica?", expanded=False):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown("""
                    <div class="glass-panel" style="text-align:center;">
                        <div style="font-size:2em; margin-bottom:8px;">📝</div>
                        <div style="font-weight:700; color:#a5b4fc; margin-bottom:6px;">1. Encoding</div>
                        <div style="font-size:0.85em; color:#64748b;">
                            Tu consulta se convierte en un vector de <b style="color:#f1f5f9">{dim}</b> números reales
                        </div>
                    </div>
                    """.format(dim=manager.dimension_vector), unsafe_allow_html=True)
                with c2:
                    st.markdown("""
                    <div class="glass-panel" style="text-align:center;">
                        <div style="font-size:2em; margin-bottom:8px;">🧮</div>
                        <div style="font-weight:700; color:#a5b4fc; margin-bottom:6px;">2. Similitud Coseno</div>
                        <div style="font-size:0.85em; color:#64748b;">
                            Se mide el ángulo entre tu vector y cada película:<br>
                            <b style="color:#f1f5f9">sim(A,B) = A·B / ‖A‖‖B‖</b>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with c3:
                    st.markdown("""
                    <div class="glass-panel" style="text-align:center;">
                        <div style="font-size:2em; margin-bottom:8px;">🏆</div>
                        <div style="font-weight:700; color:#a5b4fc; margin-bottom:6px;">3. Ranking</div>
                        <div style="font-size:0.85em; color:#64748b;">
                            Las películas se ordenan por mayor similitud semántica
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Por favor, describe qué tipo de película buscas.")


# ============================================================================
# TAB 2: COMPARADOR
# ============================================================================

with tab2:
    st.markdown('<div class="section-title">🆚 Comparador Semántico</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-subtitle">
    Selecciona dos películas y descubre su similitud semántica exacta. Útil para entender
    qué tan relacionadas están en términos de temática, tono y emoción.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🎬 Primera Película**")
        pelicula1_idx = st.selectbox(
            "Película 1",
            options=range(len(df_peliculas)),
            format_func=lambda x: f"{df_peliculas.iloc[x]['titulo']} ({df_peliculas.iloc[x]['año']})",
            key="pelicula1",
            label_visibility="collapsed"
        )
        p1 = df_peliculas.iloc[pelicula1_idx]
        st.markdown(f"""
        <div class="glass-panel" style="border-left:3px solid #6366f1;">
            <div class="movie-title">{p1['titulo']}</div>
            <div class="movie-meta">📅 {p1['año']} · <span class="genre-badge">{p1['genero']}</span></div>
            <div class="movie-description">{p1['descripcion']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("**🎬 Segunda Película**")
        pelicula2_idx = st.selectbox(
            "Película 2",
            options=range(len(df_peliculas)),
            format_func=lambda x: f"{df_peliculas.iloc[x]['titulo']} ({df_peliculas.iloc[x]['año']})",
            key="pelicula2",
            index=min(1, len(df_peliculas) - 1),
            label_visibility="collapsed"
        )
        p2 = df_peliculas.iloc[pelicula2_idx]
        st.markdown(f"""
        <div class="glass-panel" style="border-left:3px solid #a855f7;">
            <div class="movie-title">{p2['titulo']}</div>
            <div class="movie-meta">📅 {p2['año']} · <span class="genre-badge">{p2['genero']}</span></div>
            <div class="movie-description">{p2['descripcion']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    comparar = st.button("⚡ Calcular Similitud Semántica", type="primary", use_container_width=True)

    if comparar:
        with st.spinner("🧮 Analizando vectores semánticos..."):
            resultado = manager.comparar_peliculas(
                p1['descripcion'], p2['descripcion'],
                p1['titulo'], p2['titulo']
            )
        sim = resultado['similitud']
        color, score_class, label = get_similarity_color(sim)

        st.markdown(f"""
        <div class="glass-panel" style="text-align:center; margin-top:20px; border-color:rgba(99,102,241,0.3);">
            <div style="font-size:0.8em; color:#64748b; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;">
                Similitud Semántica
            </div>
            <div style="font-size:3.5em; font-weight:900; color:{color}; line-height:1;">{sim:.1%}</div>
            <div style="margin-top:10px;">
                <span class="genre-badge {score_class}">{resultado['interpretacion']}</span>
            </div>
            <div style="margin-top:20px; max-width:400px; margin-left:auto; margin-right:auto;">
                <div class="similarity-bar" style="height:8px; border-radius:4px;">
                    <div class="similarity-fill" style="width:{min(100, int(sim*100/0.8*100))}%;
                         background: linear-gradient(90deg, {color}88, {color}); height:8px;"></div>
                </div>
            </div>
            <div style="display:flex; justify-content:space-between; max-width:400px; margin:4px auto 0;
                        font-size:0.72em; color:#374151;">
                <span>0% — Sin relación</span>
                <span>100% — Idénticas</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if sim >= 0.65:
            st.success(f"**Alto parecido:** {p1['titulo']} y {p2['titulo']} comparten temática, emociones o ambientación muy similares.")
        elif sim >= 0.45:
            st.info(f"**Similitud moderada:** Hay puntos en común entre {p1['titulo']} y {p2['titulo']}, pero también diferencias notables.")
        elif sim >= 0.3:
            st.warning(f"**Baja similitud:** {p1['titulo']} y {p2['titulo']} son bastante distintas en tono y temática.")
        else:
            st.error(f"**Sin relación:** {p1['titulo']} y {p2['titulo']} van en direcciones completamente diferentes.")


# ============================================================================
# TAB 3: SORPRÉNDEME
# ============================================================================

with tab3:
    st.markdown('<div class="section-title">🎲 Modo Sorpréndeme</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-subtitle">
    ¿No sabes qué ver? Este modo usa un algoritmo de maximización de diversidad para seleccionar
    películas lo más distintas entre sí, garantizando una colección variada y sorprendente.
    </div>
    """, unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        num_sorpresa = st.slider("¿Cuántas películas?", min_value=3,
                                  max_value=min(12, len(df_peliculas)), value=6)
    with col_s2:
        semilla = None
        usar_semilla = st.checkbox("📌 Resultados reproducibles", value=False)
        if usar_semilla:
            semilla = st.number_input("Semilla", min_value=0, max_value=9999, value=42)

    st.markdown("<br>", unsafe_allow_html=True)
    sorprender = st.button("🎲 ¡Sorpréndeme ahora!", type="primary", use_container_width=True)

    if sorprender:
        with st.spinner("🌈 Seleccionando la combinación más diversa..."):
            recomendaciones = manager.recomendar_diversas(
                embeddings_dataset,
                df_peliculas['titulo'].tolist(),
                n=num_sorpresa,
                semilla=semilla
            )

        st.success(f"✅ {num_sorpresa} películas seleccionadas maximizando diversidad semántica")

        gradients = [
            "linear-gradient(135deg, #6366f1, #8b5cf6)",
            "linear-gradient(135deg, #ec4899, #f43f5e)",
            "linear-gradient(135deg, #06b6d4, #3b82f6)",
            "linear-gradient(135deg, #10b981, #059669)",
            "linear-gradient(135deg, #f59e0b, #ef4444)",
            "linear-gradient(135deg, #8b5cf6, #ec4899)",
        ]

        for i, (idx, titulo) in enumerate(recomendaciones):
            pelicula = df_peliculas.iloc[idx]
            render_movie_card_simple(pelicula, i+1, gradients[i % len(gradients)])

        # Análisis de diversidad
        generos_sel = [df_peliculas.iloc[idx]['genero'] for idx, _ in recomendaciones]
        g_unicos = len(set(generos_sel))

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Géneros únicos", f"{g_unicos}/{num_sorpresa}")
        with c2:
            st.metric("Diversidad", f"{g_unicos/num_sorpresa:.0%}")
        with c3:
            año_min = min(df_peliculas.iloc[idx]['año'] for idx, _ in recomendaciones)
            año_max = max(df_peliculas.iloc[idx]['año'] for idx, _ in recomendaciones)
            st.metric("Rango temporal", f"{año_min}–{año_max}")


# ============================================================================
# TAB 4: VISUALIZACIÓN
# ============================================================================

with tab4:
    st.markdown('<div class="section-title">📊 Espacio Vectorial de Embeddings</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-subtitle">
    Visualiza cómo los embeddings agrupan las películas en el espacio vectorial.
    Películas semánticamente cercanas aparecen cerca entre sí. Se reducen las
    {dim} dimensiones a 2D/3D para poder visualizarlas.
    </div>
    """.format(dim=manager.dimension_vector), unsafe_allow_html=True)

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        if st.button("🗺️ Generar Mapa de Dispersión", use_container_width=True):
            with st.spinner("📉 Reduciendo dimensionalidad..."):
                viz = VisualizadorEmbeddings()
                indices_resaltar = st.session_state.get('ultimos_resultados', None)
                titulo_extra = f" — Búsqueda: '{st.session_state.get('ultima_consulta', '')}'" if indices_resaltar else ""

                if dim_viz == '2D':
                    fig = viz.crear_grafico_2d(
                        embeddings_dataset,
                        df_peliculas['titulo'].tolist(),
                        titulo=f"Espacio de Embeddings 2D{titulo_extra}",
                        resaltar_indices=indices_resaltar,
                        metodo=metodo_viz.lower()
                    )
                else:
                    fig = viz.crear_grafico_3d(
                        embeddings_dataset,
                        df_peliculas['titulo'].tolist(),
                        titulo=f"Espacio de Embeddings 3D{titulo_extra}",
                        resaltar_indices=indices_resaltar,
                        metodo=metodo_viz.lower()
                    )

                # Aplicar tema oscuro al gráfico
                fig.update_layout(
                    paper_bgcolor='rgba(13,17,23,0)',
                    plot_bgcolor='rgba(13,17,23,0.5)',
                    font=dict(color='#94a3b8', family='Inter'),
                    title_font=dict(color='#f1f5f9', size=16),
                )
                st.plotly_chart(fig, use_container_width=True)

    with col_v2:
        if st.button("🔥 Generar Mapa de Calor", use_container_width=True):
            with st.spinner("🧮 Calculando matriz de similitudes..."):
                viz = VisualizadorEmbeddings()
                fig_heatmap = viz.crear_mapa_calor_similitud(
                    embeddings_dataset,
                    df_peliculas['titulo'].tolist()
                )
                fig_heatmap.update_layout(
                    paper_bgcolor='rgba(13,17,23,0)',
                    font=dict(color='#94a3b8', family='Inter'),
                    title_font=dict(color='#f1f5f9', size=16),
                )
                st.plotly_chart(fig_heatmap, use_container_width=True)

    with st.expander("🎓 Conceptos de Visualización Semántica"):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            **📐 PCA (Principal Component Analysis)**
            - Preserva varianza global
            - Determinístico: mismo resultado siempre
            - Muy rápido de calcular
            - Ideal para una primera exploración

            **Cuándo usarlo:** Visión general, comparaciones rápidas
            """)
        with c2:
            st.markdown("""
            **🌀 t-SNE**
            - Preserva relaciones locales (vecinos)
            - Muestra mejor los clusters semánticos
            - Más lento, puede variar entre ejecuciones
            - Revela grupos que PCA puede omitir

            **Cuándo usarlo:** Identificar géneros y clusters
            """)


# ============================================================================
# TAB 5: ALQUIMIA CINEMATOGRÁFICA (NUEVO)
# ============================================================================

with tab5:
    st.markdown('<div class="section-title">🧬 Alquimia Cinematográfica</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="section-subtitle">
    Descubre el punto medio matemático entre dos películas distintas. 
    Este laboratorio mezcla los vectores semánticos de dos películas para encontrar qué obra real existe en su centro absoluto.
    </div>
    """, unsafe_allow_html=True)

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.markdown("**🧪 Ingrediente 1**")
        mix1_idx = st.selectbox(
            "Película A",
            options=range(len(df_peliculas)),
            format_func=lambda x: f"{df_peliculas.iloc[x]['titulo']} ({df_peliculas.iloc[x]['año']})",
            key="mix1",
            index=0
        )
    with col_a2:
        st.markdown("**🧪 Ingrediente 2**")
        mix2_idx = st.selectbox(
            "Película B",
            options=range(len(df_peliculas)),
            format_func=lambda x: f"{df_peliculas.iloc[x]['titulo']} ({df_peliculas.iloc[x]['año']})",
            key="mix2",
            index=10 if len(df_peliculas) > 10 else 1
        )

    mezclar = st.button("✨ Fusionar Películas (Magia Semántica)", type="primary", use_container_width=True)

    if mezclar:
        if mix1_idx == mix2_idx:
            st.warning("⚠️ Debes elegir dos películas diferentes para hacer una fusión.")
        else:
            with st.spinner("🔮 Calculando vector intermedio de fusión..."):
                v1 = embeddings_dataset[mix1_idx]
                v2 = embeddings_dataset[mix2_idx]
                
                # Fusión matemática semántica
                v_mezcla = (v1 + v2) / 2.0
                v_mezcla_2d = v_mezcla.reshape(1, -1)
                
                # Calcular similitudes de la nueva "mezcla" con todas las películas
                from sklearn.metrics.pairwise import cosine_similarity
                similitudes = cosine_similarity(v_mezcla_2d, embeddings_dataset)[0]
                
                # Descartar las dos películas originales del resultado
                for i in [mix1_idx, mix2_idx]:
                    similitudes[i] = -1.0 
                    
                indices_ordenados = np.argsort(similitudes)[::-1]
                top_resultados = [(idx, float(similitudes[idx])) for idx in indices_ordenados[:3]]
                
                mejor_idx, mejor_sim = top_resultados[0]
                pelicula_mezcla = df_peliculas.iloc[mejor_idx]
                
                st.markdown(f"""
                <div style="text-align:center; padding: 20px;">
                    <h2 style="color:#a5b4fc; font-style:italic;">¡Fusión Completada!</h2>
                    <p style="color:#94a3b8;">Si metes {df_peliculas.iloc[mix1_idx]['titulo']} y {df_peliculas.iloc[mix2_idx]['titulo']} en una batidora, obtienes...</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Mostrar resultado de fusión de manera espectacular
                st.markdown(f"""
                <div class="glass-panel" style="border: 2px solid; border-image: linear-gradient(45deg, #f472b6, #ec4899) 1; transform: scale(1.02); background: rgba(236, 72, 153, 0.05); text-align: center;">
                    <div style="font-size:3em; margin-bottom: 10px;">🏆</div>
                    <div class="movie-title" style="font-size:2em; font-weight:900;">{pelicula_mezcla['titulo']}</div>
                    <div class="movie-meta" style="font-size:1.1em;">📅 {pelicula_mezcla['año']} &nbsp;·&nbsp; <span class="genre-badge">{pelicula_mezcla['genero']}</span></div>
                    <div class="movie-description" style="font-size:1.1em; max-width: 600px; margin: 20px auto; color:#f1f5f9;">{pelicula_mezcla['descripcion']}</div>
                    <div style="color:#64748b; font-size:0.9em; margin-top:20px;">Precisión de mezcla: {int(mejor_sim * 100)}%</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br><p style='text-align:center; color:#64748b;'>Otros dos subproductos de la mezcla:</p>", unsafe_allow_html=True)
                col_sub1, col_sub2 = st.columns(2)
                for idx, (sub_idx, sim) in enumerate(top_resultados[1:]):
                    p_sub = df_peliculas.iloc[sub_idx]
                    with (col_sub1 if idx == 0 else col_sub2):
                        st.markdown(f"""
                        <div class="movie-card" style="border-left: 2px solid #8b5cf6;">
                            <div class="movie-title">{p_sub['titulo']} <span style="font-size:0.7em; color:#a5b4fc;">(Coincidencia {int(sim*100)}%)</span></div>
                            <div class="movie-meta">{p_sub['genero']}</div>
                        </div>
                        """, unsafe_allow_html=True)

# ============================================================================
# TAB 6: DATASET
# ============================================================================

with tab6:
    st.markdown('<div class="section-title">🗄️ Dataset de Películas</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="section-subtitle">
    Colección de <strong style="color:#a5b4fc">{len(df_peliculas)} películas</strong> con descripciones
    enriquecidas semánticamente — capturando emociones, tono narrativo, ambientación y temas,
    diseñadas específicamente para embeddings de alta calidad.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🎬 Total", len(df_peliculas))
    with c2:
        st.metric("🏷️ Géneros únicos", df_peliculas['genero'].nunique())
    with c3:
        st.metric("📅 Película más antigua", df_peliculas['año'].min())
    with c4:
        st.metric("📅 Película más reciente", df_peliculas['año'].max())

    st.markdown("<br>", unsafe_allow_html=True)

    # Filtros
    colf1, colf2, colf3 = st.columns([2, 2, 1])
    with colf1:
        generos_disponibles = ["Todos"] + sorted(df_peliculas['genero'].unique().tolist())
        filtro_genero = st.selectbox("Filtrar por género", generos_disponibles)
    with colf2:
        busca_titulo = st.text_input("🔎 Buscar por título", placeholder="ej: Inception")
    with colf3:
        pass

    df_filtrado = df_peliculas.copy()
    if filtro_genero != "Todos":
        df_filtrado = df_filtrado[df_filtrado['genero'] == filtro_genero]
    if busca_titulo:
        df_filtrado = df_filtrado[df_filtrado['titulo'].str.contains(busca_titulo, case=False, na=False)]

    st.markdown(f"<div style='color:#64748b; font-size:0.85em; margin-bottom:8px;'>Mostrando {len(df_filtrado)} películas</div>", unsafe_allow_html=True)

    st.dataframe(
        df_filtrado[['titulo', 'año', 'genero', 'descripcion']].rename(columns={
            'titulo': 'Título', 'año': 'Año',
            'genero': 'Género', 'descripcion': 'Descripción'
        }),
        use_container_width=True,
        height=420,
        column_config={
            "Descripción": st.column_config.TextColumn(width="large"),
            "Año": st.column_config.NumberColumn(format="%d"),
        }
    )

    # Distribución por género
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**📊 Distribución por Género**")
    genero_counts = df_peliculas['genero'].value_counts().reset_index()
    genero_counts.columns = ['Género', 'Películas']

    import plotly.express as px
    fig_bar = px.bar(
        genero_counts.head(15),
        x='Películas', y='Género',
        orientation='h',
        color='Películas',
        color_continuous_scale='Viridis',
        title='Top Géneros del Dataset'
    )
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.02)',
        font=dict(color='#94a3b8', family='Inter'),
        title_font=dict(color='#f1f5f9', size=14),
        showlegend=False,
        coloraxis_showscale=False,
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        height=450,
    )
    fig_bar.update_traces(marker_line_width=0)
    st.plotly_chart(fig_bar, use_container_width=True)
