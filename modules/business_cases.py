import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from modules.database import (
    create_business_case_submission, get_business_case_submissions
)

DB_AVAILABLE = True

st.title("📈 Cas Business Data Science")
st.markdown("**Projets réalistes pour pratiquer vos compétences**")

tab1, tab2, tab3 = st.tabs(["📊 Cas Disponibles", "🎯 Mon Projet", "📝 Soumettre"])

with tab1:
    st.header("Cas d'étude disponibles")
    
    cas_studies = [
        {
            "id": 1,
            "titre": "Analyse des Ventes E-commerce",
            "niveau": "B1",
            "domaine": "Retail",
            "description": "Analysez les données de ventes d'une boutique en ligne pour identifier les tendances et opportunités.",
            "objectifs": [
                "Calculer le CA par mois et par catégorie",
                "Identifier les produits les plus vendus",
                "Analyser le comportement d'achat des clients",
                "Créer des visualisations pertinentes"
            ],
            "competences": ["Pandas", "Visualisation", "Statistiques descriptives"],
            "duree": "2-3 heures"
        },
        {
            "id": 2,
            "titre": "Prédiction du Churn Client",
            "niveau": "B2",
            "domaine": "Télécommunications",
            "description": "Construisez un modèle pour prédire quels clients risquent de quitter l'entreprise.",
            "objectifs": [
                "Explorer et nettoyer les données",
                "Feature engineering",
                "Entraîner plusieurs modèles (Logistic Regression, Random Forest)",
                "Comparer les performances",
                "Proposer des recommandations business"
            ],
            "competences": ["Machine Learning", "Classification", "Feature Engineering"],
            "duree": "4-6 heures"
        },
        {
            "id": 3,
            "titre": "Segmentation Client (RFM)",
            "niveau": "B2",
            "domaine": "Marketing",
            "description": "Segmentez les clients selon leur comportement d'achat (Récence, Fréquence, Montant).",
            "objectifs": [
                "Calculer les métriques RFM",
                "Appliquer le clustering (K-Means)",
                "Visualiser les segments",
                "Proposer des stratégies marketing par segment"
            ],
            "competences": ["Clustering", "Marketing Analytics", "Visualisation"],
            "duree": "3-4 heures"
        },
        {
            "id": 4,
            "titre": "Dashboard de Pilotage RH",
            "niveau": "B1",
            "domaine": "Ressources Humaines",
            "description": "Créez un tableau de bord interactif pour suivre les KPIs RH.",
            "objectifs": [
                "Calculer les KPIs (turnover, absentéisme, etc.)",
                "Créer des graphiques interactifs",
                "Analyser la diversité et l'équité",
                "Identifier les tendances"
            ],
            "competences": ["Dashboarding", "KPIs", "Plotly"],
            "duree": "3-4 heures"
        },
        {
            "id": 5,
            "titre": "Prévision de la Demande",
            "niveau": "B3",
            "domaine": "Supply Chain",
            "description": "Prédisez la demande future pour optimiser les stocks.",
            "objectifs": [
                "Analyser les séries temporelles",
                "Détecter la saisonnalité et tendances",
                "Appliquer des modèles de prévision",
                "Évaluer la précision des prédictions"
            ],
            "competences": ["Time Series", "Forecasting", "ARIMA/Prophet"],
            "duree": "5-7 heures"
        },
        {
            "id": 6,
            "titre": "Analyse de Sentiment Réseaux Sociaux",
            "niveau": "B3",
            "domaine": "Marketing Digital",
            "description": "Analysez les commentaires clients sur les réseaux sociaux.",
            "objectifs": [
                "Nettoyer et prétraiter le texte",
                "Appliquer l'analyse de sentiment",
                "Identifier les thèmes récurrents",
                "Visualiser les insights"
            ],
            "competences": ["NLP", "Text Mining", "Sentiment Analysis"],
            "duree": "4-5 heures"
        }
    ]
    
    niveau_filter = st.selectbox("Filtrer par niveau", ["Tous", "B1", "B2", "B3"], key="cas_filter")
    domaine_filter = st.multiselect("Filtrer par domaine", 
                                     ["Retail", "Télécommunications", "Marketing", 
                                      "Ressources Humaines", "Supply Chain", "Marketing Digital"])
    
    filtered_cases = cas_studies
    if niveau_filter != "Tous":
        filtered_cases = [c for c in filtered_cases if c["niveau"] == niveau_filter]
    if domaine_filter:
        filtered_cases = [c for c in filtered_cases if c["domaine"] in domaine_filter]
    
    for cas in filtered_cases:
        with st.expander(f"📊 {cas['titre']} - {cas['niveau']} - {cas['domaine']}"):
            st.markdown(f"**Description :** {cas['description']}")
            st.markdown(f"**⏱️ Durée estimée :** {cas['duree']}")
            
            st.markdown("**🎯 Objectifs :**")
            for obj in cas['objectifs']:
                st.markdown(f"- {obj}")
            
            st.markdown("**💪 Compétences mobilisées :**")
            st.markdown(", ".join([f"`{c}`" for c in cas['competences']]))
            
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("🚀 Démarrer", key=f"start_{cas['id']}"):
                    st.session_state['current_case'] = cas['id']
                    st.success("Projet sélectionné ! Allez dans l'onglet 'Mon Projet'")

with tab2:
    st.header("🎯 Mon Projet en Cours")
    
    if 'current_case' not in st.session_state:
        st.info("👈 Sélectionnez un cas d'étude dans l'onglet 'Cas Disponibles'")
    else:
        current_case = next((c for c in cas_studies if c['id'] == st.session_state['current_case']), None)
        
        if current_case:
            st.success(f"**Projet actuel :** {current_case['titre']}")
            
            st.markdown("### 📋 Guide étape par étape")
            
            if current_case['id'] == 1:
                st.markdown("#### Étape 1 : Charger et explorer les données")
                st.code("""
import pandas as pd
import numpy as np
import plotly.express as px

# Générer des données d'exemple
np.random.seed(42)
dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
n_rows = 1000

df = pd.DataFrame({
    'date': np.random.choice(dates, n_rows),
    'produit': np.random.choice(['Laptop', 'Smartphone', 'Tablette', 'Écouteurs', 'Souris'], n_rows),
    'categorie': np.random.choice(['Électronique', 'Accessoires'], n_rows),
    'quantite': np.random.randint(1, 10, n_rows),
    'prix_unitaire': np.random.uniform(10, 1000, n_rows),
    'client_id': np.random.randint(1, 200, n_rows)
})

df['montant_total'] = df['quantite'] * df['prix_unitaire']

# Exploration
print(df.info())
print(df.describe())
print(df.head())
                """, language="python")
                
                st.markdown("#### Étape 2 : Analyses")
                st.code("""
# CA par mois
df['mois'] = pd.to_datetime(df['date']).dt.to_period('M')
ca_mensuel = df.groupby('mois')['montant_total'].sum()

# Top produits
top_produits = df.groupby('produit').agg({
    'quantite': 'sum',
    'montant_total': 'sum'
}).sort_values('montant_total', ascending=False)

# Panier moyen
panier_moyen = df.groupby('client_id')['montant_total'].sum().mean()
                """, language="python")
                
                st.markdown("#### Étape 3 : Visualisations")
                st.code("""
# Évolution du CA
fig = px.line(ca_mensuel.reset_index(), 
              x='mois', y='montant_total',
              title='Évolution du CA mensuel')
fig.show()

# Top produits
fig = px.bar(top_produits.reset_index(), 
             x='produit', y='montant_total',
             title='CA par produit')
fig.show()
                """, language="python")
                
                if st.button("💾 Générer le dataset d'exemple"):
                    np.random.seed(42)
                    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
                    n_rows = 1000
                    
                    df_example = pd.DataFrame({
                        'date': np.random.choice(dates, n_rows),
                        'produit': np.random.choice(['Laptop', 'Smartphone', 'Tablette', 'Écouteurs', 'Souris'], n_rows),
                        'categorie': np.random.choice(['Électronique', 'Accessoires'], n_rows),
                        'quantite': np.random.randint(1, 10, n_rows),
                        'prix_unitaire': np.random.uniform(10, 1000, n_rows).round(2),
                        'client_id': np.random.randint(1, 200, n_rows)
                    })
                    
                    df_example['montant_total'] = (df_example['quantite'] * df_example['prix_unitaire']).round(2)
                    
                    csv = df_example.to_csv(index=False)
                    st.download_button(
                        label="📥 Télécharger le CSV",
                        data=csv,
                        file_name="ventes_ecommerce.csv",
                        mime="text/csv"
                    )
                    
                    st.dataframe(df_example.head(10))
            
            elif current_case['id'] == 2:
                st.markdown("#### Guide pour le Churn Prediction")
                st.code("""
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# 1. Préparation des données
# - Gérer les valeurs manquantes
# - Encoder les variables catégorielles
# - Normaliser les features numériques

# 2. Feature Engineering
# - Créer des features dérivées (ex: ancienneté, usage moyen)
# - Sélectionner les features pertinentes

# 3. Modélisation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

models = {
    'Logistic': LogisticRegression(),
    'RandomForest': RandomForestClassifier()
}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"{name} - AUC: {roc_auc_score(y_test, y_pred):.3f}")
                """, language="python")
            
            st.markdown("---")
            st.markdown("### ✅ Checklist de progression")
            
            checklist_items = current_case['objectifs']
            for i, item in enumerate(checklist_items):
                checked = st.checkbox(item, key=f"check_{current_case['id']}_{i}")

with tab3:
    st.header("📝 Soumettre votre Travail")
    
    if not DB_AVAILABLE:
        st.warning("⚠️ Base de données non disponible - Soumission désactivée")
    else:
        st.markdown("**Partagez votre projet avec la communauté UCO Data Science**")
        
        nom = st.text_input("Votre nom")
        titre_projet = st.text_input("Titre du projet")
        niveau = st.selectbox("Niveau", ["B1", "B2", "B3"])
        
        description = st.text_area("Description de votre approche", height=150)
        
        resultats = st.text_area("Principaux résultats et insights", height=150)
        
        code_file = st.file_uploader("Upload votre notebook (.ipynb) ou script (.py)", type=['ipynb', 'py'])
        
        if st.button("📤 Soumettre"):
            if nom and titre_projet and description:
                submission = {
                    'student_id': None,
                    'case_id': st.session_state.get('current_case', 1),
                    'titre': titre_projet,
                    'description': description,
                    'resultats': resultats,
                    'niveau': niveau
                }
                
                try:
                    create_business_case_submission(submission)
                    st.success("✅ Projet soumis avec succès ! Merci pour votre contribution.")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Erreur lors de la soumission : {e}")
            else:
                st.error("Veuillez remplir tous les champs obligatoires")
