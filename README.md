# UCO Data Science Hub

La plateforme de la formation **Business Data Science** de l'UCO Angers (B1, B2, B3), pour les **étudiants**, les **professeurs** et **l'administration**. Elle répond aux problèmes rencontrés avec Teams : canaux recréés chaque année, documents mal identifiés, consignes de devoirs ambiguës, informations importantes noyées.

## Ce que fait la plateforme

- **Matières stables d'une année sur l'autre**, avec leurs séances (CM, TD, TP, CC) et des documents typés : support, sujet, corrigé, données. Les documents pointent vers Teams / SharePoint.
- **Fiche devoir standard** : objectif, livrable, format, modalité, date et heure, lieu de dépôt, barème, documents. Un indicateur de clarté montre au professeur ce qui manque avant publication.
- **Questions sur la consigne** : posées sur la fiche, la réponse du professeur est visible par toute la promo.
- **Annonces** par niveau d'importance ; les urgentes restent en bandeau jusqu'à lecture.
- **Calendrier unique** : cours, rendus, contrôles, jalons de projets, vacances, fermetures.
- **Projets encadrés** avec groupes et jalons.
- **Administration** : préparer l'année suivante en recopiant la structure, charge de travail par promo (rendus qui se chevauchent), questions sans réponse, catalogue des matières.
- **Boîte à outils** : statistiques, assistant code, cas business, ressources, flashcards, datasets, entretiens, portfolio, entraide.

## Utilisation

Le site tient en **un seul fichier**, `index.html`, sans serveur.

- **Tester** : ouvrir `index.html` dans un navigateur, choisir un profil (le bouton en haut à droite permet d'en changer). Des données d'exemple (noms fictifs) montrent le fonctionnement ; on peut les retirer dans Administration › Exemples.
- **Publier sur GitHub Pages** : *Settings → Pages*, *Deploy from a branch*, branche `main`, dossier `/ (root)`. Adresse : `https://barous8585.github.io/bachelor-business-data-science/`.
- **Données** : pour l'instant, enregistrées dans le navigateur de chaque utilisateur. Tout passe par l'objet `Store` en haut du script : le brancher sur une base partagée (Supabase…) rendra annonces, devoirs et questions communs à tous.
- **À venir** : comptes et base partagée, connexion à Teams (Microsoft Graph, avec l'accord de la DSI de l'UCO), génération d'exercices par IA.

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
