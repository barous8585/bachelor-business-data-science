import streamlit as st
import random
import json
from pathlib import Path

st.title("🎤 Simulateur d'Entretiens")
st.markdown("**Préparez-vous aux entretiens techniques et études de cas**")

tab1, tab2, tab3 = st.tabs(["💬 Questions Techniques", "📊 Études de Cas", "💡 Conseils"])

with tab1:
    st.header("💬 Questions Techniques Fréquentes")
    
    categorie = st.selectbox(
        "Catégorie de questions",
        ["Python", "Statistiques", "Machine Learning", "SQL", "Data Analysis", "Général"]
    )
    
    questions_bank = {
        "Python": [
            {
                "question": "Quelle est la différence entre une liste et un tuple en Python ?",
                "reponse": "Les listes sont mutables (modifiables) tandis que les tuples sont immuables. Les listes utilisent [] et les tuples (). Les tuples sont plus rapides et utilisent moins de mémoire.",
                "conseils": "Donnez un exemple concret : ma_liste = [1,2,3] vs mon_tuple = (1,2,3)"
            },
            {
                "question": "Expliquez les list comprehensions",
                "reponse": "Syntaxe concise pour créer des listes. Ex: [x**2 for x in range(10)] crée une liste des carrés de 0 à 9. Plus pythonique et souvent plus rapide que les boucles.",
                "conseils": "Montrez la différence avec une boucle for classique"
            },
            {
                "question": "Qu'est-ce qu'un décorateur en Python ?",
                "reponse": "Fonction qui modifie le comportement d'une autre fonction. Utilise @decorator avant la fonction. Utile pour logging, timing, authentification.",
                "conseils": "Si vous n'êtes pas sûr, soyez honnête mais montrez votre compréhension des fonctions"
            },
            {
                "question": "Comment gérez-vous les erreurs en Python ?",
                "reponse": "Avec try/except. Try pour le code risqué, except pour gérer les erreurs spécifiques, finally pour le code qui s'exécute toujours.",
                "conseils": "Donnez un exemple pratique comme la lecture de fichier"
            }
        ],
        "Statistiques": [
            {
                "question": "Quelle est la différence entre corrélation et causalité ?",
                "reponse": "Corrélation : deux variables varient ensemble. Causalité : une variable influence directement l'autre. Corrélation n'implique pas causalité !",
                "conseils": "Exemple : ventes de glaces et noyades sont corrélées (chaleur) mais pas causales"
            },
            {
                "question": "Expliquez le théorème central limite",
                "reponse": "La distribution des moyennes d'échantillons tend vers une loi normale, quelle que soit la distribution d'origine, si l'échantillon est assez grand (n≥30).",
                "conseils": "Mentionnez l'importance pour les tests d'hypothèses"
            },
            {
                "question": "Qu'est-ce qu'une p-value ?",
                "reponse": "Probabilité d'obtenir un résultat au moins aussi extrême que celui observé, si H₀ est vraie. Si p < α (souvent 0.05), on rejette H₀.",
                "conseils": "Attention à ne pas dire 'probabilité que H₀ soit vraie'"
            },
            {
                "question": "Différence entre variance et écart-type ?",
                "reponse": "Variance : moyenne des écarts au carré. Écart-type : racine carrée de la variance. L'écart-type a l'avantage d'être dans la même unité que les données.",
                "conseils": "Exemple concret avec des données en euros"
            }
        ],
        "Machine Learning": [
            {
                "question": "Qu'est-ce que l'overfitting et comment l'éviter ?",
                "reponse": "Le modèle apprend trop bien les données d'entraînement (bruit inclus) et généralise mal. Solutions : régularisation (L1/L2), plus de données, cross-validation, réduire la complexité.",
                "conseils": "Mentionnez la différence entre erreur train et test"
            },
            {
                "question": "Différence entre classification et régression ?",
                "reponse": "Classification : prédire une catégorie (discret). Régression : prédire une valeur numérique (continu). Ex: spam/non-spam vs prix d'une maison.",
                "conseils": "Donnez des exemples concrets de votre expérience"
            },
            {
                "question": "Comment choisir entre précision et recall ?",
                "reponse": "Dépend du contexte. Précision si les faux positifs sont coûteux. Recall si les faux négatifs sont critiques. Ex: détection cancer → privilégier recall.",
                "conseils": "Mentionnez le F1-score comme compromis"
            },
            {
                "question": "Expliquez la validation croisée",
                "reponse": "Technique pour évaluer la performance. Divise les données en k folds, entraîne sur k-1 et teste sur 1, répète k fois. Donne une estimation plus robuste.",
                "conseils": "Mentionnez k=5 ou 10 comme standards"
            }
        ],
        "SQL": [
            {
                "question": "Différence entre INNER JOIN et LEFT JOIN ?",
                "reponse": "INNER JOIN : garde seulement les lignes avec correspondance dans les deux tables. LEFT JOIN : garde toutes les lignes de la table de gauche + correspondances.",
                "conseils": "Dessinez un diagramme de Venn si possible"
            },
            {
                "question": "Qu'est-ce qu'un index et pourquoi l'utiliser ?",
                "reponse": "Structure de données qui accélère les recherches dans une table. Comme un index de livre. Améliore les SELECT mais ralentit les INSERT/UPDATE.",
                "conseils": "Mentionnez l'importance pour les grosses tables"
            },
            {
                "question": "Différence entre WHERE et HAVING ?",
                "reponse": "WHERE filtre les lignes avant le GROUP BY. HAVING filtre les groupes après le GROUP BY. HAVING fonctionne avec les fonctions d'agrégation.",
                "conseils": "Donnez un exemple avec COUNT ou SUM"
            }
        ],
        "Data Analysis": [
            {
                "question": "Comment traitez-vous les valeurs manquantes ?",
                "reponse": "Dépend du contexte : suppression (si peu de valeurs), imputation (moyenne, médiane, mode), prédiction (ML), ou garder comme catégorie. Analyser le pattern de manque d'abord.",
                "conseils": "Mentionnez MCAR, MAR, MNAR si vous connaissez"
            },
            {
                "question": "Comment détectez-vous les outliers ?",
                "reponse": "Visualisation (boxplot), méthodes statistiques (IQR, z-score > 3), ou algorithmes (Isolation Forest). Important de comprendre s'ils sont erreurs ou information.",
                "conseils": "Donnez un exemple de votre expérience"
            },
            {
                "question": "Expliquez votre processus d'EDA",
                "reponse": "1) Comprendre les données (info, describe), 2) Qualité (valeurs manquantes, doublons), 3) Distributions univariées, 4) Relations bivariées, 5) Insights et hypothèses.",
                "conseils": "Structurez votre réponse, montrez votre méthodologie"
            }
        ],
        "Général": [
            {
                "question": "Parlez-moi d'un projet data science que vous avez réalisé",
                "reponse": "Structure STAR : Situation (contexte), Tâche (objectif), Action (ce que vous avez fait), Résultat (outcome, metrics).",
                "conseils": "Préparez 2-3 projets à l'avance avec des chiffres concrets"
            },
            {
                "question": "Quelles sont vos faiblesses ?",
                "reponse": "Soyez honnête mais montrez que vous travaillez dessus. Ex: 'Je manque d'expérience en deep learning mais je suis en train de suivre le cours fast.ai'",
                "conseils": "Transformez la faiblesse en apprentissage"
            },
            {
                "question": "Pourquoi voulez-vous travailler en data science ?",
                "reponse": "Parlez de votre passion pour résoudre des problèmes avec des données, l'impact business, l'apprentissage continu. Soyez authentique.",
                "conseils": "Reliez à votre parcours et expériences"
            }
        ]
    }
    
    if categorie in questions_bank:
        questions = questions_bank[categorie]
        
        st.info(f"💡 {len(questions)} questions disponibles dans cette catégorie")
        
        if st.button("🎲 Question aléatoire", width="stretch"):
            st.session_state['random_question'] = random.choice(questions)
        
        if 'random_question' in st.session_state:
            q = st.session_state['random_question']
            
            st.markdown("---")
            st.markdown(f"### ❓ Question")
            st.markdown(f"## {q['question']}")
            
            with st.expander("💡 Voir la réponse suggérée"):
                st.success(f"**Réponse :** {q['reponse']}")
                st.info(f"**Conseil :** {q['conseils']}")
            
            if st.button("⏭️ Question suivante"):
                st.session_state['random_question'] = random.choice(questions)
                st.rerun()

with tab2:
    st.header("📊 Études de Cas Business")
    
    case_studies = [
        {
            "titre": "Réduction du Churn Client",
            "contexte": "Une entreprise de télécommunications perd 25% de ses clients chaque année. Le coût d'acquisition d'un nouveau client est 5x celui de rétention.",
            "question": "Comment utiliseriez-vous la data science pour réduire le churn ?",
            "points_cles": [
                "Définir le churn (ex: pas d'activité depuis 3 mois)",
                "Collecter les données pertinentes (usage, paiements, support)",
                "Analyse exploratoire pour identifier les patterns",
                "Modèle prédictif (classification : va churner ou non)",
                "Actions ciblées selon le score de risque",
                "Mesurer l'impact (A/B testing)"
            ],
            "metrics": ["Taux de churn", "CLV", "Précision du modèle", "ROI des actions"]
        },
        {
            "titre": "Optimisation des Prix E-commerce",
            "contexte": "Un site e-commerce veut optimiser ses prix pour maximiser le revenu. Ils ont 2 ans de données de ventes.",
            "question": "Quelle approche data-driven proposeriez-vous ?",
            "points_cles": [
                "Analyse de l'élasticité-prix par catégorie",
                "Segmentation des produits et clients",
                "Analyse de la concurrence",
                "Tests A/B sur différentes stratégies de prix",
                "Modèle de prédiction de la demande",
                "Optimisation dynamique des prix"
            ],
            "metrics": ["Revenu total", "Marge", "Volume de ventes", "Élasticité-prix"]
        },
        {
            "titre": "Prévision de la Demande",
            "contexte": "Une chaîne de supermarchés a des problèmes de sur-stock et ruptures. Ils veulent améliorer leurs prévisions.",
            "question": "Comment construiriez-vous un système de prévision ?",
            "points_cles": [
                "Analyse des séries temporelles (tendance, saisonnalité)",
                "Features externes (météo, jours fériés, promotions)",
                "Modèles par catégorie/magasin",
                "Choix du modèle (ARIMA, Prophet, ML)",
                "Gestion des événements spéciaux",
                "Mise à jour continue du modèle"
            ],
            "metrics": ["MAPE", "RMSE", "Taux de rupture", "Coût de stock"]
        },
        {
            "titre": "Système de Recommandation",
            "contexte": "Une plateforme de streaming veut augmenter l'engagement en recommandant du contenu personnalisé.",
            "question": "Quel système de recommandation proposeriez-vous ?",
            "points_cles": [
                "Collaborative filtering (user-based ou item-based)",
                "Content-based (features du contenu)",
                "Hybride pour combiner les avantages",
                "Gestion du cold start (nouveaux users/items)",
                "Diversité vs précision",
                "Évaluation online (CTR, temps de visionnage)"
            ],
            "metrics": ["Précision@k", "Recall@k", "CTR", "Temps d'engagement"]
        }
    ]
    
    for case in case_studies:
        with st.expander(f"📋 {case['titre']}"):
            st.markdown(f"**Contexte :** {case['contexte']}")
            st.markdown(f"**Question :** {case['question']}")
            
            with st.expander("💡 Points clés à aborder"):
                for point in case['points_cles']:
                    st.markdown(f"- {point}")
            
            with st.expander("📊 Métriques importantes"):
                st.markdown(", ".join([f"`{m}`" for m in case['metrics']]))
    
    st.markdown("---")
    st.markdown("### 💡 Framework pour les études de cas")
    st.info("""
    **Structure recommandée :**
    
    1. **Clarifier** : Posez des questions pour bien comprendre
    2. **Définir** : Objectif business et métriques de succès
    3. **Données** : Quelles données nécessaires et disponibles ?
    4. **Approche** : Méthodologie data science (exploratoire → modèle → déploiement)
    5. **Challenges** : Anticipez les difficultés
    6. **Impact** : Comment mesurer le succès ?
    """)

with tab3:
    st.header("💡 Conseils pour Réussir vos Entretiens")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ À FAIRE")
        st.markdown("""
        - **Préparez des exemples concrets** de vos projets
        - **Posez des questions** pour clarifier
        - **Pensez à voix haute** pendant les cas pratiques
        - **Montrez votre raisonnement**, pas juste la réponse
        - **Soyez honnête** si vous ne savez pas
        - **Reliez à l'impact business** quand possible
        - **Préparez des questions** pour le recruteur
        - **Entraînez-vous à expliquer** simplement
        """)
    
    with col2:
        st.subheader("❌ À ÉVITER")
        st.markdown("""
        - **Ne pas bluffer** sur vos compétences
        - **Ne pas partir tête baissée** sans réfléchir
        - **Évitez le jargon excessif** sans explication
        - **Ne critiquez pas** vos employeurs précédents
        - **N'oubliez pas l'aspect business** (focus tech uniquement)
        - **Ne soyez pas trop vague** dans vos réponses
        - **Évitez les réponses trop longues** et confuses
        - **Ne négligez pas les soft skills**
        """)
    
    st.markdown("---")
    st.subheader("📝 Checklist de Préparation")
    
    checklist = [
        "J'ai relu mon CV et peux expliquer chaque projet",
        "J'ai préparé 3 projets à présenter en détail",
        "Je connais l'entreprise et ses produits/services",
        "J'ai des questions pertinentes à poser",
        "J'ai révisé les fondamentaux (stats, ML, Python)",
        "Je peux expliquer mes choix techniques",
        "J'ai des exemples de travail d'équipe",
        "Je connais mes forces et axes d'amélioration",
        "J'ai testé ma connexion/caméra (si remote)",
        "J'ai préparé un environnement calme"
    ]
    
    for item in checklist:
        st.checkbox(item, key=f"prep_{item}")
    
    st.markdown("---")
    st.subheader("🎯 Questions à Poser au Recruteur")
    
    questions_to_ask = [
        "Quels sont les projets data en cours dans l'équipe ?",
        "Quelle est la stack technique utilisée ?",
        "Comment est organisée l'équipe data ?",
        "Quelles sont les opportunités de formation/montée en compétences ?",
        "Comment mesurez-vous l'impact des projets data ?",
        "Quel est le processus de déploiement de modèles ?",
        "Comment collaborez-vous avec les équipes métier ?",
        "Quels sont les défis data actuels de l'entreprise ?"
    ]
    
    for q in questions_to_ask:
        st.markdown(f"- {q}")
