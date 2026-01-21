import streamlit as st
import json
from pathlib import Path

st.title("🔗 Bibliothèque de Ressources")
st.markdown("**Tutoriels, datasets et documentation pour Data Science**")

tab1, tab2, tab3, tab4 = st.tabs(["📖 Tutoriels", "📊 Datasets", "📚 Documentation", "🎥 Vidéos"])

with tab1:
    st.header("📖 Tutoriels Recommandés")
    
    categories = st.radio(
        "Catégorie",
        ["Python", "Data Analysis", "Machine Learning", "Visualisation", "SQL", "Tous"],
        horizontal=True
    )
    
    tutorials = [
        {
            "titre": "Python pour la Data Science - Guide Complet",
            "categorie": "Python",
            "niveau": "Débutant",
            "url": "https://www.python.org/about/gettingstarted/",
            "description": "Introduction complète à Python avec focus Data Science"
        },
        {
            "titre": "Pandas - 10 minutes to pandas",
            "categorie": "Data Analysis",
            "niveau": "Débutant",
            "url": "https://pandas.pydata.org/docs/user_guide/10min.html",
            "description": "Guide rapide officiel de Pandas"
        },
        {
            "titre": "Scikit-learn Tutorial",
            "categorie": "Machine Learning",
            "niveau": "Intermédiaire",
            "url": "https://scikit-learn.org/stable/tutorial/index.html",
            "description": "Tutoriel officiel de scikit-learn pour le ML"
        },
        {
            "titre": "Plotly Express Guide",
            "categorie": "Visualisation",
            "niveau": "Débutant",
            "url": "https://plotly.com/python/plotly-express/",
            "description": "Créer des visualisations interactives rapidement"
        },
        {
            "titre": "SQL Tutorial",
            "categorie": "SQL",
            "niveau": "Débutant",
            "url": "https://www.w3schools.com/sql/",
            "description": "Apprenez SQL de A à Z"
        },
        {
            "titre": "Kaggle Learn",
            "categorie": "Machine Learning",
            "niveau": "Tous",
            "url": "https://www.kaggle.com/learn",
            "description": "Micro-cours gratuits sur divers sujets de Data Science"
        }
    ]
    
    filtered = tutorials if categories == "Tous" else [t for t in tutorials if t['categorie'] == categories]
    
    for tuto in filtered:
        with st.expander(f"📘 {tuto['titre']} - {tuto['niveau']}"):
            st.markdown(f"**Catégorie :** {tuto['categorie']}")
            st.markdown(f"**Niveau :** {tuto['niveau']}")
            st.markdown(f"**Description :** {tuto['description']}")
            st.markdown(f"🔗 [Accéder au tutoriel]({tuto['url']})")

with tab2:
    st.header("📊 Datasets pour Pratiquer")
    
    domaine = st.selectbox(
        "Domaine",
        ["Tous", "E-commerce", "Finance", "Santé", "Marketing", "Général"]
    )
    
    datasets = [
        {
            "nom": "Iris Dataset",
            "domaine": "Général",
            "description": "Dataset classique de classification (150 fleurs, 4 features)",
            "use_case": "Classification, clustering",
            "source": "Scikit-learn",
            "code": """
from sklearn.datasets import load_iris
import pandas as pd

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['species'] = iris.target
            """
        },
        {
            "nom": "Titanic Dataset",
            "domaine": "Général",
            "description": "Prédire la survie des passagers du Titanic",
            "use_case": "Classification binaire, feature engineering",
            "source": "Kaggle",
            "code": """
import pandas as pd

url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'
df = pd.read_csv(url)
            """
        },
        {
            "nom": "Online Retail Dataset",
            "domaine": "E-commerce",
            "description": "Transactions e-commerce (500K+ lignes)",
            "use_case": "RFM analysis, market basket analysis",
            "source": "UCI ML Repository",
            "code": """
import pandas as pd

url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx'
df = pd.read_excel(url)
            """
        },
        {
            "nom": "California Housing",
            "domaine": "Finance",
            "description": "Prix des maisons en Californie",
            "use_case": "Régression, feature engineering",
            "source": "Scikit-learn",
            "code": """
from sklearn.datasets import fetch_california_housing
import pandas as pd

housing = fetch_california_housing()
df = pd.DataFrame(housing.data, columns=housing.feature_names)
df['price'] = housing.target
            """
        },
        {
            "nom": "Advertising Dataset",
            "domaine": "Marketing",
            "description": "Budget publicitaire vs ventes",
            "use_case": "Régression linéaire, analyse marketing",
            "source": "Public",
            "code": """
import pandas as pd

url = 'https://www.statlearning.com/s/Advertising.csv'
df = pd.read_csv(url)
            """
        }
    ]
    
    filtered_datasets = datasets if domaine == "Tous" else [d for d in datasets if d['domaine'] == domaine]
    
    for dataset in filtered_datasets:
        with st.expander(f"📊 {dataset['nom']} - {dataset['domaine']}"):
            st.markdown(f"**Description :** {dataset['description']}")
            st.markdown(f"**Use case :** {dataset['use_case']}")
            st.markdown(f"**Source :** {dataset['source']}")
            st.markdown("**Code pour charger :**")
            st.code(dataset['code'], language='python')

with tab3:
    st.header("📚 Documentation Officielle")
    
    docs = [
        {
            "nom": "Python",
            "logo": "🐍",
            "url": "https://docs.python.org/3/",
            "description": "Documentation officielle Python"
        },
        {
            "nom": "Pandas",
            "logo": "🐼",
            "url": "https://pandas.pydata.org/docs/",
            "description": "Manipulation et analyse de données"
        },
        {
            "nom": "NumPy",
            "logo": "🔢",
            "url": "https://numpy.org/doc/",
            "description": "Calcul scientifique et tableaux multidimensionnels"
        },
        {
            "nom": "Matplotlib",
            "logo": "📊",
            "url": "https://matplotlib.org/stable/contents.html",
            "description": "Visualisation de données"
        },
        {
            "nom": "Seaborn",
            "logo": "🎨",
            "url": "https://seaborn.pydata.org/",
            "description": "Visualisation statistique"
        },
        {
            "nom": "Plotly",
            "logo": "📈",
            "url": "https://plotly.com/python/",
            "description": "Graphiques interactifs"
        },
        {
            "nom": "Scikit-learn",
            "logo": "🤖",
            "url": "https://scikit-learn.org/stable/",
            "description": "Machine Learning"
        },
        {
            "nom": "TensorFlow",
            "logo": "🧠",
            "url": "https://www.tensorflow.org/api_docs",
            "description": "Deep Learning"
        },
        {
            "nom": "Streamlit",
            "logo": "🚀",
            "url": "https://docs.streamlit.io/",
            "description": "Applications web pour Data Science"
        },
        {
            "nom": "SQL",
            "logo": "🗄️",
            "url": "https://www.postgresql.org/docs/",
            "description": "PostgreSQL Documentation"
        }
    ]
    
    col1, col2 = st.columns(2)
    
    for i, doc in enumerate(docs):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
                <h3 style='color: white; margin: 0;'>{doc['logo']} {doc['nom']}</h3>
                <p style='color: white; margin: 0.5rem 0;'>{doc['description']}</p>
                <a href='{doc['url']}' target='_blank' 
                   style='color: white; text-decoration: underline;'>📖 Accéder à la doc</a>
            </div>
            """, unsafe_allow_html=True)

with tab4:
    st.header("🎥 Chaînes YouTube Recommandées")
    
    channels = [
        {
            "nom": "StatQuest with Josh Starmer",
            "description": "Statistiques et ML expliqués simplement",
            "url": "https://www.youtube.com/@statquest",
            "focus": "Stats, ML, Concepts"
        },
        {
            "nom": "3Blue1Brown",
            "description": "Mathématiques visuelles et intuitives",
            "url": "https://www.youtube.com/@3blue1brown",
            "focus": "Maths, Algèbre linéaire, NN"
        },
        {
            "nom": "Sentdex",
            "description": "Python et Machine Learning pratique",
            "url": "https://www.youtube.com/@sentdex",
            "focus": "Python, ML, Trading"
        },
        {
            "nom": "Krish Naik",
            "description": "Data Science et ML de A à Z",
            "url": "https://www.youtube.com/@krishnaik06",
            "focus": "DS, ML, Projets"
        },
        {
            "nom": "Ken Jee",
            "description": "Carrière en Data Science",
            "url": "https://www.youtube.com/@KenJee_ds",
            "focus": "Projets, Portfolio, Conseils"
        },
        {
            "nom": "Corey Schafer",
            "description": "Tutoriels Python de qualité",
            "url": "https://www.youtube.com/@coreyms",
            "focus": "Python, Web, Best practices"
        }
    ]
    
    for channel in channels:
        with st.expander(f"🎬 {channel['nom']}"):
            st.markdown(f"**Description :** {channel['description']}")
            st.markdown(f"**Focus :** {channel['focus']}")
            st.markdown(f"🔗 [Accéder à la chaîne]({channel['url']})")
    
    st.markdown("---")
    st.markdown("### 💡 Conseils")
    st.info("""
    - **Pratiquez en même temps** que vous regardez les tutoriels
    - **Prenez des notes** sur les concepts clés
    - **Refaites les projets** avec vos propres données
    - **Activez les sous-titres** pour mieux comprendre (en anglais)
    - **Utilisez la vitesse 1.25x ou 1.5x** si vous êtes à l'aise
    """)
