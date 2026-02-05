import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.title("🎲 Générateur de Datasets")
st.markdown("**Créez des données synthétiques pour vous entraîner**")

tab1, tab2, tab3 = st.tabs(["📊 Datasets Prédéfinis", "🛠️ Générateur Personnalisé", "📥 Mes Datasets"])

with tab1:
    st.header("📊 Datasets Prédéfinis")
    
    dataset_type = st.selectbox(
        "Choisissez un type de dataset",
        ["Ventes E-commerce", "Données Clients (CRM)", "Données Médicales", 
         "Données Financières", "Logs Utilisateurs", "Données Marketing"]
    )
    
    n_rows = st.slider("Nombre de lignes", 100, 10000, 1000, 100)
    
    if dataset_type == "Ventes E-commerce":
        st.markdown("**Dataset de ventes e-commerce**")
        st.markdown("Colonnes : date, produit, catégorie, quantité, prix_unitaire, montant_total, client_id, pays")
        
        if st.button("🎲 Générer le dataset"):
            np.random.seed(42)
            
            dates = pd.date_range(end=datetime.now(), periods=n_rows, freq='H')
            
            produits = ['Laptop', 'Smartphone', 'Tablette', 'Écouteurs', 'Clavier', 
                       'Souris', 'Moniteur', 'Webcam', 'Chargeur', 'Câble USB']
            categories = {'Laptop': 'Informatique', 'Smartphone': 'Mobile', 
                         'Tablette': 'Mobile', 'Écouteurs': 'Audio', 
                         'Clavier': 'Accessoires', 'Souris': 'Accessoires',
                         'Moniteur': 'Informatique', 'Webcam': 'Accessoires',
                         'Chargeur': 'Accessoires', 'Câble USB': 'Accessoires'}
            prix = {'Laptop': (500, 2000), 'Smartphone': (300, 1200), 
                   'Tablette': (200, 800), 'Écouteurs': (20, 300),
                   'Clavier': (15, 150), 'Souris': (10, 100),
                   'Moniteur': (150, 800), 'Webcam': (30, 200),
                   'Chargeur': (10, 50), 'Câble USB': (5, 30)}
            
            data = []
            for i in range(n_rows):
                produit = np.random.choice(produits)
                quantite = np.random.randint(1, 5)
                prix_unitaire = round(np.random.uniform(*prix[produit]), 2)
                
                data.append({
                    'date': dates[i],
                    'produit': produit,
                    'categorie': categories[produit],
                    'quantite': quantite,
                    'prix_unitaire': prix_unitaire,
                    'montant_total': round(quantite * prix_unitaire, 2),
                    'client_id': np.random.randint(1, 500),
                    'pays': np.random.choice(['France', 'Belgique', 'Suisse', 'Canada', 'Luxembourg'], 
                                            p=[0.6, 0.15, 0.1, 0.1, 0.05])
                })
            
            df = pd.DataFrame(data)
            
            st.success(f"✅ Dataset généré avec {len(df)} lignes")
            st.dataframe(df.head(20))
            
            st.markdown("### 📊 Aperçu Statistique")
            col1, col2, col3 = st.columns(3)
            col1.metric("CA Total", f"{df['montant_total'].sum():,.0f} €")
            col2.metric("Panier Moyen", f"{df['montant_total'].mean():.2f} €")
            col3.metric("Nb Clients", df['client_id'].nunique())
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Télécharger en CSV",
                data=csv,
                file_name=f"ventes_ecommerce_{n_rows}.csv",
                mime="text/csv"
            )
    
    elif dataset_type == "Données Clients (CRM)":
        st.markdown("**Dataset de clients CRM**")
        st.markdown("Colonnes : client_id, age, sexe, ville, date_inscription, nb_achats, ca_total, segment, churn")
        
        if st.button("🎲 Générer le dataset"):
            np.random.seed(42)
            
            villes = ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice', 'Nantes', 
                     'Strasbourg', 'Bordeaux', 'Lille', 'Rennes']
            
            data = []
            for i in range(n_rows):
                age = int(np.random.normal(40, 15))
                age = max(18, min(80, age))
                
                nb_achats = int(np.random.exponential(5))
                ca_total = round(nb_achats * np.random.uniform(50, 300), 2)
                
                if ca_total > 2000:
                    segment = 'Premium'
                elif ca_total > 500:
                    segment = 'Standard'
                else:
                    segment = 'Bronze'
                
                churn_prob = 0.3 if nb_achats < 2 else 0.1 if segment == 'Premium' else 0.2
                
                data.append({
                    'client_id': 1000 + i,
                    'age': age,
                    'sexe': np.random.choice(['M', 'F']),
                    'ville': np.random.choice(villes),
                    'date_inscription': (datetime.now() - timedelta(days=np.random.randint(1, 1000))).strftime('%Y-%m-%d'),
                    'nb_achats': nb_achats,
                    'ca_total': ca_total,
                    'segment': segment,
                    'churn': np.random.choice([0, 1], p=[1-churn_prob, churn_prob])
                })
            
            df = pd.DataFrame(data)
            
            st.success(f"✅ Dataset généré avec {len(df)} clients")
            st.dataframe(df.head(20))
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Nb Clients", len(df))
            col2.metric("Taux de Churn", f"{df['churn'].mean()*100:.1f}%")
            col3.metric("CA Moyen", f"{df['ca_total'].mean():.2f} €")
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Télécharger en CSV",
                data=csv,
                file_name=f"clients_crm_{n_rows}.csv",
                mime="text/csv"
            )
    
    elif dataset_type == "Données Financières":
        st.markdown("**Dataset de transactions financières**")
        st.markdown("Colonnes : date, montant, type, categorie, compte, fraude")
        
        if st.button("🎲 Générer le dataset"):
            np.random.seed(42)
            
            dates = pd.date_range(end=datetime.now(), periods=n_rows, freq='3H')
            
            types_transaction = ['Achat', 'Retrait', 'Virement', 'Prélèvement', 'Dépôt']
            categories = ['Alimentation', 'Transport', 'Logement', 'Loisirs', 
                         'Santé', 'Shopping', 'Épargne', 'Autre']
            
            data = []
            for i in range(n_rows):
                type_trans = np.random.choice(types_transaction, p=[0.5, 0.2, 0.15, 0.1, 0.05])
                
                if type_trans == 'Achat':
                    montant = round(np.random.exponential(50), 2)
                    categorie = np.random.choice(categories, p=[0.3, 0.15, 0.2, 0.15, 0.05, 0.1, 0.03, 0.02])
                elif type_trans == 'Retrait':
                    montant = round(np.random.choice([20, 50, 100, 200]), 2)
                    categorie = 'Autre'
                elif type_trans == 'Virement':
                    montant = round(np.random.uniform(100, 2000), 2)
                    categorie = 'Autre'
                elif type_trans == 'Prélèvement':
                    montant = round(np.random.uniform(20, 500), 2)
                    categorie = np.random.choice(['Logement', 'Autre'], p=[0.6, 0.4])
                else:
                    montant = round(np.random.uniform(500, 3000), 2)
                    categorie = 'Épargne'
                
                fraude = 1 if (montant > 5000 or (type_trans == 'Retrait' and montant > 500)) and np.random.random() < 0.02 else 0
                
                data.append({
                    'date': dates[i],
                    'montant': montant,
                    'type': type_trans,
                    'categorie': categorie,
                    'compte': f"COMPTE_{np.random.randint(1, 100)}",
                    'fraude': fraude
                })
            
            df = pd.DataFrame(data)
            
            st.success(f"✅ Dataset généré avec {len(df)} transactions")
            st.dataframe(df.head(20))
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Nb Transactions", len(df))
            col2.metric("Montant Total", f"{df['montant'].sum():,.0f} €")
            col3.metric("Taux de Fraude", f"{df['fraude'].mean()*100:.2f}%")
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Télécharger en CSV",
                data=csv,
                file_name=f"transactions_{n_rows}.csv",
                mime="text/csv"
            )

with tab2:
    st.header("🛠️ Générateur Personnalisé")
    
    st.markdown("**Créez votre propre dataset en définissant les colonnes**")
    
    n_rows_custom = st.number_input("Nombre de lignes", min_value=10, max_value=10000, value=100)
    
    st.markdown("### Définir les colonnes")
    
    if 'custom_columns' not in st.session_state:
        st.session_state.custom_columns = []
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        col_name = st.text_input("Nom de la colonne")
    
    with col2:
        col_type = st.selectbox("Type", ["Numérique (int)", "Numérique (float)", "Texte", "Date", "Booléen", "Catégoriel"])
    
    with col3:
        if st.button("➕ Ajouter"):
            if col_name:
                st.session_state.custom_columns.append({'nom': col_name, 'type': col_type})
                st.rerun()
    
    if st.session_state.custom_columns:
        st.markdown("**Colonnes définies :**")
        for i, col in enumerate(st.session_state.custom_columns):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.text(col['nom'])
            with col2:
                st.text(col['type'])
            with col3:
                if st.button("❌", key=f"remove_{i}"):
                    st.session_state.custom_columns.pop(i)
                    st.rerun()
        
        if st.button("🎲 Générer le dataset personnalisé"):
            data = {}
            
            for col in st.session_state.custom_columns:
                if col['type'] == "Numérique (int)":
                    data[col['nom']] = np.random.randint(0, 100, n_rows_custom)
                elif col['type'] == "Numérique (float)":
                    data[col['nom']] = np.round(np.random.uniform(0, 100, n_rows_custom), 2)
                elif col['type'] == "Texte":
                    data[col['nom']] = [f"Text_{i}" for i in range(n_rows_custom)]
                elif col['type'] == "Date":
                    data[col['nom']] = pd.date_range(end=datetime.now(), periods=n_rows_custom, freq='D')
                elif col['type'] == "Booléen":
                    data[col['nom']] = np.random.choice([True, False], n_rows_custom)
                elif col['type'] == "Catégoriel":
                    data[col['nom']] = np.random.choice(['A', 'B', 'C', 'D'], n_rows_custom)
            
            df = pd.DataFrame(data)
            
            st.success(f"✅ Dataset généré avec {len(df)} lignes et {len(df.columns)} colonnes")
            st.dataframe(df.head(20))
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Télécharger en CSV",
                data=csv,
                file_name="dataset_personnalise.csv",
                mime="text/csv"
            )

with tab3:
    st.header("📥 Datasets Sauvegardés")
    
    st.info("💡 Cette section pourrait stocker vos datasets générés pour un accès rapide. (Fonctionnalité à implémenter)")
    
    st.markdown("### Exemples de datasets utiles pour s'entraîner :")
    
    examples = [
        {"nom": "Iris", "description": "Classification de fleurs (150 lignes)", "source": "Scikit-learn"},
        {"nom": "Titanic", "description": "Prédiction de survie (891 lignes)", "source": "Kaggle"},
        {"nom": "California Housing", "description": "Régression prix immobilier (20K lignes)", "source": "Scikit-learn"},
        {"nom": "MNIST", "description": "Reconnaissance de chiffres (60K images)", "source": "TensorFlow"},
    ]
    
    for ex in examples:
        st.markdown(f"**{ex['nom']}** - {ex['description']} - Source: {ex['source']}")
