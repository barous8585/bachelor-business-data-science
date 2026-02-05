import streamlit as st
import pandas as pd
from datetime import datetime
from modules.database import (
    create_project, get_projects, get_project_by_id, 
    update_project_status, delete_project,
    add_project_task, update_task_status, delete_task
)

DB_AVAILABLE = True

st.title("📁 Gestionnaire de Projets Data Science")
st.markdown("**Organisez vos projets académiques et personnels**")

tab1, tab2, tab3 = st.tabs(["📊 Mes Projets", "➕ Nouveau Projet", "📚 Templates"])

with tab1:
    st.header("Mes Projets")
    
    projects = get_projects()
    
    if not projects:
        st.info("Aucun projet pour le moment. Créez votre premier projet dans l'onglet 'Nouveau Projet' !")
    else:
        status_filter = st.selectbox("Filtrer par statut", ["Tous", "En cours", "Terminé", "En pause"])
        
        for project in projects:
            if status_filter != "Tous" and project['status'] != status_filter:
                continue
            
            status_color = {
                "En cours": "🟢",
                "Terminé": "✅",
                "En pause": "🟡"
            }
            
            with st.expander(f"{status_color.get(project['status'], '⚪')} {project['nom']} - {project['type']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Description :** {project['description']}")
                    st.markdown(f"**Statut :** {project['status']}")
                    st.markdown(f"**Début :** {project['date_debut'][:10]}")
                    if project.get('date_fin'):
                        st.markdown(f"**Fin :** {project['date_fin'][:10]}")
                
                with col2:
                    st.markdown("**Technologies :**")
                    technologies = project.get('technologies', [])
                    if technologies:
                        for tech in technologies:
                            st.markdown(f"- {tech}")
                
                st.markdown("---")
                st.markdown("**📋 Tâches :**")
                
                tasks = project.get('tasks', [])
                if tasks:
                    for task in tasks:
                        done = "✅" if task.get('done', False) else "⬜"
                        st.markdown(f"{done} {task['nom']}")
                
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                
                with col2:
                    if st.button("🗑️ Supprimer", key=f"delete_{project['id']}"):
                        delete_project(project['id'])
                        st.rerun()
                
                with col3:
                    new_status = st.selectbox(
                        "Changer statut", 
                        ["En cours", "En pause", "Terminé"],
                        index=["En cours", "En pause", "Terminé"].index(project['status']),
                        key=f"status_{project['id']}"
                    )
                    if new_status != project['status']:
                        update_project_status(project['id'], new_status)
                        st.rerun()

with tab2:
    st.header("➕ Créer un Nouveau Projet")
    
    nom = st.text_input("Nom du projet *")
    
    type_projet = st.selectbox(
        "Type de projet",
        ["Projet académique", "Projet personnel", "Kaggle Competition", "Stage/Alternance", "Autre"]
    )
    
    description = st.text_area("Description", height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        date_debut = st.date_input("Date de début")
    with col2:
        status = st.selectbox("Statut", ["En cours", "En pause", "Terminé"])
    
    technologies = st.multiselect(
        "Technologies utilisées",
        ["Python", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", 
         "Matplotlib", "Seaborn", "Plotly", "SQL", "MongoDB", "Streamlit", 
         "Flask", "FastAPI", "Docker", "Git"]
    )
    
    st.markdown("**Tâches du projet**")
    
    if 'task_list' not in st.session_state:
        st.session_state.task_list = []
    
    nouvelle_tache = st.text_input("Ajouter une tâche", key="new_task")
    if st.button("➕ Ajouter tâche"):
        if nouvelle_tache:
            st.session_state.task_list.append({'nom': nouvelle_tache, 'done': False})
            st.rerun()
    
    if st.session_state.task_list:
        st.markdown("**Tâches ajoutées :**")
        for i, tache in enumerate(st.session_state.task_list):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"- {tache['nom']}")
            with col2:
                if st.button("❌", key=f"remove_task_{i}"):
                    st.session_state.task_list.pop(i)
                    st.rerun()
    
    if st.button("💾 Enregistrer le projet"):
        if nom:
            new_project = {
                'nom': nom,
                'type': type_projet,
                'description': description,
                'date_debut': str(date_debut),
                'date_fin': None,
                'status': status,
                'technologies': technologies,
                'student_id': None,
                'tasks': st.session_state.task_list
            }
            
            try:
                create_project(new_project)
                st.success("✅ Projet créé avec succès !")
                st.session_state.task_list = []
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur lors de la création : {e}")
        else:
            st.error("Le nom du projet est obligatoire")

with tab3:
    st.header("📚 Templates de Projets")
    
    templates = [
        {
            "nom": "Analyse Exploratoire de Données (EDA)",
            "description": "Template pour une analyse exploratoire complète",
            "taches": [
                "Chargement et première exploration des données",
                "Nettoyage des données (valeurs manquantes, doublons)",
                "Analyse univariée (distributions, stats descriptives)",
                "Analyse bivariée (corrélations, relations)",
                "Visualisations clés",
                "Rapport de conclusions"
            ],
            "technologies": ["Python", "Pandas", "Matplotlib", "Seaborn"]
        },
        {
            "nom": "Projet de Classification",
            "description": "Pipeline complet de classification supervisée",
            "taches": [
                "Exploration et compréhension des données",
                "Prétraitement et feature engineering",
                "Split train/test et validation",
                "Entraînement de plusieurs modèles",
                "Évaluation et comparaison (metrics, confusion matrix)",
                "Optimisation du meilleur modèle",
                "Interprétation et conclusions"
            ],
            "technologies": ["Python", "Pandas", "Scikit-learn", "Matplotlib"]
        },
        {
            "nom": "Dashboard Interactif",
            "description": "Création d'un tableau de bord avec Streamlit",
            "taches": [
                "Définir les KPIs à afficher",
                "Préparer les données",
                "Créer la structure de navigation",
                "Implémenter les visualisations",
                "Ajouter les filtres interactifs",
                "Tests et déploiement"
            ],
            "technologies": ["Python", "Streamlit", "Plotly", "Pandas"]
        },
        {
            "nom": "Projet de Web Scraping",
            "description": "Collecte et analyse de données web",
            "taches": [
                "Identifier la source et structure HTML",
                "Développer le scraper",
                "Gérer les erreurs et rate limiting",
                "Nettoyer et structurer les données",
                "Stockage (CSV/Database)",
                "Analyse des données collectées"
            ],
            "technologies": ["Python", "BeautifulSoup", "Requests", "Pandas"]
        }
    ]
    
    for template in templates:
        with st.expander(f"📋 {template['nom']}"):
            st.markdown(f"**Description :** {template['description']}")
            
            st.markdown("**Tâches suggérées :**")
            for tache in template['taches']:
                st.markdown(f"- {tache}")
            
            st.markdown(f"**Technologies :** {', '.join(template['technologies'])}")
            
            if st.button(f"📥 Utiliser ce template", key=f"use_template_{template['nom']}"):
                st.session_state.task_list = [{'nom': t, 'done': False} for t in template['taches']]
                st.success("Template chargé ! Allez dans 'Nouveau Projet' pour personnaliser.")
