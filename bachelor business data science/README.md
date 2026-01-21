# 🎓 UCO Data Science Hub

Plateforme complète d'outils pour les étudiants du **Bachelor Business Data Science** de l'Université Catholique de l'Ouest (UCO) à Angers.

## 🚀 Fonctionnalités

### 📚 Outils d'Apprentissage
- **📊 Statistiques & Probabilités** : Visualisations interactives, calculateurs de tests, exercices corrigés, formulaire
- **💻 Assistant Code & Debug** : Analyseur d'erreurs Python, bibliothèque de snippets (Pandas, NumPy, ML, SQL), quiz
- **📈 Cas Business Data Science** : Projets réalistes avec datasets, scénarios guidés

### 🎯 Outils de Productivité
- **📁 Gestionnaire de Projets** : Templates, checklists, suivi de progression
- **📚 Planificateur de Révisions** : Système de répétition espacée, flashcards personnalisables
- **🔗 Bibliothèque de Ressources** : Tutoriels, datasets, documentation, vidéos

### 💼 Préparation Professionnelle
- **🎤 Simulateur d'Entretiens** : Questions techniques, études de cas business, conseils
- **💼 Portfolio Generator** : Création et export de portfolio professionnel en HTML

### 🤝 Outils Collaboratifs
- **🤝 Forum d'Entraide** : Q&A par matière, recherche de binômes, calendrier de deadlines
- **🎲 Générateur de Datasets** : Données synthétiques pour s'entraîner (e-commerce, CRM, finance...)

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**
```bash
cd "bachelor business data science"
```

2. **Créer un environnement virtuel (recommandé)**
```bash
# Sur macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Sur Windows
python -m venv venv
venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

## 🎮 Utilisation

### Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur par défaut à l'adresse `http://localhost:8501`

### Navigation

Utilisez le menu latéral (sidebar) pour naviguer entre les différents outils :
- 🏠 **Accueil** : Vue d'ensemble de tous les outils
- Choisissez l'outil qui vous intéresse dans la liste

## 📂 Structure du Projet

```
bachelor business data science/
├── app.py                          # Application principale
├── requirements.txt                # Dépendances Python
├── README.md                       # Ce fichier
├── data/                          # Données sauvegardées (générées automatiquement)
│   ├── projects.json
│   ├── flashcards.json
│   ├── portfolio.json
│   └── forum_posts.json
├── pages/                         # Pages de l'application
│   ├── stats_proba.py            # Statistiques & Probabilités
│   ├── code_assistant.py         # Assistant Code
│   ├── business_cases.py         # Cas Business
│   ├── project_manager.py        # Gestionnaire de Projets
│   ├── revision_planner.py       # Planificateur de Révisions
│   ├── resources_library.py      # Bibliothèque de Ressources
│   ├── interview_simulator.py    # Simulateur d'Entretiens
│   ├── portfolio_generator.py    # Portfolio Generator
│   ├── forum.py                  # Forum d'Entraide
│   └── dataset_generator.py      # Générateur de Datasets
└── assets/                        # Ressources (images, etc.)
```

## 💡 Exemples d'Utilisation

### Statistiques & Probabilités
1. Visualisez différentes distributions (Normale, Binomiale, Poisson...)
2. Calculez des tests statistiques (test Z, test t, intervalles de confiance)
3. Pratiquez avec des exercices corrigés
4. Consultez le formulaire de statistiques

### Planificateur de Révisions
1. Créez vos propres flashcards par matière
2. Importez des sets prédéfinis (Stats, Python, ML)
3. Révisez avec le système de répétition espacée
4. Suivez votre progression

### Portfolio Generator
1. Remplissez vos informations personnelles
2. Ajoutez vos projets avec technologies et résultats
3. Définissez vos compétences et leur niveau
4. Exportez en HTML pour le web

### Générateur de Datasets
1. Choisissez un dataset prédéfini (e-commerce, CRM, finance...)
2. Personnalisez la taille (100 à 10,000 lignes)
3. Téléchargez en CSV
4. Utilisez pour vos projets d'entraînement

## 🛠️ Technologies Utilisées

- **Streamlit** : Framework web pour applications data science
- **Pandas** : Manipulation et analyse de données
- **NumPy** : Calcul scientifique
- **Plotly** : Visualisations interactives
- **Scipy** : Tests statistiques
- **Scikit-learn** : Machine learning (pour les datasets)

## 📝 Notes

- Les données sont sauvegardées localement dans le dossier `data/` au format JSON
- L'application fonctionne entièrement en local, aucune connexion internet requise (sauf pour les ressources externes)
- Les fichiers JSON sont créés automatiquement au premier lancement

## 🤝 Contribution

Ce projet est conçu pour les étudiants UCO. N'hésitez pas à :
- Suggérer de nouvelles fonctionnalités
- Signaler des bugs
- Partager vos améliorations

## 📧 Contact

Pour toute question ou suggestion, utilisez le forum intégré dans l'application !

## 📄 Licence

Projet éducatif pour les étudiants du Bachelor Business Data Science - UCO Angers

---

**Développé avec ❤️ pour les étudiants UCO Data Science**

*Bonne utilisation et bon apprentissage ! 🚀*
# bachelor-business-data-science
