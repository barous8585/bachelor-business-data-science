import streamlit as st
import sys
from pathlib import Path

st.set_page_config(
    page_title="UCO Data Science Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

sys.path.insert(0, str(Path(__file__).parent))

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
        "👨‍🏫 Espace Professeur",
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
        st.markdown('<div class="stat-box"><div class="stat-number">11</div><div class="stat-label">Outils disponibles</div></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stat-box"><div class="stat-number">3</div><div class="stat-label">Années de formation</div></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stat-box"><div class="stat-number">∞</div><div class="stat-label">Possibilités</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## 👨‍🏫 Espace Professeur")
    
    st.markdown("""
    <div class="tool-card">
        <h3>👨‍🏫 Espace Professeur - NOUVEAU !</h3>
        <p>Uploadez vos cours et générez automatiquement des exercices pour vos étudiants B1</p>
    </div>
    """, unsafe_allow_html=True)
    
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

else:
    module_map = {
        "👨‍🏫 Espace Professeur": "modules/teacher_space.py",
        "📊 Statistiques & Probabilités": "modules/stats_proba.py",
        "💻 Assistant Code & Debug": "modules/code_assistant.py",
        "📈 Cas Business Data Science": "modules/business_cases.py",
        "📁 Gestionnaire de Projets": "modules/project_manager.py",
        "📚 Planificateur de Révisions": "modules/revision_planner.py",
        "🔗 Bibliothèque de Ressources": "modules/resources_library.py",
        "🎤 Simulateur d'Entretiens": "modules/interview_simulator.py",
        "💼 Portfolio Generator": "modules/portfolio_generator.py",
        "🤝 Forum d'Entraide": "modules/forum.py",
        "🎲 Générateur de Datasets": "modules/dataset_generator.py"
    }
    
    module_path = module_map.get(page)
    if module_path:
        with open(module_path, 'r', encoding='utf-8') as f:
            exec(f.read(), globals())
