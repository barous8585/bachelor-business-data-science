import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import pandas as pd
import re

# Importer le module IA
try:
    from modules.ai_generator import generate_exercises_with_ai, analyze_course_content, test_api_connection
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    st.warning("⚠️ Module IA non disponible. Génération basique activée.")

st.title("👨‍🏫 Espace Professeur")
st.markdown("**Uploadez vos cours et générez automatiquement des exercices pour vos étudiants**")

# Indicateur de statut IA
if AI_AVAILABLE:
    ia_status = test_api_connection()
    if ia_status:
        st.success("✅ IA Gemini 2.5 Flash connectée - Génération intelligente activée ! 🚀")
    else:
        st.warning("⚠️ IA non connectée - Génération basique activée")
else:
    st.info("ℹ️ Module IA non disponible - Génération basique activée")

DATA_DIR = Path("data/courses")
DATA_DIR.mkdir(parents=True, exist_ok=True)

EXERCISES_DIR = Path("data/exercises")
EXERCISES_DIR.mkdir(parents=True, exist_ok=True)

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

def load_courses():
    courses_file = DATA_DIR / "courses_list.json"
    if courses_file.exists():
        with open(courses_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_courses(courses):
    courses_file = DATA_DIR / "courses_list.json"
    with open(courses_file, 'w', encoding='utf-8') as f:
        json.dump(courses, f, ensure_ascii=False, indent=2)

def load_exercises():
    exercises_file = EXERCISES_DIR / "exercises_list.json"
    if exercises_file.exists():
        with open(exercises_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_exercises(exercises):
    exercises_file = EXERCISES_DIR / "exercises_list.json"
    with open(exercises_file, 'w', encoding='utf-8') as f:
        json.dump(exercises, f, ensure_ascii=False, indent=2)

def extract_keywords(text):
    """Extrait les mots-clés importants du texte"""
    # Mots-clés techniques communs en data science
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

def generate_exercises_from_course(course_content, matiere, niveau_difficulte):
    """Génère automatiquement des exercices basés sur le contenu du cours"""
    exercises = []
    
    keywords = extract_keywords(course_content)
    
    # Templates d'exercices selon la matière
    if "Statistique" in matiere:
        exercises.append({
            "type": "QCM",
            "question": f"Quelle est la formule correcte pour calculer la {keywords[0] if keywords else 'moyenne'} ?",
            "options": [
                "Σ(xi) / n",
                "Σ(xi - μ)² / n",
                "√(variance)",
                "Cov(X,Y) / (σx × σy)"
            ],
            "correct": 0,
            "explication": "La moyenne arithmétique est la somme des valeurs divisée par le nombre de valeurs."
        })
        
        exercises.append({
            "type": "Exercice pratique",
            "question": "Calculez la moyenne et l'écart-type du dataset suivant : [10, 15, 20, 25, 30]",
            "solution": "Moyenne = 20, Écart-type ≈ 7.07",
            "etapes": [
                "1. Calculer la moyenne : (10+15+20+25+30)/5 = 20",
                "2. Calculer les écarts : (10-20)², (15-20)², ...",
                "3. Calculer la variance : moyenne des carrés des écarts",
                "4. Écart-type = √variance"
            ]
        })
    
    elif "Probabilité" in matiere:
        exercises.append({
            "type": "QCM",
            "question": "Quelle est la probabilité d'obtenir un 6 en lançant un dé équilibré ?",
            "options": ["1/6", "1/3", "1/2", "1/12"],
            "correct": 0,
            "explication": "Un dé a 6 faces équiprobables, donc P(6) = 1/6"
        })
        
        exercises.append({
            "type": "Problème",
            "question": "On tire 2 cartes dans un jeu de 52 cartes. Quelle est la probabilité d'obtenir 2 as ?",
            "solution": "P = (4/52) × (3/51) ≈ 0.0045",
            "explication": "Tirage sans remise : 4 as sur 52 cartes, puis 3 as sur 51 cartes restantes"
        })
    
    elif "Programmation" in matiere or "Algorithmique" in matiere:
        exercises.append({
            "type": "Code Python",
            "question": "Écrivez une fonction qui calcule la factorielle d'un nombre",
            "solution": """def factorielle(n):
    if n <= 1:
        return 1
    return n * factorielle(n-1)""",
            "test_cases": [
                "factorielle(5) devrait retourner 120",
                "factorielle(0) devrait retourner 1"
            ]
        })
        
        exercises.append({
            "type": "Débogage",
            "question": "Trouvez et corrigez l'erreur dans ce code",
            "code_erreur": """def moyenne(liste):
    somme = 0
    for i in range(liste):
        somme += liste[i]
    return somme / len(liste)""",
            "correction": "range(liste) devrait être range(len(liste))",
            "explication": "range() nécessite un entier, pas une liste"
        })
    
    elif "Exploitation des données" in matiere:
        exercises.append({
            "type": "Pandas",
            "question": "Comment filtrer un DataFrame pandas pour garder seulement les lignes où 'age' > 18 ?",
            "options": [
                "df[df['age'] > 18]",
                "df.filter('age' > 18)",
                "df.select(age > 18)",
                "df.where('age' > 18)"
            ],
            "correct": 0,
            "explication": "On utilise l'indexation booléenne avec df[condition]"
        })
    
    # Ajouter des métadonnées
    for i, ex in enumerate(exercises):
        ex['id'] = f"{matiere.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}_{i}"
        ex['matiere'] = matiere
        ex['niveau'] = niveau_difficulte
        ex['date_creation'] = str(datetime.now().strftime('%Y-%m-%d %H:%M'))
        ex['keywords'] = keywords[:3]
    
    return exercises

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

La moyenne arithmétique est définie par :
μ = (1/n) × Σ(xi)

Propriétés :
- Sensible aux valeurs extrêmes
- Facile à calculer
- Utilisée pour les données quantitatives

## 2. Mesures de dispersion

L'écart-type mesure la dispersion autour de la moyenne...
"""
        )
    else:
        uploaded_file = st.file_uploader(
            "Choisir un fichier", 
            type=['txt', 'md', 'pdf', 'docx'],
            help="Formats acceptés : TXT, Markdown, PDF, Word"
        )
        
        if uploaded_file:
            if uploaded_file.type == "text/plain":
                course_content = uploaded_file.read().decode('utf-8')
                st.success(f"✅ Fichier chargé : {uploaded_file.name} ({len(course_content)} caractères)")
            elif uploaded_file.name.endswith('.md'):
                course_content = uploaded_file.read().decode('utf-8')
                st.success(f"✅ Fichier Markdown chargé : {uploaded_file.name}")
            else:
                st.warning("⚠️ Type de fichier non supporté pour le moment. Utilisez TXT ou MD.")
    
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
    
    if st.button("💾 Enregistrer le cours", type="primary", width="stretch"):
        if prof_name and matiere and chapitre and course_content:
            # Sauvegarder le cours
            course_id = f"{matiere.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            course_data = {
                'id': course_id,
                'prof': prof_name,
                'matiere': matiere,
                'chapitre': chapitre,
                'niveau': niveau,
                'content': course_content,
                'date_upload': str(datetime.now().strftime('%Y-%m-%d %H:%M')),
                'visible': visible_students,
                'keywords': extract_keywords(course_content)
            }
            
            # Sauvegarder le fichier du cours
            course_file = DATA_DIR / f"{course_id}.json"
            with open(course_file, 'w', encoding='utf-8') as f:
                json.dump(course_data, f, ensure_ascii=False, indent=2)
            
            # Ajouter à la liste des cours
            courses = load_courses()
            courses.append(course_data)
            save_courses(courses)
            
            st.success(f"✅ Cours enregistré avec succès ! ID: {course_id}")
            
            # Générer les exercices
            if generate_exercises:
                with st.spinner("🎯 Génération des exercices avec IA en cours..."):
                    # Utiliser l'IA si disponible, sinon méthode basique
                    if AI_AVAILABLE and test_api_connection():
                        st.info("🤖 Utilisation de Gemini 2.5 Flash pour la génération...")
                        exercises = generate_exercises_with_ai(
                            course_content=course_content,
                            matiere=matiere,
                            niveau=niveau,
                            nb_exercises=nb_exercises
                        )
                    else:
                        st.info("📝 Utilisation de la génération basique...")
                        exercises = generate_exercises_from_course(course_content, matiere, niveau)
                    
                    # Sauvegarder les exercices
                    all_exercises = load_exercises()
                    for ex in exercises:
                        ex['course_id'] = course_id
                    all_exercises.extend(exercises)
                    save_exercises(all_exercises)
                    
                    st.success(f"✅ {len(exercises)} exercices générés automatiquement !")
                    
                    with st.expander("👁️ Voir les exercices générés"):
                        for i, ex in enumerate(exercises, 1):
                            st.markdown(f"**Exercice {i} - {ex['type']}**")
                            st.markdown(f"_{ex['question']}_")
                            st.markdown("---")
            
            st.balloons()
        else:
            st.error("❌ Veuillez remplir tous les champs obligatoires")

with tab2:
    st.header("📚 Cours Disponibles")
    
    courses = load_courses()
    
    if not courses:
        st.info("Aucun cours uploadé pour le moment. Commencez par uploader un cours dans l'onglet 'Upload Cours' !")
    else:
        # Filtres
        col1, col2, col3 = st.columns(3)
        
        with col1:
            matiere_filter = st.selectbox("Filtrer par matière", ["Toutes"] + MATIERES_B1, key="filter_mat")
        
        with col2:
            prof_filter = st.selectbox("Filtrer par professeur", 
                                       ["Tous"] + list(set([c['prof'] for c in courses])))
        
        with col3:
            niveau_filter = st.selectbox("Filtrer par niveau", 
                                         ["Tous", "Débutant", "Intermédiaire", "Avancé"])
        
        # Appliquer les filtres
        filtered_courses = courses
        if matiere_filter != "Toutes":
            filtered_courses = [c for c in filtered_courses if c['matiere'] == matiere_filter]
        if prof_filter != "Tous":
            filtered_courses = [c for c in filtered_courses if c['prof'] == prof_filter]
        if niveau_filter != "Tous":
            filtered_courses = [c for c in filtered_courses if c['niveau'] == niveau_filter]
        
        st.markdown(f"**{len(filtered_courses)} cours trouvé(s)**")
        
        for course in filtered_courses:
            with st.expander(f"📖 {course['chapitre']} - {course['matiere']} ({course['prof']})"):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**Professeur :** {course['prof']}")
                    st.markdown(f"**Matière :** {course['matiere']}")
                    st.markdown(f"**Niveau :** {course['niveau']}")
                
                with col2:
                    st.markdown(f"**Date :** {course['date_upload']}")
                    st.markdown(f"**Visible :** {'✅ Oui' if course['visible'] else '❌ Non'}")
                
                with col3:
                    if course.get('keywords'):
                        st.markdown("**Tags :**")
                        for kw in course['keywords'][:5]:
                            st.markdown(f"- {kw}")
                
                st.markdown("---")
                st.markdown("**Contenu :**")
                st.markdown(course['content'][:300] + "..." if len(course['content']) > 300 else course['content'])
                
                if st.button("📥 Télécharger", key=f"dl_{course['id']}"):
                    st.download_button(
                        label="💾 Télécharger le cours complet",
                        data=course['content'],
                        file_name=f"{course['chapitre']}.txt",
                        mime="text/plain",
                        key=f"dlbtn_{course['id']}"
                    )

with tab3:
    st.header("🎯 Exercices Générés Automatiquement")
    
    exercises = load_exercises()
    
    if not exercises:
        st.info("Aucun exercice généré pour le moment. Les exercices sont créés automatiquement lors de l'upload d'un cours.")
    else:
        # Filtres
        col1, col2 = st.columns(2)
        
        with col1:
            matiere_filter_ex = st.selectbox("Filtrer par matière", 
                                            ["Toutes"] + MATIERES_B1, 
                                            key="filter_mat_ex")
        
        with col2:
            type_filter = st.selectbox("Filtrer par type", 
                                      ["Tous", "QCM", "Exercice pratique", "Problème", 
                                       "Code Python", "Débogage", "Pandas"])
        
        # Appliquer les filtres
        filtered_exercises = exercises
        if matiere_filter_ex != "Toutes":
            filtered_exercises = [e for e in filtered_exercises if e['matiere'] == matiere_filter_ex]
        if type_filter != "Tous":
            filtered_exercises = [e for e in filtered_exercises if e.get('type') == type_filter]
        
        st.markdown(f"**{len(filtered_exercises)} exercice(s) trouvé(s)**")
        
        for i, ex in enumerate(filtered_exercises):
            with st.expander(f"🎯 {ex.get('type', 'Exercice')} - {ex['matiere']} (Niveau {ex['niveau']})"):
                st.markdown(f"**Question :** {ex['question']}")
                
                if ex.get('type') == 'QCM' and ex.get('options'):
                    st.markdown("**Options :**")
                    for j, opt in enumerate(ex['options']):
                        prefix = "✅" if j == ex.get('correct', -1) else "⬜"
                        st.markdown(f"{prefix} {opt}")
                
                with st.expander("💡 Voir la solution"):
                    if ex.get('solution'):
                        st.success(f"**Solution :** {ex['solution']}")
                    
                    if ex.get('explication'):
                        st.info(f"**Explication :** {ex['explication']}")
                    
                    if ex.get('etapes'):
                        st.markdown("**Étapes de résolution :**")
                        for etape in ex['etapes']:
                            st.markdown(f"- {etape}")
                    
                    if ex.get('code_erreur'):
                        st.code(ex['code_erreur'], language='python')
                        st.markdown(f"**Correction :** {ex.get('correction')}")
                
                st.caption(f"📅 Créé le {ex['date_creation']} | 🔖 Tags: {', '.join(ex.get('keywords', []))}")

with tab4:
    st.header("📊 Statistiques")
    
    courses = load_courses()
    exercises = load_exercises()
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("📚 Cours uploadés", len(courses))
    col2.metric("🎯 Exercices générés", len(exercises))
    col3.metric("👨‍🏫 Professeurs", len(set([c['prof'] for c in courses])) if courses else 0)
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
