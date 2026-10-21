# UCO Data Science Hub

Outils de révision et de pratique pour les étudiants du **Bachelor Business Data Science** de l'UCO Angers : statistiques interactives, assistant code, cas business, flashcards à répétition espacée, générateur de datasets, entretiens, portfolio, entraide et espace professeur.

## Version web (`index.html`)

Le site tient en **un seul fichier**, `index.html`, sans serveur ni installation.

- **Tester en local** : double-clique sur `index.html` (connexion Internet nécessaire pour les polices, KaTeX et jStat).
- **Publier sur GitHub Pages** : dans le dépôt GitHub, *Settings → Pages → Build and deployment*, choisis *Deploy from a branch*, branche `main`, dossier `/ (root)`, puis *Save*. Le site sera en ligne sur `https://barous8585.github.io/bachelor-business-data-science/`.
- **Données** : pour l'instant, tout est enregistré dans le navigateur de chaque utilisateur (localStorage). Tout l'accès aux données passe par l'objet `Store` en haut du script : pour brancher une base en ligne (Supabase, Firebase…), il suffit de réécrire ses méthodes.
- **Contenu** : les questions, flashcards, cas business, ressources, etc. sont dans l'objet `CONTENT` au milieu du fichier, modifiables directement.
- **À venir** : comptes utilisateurs, base de données partagée, génération d'exercices par IA (via un service qui garde la clé API secrète).

## Ancienne version Streamlit

Le code Streamlit (`app.py`, `modules/`) est conservé tel quel pour réutilisation. La documentation ci-dessous le concerne.

---

## 🚀 Fonctionnalités

### 👨‍🏫 Pour les Professeurs
- **Upload de cours** : TXT, Markdown
- **Génération automatique d'exercices** avec IA Gemini 2.5 Flash
- **Statistiques** : Suivi de l'engagement des étudiants

### 📚 Pour les Étudiants
- **Gestionnaire de Projets** : Templates, checklists, suivi
- **Planificateur de Révisions** : Flashcards avec répétition espacée
- **Portfolio Generator** : Création et export HTML
- **Cas Business** : Projets réalistes avec datasets
- **Forum d'Entraide** : Q&A entre étudiants
- **Simulateur d'Entretiens** : Préparation aux entretiens techniques
- **Assistant Code** : Débogage Python/SQL
- **Générateur de Datasets** : Données synthétiques pour s'entraîner

---

## 🏗️ Architecture Technique

### Stack
- **Frontend** : Streamlit
- **Backend** : Python 3.9+
- **Base de données** : SQLite
- **IA** : Google Gemini 2.5 Flash
- **Visualisation** : Plotly, Matplotlib, Seaborn

---

## 📦 Installation Locale

### Prérequis
- Python 3.9 ou supérieur
- pip

### Installation

1. **Cloner le repository**
```bash
git clone https://github.com/barous8585/bachelor-business-data-science.git
cd bachelor-business-data-science
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer l'API Gemini**

Créer un fichier `.streamlit/secrets.toml` :
```toml
[api]
gemini_key = "votre_clé_api_ici"
```

4. **Lancer l'application**
```bash
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`

---

## ☁️ Déploiement sur Streamlit Cloud

### Étapes

1. **Fork ce repository**

2. **Connecter à Streamlit Cloud**
   - Aller sur [share.streamlit.io](https://share.streamlit.io)
   - Connecter votre compte GitHub
   - Sélectionner ce repository

3. **Configurer les Secrets**
   
   Dans les paramètres de l'app sur Streamlit Cloud, ajouter :
   ```toml
   [api]
   gemini_key = "votre_clé_api_gemini"
   ```

4. **Déployer** 🚀

---

## 🔑 Obtenir une Clé API Gemini

1. Aller sur [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Créer un projet
3. Générer une clé API
4. Gratuit : 1,500 requêtes/jour avec Gemini 2.5 Flash

---

## 🎯 Matières Couvertes (B1 BDS UCO)

1. Algorithmique et Programmation
2. Compléments de Maths
3. Exploitation des données
4. Probabilités
5. Statistique Descriptive
6. Statistique Inférentielle
7. Outils de pilotage

---

## 📝 Scripts Utiles

### Vérifier l'intégrité
```bash
python3 verify_app.py
```

---

## 👥 Auteur

- **Thierno Ousmane Barry** - Étudiant B1 BDS UCO Angers

---

**Made with ❤️ for UCO Data Science Students**

*Dernière mise à jour : 21 octobre 2026*
