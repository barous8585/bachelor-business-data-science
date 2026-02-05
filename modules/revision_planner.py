import streamlit as st
import pandas as pd
from datetime import datetime
import random
from modules.database import (
    create_flashcard, get_flashcards, update_flashcard_review,
    get_flashcards_by_matiere
)

DB_AVAILABLE = True

st.title("📚 Planificateur de Révisions")
st.markdown("**Système de répétition espacée pour optimiser votre apprentissage**")

tab1, tab2, tab3, tab4 = st.tabs(["🎴 Réviser", "➕ Créer Flashcards", "📊 Progression", "📚 Bibliothèque"])

with tab1:
    st.header("🎴 Session de Révision")
    
    flashcards = get_flashcards()
    
    if not flashcards:
        st.info("Aucune flashcard disponible. Créez-en dans l'onglet 'Créer Flashcards' !")
    else:
        matieres = list(set([fc['matiere'] for fc in flashcards]))
        matiere_filter = st.selectbox("Choisir la matière", ["Toutes"] + matieres)
        
        if matiere_filter == "Toutes":
            cards_to_review = flashcards
        else:
            cards_to_review = get_flashcards_by_matiere(matiere_filter)
        
        if cards_to_review:
            st.info(f"📚 {len(cards_to_review)} flashcards à réviser")
            
            if 'current_card_index' not in st.session_state:
                st.session_state.current_card_index = 0
                random.shuffle(cards_to_review)
                st.session_state.cards_to_review = cards_to_review
                st.session_state.show_answer = False
            
            if st.session_state.current_card_index < len(st.session_state.cards_to_review):
                current_card = st.session_state.cards_to_review[st.session_state.current_card_index]
                
                st.progress((st.session_state.current_card_index + 1) / len(st.session_state.cards_to_review))
                st.caption(f"Carte {st.session_state.current_card_index + 1} / {len(st.session_state.cards_to_review)}")
                
                st.markdown(f"### 📌 {current_card['matiere']}")
                
                st.markdown("---")
                st.markdown(f"## Question")
                st.markdown(f"### {current_card['question']}")
                
                if not st.session_state.show_answer:
                    if st.button("🔍 Afficher la réponse", use_container_width=True):
                        st.session_state.show_answer = True
                        st.rerun()
                else:
                    st.markdown("---")
                    st.markdown(f"## Réponse")
                    st.success(current_card['reponse'])
                    
                    if current_card.get('explication'):
                        st.info(f"**💡 Explication :** {current_card['explication']}")
                    
                    st.markdown("---")
                    st.markdown("**Comment avez-vous trouvé cette carte ?**")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("❌ Difficile", use_container_width=True):
                            update_flashcard_review(current_card['id'], 'difficile')
                            st.session_state.current_card_index += 1
                            st.session_state.show_answer = False
                            st.rerun()
                    
                    with col2:
                        if st.button("🟡 Moyen", use_container_width=True):
                            update_flashcard_review(current_card['id'], 'moyen')
                            st.session_state.current_card_index += 1
                            st.session_state.show_answer = False
                            st.rerun()
                    
                    with col3:
                        if st.button("✅ Facile", use_container_width=True):
                            update_flashcard_review(current_card['id'], 'facile')
                            st.session_state.current_card_index += 1
                            st.session_state.show_answer = False
                            st.rerun()
            else:
                st.success("🎉 Session terminée ! Bravo !")
                if st.button("🔄 Recommencer"):
                    st.session_state.current_card_index = 0
                    st.rerun()

with tab2:
    st.header("➕ Créer des Flashcards")
    
    matiere = st.selectbox(
        "Matière",
        ["Statistiques", "Probabilités", "Python", "SQL", "Machine Learning", 
         "Mathématiques", "Business Intelligence", "Data Visualization", "Autre"]
    )
    
    if matiere == "Autre":
        matiere = st.text_input("Nom de la matière")
    
    question = st.text_area("Question", height=100, 
                           placeholder="Ex: Quelle est la formule de la variance ?")
    
    reponse = st.text_area("Réponse", height=100,
                          placeholder="Ex: Var(X) = E[(X - μ)²]")
    
    explication = st.text_area("Explication (optionnel)", height=80,
                              placeholder="Contexte ou détails supplémentaires")
    
    if st.button("💾 Créer la flashcard"):
        if question and reponse and matiere:
            flashcard = {
                'matiere': matiere,
                'question': question,
                'reponse': reponse,
                'explication': explication,
                'student_id': None,
                'difficulte': None
            }
            
            try:
                create_flashcard(flashcard)
                st.success("✅ Flashcard créée avec succès !")
            except Exception as e:
                st.error(f"❌ Erreur : {e}")
        else:
            st.error("Veuillez remplir tous les champs obligatoires")

with tab3:
    st.header("📊 Suivi de Progression")
    
    flashcards = get_flashcards()
    
    if not flashcards:
        st.info("Aucune donnée de progression pour le moment")
    else:
        col1, col2, col3, col4 = st.columns(4)
        
        total = len(flashcards)
        revues = len([fc for fc in flashcards if fc.get('dernier_revu')])
        faciles = len([fc for fc in flashcards if fc.get('difficulte') == 'facile'])
        difficiles = len([fc for fc in flashcards if fc.get('difficulte') == 'difficile'])
        
        col1.metric("Total Flashcards", total)
        col2.metric("Déjà révisées", revues)
        col3.metric("Maîtrisées", faciles)
        col4.metric("À retravailler", difficiles)
        
        st.markdown("---")
        
        matiere_counts = pd.DataFrame([
            {'Matière': fc['matiere'], 'Count': 1} 
            for fc in flashcards
        ]).groupby('Matière').count().reset_index()
        
        if not matiere_counts.empty:
            import plotly.express as px
            fig = px.bar(matiere_counts, x='Matière', y='Count', 
                        title='Répartition des flashcards par matière')
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📅 Calendrier de révision")
        st.info("💡 Astuce : Révisez régulièrement pour maximiser la rétention !")

with tab4:
    st.header("📚 Bibliothèque de Flashcards Prédéfinies")
    
    st.markdown("**Importez des sets de flashcards prêts à l'emploi**")
    
    predefined_sets = {
        "Statistiques - Formules de base": [
            {
                "question": "Formule de la moyenne",
                "reponse": "x̄ = (1/n) × Σxᵢ",
                "explication": "Somme de toutes les valeurs divisée par le nombre de valeurs"
            },
            {
                "question": "Formule de la variance",
                "reponse": "s² = (1/(n-1)) × Σ(xᵢ - x̄)²",
                "explication": "Mesure la dispersion des données autour de la moyenne"
            },
            {
                "question": "Formule de l'écart-type",
                "reponse": "s = √(variance)",
                "explication": "Racine carrée de la variance, même unité que les données"
            },
            {
                "question": "Coefficient de corrélation de Pearson",
                "reponse": "r = Cov(X,Y) / (σₓ × σᵧ)",
                "explication": "Mesure la force de la relation linéaire entre deux variables"
            }
        ],
        "Python - Pandas": [
            {
                "question": "Comment lire un fichier CSV ?",
                "reponse": "df = pd.read_csv('fichier.csv')",
                "explication": "Charge les données dans un DataFrame"
            },
            {
                "question": "Comment afficher les 5 premières lignes ?",
                "reponse": "df.head()",
                "explication": "Par défaut affiche 5 lignes, peut être modifié avec head(n)"
            },
            {
                "question": "Comment filtrer les lignes ?",
                "reponse": "df[df['colonne'] > valeur]",
                "explication": "Utilise une condition booléenne pour filtrer"
            },
            {
                "question": "Comment grouper et agréger ?",
                "reponse": "df.groupby('col')['val'].sum()",
                "explication": "Groupe par une colonne et applique une fonction d'agrégation"
            }
        ],
        "Machine Learning - Concepts": [
            {
                "question": "Qu'est-ce que l'overfitting ?",
                "reponse": "Modèle qui apprend trop bien les données d'entraînement et généralise mal",
                "explication": "Le modèle mémorise le bruit au lieu d'apprendre les patterns"
            },
            {
                "question": "Différence entre classification et régression ?",
                "reponse": "Classification: prédire une catégorie. Régression: prédire une valeur numérique",
                "explication": "Classification = sortie discrète, Régression = sortie continue"
            },
            {
                "question": "À quoi sert la validation croisée ?",
                "reponse": "Évaluer la performance du modèle de manière robuste en utilisant plusieurs splits",
                "explication": "Réduit le biais lié au choix du split train/test"
            }
        ]
    }
    
    for set_name, cards in predefined_sets.items():
        with st.expander(f"📦 {set_name} ({len(cards)} cartes)"):
            for card in cards:
                st.markdown(f"**Q:** {card['question']}")
                st.markdown(f"**R:** {card['reponse']}")
                st.caption(card['explication'])
                st.markdown("---")
            
            if st.button(f"📥 Importer ce set", key=f"import_{set_name}"):
                for card in cards:
                    flashcard = {
                        'matiere': set_name.split(' - ')[0],
                        'question': card['question'],
                        'reponse': card['reponse'],
                        'explication': card['explication'],
                        'student_id': None,
                        'difficulte': None
                    }
                    create_flashcard(flashcard)
                
                st.success(f"✅ {len(cards)} flashcards importées !")
