import streamlit as st
from pathlib import Path
from datetime import datetime
import pandas as pd
from modules.ai_generator import generate_exercises_with_ai, analyze_course_content, test_api_connection
from modules.database import (
    create_course, get_courses, get_course_by_id, update_course_exercises_count,
    create_exercise, get_exercises
)

AI_AVAILABLE = True
DB_AVAILABLE = True

st.title("👨‍🏫 Espace Professeur")
st.markdown("**Uploadez vos cours et générez automatiquement des exercices pour vos étudiants**")

# Indicateur de statut
col1, col2 = st.columns(2)
with col1:
    if AI_AVAILABLE and test_api_connection():
        st.success("✅ IA Gemini 2.5 Flash connectée")
    else:
        st.warning("⚠️ IA non connectée")

with col2:
    if DB_AVAILABLE:
        st.success("✅ Base de données SQLite active")
    else:
        st.error("❌ Base de données indisponible")

# Matières du B1 BDS UCO
MATIERES_B1 = [
    "Algorithmique et Programmation",
    "Compléments de Maths",
    "Exploitation des données",
    "Probabilités",
    "Statistique Descriptive",
    "Statistique Inférentielle",
    "Supports de cours Outils de pilotage 1"
]

def extract_keywords(text):
    """Extrait les mots-clés importants du texte"""
    import re
    keywords = []
    patterns = [
        r'\b(moyenne|médiane|écart-type|variance|corrélation)\b',
        r'\b(probabilité|loi normale|distribution|échantillon)\b',
        r'\b(régression|classification|clustering|modèle)\b',
        r'\b(python|pandas|numpy|matplotlib|sql)\b',
        r'\b(algorithme|fonction|variable|tableau|boucle)\b',
        r'\b(test|hypothèse|p-value|significativité)\b',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        keywords.extend(matches)
    
    return list(set(keywords))[:10]

tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload Cours", "📚 Cours Disponibles", "🎯 Exercices Générés", "👥 Statistiques"])

with tab1:
    st.header("📤 Upload d'un Nouveau Cours")
    
    st.markdown("### Informations du cours")
    
    col1, col2 = st.columns(2)
    
    with col1:
        prof_name = st.text_input("Nom du professeur *", placeholder="Ex: Dr. Martin")
        matiere = st.selectbox("Matière *", MATIERES_B1)
    
    with col2:
        chapitre = st.text_input("Titre du chapitre *", placeholder="Ex: Introduction aux probabilités")
        niveau = st.selectbox("Niveau de difficulté", ["Débutant", "Intermédiaire", "Avancé"])
    
    st.markdown("### Contenu du cours")
    
    upload_method = st.radio("Méthode d'upload", ["📝 Saisir le texte", "📄 Upload fichier"])
    
    course_content = ""
    
    if upload_method == "📝 Saisir le texte":
        course_content = st.text_area(
            "Contenu du cours",
            height=300,
            placeholder="""Saisissez ici le contenu de votre cours...

Exemple :
# Chapitre 1 : Statistique Descriptive

## 1. Mesures de tendance centrale
La moyenne arithmétique est définie par : μ = (1/n) × Σ(xi)
...
"""
        )
    else:
        uploaded_file = st.file_uploader(
            "Choisir un fichier", 
            type=['txt', 'md'],
            help="Formats acceptés : TXT, Markdown"
        )
        
        if uploaded_file:
            course_content = uploaded_file.read().decode('utf-8')
            st.success(f"✅ Fichier chargé : {uploaded_file.name} ({len(course_content)} caractères)")
    
    if course_content:
        st.markdown("### Aperçu du contenu")
        with st.expander("👁️ Voir l'aperçu"):
            st.markdown(course_content[:500] + ("..." if len(course_content) > 500 else ""))
        
        keywords = extract_keywords(course_content)
        if keywords:
            st.info(f"**📌 Mots-clés détectés :** {', '.join(keywords)}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        generate_exercises = st.checkbox("🎯 Générer automatiquement des exercices", value=True)
        if generate_exercises:
            nb_exercises = st.slider("Nombre d'exercices à générer", 2, 10, 5)
    
    with col2:
        visible_students = st.checkbox("👥 Visible par les étudiants", value=True)
    
    if st.button("💾 Enregistrer le cours", type="primary", use_container_width=True):
        if prof_name and matiere and chapitre and course_content:
            course_id = f"{matiere.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            course_data = {
                'course_id': course_id,
                'prof_id': None,
                'prof_name': prof_name,
                'matiere': matiere,
                'chapitre': chapitre,
                'niveau': niveau,
                'content': course_content,
                'keywords': extract_keywords(course_content),
                'visible': visible_students
            }
            
            try:
                db_course_id = create_course(course_data)
                st.success(f"✅ Cours enregistré avec succès ! ID: {course_id}")
                
                if generate_exercises:
                    with st.spinner("🎯 Génération des exercices avec IA en cours..."):
                        if AI_AVAILABLE and test_api_connection():
                            st.info("🤖 Utilisation de Gemini 2.5 Flash...")
                            exercises = generate_exercises_with_ai(
                                course_content=course_content,
                                matiere=matiere,
                                niveau=niveau,
                                nb_exercises=nb_exercises
                            )
                        else:
                            st.warning("⚠️ IA non disponible, pas d'exercices générés")
                            exercises = []
                        
                        if exercises:
                            for i, ex in enumerate(exercises):
                                ex['exercise_id'] = f"{course_id}_ex_{i+1}"
                                ex['matiere'] = matiere
                                ex['niveau'] = niveau
                                create_exercise(ex)
                            
                            update_course_exercises_count(db_course_id, len(exercises))
                            st.success(f"✅ {len(exercises)} exercices générés et sauvegardés !")
                            
                            with st.expander("👁️ Voir les exercices générés"):
                                for i, ex in enumerate(exercises, 1):
                                    st.markdown(f"**Exercice {i} - {ex.get('type', 'N/A')}**")
                                    st.markdown(f"_{ex['question'][:150]}..._")
                                    st.markdown("---")
                        else:
                            st.warning("⚠️ Aucun exercice généré")
                
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la sauvegarde : {e}")
        else:
            st.error("❌ Veuillez remplir tous les champs obligatoires")

with tab2:
    st.header("📚 Cours Disponibles")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        matiere_filter = st.selectbox("Filtrer par matière", ["Toutes"] + MATIERES_B1, key="filter_mat")
    
    with col2:
        courses_list = get_courses()
        prof_names = list(set([c['prof_name'] for c in courses_list]))
        prof_filter = st.selectbox("Filtrer par professeur", ["Tous"] + prof_names)
    
    with col3:
        niveau_filter = st.selectbox("Filtrer par niveau", ["Tous", "Débutant", "Intermédiaire", "Avancé"])
    
    filtered_courses = courses_list
    if matiere_filter != "Toutes":
        filtered_courses = [c for c in filtered_courses if c['matiere'] == matiere_filter]
    if prof_filter != "Tous":
        filtered_courses = [c for c in filtered_courses if c['prof_name'] == prof_filter]
    if niveau_filter != "Tous":
        filtered_courses = [c for c in filtered_courses if c['niveau'] == niveau_filter]
    
    st.markdown(f"**{len(filtered_courses)} cours trouvé(s)**")
    
    for course in filtered_courses:
        with st.expander(f"📖 {course['chapitre']} - {course['matiere']} ({course['prof_name']})"):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**Professeur :** {course['prof_name']}")
                st.markdown(f"**Matière :** {course['matiere']}")
                st.markdown(f"**Niveau :** {course['niveau']}")
            
            with col2:
                date_str = course.get('date_upload', '')
                if date_str:
                    st.markdown(f"**Date :** {date_str[:10]}")
                st.markdown(f"**Visible :** {'✅ Oui' if course.get('visible') else '❌ Non'}")
            
            with col3:
                if course.get('keywords'):
                    st.markdown("**Tags :**")
                    for kw in course['keywords'][:3]:
                        st.markdown(f"- {kw}")
            
            st.markdown("---")
            st.markdown("**Aperçu du contenu :**")
            content = course.get('content', '')
            st.markdown(content[:300] + "..." if len(content) > 300 else content)
            
            col1, col2 = st.columns(2)
            with col1:
                nb_ex = course.get('nb_exercises_generated', 0)
                st.info(f"📝 {nb_ex} exercice(s) généré(s)")
            
            with col2:
                if st.button("📥 Télécharger", key=f"dl_{course['id']}"):
                    st.download_button(
                        label="💾 Télécharger le cours",
                        data=content,
                        file_name=f"{course['chapitre']}.txt",
                        mime="text/plain",
                        key=f"dlbtn_{course['id']}"
                    )

with tab3:
    st.header("🎯 Exercices Générés Automatiquement")
    
    col1, col2 = st.columns(2)
    
    with col1:
        matiere_filter_ex = st.selectbox("Filtrer par matière", ["Toutes"] + MATIERES_B1, key="filter_mat_ex")
    
    with col2:
        type_filter = st.selectbox("Filtrer par type", 
                                  ["Tous", "QCM", "Exercice pratique", "Problème", 
                                   "Code Python", "Débogage", "Pandas", "Exercice de calcul"])
    
    exercises = get_exercises(
        matiere=None if matiere_filter_ex == "Toutes" else matiere_filter_ex,
        exercise_type=None if type_filter == "Tous" else type_filter
    )
    
    st.markdown(f"**{len(exercises)} exercice(s) trouvé(s)**")
    
    for ex in exercises:
        ex_type = ex.get('type', 'Exercice')
        with st.expander(f"🎯 {ex_type} - {ex['matiere']} (Niveau {ex['niveau']})"):
            st.markdown(f"**Question :** {ex['question']}")
            
            if ex.get('type') == 'QCM' and ex.get('options'):
                st.markdown("**Options :**")
                for j, opt in enumerate(ex['options']):
                    prefix = "✅" if j == ex.get('correct_index', -1) else "⬜"
                    st.markdown(f"{prefix} {opt}")
            
            with st.expander("💡 Voir la solution"):
                if ex.get('solution'):
                    st.success(f"**Solution :** {ex['solution']}")
                
                if ex.get('explication'):
                    st.info(f"**Explication :** {ex['explication']}")
                
                if ex.get('concepts'):
                    st.markdown(f"**Concepts :** {', '.join(ex['concepts'])}")
            
            date_str = ex.get('date_creation', '')
            if date_str:
                st.caption(f"📅 Créé le {date_str[:16]} | 🤖 Source: {ex.get('source', 'N/A')}")

with tab4:
    st.header("📊 Statistiques")
    
    courses = get_courses()
    exercises = get_exercises()
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("📚 Cours uploadés", len(courses))
    col2.metric("🎯 Exercices générés", len(exercises))
    col3.metric("👨‍🏫 Professeurs", len(set([c['prof_name'] for c in courses])) if courses else 0)
    col4.metric("📖 Matières couvertes", len(set([c['matiere'] for c in courses])) if courses else 0)
    
    if courses:
        st.markdown("---")
        st.subheader("📊 Répartition par matière")
        
        matiere_counts = {}
        for course in courses:
            mat = course['matiere']
            matiere_counts[mat] = matiere_counts.get(mat, 0) + 1
        
        df_stats = pd.DataFrame(list(matiere_counts.items()), columns=['Matière', 'Nombre de cours'])
        st.bar_chart(df_stats.set_index('Matière'))
    
    if exercises:
        st.markdown("---")
        st.subheader("🎯 Types d'exercices générés")
        
        type_counts = {}
        for ex in exercises:
            ex_type = ex.get('type', 'Autre')
            type_counts[ex_type] = type_counts.get(ex_type, 0) + 1
        
        for ex_type, count in type_counts.items():
            st.markdown(f"- **{ex_type}** : {count} exercices")
