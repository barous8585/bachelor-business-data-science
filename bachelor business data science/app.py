import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="UCO Data Science Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def load_custom_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .tool-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .tool-card h3 {
        color: white;
        margin-top: 0;
    }
    .stat-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    .stat-label {
        color: #666;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

load_custom_css()

st.markdown('<h1 class="main-header">🎓 UCO Data Science Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Plateforme complète pour les étudiants du Bachelor Business Data Science - UCO Angers</p>', unsafe_allow_html=True)

st.sidebar.title("🧭 Navigation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Choisissez un outil :",
    [
        "🏠 Accueil",
        "📊 Statistiques & Probabilités",
        "💻 Assistant Code & Debug",
        "📈 Cas Business Data Science",
        "📁 Gestionnaire de Projets",
        "📚 Planificateur de Révisions",
        "🔗 Bibliothèque de Ressources",
        "🎤 Simulateur d'Entretiens",
        "💼 Portfolio Generator",
        "🤝 Forum d'Entraide",
        "🎲 Générateur de Datasets"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("**Bachelor Business Data Science**\n\nUniversité Catholique de l'Ouest - Angers")

if page == "🏠 Accueil":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="stat-box"><div class="stat-number">10</div><div class="stat-label">Outils disponibles</div></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stat-box"><div class="stat-number">3</div><div class="stat-label">Années de formation</div></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stat-box"><div class="stat-number">∞</div><div class="stat-label">Possibilités</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## 📚 Outils d'Apprentissage")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="tool-card">
            <h3>📊 Statistiques & Probas</h3>
            <p>Visualisations interactives, calculateurs de tests, exercices corrigés</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tool-card">
            <h3>💻 Assistant Code</h3>
            <p>Débogage Python/SQL, snippets, explications d'erreurs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="tool-card">
            <h3>📈 Cas Business</h3>
            <p>Projets réalistes, datasets, scénarios guidés</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("## 🎯 Productivité")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="tool-card">
            <h3>📁 Gestion de Projets</h3>
            <p>Templates, checklists, suivi de progression</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tool-card">
            <h3>📚 Planificateur</h3>
            <p>Révisions espacées, flashcards, suivi</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="tool-card">
            <h3>🔗 Ressources</h3>
            <p>Tutoriels, datasets, documentation</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("## 💼 Préparation Pro")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="tool-card">
            <h3>🎤 Simulateur d'Entretiens</h3>
            <p>Questions techniques, études de cas, conseils</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tool-card">
            <h3>💼 Portfolio</h3>
            <p>Présentation de projets, visualisations, export web</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("## 🤝 Collaboration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="tool-card">
            <h3>🤝 Forum d'Entraide</h3>
            <p>Q&A, partage de notes, binômes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tool-card">
            <h3>🎲 Générateur de Datasets</h3>
            <p>Données synthétiques pour s'entraîner</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.success("👈 **Utilisez le menu latéral pour accéder aux différents outils**")

elif page == "📊 Statistiques & Probabilités":
    exec(open("modules/stats_proba.py").read())

elif page == "💻 Assistant Code & Debug":
    exec(open("modules/code_assistant.py").read())

elif page == "📈 Cas Business Data Science":
    exec(open("modules/business_cases.py").read())

elif page == "📁 Gestionnaire de Projets":
    exec(open("modules/project_manager.py").read())

elif page == "📚 Planificateur de Révisions":
    exec(open("modules/revision_planner.py").read())

elif page == "🔗 Bibliothèque de Ressources":
    exec(open("modules/resources_library.py").read())

elif page == "🎤 Simulateur d'Entretiens":
    exec(open("modules/interview_simulator.py").read())

elif page == "💼 Portfolio Generator":
    exec(open("modules/portfolio_generator.py").read())

elif page == "🤝 Forum d'Entraide":
    exec(open("modules/forum.py").read())

elif page == "🎲 Générateur de Datasets":
    exec(open("modules/dataset_generator.py").read())
