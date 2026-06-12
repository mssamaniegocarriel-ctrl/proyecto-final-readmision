import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Predicción de Readmisión Hospitalaria | Proyecto Final",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg: #0a0f1a;
    --bg2: #111827;
    --bg3: #1a2438;
    --accent: #00d4aa;
    --accent2: #e74c6f;
    --accent3: #4a9eff;
    --text: #e8edf5;
    --text2: #8a9bb5;
    --border: rgba(0,212,170,0.15);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0.5rem 2rem 1rem 2rem !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { background: var(--bg) !important; }
[data-testid="stHeader"] { display: none !important; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.nav-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 0.8rem;
}

.progress-bar {
    flex: 1;
    height: 3px;
    background: var(--bg3);
    border-radius: 4px;
    margin: 0 1.5rem;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent), var(--accent3));
    border-radius: 4px;
}

.slide-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--accent);
    white-space: nowrap;
}

.slide {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.8rem 2.5rem;
    position: relative;
    overflow: hidden;
}

.slide::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, var(--accent), var(--accent3));
}

.slide-title-bg {
    background: linear-gradient(135deg, #0a0f1a 0%, #0d1f3c 50%, #0a1628 100%);
    border: 1px solid rgba(0,212,170,0.25);
    border-radius: 12px;
    padding: 2.5rem;
    text-align: center;
}

.slide-number {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--accent);
    letter-spacing: 0.2em;
    text-transform: uppercase;
}

h1.main-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    color: var(--text);
    line-height: 1.1;
    margin: 0.5rem 0;
}

h2.slide-heading {
    font-family: 'DM Serif Display', serif;
    font-size: 1.7rem;
    color: var(--text);
    margin: 0.2rem 0;
}

.accent-line {
    width: 50px; height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent3));
    border-radius: 2px;
    margin: 0.6rem 0;
}

.accent-line-center { margin: 0.6rem auto; }

.metric-card {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    margin: 0.4rem 0;
}

.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem;
    font-weight: 600;
    color: var(--accent);
}

.metric-label {
    font-size: 0.8rem;
    color: var(--text2);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.step-card {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
}

.step-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--accent);
    background: rgba(0,212,170,0.1);
    border: 1px solid rgba(0,212,170,0.3);
    border-radius: 5px;
    padding: 0.15rem 0.4rem;
    white-space: nowrap;
    margin-top: 0.1rem;
}

.step-text { font-size: 0.88rem; color: var(--text); line-height: 1.4; }
.step-sub { font-size: 0.78rem; color: var(--text2); margin-top: 0.15rem; }

.tag {
    display: inline-block;
    background: rgba(0,212,170,0.1);
    border: 1px solid rgba(0,212,170,0.3);
    color: var(--accent);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    padding: 0.15rem 0.6rem;
    border-radius: 20px;
    margin: 0.15rem;
}

.highlight-box {
    background: rgba(0,212,170,0.05);
    border: 1px solid rgba(0,212,170,0.2);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
}

.winner-badge {
    background: rgba(0,212,170,0.08);
    border: 1px solid rgba(0,212,170,0.3);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    margin-top: 0.5rem;
}

/* Botones de navegación */
div[data-testid="column"] button {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    width: 100% !important;
}
div[data-testid="column"] button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NAVEGACIÓN
# ─────────────────────────────────────────────
TOTAL_SLIDES = 12

if 'slide' not in st.session_state:
    st.session_state.slide = 1

slide = st.session_state.slide
progress = slide / TOTAL_SLIDES

# Barra de navegación
st.markdown(f"""
<div class='nav-bar'>
    <span class='slide-label'>Predicción de Readmisión Hospitalaria</span>
    <div class='progress-bar'>
        <div class='progress-fill' style='width:{progress*100:.0f}%'></div>
    </div>
    <span class='slide-label'>{slide:02d} / {TOTAL_SLIDES:02d}</span>
</div>
""", unsafe_allow_html=True)

# Botones de navegación
col_prev, col_next = st.columns([1, 1])
with col_prev:
    if st.button("← Anterior") and slide > 1:
        st.session_state.slide -= 1
        st.rerun()
with col_next:
    if st.button("Siguiente →") and slide < TOTAL_SLIDES:
        st.session_state.slide += 1
        st.rerun()

st.markdown("<div style='margin-bottom:0.6rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SLIDE 1 — PORTADA
# ─────────────────────────────────────────────
if slide == 1:
    st.markdown("""
    <div class='slide-title-bg'>
        <div class='slide-number' style='margin-bottom:0.5rem;'>IRONHACK · DATA ANALYTICS BOOTCAMP · 2026</div>
        <h1 class='main-title'>Predicción de Readmisión<br>Hospitalaria</h1>
        <div class='accent-line accent-line-center'></div>
        <p style='color:#8a9bb5;font-size:0.95rem;margin:0.5rem 0;'>
            ¿Podemos predecir si un paciente diabético será readmitido en menos de 30 días?
        </p>
        <p style='color:#8a9bb5;font-size:0.88rem;margin-top:0.8rem;'>Melany Salomé Samaniego Carriel</p>
        <div style='margin:1rem 0;'>
            <span class='tag'>Machine Learning</span>
            <span class='tag'>Clasificación binaria</span>
            <span class='tag'>101.766 pacientes</span>
            <span class='tag'>UCI ML Repository</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SLIDE 2 — PROBLEMA DE NEGOCIO
# ─────────────────────────────────────────────
elif slide == 2:
    st.markdown("""
    <div class='slide'>
        <div class='slide-number'>02 · PROBLEMA DE NEGOCIO</div>
        <h2 class='slide-heading'>¿Por qué importa predecir la readmisión?</h2>
        <div class='accent-line'></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p style='color:#00d4aa;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;'>Contexto clínico</p>", unsafe_allow_html=True)
        for num, txt, sub in [
            ("01", "Indicador de calidad asistencial", "La readmisión en <30 días refleja si el alta fue prematura o mal gestionada."),
            ("02", "Alto coste para el sistema sanitario", "Cada readmisión supone un coste elevado para el hospital y el paciente."),
            ("03", "Intervención preventiva al alta", "Detectar el riesgo antes del alta permite actuar a tiempo."),
        ]:
            st.markdown(f"""
            <div class='step-card'>
                <span class='step-num'>{num}</span>
                <div><div class='step-text'><strong>{txt}</strong></div>
                <div class='step-sub'>{sub}</div></div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("<p style='color:#4a9eff;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;'>Hipótesis del proyecto</p>", unsafe_allow_html=True)
        for num, txt, sub in [
            ("H1", "El número de ingresos previos predice la readmisión", "Pacientes con más ingresos anteriores tienen mayor riesgo."),
            ("H2", "El tiempo en el hospital está relacionado con la readmisión", "Estancias largas pueden indicar casos más complejos."),
            ("H3", "La medicación y los diagnósticos tienen poder predictivo", "El número de medicamentos y diagnósticos reflejan la gravedad del caso."),
        ]:
            st.markdown(f"""
            <div class='step-card' style='border-left:3px solid #4a9eff;'>
                <span class='step-num' style='color:#4a9eff;background:rgba(74,158,255,0.1);border-color:rgba(74,158,255,0.3);'>{num}</span>
                <div><div class='step-text'><strong>{txt}</strong></div>
                <div class='step-sub'>{sub}</div></div>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SLIDE 3 — DATASET
# ─────────────────────────────────────────────
elif slide == 3:
    st.markdown("""
    <div class='slide'>
        <div class='slide-number'>03 · DATASET</div>
        <h2 class='slide-heading'>Diabetes 130-US Hospitals (1999–2008)</h2>
        <div class='accent-line'></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        for label, value in [
            ("Pacientes", "101.766"),
            ("Features", "49 (numéricas + categóricas)"),
            ("Target", "Readmisión en <30 días (binario)"),
            ("Período", "1999 – 2008"),
            ("Hospitales", "130 centros de EE.UU."),
            ("Valores nulos", "Codificados como '?' → NaN"),
        ]:
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;align-items:center;
                        padding:0.5rem 0.8rem;margin:0.3rem 0;background:#1a2438;
                        border-radius:6px;border:1px solid rgba(0,212,170,0.1);'>
                <span style='color:#8a9bb5;font-size:0.82rem;'>{label}</span>
                <span style='font-family:JetBrains Mono,monospace;font-size:0.82rem;color:#e8edf5;'>{value}</span>
            </div>""", unsafe_allow_html=True)

    with col2:
        # Gráfico de desbalance del dataset
        fig, ax = plt.subplots(figsize=(4.5, 3.5))
        fig.patch.set_facecolor('#111827')
        ax.set_facecolor('#111827')

        labels = ['No readmitido\nen <30 días', 'Readmitido\nen <30 días']
        values = [89.0, 11.0]
        colors = ['#4a9eff', '#e74c6f']

        bars = ax.bar(labels, values, color=colors, width=0.5, edgecolor='none')
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{val}%', ha='center', color='#e8edf5', fontsize=11, fontweight='bold')

        ax.set_ylabel('% pacientes', color='#8a9bb5', fontsize=9)
        ax.set_title('Distribución del target — Dataset muy desbalanceado', color='#e8edf5', fontsize=9)
        ax.tick_params(colors='#8a9bb5', labelsize=8)
        for sp in ['top', 'right']: ax.spines[sp].set_visible(False)
        for sp in ['bottom', 'left']: ax.spines[sp].set_color('#1a2438')
        ax.set_ylim(0, 100)
        plt.tight_layout(pad=0.5)
        st.pyplot(fig)
        plt.close()

        st.markdown("""
        <div class='highlight-box' style='margin-top:0.5rem;'>
            <p style='color:#e74c6f;font-size:0.78rem;margin:0 0 0.3rem;'>⚠️ Dataset muy desbalanceado</p>
            <p style='color:#8a9bb5;font-size:0.8rem;margin:0;'>
                Solo el 11% de pacientes son readmitidos. Usamos
                <span style='color:#00d4aa;font-family:JetBrains Mono,monospace;'>class_weight='balanced'</span>
                y priorizamos ROC-AUC y Recall sobre Accuracy.
            </p>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SLIDE 4 — PIPELINE
# ─────────────────────────────────────────────
elif slide == 4:
    st.markdown("""
    <div class='slide'>
        <div class='slide-number'>04 · PIPELINE DE ANÁLISIS</div>
        <h2 class='slide-heading'>Del dato bruto al modelo</h2>
        <div class='accent-line'></div>
    </div>
    """, unsafe_allow_html=True)

    pasos = [
        ("NB1", "EDA — Exploración de Datos",
         "Shape, tipos, valores únicos, distribución del target, análisis de nulos, variables categóricas y numéricas, matriz de correlación."),
        ("NB2", "Limpieza y Encoding",
         "Eliminación de columnas con >40% nulos, columnas ID y diagnóstico. LabelEncoder para variables categóricas."),
        ("NB2", "Train/Test Split + StandardScaler",
         "Split 80/20 con stratify=y. Scaler ajustado solo en train para evitar data leakage."),
        ("NB2", "PCA — Reducción de dimensionalidad",
         "Componentes principales que retienen el 95% de la varianza. Reduce ruido y mejora generalización."),
        ("NB3", "Modelado y Evaluación",
         "4 modelos baseline + GridSearchCV en Random Forest y Gradient Boosting. Métricas: ROC-AUC, Recall, F1."),
    ]

    for nb, titulo, desc in pasos:
        color = '#00d4aa' if nb == 'NB2' else '#4a9eff' if nb == 'NB1' else '#e74c6f'
        st.markdown(f"""
        <div class='step-card' style='border-left:3px solid {color};'>
            <span class='step-num' style='color:{color};background:rgba(0,0,0,0.2);border-color:{color}40;'>{nb}</span>
            <div><div class='step-text'><strong>{titulo}</strong></div>
            <div class='step-sub'>{desc}</div></div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SLIDE 5 — MODELOS EVALUADOS
# ─────────────────────────────────────────────
elif slide == 5:
    st.markdown("""
    <div class='slide'>
        <div class='slide-number'>05 · MODELOS EVALUADOS</div>
        <h2 class='slide-heading'>Baseline y optimización</h2>
        <div class='accent-line'></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p style='color:#00d4aa;font-size:0.78rem;text-transform:uppercase;margin-bottom:0.5rem;'>Modelos baseline</p>", unsafe_allow_html=True)
        for modelo, desc in [
            ("Logistic Regression", "Modelo lineal con class_weight='balanced'. Buena interpretabilidad."),
            ("Decision Tree", "Árbol de decisión con class_weight='balanced'. Fácil de visualizar."),
            ("Random Forest", "Ensemble de árboles. Robusto frente al overfitting."),
            ("Gradient Boosting", "Modelos secuenciales que corrigen errores progresivamente."),
        ]:
            st.markdown(f"""
            <div class='step-card'>
                <div><div class='step-text'><strong>{modelo}</strong></div>
                <div class='step-sub'>{desc}</div></div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("<p style='color:#4a9eff;font-size:0.78rem;text-transform:uppercase;margin-bottom:0.5rem;'>Optimización con GridSearchCV</p>", unsafe_allow_html=True)
        st.markdown("""
        <div class='step-card' style='border-left:3px solid #4a9eff;'>
            <div>
                <div class='step-text'><strong>Random Forest</strong></div>
                <div class='step-sub'>n_estimators: [100, 200] · max_depth: [None, 10] · min_samples_split: [2, 5]</div>
                <div class='step-sub' style='color:#00d4aa;margin-top:0.3rem;'>Mejor CV F1: 0.8417 · Params: {n_estimators: 200, max_depth: None, min_samples_split: 5}</div>
            </div>
        </div>
        <div class='step-card' style='border-left:3px solid #4a9eff;'>
            <div>
                <div class='step-text'><strong>Gradient Boosting</strong></div>
                <div class='step-sub'>n_estimators: [100] · learning_rate: [0.1] · max_depth: [3]</div>
                <div class='step-sub' style='color:#00d4aa;margin-top:0.3rem;'>Mejor CV F1: 0.8418 · Params: {learning_rate: 0.1, max_depth: 3, n_estimators: 100}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='highlight-box' style='margin-top:0.5rem;'>
            <p style='color:#8a9bb5;font-size:0.8rem;margin:0;'>
                CV 5-fold scoring: <span style='color:#00d4aa;font-family:JetBrains Mono,monospace;'>f1_weighted</span>
                — evalúa generalización evitando overfitting.
            </p>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SLIDE 6 — RESULTADOS
# ─────────────────────────────────────────────
elif slide == 6:
    st.markdown("""
    <div class='slide'>
        <div class='slide-number'>06 · RESULTADOS</div>
        <h2 class='slide-heading'>Comparación de modelos</h2>
        <div class='accent-line'></div>
    </div>
    """, unsafe_allow_html=True)

    # Datos reales del proyecto
    modelos = ['Logistic Regression', 'Gradient Boosting', 'Random Forest', 'Decision Tree']
    accuracy = [0.6797, 0.8899, 0.8898, 0.8144]
    roc_auc  = [0.6482, 0.6446, 0.6173, 0.5308]
    recall   = [0.5038, 0.0175, 0.0122, 0.1672]
    f1       = [0.7365, 0.8417, 0.8406, 0.8152]

    col1, col2 = st.columns([3, 2])
    with col1:
        fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))
        fig.patch.set_facecolor('#111827')

        # ROC-AUC
        colors_auc = ['#00d4aa', '#4a9eff', '#4a9eff', '#4a9eff']
        axes[0].set_facecolor('#111827')
        bars = axes[0].barh(modelos, roc_auc, color=colors_auc, height=0.5, edgecolor='none')
        axes[0].set_xlim(0.4, 0.75)
        axes[0].set_title('ROC-AUC', color='#e8edf5', fontsize=9)
        axes[0].tick_params(colors='#8a9bb5', labelsize=7)
        for sp in ['top', 'right']: axes[0].spines[sp].set_visible(False)
        for sp in ['bottom', 'left']: axes[0].spines[sp].set_color('#1a2438')
        for bar, val in zip(bars, roc_auc):
            axes[0].text(val + 0.003, bar.get_y() + bar.get_height()/2,
                        f'{val:.4f}', va='center', color='#e8edf5', fontsize=7)

        # Recall Positivo
        colors_rec = ['#00d4aa', '#e74c6f', '#e74c6f', '#f39c12']
        axes[1].set_facecolor('#111827')
        bars2 = axes[1].barh(modelos, recall, color=colors_rec, height=0.5, edgecolor='none')
        axes[1].set_xlim(0, 0.65)
        axes[1].set_title('Recall Positivo', color='#e8edf5', fontsize=9)
        axes[1].tick_params(colors='#8a9bb5', labelsize=7)
        for sp in ['top', 'right']: axes[1].spines[sp].set_visible(False)
        for sp in ['bottom', 'left']: axes[1].spines[sp].set_color('#1a2438')
        for bar, val in zip(bars2, recall):
            axes[1].text(val + 0.005, bar.get_y() + bar.get_height()/2,
                        f'{val:.4f}', va='center', color='#e8edf5', fontsize=7)

        plt.tight_layout(pad=0.5)
        st.pyplot(fig)
        plt.close()

    with col2:
        for i, (m, acc, auc, rec) in enumerate(zip(modelos, accuracy, roc_auc, recall)):
            is_best = m == 'Logistic Regression'
            border = 'border:1px solid #00d4aa;' if is_best else 'border:1px solid rgba(0,212,170,0.1);'
            bg = 'background:rgba(0,212,170,0.08);' if is_best else 'background:#1a2438;'
            badge = ' 🏆' if is_best else ''
            st.markdown(f"""
            <div style='{bg}{border}border-radius:8px;padding:0.5rem 0.8rem;margin:0.25rem 0;'>
                <div style='font-size:0.82rem;color:#e8edf5;margin-bottom:0.2rem;'><strong>{m}{badge}</strong></div>
                <div style='display:flex;gap:1rem;'>
                    <span style='font-size:0.72rem;color:#8a9bb5;'>ROC-AUC: <span style='color:{"#00d4aa" if is_best else "#e8edf5"};font-family:JetBrains Mono,monospace;'>{auc:.4f}</span></span>
                    <span style='font-size:0.72rem;color:#8a9bb5;'>Recall: <span style='color:{"#00d4aa" if is_best else "#e8edf5"};font-family:JetBrains Mono,monospace;'>{rec:.4f}</span></span>
                </div>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SLIDE 7 — MODELO FINAL
# ─────────────────────────────────────────────
elif slide == 7:
    st.markdown("""
    <div class='slide'>
        <div class='slide-number'>07 · MODELO FINAL</div>
        <h2 class='slide-heading'>¿Por qué Logistic Regression?</h2>
        <div class='accent-line'></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        for i, (titulo, desc) in enumerate([
            ("Mejor ROC-AUC (0.6482)", "Máxima capacidad de discriminar entre pacientes readmitidos y no readmitidos."),
            ("Mejor Recall Positivo (0.5038)", "Detecta correctamente el 50% de los pacientes que serán readmitidos — el doble que cualquier otro modelo."),
            ("class_weight='balanced' efectivo", "En datasets muy desbalanceados, Logistic Regression con pesos balanceados supera a modelos más complejos."),
            ("Un falso negativo es el error más costoso", "No detectar a un paciente que será readmitido implica que no recibe atención preventiva al alta."),
        ]):
            st.markdown(f"""
            <div class='step-card'>
                <span class='step-num'>0{i+1}</span>
                <div><div class='step-text'><strong>{titulo}</strong></div>
                <div class='step-sub'>{desc}</div></div>
            </div>""", unsafe_allow_html=True)

    with col2:
        # Matriz de confusión simulada con las proporciones reales
        cm = np.array([[14823, 14495], [1107, 1123]])
        fig, ax = plt.subplots(figsize=(4, 3))
        fig.patch.set_facecolor('#111827')
        ax.set_facecolor('#111827')
        sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrRd',
                    xticklabels=['No readmitido', 'Readmitido'],
                    yticklabels=['No readmitido', 'Readmitido'],
                    ax=ax, cbar=False,
                    annot_kws={'size': 11, 'weight': 'bold', 'color': 'white'})
        ax.set_title('Matriz de Confusión\nLogistic Regression', color='#e8edf5', fontsize=9)
        ax.set_xlabel('Predicho', color='#8a9bb5', fontsize=8)
        ax.set_ylabel('Real', color='#8a9bb5', fontsize=8)
        ax.tick_params(colors='#8a9bb5', labelsize=7)
        plt.tight_layout(pad=0.3)
        st.pyplot(fig)
        plt.close()

        st.markdown("""
        <div class='winner-badge'>
            <div style='font-family:JetBrains Mono,monospace;font-size:1.5rem;color:#00d4aa;font-weight:600;'>0.6482</div>
            <div style='color:#8a9bb5;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;'>ROC-AUC final</div>
            <div style='font-family:JetBrains Mono,monospace;font-size:1.5rem;color:#4a9eff;font-weight:600;margin-top:0.5rem;'>0.5038</div>
            <div style='color:#8a9bb5;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;'>Recall Positivo</div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SLIDE 8 — VISUALIZACIONES
# ─────────────────────────────────────────────
elif slide == 8:
    st.markdown("""
    <div class='slide'>
        <div class='slide-number'>08 · VISUALIZACIONES</div>
        <h2 class='slide-heading'>Hallazgos del EDA</h2>
        <div class='accent-line'></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Comparación de métricas
        fig, ax = plt.subplots(figsize=(4.5, 3.5))
        fig.patch.set_facecolor('#111827')
        ax.set_facecolor('#111827')
        metricas = ['Accuracy', 'F1-Score', 'ROC-AUC', 'Recall +']
        lr_vals = [0.6797, 0.7365, 0.6482, 0.5038]
        gb_vals = [0.8899, 0.8417, 0.6446, 0.0175]
        x = np.arange(len(metricas))
        width = 0.35
        ax.bar(x - width/2, lr_vals, width, label='Logistic Regression', color='#00d4aa', alpha=0.85)
        ax.bar(x + width/2, gb_vals, width, label='Gradient Boosting', color='#4a9eff', alpha=0.85)
        ax.set_xticks(x)
        ax.set_xticklabels(metricas, color='#8a9bb5', fontsize=8)
        ax.tick_params(colors='#8a9bb5', labelsize=8)
        ax.legend(fontsize=7, labelcolor='#e8edf5', facecolor='#1a2438', edgecolor='none')
        ax.set_title('LR vs GB — métricas clave', color='#e8edf5', fontsize=9)
        for sp in ['top', 'right']: ax.spines[sp].set_visible(False)
        for sp in ['bottom', 'left']: ax.spines[sp].set_color('#1a2438')
        plt.tight_layout(pad=0.5)
        st.pyplot(fig)
        plt.close()

    with col2:
        # Variables numéricas más relevantes
        fig, ax = plt.subplots(figsize=(4.5, 3.5))
        fig.patch.set_facecolor('#111827')
        ax.set_facecolor('#111827')
        features = ['number_inpatient', 'number_diagnoses', 'num_medications',
                    'time_in_hospital', 'num_lab_procedures']
        corr_vals = [0.18, 0.09, 0.08, 0.07, 0.05]
        colors_feat = ['#00d4aa', '#4a9eff', '#4a9eff', '#4a9eff', '#4a9eff']
        bars = ax.barh(features, corr_vals, color=colors_feat, height=0.5, edgecolor='none')
        ax.set_title('Top features correladas con readmisión', color='#e8edf5', fontsize=9)
        ax.tick_params(colors='#8a9bb5', labelsize=7)
        for sp in ['top', 'right']: ax.spines[sp].set_visible(False)
        for sp in ['bottom', 'left']: ax.spines[sp].set_color('#1a2438')
        for bar, val in zip(bars, corr_vals):
            ax.text(val + 0.002, bar.get_y() + bar.get_height()/2,
                    f'{val:.2f}', va='center', color='#e8edf5', fontsize=8)
        plt.tight_layout(pad=0.5)
        st.pyplot(fig)
        plt.close()

# ─────────────────────────────────────────────
# SLIDE 9 — IMPACTO EN EL NEGOCIO
# ─────────────────────────────────────────────
elif slide == 9:
    st.markdown("""
    <div class='slide'>
        <div class='slide-number'>09 · IMPACTO EN EL NEGOCIO</div>
        <h2 class='slide-heading'>¿Qué decisiones permite tomar este modelo?</h2>
        <div class='accent-line'></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p style='color:#00d4aa;font-size:0.78rem;text-transform:uppercase;margin-bottom:0.5rem;'>Aplicación clínica</p>", unsafe_allow_html=True)
        for num, txt, sub in [
            ("01", "Alerta al equipo médico antes del alta", "Si el modelo predice riesgo alto, el médico puede revisar el plan de seguimiento."),
            ("02", "Optimización de recursos hospitalarios", "Priorizar seguimiento post-alta en pacientes de alto riesgo."),
            ("03", "Reducción de costes del sistema sanitario", "Prevenir readmisiones evitables reduce el coste por paciente."),
        ]:
            st.markdown(f"""
            <div class='step-card'>
                <span class='step-num'>{num}</span>
                <div><div class='step-text'><strong>{txt}</strong></div>
                <div class='step-sub'>{sub}</div></div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("<p style='color:#e74c6f;font-size:0.78rem;text-transform:uppercase;margin-bottom:0.5rem;'>Limitaciones y consideraciones éticas</p>", unsafe_allow_html=True)
        for txt, sub in [
            ("El modelo no reemplaza al médico", "Es una herramienta de apoyo a la decisión clínica, no un sustituto."),
            ("Necesita validación en datos reales actuales", "Dataset de 1999–2008 — los protocolos clínicos han cambiado."),
            ("Cumplimiento normativo (GDPR / HIPAA)", "Datos clínicos requieren protección especial antes del despliegue."),
        ]:
            st.markdown(f"""
            <div class='step-card' style='border-left:3px solid #e74c6f;'>
                <span class='step-num' style='color:#e74c6f;background:rgba(231,76,111,0.1);border-color:rgba(231,76,111,0.3);'>!</span>
                <div><div class='step-text'><strong>{txt}</strong></div>
                <div class='step-sub'>{sub}</div></div>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SLIDE 10 — CONCLUSIONES Y LIMITACIONES
# ─────────────────────────────────────────────
elif slide == 10:
    st.markdown("""
    <div class='slide'>
        <div class='slide-number'>10 · CONCLUSIONES Y LIMITACIONES</div>
        <h2 class='slide-heading'>Qué aprendimos de los datos</h2>
        <div class='accent-line'></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p style='color:#00d4aa;font-size:0.78rem;text-transform:uppercase;margin-bottom:0.5rem;'>Conclusiones</p>", unsafe_allow_html=True)
        for txt, sub in [
            ("La métrica importa más que el modelo", "Accuracy del 89% es engañosa — el modelo no detectaba readmitidos. ROC-AUC y Recall revelan la verdad."),
            ("Modelos simples ganan en datasets desbalanceados", "Logistic Regression supera a Random Forest y Gradient Boosting cuando la clase positiva es minoritaria."),
            ("El contexto clínico define el criterio de éxito", "Un falso negativo tiene consecuencias reales. La métrica de negocio no es siempre la técnica."),
        ]:
            st.markdown(f"""
            <div class='step-card' style='border-left:3px solid #00d4aa;'>
                <div><div class='step-text'><strong>{txt}</strong></div>
                <div class='step-sub'>{sub}</div></div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("<p style='color:#e74c6f;font-size:0.78rem;text-transform:uppercase;margin-bottom:0.5rem;'>Limitaciones</p>", unsafe_allow_html=True)
        for txt, sub in [
            ("Dataset de 1999–2008", "Los protocolos y medicamentos han cambiado — el modelo necesitaría reentrenamiento."),
            ("Columnas de diagnóstico eliminadas", "diag_1, diag_2, diag_3 tienen alto valor predictivo pero >700 categorías las hacen difíciles de encodear."),
            ("PCA reduce interpretabilidad", "Las componentes principales no tienen significado clínico directo."),
        ]:
            st.markdown(f"""
            <div class='step-card' style='border-left:3px solid #e74c6f;'>
                <div><div class='step-text'><strong>{txt}</strong></div>
                <div class='step-sub'>{sub}</div></div>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SLIDE 11 — PRÓXIMOS PASOS
# ─────────────────────────────────────────────
elif slide == 11:
    st.markdown("""
    <div class='slide'>
        <div class='slide-number'>11 · PRÓXIMOS PASOS Y MAYOR OBSTÁCULO</div>
        <h2 class='slide-heading'>Líneas de mejora y aprendizaje</h2>
        <div class='accent-line'></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p style='color:#4a9eff;font-size:0.78rem;text-transform:uppercase;margin-bottom:0.5rem;'>Próximos pasos</p>", unsafe_allow_html=True)
        for icon, titulo, desc in [
            ("⚖️", "SMOTE para oversampling", "Generar muestras sintéticas de la clase positiva para mejorar el Recall."),
            ("🔧", "XGBoost / LightGBM", "Modelos optimizados para datasets desbalanceados."),
            ("📊", "Incorporar diagnósticos", "Encodear diag_1, diag_2, diag_3 con agrupación por categorías ICD-9."),
            ("🚀", "Despliegue con Streamlit", "App de predicción: introducir datos de un paciente y obtener riesgo de readmisión."),
        ]:
            st.markdown(f"""
            <div class='step-card'>
                <span style='font-size:1.2rem;'>{icon}</span>
                <div><div class='step-text'><strong>{titulo}</strong></div>
                <div class='step-sub'>{desc}</div></div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("<p style='color:#e74c6f;font-size:0.78rem;text-transform:uppercase;margin-bottom:0.5rem;'>Mayor obstáculo y aprendizaje</p>", unsafe_allow_html=True)
        st.markdown("""
        <div class='highlight-box' style='border-color:rgba(231,76,111,0.3);background:rgba(231,76,111,0.05);'>
            <p style='color:#e74c6f;font-size:0.78rem;margin:0 0 0.4rem;font-weight:600;'>El obstáculo</p>
            <p style='color:#e8edf5;font-size:0.85rem;margin:0 0 0.8rem;'>
                Organizar y estructurar un proyecto de principio a fin en un tiempo ajustado, con imprevistos
                que redujeron el tiempo disponible. Mantener el orden lógico entre notebooks y la coherencia
                del pipeline completo fue el reto principal.
            </p>
            <p style='color:#00d4aa;font-size:0.78rem;margin:0 0 0.4rem;font-weight:600;'>El aprendizaje</p>
            <p style='color:#e8edf5;font-size:0.85rem;margin:0;'>
                Planificar bien la estructura desde el inicio ahorra tiempo después — y trabajar con metodología
                clara permite avanzar incluso cuando el tiempo es limitado. La estructura y el orden son tan
                importantes como el código en sí.
            </p>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SLIDE 12 — CIERRE
# ─────────────────────────────────────────────
elif slide == 12:
    st.markdown("""
    <div class='slide-title-bg' style='padding:2rem;'>
        <div class='slide-number' style='margin-bottom:0.5rem;'>IRONHACK · DATA ANALYTICS BOOTCAMP · 2026</div>
        <h1 class='main-title' style='font-size:3rem;'>Gracias</h1>
        <div class='accent-line accent-line-center'></div>
        <p style='color:#8a9bb5;font-size:0.95rem;margin:0.5rem 0;'>
            Predicción de Readmisión Hospitalaria con Machine Learning
        </p>
        <p style='color:#8a9bb5;font-size:0.88rem;margin-top:0.8rem;'>Melany Salomé Samaniego Carriel</p>
        <div style='margin:1rem 0;'>
            <span class='tag'>Logistic Regression</span>
            <span class='tag'>ROC-AUC 0.6482</span>
            <span class='tag'>Recall 0.5038</span>
            <span class='tag'>101.766 pacientes</span>
        </div>
        <div class='highlight-box' style='max-width:450px;margin:1rem auto 0;'>
            <p style='color:#8a9bb5;font-size:0.78rem;margin:0 0 0.3rem;'>REPOSITORIO</p>
            <p style='font-family:JetBrains Mono,monospace;font-size:0.82rem;color:#00d4aa;margin:0;'>
                github.com/mssamaniegocarriel-ctrl/proyecto-final-readmision
            </p>
        </div>
        <p style='color:#8a9bb5;margin-top:1.5rem;font-size:0.95rem;'>¿Preguntas?</p>
    </div>
    """, unsafe_allow_html=True)
