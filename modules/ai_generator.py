"""
Module de génération d'exercices par IA avec Google Gemini
"""

import json
import os
import streamlit as st
from pathlib import Path
from google import genai
from google.genai import types
from typing import List, Dict, Optional

# Charger la configuration
CONFIG_FILE = Path("config/api_config.json")

def get_api_key():
    """Récupère la clé API depuis secrets.toml, config ou .env"""
    # 1. Essayer depuis Streamlit secrets (Streamlit Cloud)
    try:
        return st.secrets["api"]["gemini_key"]
    except:
        pass
    
    # 2. Essayer depuis config/api_config.json (local)
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            if config.get('GEMINI_API_KEY'):
                return config['GEMINI_API_KEY']
    
    # 3. Essayer depuis .env (local)
    try:
        from dotenv import load_dotenv
        load_dotenv()
        key = os.getenv("GEMINI_API_KEY")
        if key:
            return key
    except:
        pass
    
    return None

def load_api_config():
    """Charge la configuration de l'API (legacy)"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None

def get_gemini_client():
    """Initialise et retourne le client Gemini"""
    api_key = get_api_key()
    if api_key:
        client = genai.Client(api_key=api_key)
        return client
    return None

def generate_exercises_with_ai(
    course_content: str,
    matiere: str,
    niveau: str = "Intermédiaire",
    nb_exercises: int = 5,
    exercise_types: List[str] = None
) -> List[Dict]:
    """
    Génère des exercices intelligents basés sur le contenu du cours
    
    Args:
        course_content: Contenu textuel du cours
        matiere: Matière (ex: "Statistiques", "Python")
        niveau: Niveau de difficulté
        nb_exercises: Nombre d'exercices à générer
        exercise_types: Types d'exercices souhaités
        
    Returns:
        Liste d'exercices générés
    """
    
    client = get_gemini_client()
    if not client:
        return []
    
    # Types d'exercices par défaut selon la matière
    if exercise_types is None:
        if "Statistique" in matiere or "Probabilité" in matiere:
            exercise_types = ["QCM", "Exercice de calcul", "Problème appliqué", "Vrai/Faux"]
        elif "Programmation" in matiere or "Algorithmique" in matiere:
            exercise_types = ["Code à compléter", "Débogage", "Algorithme", "QCM"]
        elif "Exploitation" in matiere or "données" in matiere.lower():
            exercise_types = ["QCM", "Code Pandas", "Analyse de cas", "SQL"]
        else:
            exercise_types = ["QCM", "Exercice pratique", "Problème"]
    
    # Prompt engineering pour Gemini
    prompt = f"""Tu es un expert pédagogue en Data Science spécialisé en {matiere}.

**COURS À ANALYSER :**
{course_content[:3000]}  

**CONSIGNES :**
Génère exactement {nb_exercises} exercices pédagogiques de niveau {niveau} pour des étudiants de Licence en Data Science (Bachelor).

**TYPES D'EXERCICES À CRÉER :**
{', '.join(exercise_types)}

**FORMAT DE SORTIE (JSON strict) :**
Retourne UNIQUEMENT un tableau JSON valide, sans texte avant ou après, avec cette structure :

```json
[
  {{
    "type": "QCM",
    "question": "Question claire et précise",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_index": 0,
    "explication": "Explication détaillée de la réponse",
    "difficulte": "{niveau}",
    "concepts": ["concept1", "concept2"],
    "temps_estime": "5 min"
  }},
  {{
    "type": "Exercice de calcul",
    "question": "Énoncé complet avec données",
    "solution": "Solution étape par étape",
    "explication": "Méthodologie et raisonnement",
    "difficulte": "{niveau}",
    "concepts": ["concept1"],
    "temps_estime": "10 min"
  }}
]
```

**CRITÈRES DE QUALITÉ :**
1. Questions basées UNIQUEMENT sur le contenu du cours fourni
2. Progression logique de difficulté
3. Explications claires et pédagogiques
4. Calculs vérifiables et corrects
5. Éviter les questions trop simples ou trop complexes
6. Contexte réaliste et applicable

**TYPES D'EXERCICES DÉTAILLÉS :**

- **QCM** : 4 options, 1 seule correcte, pièges pédagogiques
- **Exercice de calcul** : Données numériques, résolution étape par étape
- **Code à compléter** : Squelette de code avec parties manquantes
- **Débogage** : Code avec erreur(s) à identifier et corriger
- **Problème appliqué** : Cas réel d'entreprise à résoudre
- **Vrai/Faux** : Affirmation avec justification obligatoire
- **Algorithme** : Pseudo-code ou organigramme
- **SQL** : Requête à écrire sur une base donnée
- **Code Pandas** : Manipulation de DataFrame

Génère maintenant les exercices en JSON pur :
"""

    try:
        # Générer le contenu avec le nouveau SDK
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                top_p=0.95,
                top_k=40,
                max_output_tokens=4096,
            )
        )
        
        # Extraire le JSON de la réponse
        text = response.text.strip()
        
        # Nettoyer le texte (enlever les balises markdown si présentes)
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        # Parser le JSON
        exercises = json.loads(text)
        
        # Valider et enrichir les exercices
        validated_exercises = []
        for i, ex in enumerate(exercises[:nb_exercises]):
            if not isinstance(ex, dict):
                continue
            
            # Ajouter des métadonnées
            ex['id'] = f"{matiere.replace(' ', '_')}_{i+1}"
            ex['matiere'] = matiere
            ex['source'] = 'IA Gemini'
            ex['niveau'] = niveau
            
            # S'assurer que les champs requis existent
            if 'question' in ex and ex['question']:
                validated_exercises.append(ex)
        
        return validated_exercises
        
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de parsing JSON : {e}")
        print(f"Réponse brute : {text[:500]}")
        return []
    except Exception as e:
        print(f"❌ Erreur lors de la génération : {e}")
        return []

def analyze_course_content(course_content: str) -> Dict:
    """
    Analyse le contenu d'un cours et extrait les concepts clés
    
    Returns:
        Dict avec: concepts, difficulte_estimee, themes, mots_cles
    """
    
    client = get_gemini_client()
    if not client:
        return {}
    
    prompt = f"""Analyse ce cours de Data Science et extrais les informations clés.

**COURS :**
{course_content[:2000]}

**FORMAT DE SORTIE (JSON) :**
```json
{{
  "concepts_principaux": ["concept1", "concept2", "concept3"],
  "difficulte_estimee": "Débutant|Intermédiaire|Avancé",
  "themes": ["theme1", "theme2"],
  "mots_cles": ["mot1", "mot2", "mot3", "mot4", "mot5"],
  "prerequis": ["prérequis1", "prérequis2"],
  "duree_lecture_min": 15,
  "resume_une_phrase": "Résumé concis du cours"
}}
```

Retourne UNIQUEMENT le JSON :
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        
        analysis = json.loads(text)
        return analysis
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse : {e}")
        return {}

def generate_personalized_explanation(
    question: str,
    student_answer: str,
    correct_answer: str,
    matiere: str
) -> str:
    """
    Génère une explication personnalisée basée sur la réponse de l'étudiant
    """
    
    client = get_gemini_client()
    if not client:
        return "Explication non disponible"
    
    prompt = f"""Tu es un tuteur pédagogue en {matiere}.

**QUESTION :** {question}

**RÉPONSE DE L'ÉTUDIANT :** {student_answer}

**BONNE RÉPONSE :** {correct_answer}

**CONSIGNE :**
Fournis une explication personnalisée et bienveillante qui :
1. Identifie l'erreur de raisonnement (si erreur)
2. Explique pourquoi la bonne réponse est correcte
3. Donne un conseil pour ne plus faire cette erreur
4. Encourage l'étudiant

Ton explication (200 mots max) :
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Explication non disponible : {e}"

def test_api_connection() -> bool:
    """
    Teste la connexion à l'API Gemini
    
    Returns:
        True si la connexion fonctionne, False sinon
    """
    try:
        client = get_gemini_client()
        if not client:
            return False
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents="Dis simplement 'OK' si tu me reçois."
        )
        
        return "OK" in response.text or "ok" in response.text.lower()
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")
        return False
