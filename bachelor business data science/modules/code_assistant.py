import streamlit as st
import json
from pathlib import Path

st.title("💻 Assistant Code & Debug")
st.markdown("**Aide au débogage et snippets de code Python/SQL**")

tab1, tab2, tab3, tab4 = st.tabs(["🐛 Analyseur d'Erreurs", "📚 Bibliothèque de Snippets", "🎯 Quiz Python", "💡 Bonnes Pratiques"])

with tab1:
    st.header("Analyseur d'Erreurs Python")
    
    st.markdown("**Collez votre message d'erreur ci-dessous pour obtenir une explication détaillée :**")
    
    error_input = st.text_area("Message d'erreur", height=150, placeholder="Exemple: IndexError: list index out of range")
    
    if st.button("Analyser l'erreur"):
        error_explanations = {
            "IndexError": {
                "titre": "IndexError - Indice hors limites",
                "explication": "Cette erreur survient lorsque vous essayez d'accéder à un indice qui n'existe pas dans une liste, tuple ou chaîne.",
                "exemple": """```python
# ❌ Erreur
ma_liste = [1, 2, 3]
print(ma_liste[5])  # IndexError!

# ✅ Solution
if len(ma_liste) > 5:
    print(ma_liste[5])
else:
    print("Indice inexistant")
```""",
                "conseils": ["Vérifiez la longueur avec len()", "Utilisez des conditions", "Pensez à la méthode .get() pour les dictionnaires"]
            },
            "KeyError": {
                "titre": "KeyError - Clé inexistante",
                "explication": "Cette erreur apparaît quand vous cherchez une clé qui n'existe pas dans un dictionnaire.",
                "exemple": """```python
# ❌ Erreur
mon_dict = {'nom': 'Jean', 'age': 25}
print(mon_dict['ville'])  # KeyError!

# ✅ Solution 1: get()
print(mon_dict.get('ville', 'Non spécifié'))

# ✅ Solution 2: vérification
if 'ville' in mon_dict:
    print(mon_dict['ville'])
```""",
                "conseils": ["Utilisez .get() avec une valeur par défaut", "Vérifiez avec 'in'", "Utilisez .keys() pour lister les clés"]
            },
            "TypeError": {
                "titre": "TypeError - Type incompatible",
                "explication": "L'opération n'est pas supportée pour ce type de données.",
                "exemple": """```python
# ❌ Erreur
resultat = "5" + 10  # TypeError!

# ✅ Solution
resultat = int("5") + 10  # ou str(10)
print(resultat)  # 15
```""",
                "conseils": ["Vérifiez les types avec type()", "Convertissez avec int(), str(), float()", "Utilisez isinstance() pour vérifier"]
            },
            "ValueError": {
                "titre": "ValueError - Valeur inappropriée",
                "explication": "La valeur n'est pas appropriée pour l'opération même si le type est correct.",
                "exemple": """```python
# ❌ Erreur
nombre = int("abc")  # ValueError!

# ✅ Solution
try:
    nombre = int(input("Entrez un nombre: "))
except ValueError:
    print("Veuillez entrer un nombre valide")
    nombre = 0
```""",
                "conseils": ["Utilisez try/except", "Validez les entrées utilisateur", "Vérifiez le format des données"]
            },
            "AttributeError": {
                "titre": "AttributeError - Attribut inexistant",
                "explication": "L'objet n'a pas l'attribut ou la méthode demandée.",
                "exemple": """```python
# ❌ Erreur
ma_liste = [1, 2, 3]
ma_liste.append(4)  # OK
ma_liste.push(5)  # AttributeError! (push n'existe pas)

# ✅ Solution
ma_liste.append(5)  # Utilisez la bonne méthode
```""",
                "conseils": ["Vérifiez la documentation", "Utilisez dir(objet) pour lister les attributs", "Attention aux typos"]
            },
            "ImportError": {
                "titre": "ImportError / ModuleNotFoundError",
                "explication": "Le module ou package n'a pas pu être importé.",
                "exemple": """```python
# ❌ Erreur
import pandas  # ModuleNotFoundError!

# ✅ Solution: Installer d'abord
# pip install pandas
import pandas as pd
```""",
                "conseils": ["Installez avec pip install", "Vérifiez l'orthographe du module", "Utilisez des environnements virtuels"]
            }
        }
        
        detected = False
        for error_type, info in error_explanations.items():
            if error_type.lower() in error_input.lower():
                detected = True
                st.error(f"### {info['titre']}")
                st.markdown(f"**Explication :** {info['explication']}")
                st.markdown("**Exemple :**")
                st.markdown(info['exemple'])
                st.markdown("**Conseils :**")
                for conseil in info['conseils']:
                    st.markdown(f"- {conseil}")
                break
        
        if not detected and error_input:
            st.info("💡 **Conseils généraux de débogage :**")
            st.markdown("""
            1. **Lisez attentivement le message d'erreur** - Il indique souvent la ligne et le type d'erreur
            2. **Vérifiez les types de données** - Utilisez `type()` et `print()` pour debugger
            3. **Utilisez try/except** - Pour gérer les erreurs de manière élégante
            4. **Ajoutez des prints** - Pour suivre l'exécution de votre code
            5. **Consultez la documentation** - Python docs, Stack Overflow
            """)

with tab2:
    st.header("Bibliothèque de Snippets")
    
    category = st.selectbox(
        "Catégorie",
        ["Pandas", "NumPy", "Matplotlib/Plotly", "Scikit-learn", "SQL", "Statistiques"]
    )
    
    if category == "Pandas":
        st.subheader("🐼 Snippets Pandas")
        
        with st.expander("📥 Charger des données"):
            st.code("""
# CSV
df = pd.read_csv('fichier.csv')
df = pd.read_csv('fichier.csv', sep=';', encoding='utf-8')

# Excel
df = pd.read_excel('fichier.xlsx', sheet_name='Sheet1')

# JSON
df = pd.read_json('fichier.json')

# SQL
import sqlite3
conn = sqlite3.connect('database.db')
df = pd.read_sql('SELECT * FROM table', conn)
            """, language="python")
        
        with st.expander("🔍 Exploration des données"):
            st.code("""
# Informations générales
df.info()
df.describe()
df.head(10)
df.tail()

# Dimensions
df.shape
len(df)

# Colonnes et types
df.columns
df.dtypes

# Valeurs manquantes
df.isnull().sum()
df.isna().sum()

# Valeurs uniques
df['colonne'].unique()
df['colonne'].nunique()
df['colonne'].value_counts()
            """, language="python")
        
        with st.expander("🧹 Nettoyage des données"):
            st.code("""
# Supprimer les doublons
df = df.drop_duplicates()

# Gérer les valeurs manquantes
df = df.dropna()  # Supprimer
df = df.fillna(0)  # Remplacer par 0
df['col'] = df['col'].fillna(df['col'].mean())  # Par la moyenne

# Renommer colonnes
df = df.rename(columns={'ancien': 'nouveau'})

# Changer le type
df['colonne'] = df['colonne'].astype(int)

# Supprimer des colonnes
df = df.drop(['col1', 'col2'], axis=1)

# Filtrer les données
df = df[df['age'] > 18]
df = df[(df['age'] > 18) & (df['ville'] == 'Paris')]
            """, language="python")
        
        with st.expander("📊 Agrégation et groupement"):
            st.code("""
# GroupBy
df.groupby('categorie')['ventes'].sum()
df.groupby(['region', 'produit'])['ventes'].agg(['sum', 'mean', 'count'])

# Pivot table
pd.pivot_table(df, values='ventes', index='region', 
               columns='produit', aggfunc='sum')

# Tri
df = df.sort_values('colonne', ascending=False)
df = df.sort_values(['col1', 'col2'], ascending=[True, False])
            """, language="python")
    
    elif category == "NumPy":
        st.subheader("🔢 Snippets NumPy")
        
        with st.expander("📐 Création de tableaux"):
            st.code("""
import numpy as np

# Tableaux de base
arr = np.array([1, 2, 3, 4, 5])
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])

# Tableaux spéciaux
zeros = np.zeros((3, 4))
ones = np.ones((2, 3))
identity = np.eye(5)

# Séquences
np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]
np.linspace(0, 1, 5)  # [0, 0.25, 0.5, 0.75, 1]

# Aléatoires
np.random.rand(3, 3)  # Uniforme [0, 1)
np.random.randn(3, 3)  # Normale N(0,1)
np.random.randint(0, 10, size=(3, 3))  # Entiers
            """, language="python")
        
        with st.expander("🧮 Opérations"):
            st.code("""
# Opérations mathématiques
arr + 5
arr * 2
arr ** 2
np.sqrt(arr)
np.exp(arr)
np.log(arr)

# Statistiques
arr.mean()
arr.std()
arr.min()
arr.max()
arr.sum()

# Axes
arr_2d.sum(axis=0)  # Somme par colonne
arr_2d.mean(axis=1)  # Moyenne par ligne
            """, language="python")
    
    elif category == "Scikit-learn":
        st.subheader("🤖 Snippets Scikit-learn")
        
        with st.expander("📊 Préparation des données"):
            st.code("""
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Normalisation
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Encodage
le = LabelEncoder()
y_encoded = le.fit_transform(y)
            """, language="python")
        
        with st.expander("🎯 Modèles de classification"):
            st.code("""
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Régression logistique
model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Arbre de décision
dt = DecisionTreeClassifier(max_depth=5, random_state=42)
dt.fit(X_train, y_train)

# Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Évaluation
accuracy = accuracy_score(y_test, y_pred)
print(classification_report(y_test, y_pred))
            """, language="python")
        
        with st.expander("📈 Modèles de régression"):
            st.code("""
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Régression linéaire
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Coefficients
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# Évaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"MSE: {mse:.2f}")
print(f"R²: {r2:.2f}")
            """, language="python")
    
    elif category == "SQL":
        st.subheader("🗄️ Snippets SQL")
        
        with st.expander("📋 Requêtes de base"):
            st.code("""
-- SELECT simple
SELECT * FROM clients;
SELECT nom, email FROM clients;

-- WHERE
SELECT * FROM commandes WHERE montant > 100;
SELECT * FROM clients WHERE ville = 'Paris' AND age >= 18;

-- ORDER BY
SELECT * FROM produits ORDER BY prix DESC;

-- LIMIT
SELECT * FROM ventes ORDER BY date DESC LIMIT 10;

-- DISTINCT
SELECT DISTINCT categorie FROM produits;
            """, language="sql")
        
        with st.expander("📊 Agrégations"):
            st.code("""
-- COUNT, SUM, AVG, MIN, MAX
SELECT COUNT(*) FROM clients;
SELECT SUM(montant) FROM commandes;
SELECT AVG(prix) FROM produits;
SELECT MIN(date), MAX(date) FROM ventes;

-- GROUP BY
SELECT categorie, COUNT(*) as nb_produits
FROM produits
GROUP BY categorie;

SELECT client_id, SUM(montant) as total
FROM commandes
GROUP BY client_id
HAVING total > 1000;
            """, language="sql")
        
        with st.expander("🔗 JOINs"):
            st.code("""
-- INNER JOIN
SELECT c.nom, co.montant
FROM clients c
INNER JOIN commandes co ON c.id = co.client_id;

-- LEFT JOIN
SELECT c.nom, co.montant
FROM clients c
LEFT JOIN commandes co ON c.id = co.client_id;

-- Plusieurs JOINs
SELECT c.nom, co.date, p.nom as produit
FROM clients c
INNER JOIN commandes co ON c.id = co.client_id
INNER JOIN produits p ON co.produit_id = p.id;
            """, language="sql")

with tab3:
    st.header("🎯 Quiz Python")
    
    quiz_questions = [
        {
            "question": "Quelle est la sortie de: `print(type([1, 2, 3]))`",
            "options": ["<class 'list'>", "<class 'tuple'>", "<class 'array'>", "<class 'dict'>"],
            "correct": 0
        },
        {
            "question": "Comment ajouter un élément à la fin d'une liste ?",
            "options": [".append()", ".add()", ".push()", ".insert()"],
            "correct": 0
        },
        {
            "question": "Quelle méthode retourne les clés d'un dictionnaire ?",
            "options": [".keys()", ".get_keys()", ".values()", ".items()"],
            "correct": 0
        },
        {
            "question": "Comment lire un fichier CSV avec pandas ?",
            "options": ["pd.read_csv()", "pd.load_csv()", "pd.import_csv()", "pd.open_csv()"],
            "correct": 0
        },
        {
            "question": "Quelle bibliothèque pour le machine learning ?",
            "options": ["scikit-learn", "pandas", "matplotlib", "requests"],
            "correct": 0
        }
    ]
    
    score = 0
    for i, q in enumerate(quiz_questions):
        st.markdown(f"**Question {i+1} :** {q['question']}")
        answer = st.radio("", q['options'], key=f"quiz_{i}")
        
        if st.button("Vérifier", key=f"check_{i}"):
            if q['options'].index(answer) == q['correct']:
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Incorrect. La bonne réponse est: {q['options'][q['correct']]}")
        st.markdown("---")

with tab4:
    st.header("💡 Bonnes Pratiques")
    
    st.subheader("📝 Conventions de nommage")
    st.code("""
# Variables et fonctions : snake_case
ma_variable = 10
def calculer_moyenne(liste_nombres):
    pass

# Classes : PascalCase
class MonModele:
    pass

# Constantes : UPPER_CASE
PI = 3.14159
MAX_ITERATIONS = 100
    """, language="python")
    
    st.subheader("🎯 Structure de code")
    st.code("""
# Imports organisés
import os
import sys

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

# Fonctions documentées
def charger_donnees(chemin: str) -> pd.DataFrame:
    \"\"\"
    Charge les données depuis un fichier CSV.
    
    Args:
        chemin: Chemin vers le fichier CSV
        
    Returns:
        DataFrame pandas contenant les données
    \"\"\"
    return pd.read_csv(chemin)
    """, language="python")
    
    st.subheader("🛡️ Gestion des erreurs")
    st.code("""
# Toujours gérer les erreurs potentielles
try:
    df = pd.read_csv('fichier.csv')
except FileNotFoundError:
    print("Le fichier n'existe pas")
except pd.errors.EmptyDataError:
    print("Le fichier est vide")
except Exception as e:
    print(f"Erreur inattendue: {e}")
    """, language="python")
