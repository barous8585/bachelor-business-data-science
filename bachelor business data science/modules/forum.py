import streamlit as st
import json
from pathlib import Path
from datetime import datetime

st.title("🤝 Forum d'Entraide UCO")
st.markdown("**Posez vos questions et partagez vos connaissances**")

DATA_FILE = Path("data/forum_posts.json")
DATA_FILE.parent.mkdir(exist_ok=True)

def load_posts():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

tab1, tab2, tab3 = st.tabs(["💬 Questions", "➕ Poser une Question", "👥 Binômes & Groupes"])

with tab1:
    st.header("💬 Questions & Réponses")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search = st.text_input("🔍 Rechercher", placeholder="Mots-clés...")
    
    with col2:
        matiere_filter = st.selectbox(
            "Filtrer par matière",
            ["Toutes", "Python", "Statistiques", "Machine Learning", "SQL", 
             "Mathématiques", "Business Intelligence", "Autre"]
        )
    
    posts = load_posts()
    
    filtered_posts = posts
    if matiere_filter != "Toutes":
        filtered_posts = [p for p in filtered_posts if p.get('matiere') == matiere_filter]
    if search:
        filtered_posts = [p for p in filtered_posts if search.lower() in p.get('titre', '').lower() or search.lower() in p.get('contenu', '').lower()]
    
    if not filtered_posts:
        st.info("Aucune question pour le moment. Soyez le premier à poser une question !")
    else:
        filtered_posts.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        for i, post in enumerate(filtered_posts):
            status_icon = "✅" if post.get('resolu', False) else "❓"
            
            with st.expander(f"{status_icon} {post['titre']} - {post['matiere']} - par {post['auteur']}"):
                st.caption(f"📅 {post.get('date', '')}")
                st.markdown(f"**Question :**")
                st.markdown(post['contenu'])
                
                if post.get('code'):
                    st.code(post['code'], language='python')
                
                st.markdown("---")
                st.markdown("**💬 Réponses :**")
                
                if 'reponses' not in post:
                    post['reponses'] = []
                
                if post['reponses']:
                    for j, reponse in enumerate(post['reponses']):
                        st.markdown(f"**{reponse['auteur']}** - {reponse.get('date', '')}")
                        st.markdown(reponse['contenu'])
                        if reponse.get('code'):
                            st.code(reponse['code'], language='python')
                        st.markdown("---")
                else:
                    st.info("Aucune réponse pour le moment. Soyez le premier à aider !")
                
                st.markdown("**➕ Ajouter une réponse**")
                
                auteur_reponse = st.text_input("Votre nom", key=f"auteur_rep_{i}")
                contenu_reponse = st.text_area("Votre réponse", key=f"contenu_rep_{i}", height=100)
                code_reponse = st.text_area("Code (optionnel)", key=f"code_rep_{i}", height=80)
                
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    if st.button("📤 Publier", key=f"publish_rep_{i}"):
                        if auteur_reponse and contenu_reponse:
                            nouvelle_reponse = {
                                'auteur': auteur_reponse,
                                'contenu': contenu_reponse,
                                'code': code_reponse,
                                'date': str(datetime.now().strftime("%Y-%m-%d %H:%M"))
                            }
                            post['reponses'].append(nouvelle_reponse)
                            save_posts(posts)
                            st.success("✅ Réponse publiée !")
                            st.rerun()
                        else:
                            st.error("Nom et contenu requis")
                
                with col2:
                    if not post.get('resolu', False):
                        if st.button("✅ Marquer comme résolu", key=f"resolve_{i}"):
                            post['resolu'] = True
                            save_posts(posts)
                            st.rerun()

with tab2:
    st.header("➕ Poser une Nouvelle Question")
    
    auteur = st.text_input("Votre nom *")
    titre = st.text_input("Titre de la question *", 
                         placeholder="Ex: Comment normaliser des données avec Pandas ?")
    
    matiere = st.selectbox(
        "Matière *",
        ["Python", "Statistiques", "Machine Learning", "SQL", 
         "Mathématiques", "Business Intelligence", "Autre"]
    )
    
    contenu = st.text_area(
        "Décrivez votre question en détail *",
        height=150,
        placeholder="Soyez précis : contexte, ce que vous avez essayé, erreur rencontrée..."
    )
    
    code = st.text_area(
        "Code (optionnel)",
        height=100,
        placeholder="Collez votre code si pertinent"
    )
    
    tags = st.multiselect(
        "Tags (optionnel)",
        ["Débutant", "Intermédiaire", "Avancé", "Urgent", "Projet", "Examen", "TP"]
    )
    
    if st.button("📤 Publier la Question", use_container_width=True):
        if auteur and titre and contenu:
            nouvelle_question = {
                'auteur': auteur,
                'titre': titre,
                'matiere': matiere,
                'contenu': contenu,
                'code': code,
                'tags': tags,
                'date': str(datetime.now().strftime("%Y-%m-%d %H:%M")),
                'resolu': False,
                'reponses': []
            }
            
            posts = load_posts()
            posts.append(nouvelle_question)
            save_posts(posts)
            
            st.success("✅ Question publiée avec succès !")
            st.balloons()
        else:
            st.error("Veuillez remplir tous les champs obligatoires (*)")

with tab3:
    st.header("👥 Recherche de Binômes & Groupes")
    
    st.markdown("**Trouvez des camarades pour vos projets**")
    
    annonces = [
        {
            "auteur": "Marie D.",
            "type": "Recherche binôme",
            "projet": "Projet Kaggle - Prédiction de prix immobiliers",
            "competences": ["Python", "Pandas", "Scikit-learn"],
            "niveau": "B2",
            "contact": "marie.d@example.com"
        },
        {
            "auteur": "Thomas L.",
            "type": "Groupe de révision",
            "projet": "Révisions Stats & Probas pour l'examen",
            "competences": ["Statistiques", "Probabilités"],
            "niveau": "B1",
            "contact": "thomas.l@example.com"
        },
        {
            "auteur": "Sarah K.",
            "type": "Recherche binôme",
            "projet": "Dashboard Streamlit sur données COVID",
            "competences": ["Streamlit", "Plotly", "Python"],
            "niveau": "B2",
            "contact": "sarah.k@example.com"
        }
    ]
    
    for annonce in annonces:
        with st.expander(f"👤 {annonce['auteur']} - {annonce['type']} - Niveau {annonce['niveau']}"):
            st.markdown(f"**Projet :** {annonce['projet']}")
            st.markdown(f"**Compétences recherchées :** {', '.join(annonce['competences'])}")
            st.markdown(f"**Contact :** {annonce['contact']}")
    
    st.markdown("---")
    st.markdown("### ➕ Publier une Annonce")
    
    auteur_annonce = st.text_input("Votre nom")
    type_annonce = st.radio("Type", ["Recherche binôme", "Recherche groupe", "Groupe de révision"])
    projet_annonce = st.text_input("Projet / Objectif")
    competences_annonce = st.text_input("Compétences recherchées", placeholder="Ex: Python, ML, SQL")
    niveau_annonce = st.selectbox("Niveau", ["B1", "B2", "B3"])
    contact_annonce = st.text_input("Contact (email ou Discord)")
    
    if st.button("📤 Publier l'annonce"):
        if auteur_annonce and projet_annonce:
            st.success("✅ Annonce publiée ! (fonctionnalité de démonstration)")
        else:
            st.error("Veuillez remplir les champs obligatoires")
    
    st.markdown("---")
    st.markdown("### 📅 Calendrier des Deadlines Partagées")
    
    deadlines = [
        {"cours": "Python Avancé", "type": "TP", "date": "2026-01-20", "description": "TP sur les classes et POO"},
        {"cours": "Statistiques", "type": "Examen", "date": "2026-01-25", "description": "Examen mi-semestre"},
        {"cours": "Machine Learning", "type": "Projet", "date": "2026-02-01", "description": "Rendu projet classification"},
    ]
    
    for deadline in deadlines:
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            st.markdown(f"**{deadline['cours']}**")
        with col2:
            st.markdown(f"`{deadline['type']}`")
        with col3:
            st.markdown(f"📅 {deadline['date']}")
        
        st.caption(deadline['description'])
        st.markdown("---")
