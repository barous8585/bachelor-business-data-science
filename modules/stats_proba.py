import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import json
from pathlib import Path

st.title("📊 Statistiques & Probabilités")
st.markdown("**Outils interactifs pour maîtriser les stats et probas**")

tab1, tab2, tab3, tab4 = st.tabs(["📈 Distributions", "🧮 Calculateurs", "📝 Exercices", "📖 Formulaire"])

with tab1:
    st.header("Visualisation des Distributions")
    
    distribution = st.selectbox(
        "Choisissez une distribution :",
        ["Normale", "Binomiale", "Poisson", "Exponentielle", "Uniforme", "Student (t)"]
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("Paramètres")
        
        if distribution == "Normale":
            mu = st.slider("Moyenne (μ)", -10.0, 10.0, 0.0, 0.1)
            sigma = st.slider("Écart-type (σ)", 0.1, 5.0, 1.0, 0.1)
            x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
            y = stats.norm.pdf(x, mu, sigma)
            st.latex(f"X \\sim N({mu}, {sigma}^2)")
            
        elif distribution == "Binomiale":
            n = st.slider("Nombre d'essais (n)", 1, 100, 20)
            p = st.slider("Probabilité de succès (p)", 0.0, 1.0, 0.5, 0.01)
            x = np.arange(0, n+1)
            y = stats.binom.pmf(x, n, p)
            st.latex(f"X \\sim B({n}, {p})")
            
        elif distribution == "Poisson":
            lambda_val = st.slider("Lambda (λ)", 0.1, 20.0, 5.0, 0.1)
            x = np.arange(0, int(lambda_val * 3))
            y = stats.poisson.pmf(x, lambda_val)
            st.latex(f"X \\sim P({lambda_val})")
            
        elif distribution == "Exponentielle":
            lambda_val = st.slider("Lambda (λ)", 0.1, 5.0, 1.0, 0.1)
            x = np.linspace(0, 10/lambda_val, 1000)
            y = stats.expon.pdf(x, scale=1/lambda_val)
            st.latex(f"X \\sim Exp({lambda_val})")
            
        elif distribution == "Uniforme":
            a = st.slider("Borne inférieure (a)", -10.0, 10.0, 0.0, 0.1)
            b = st.slider("Borne supérieure (b)", a+0.1, 20.0, 10.0, 0.1)
            x = np.linspace(a-1, b+1, 1000)
            y = stats.uniform.pdf(x, a, b-a)
            st.latex(f"X \\sim U({a}, {b})")
            
        elif distribution == "Student (t)":
            df = st.slider("Degrés de liberté (df)", 1, 30, 10)
            x = np.linspace(-5, 5, 1000)
            y = stats.t.pdf(x, df)
            st.latex(f"X \\sim t({df})")
    
    with col1:
        fig = go.Figure()
        
        if distribution in ["Binomiale", "Poisson"]:
            fig.add_trace(go.Bar(x=x, y=y, name=distribution, marker_color='#667eea'))
        else:
            fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', name=distribution, line=dict(color='#667eea', width=3)))
        
        fig.update_layout(
            title=f"Distribution {distribution}",
            xaxis_title="x",
            yaxis_title="Densité de probabilité" if distribution not in ["Binomiale", "Poisson"] else "Probabilité",
            height=500,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, width="stretch")
        
        if distribution == "Normale":
            st.info(f"**Propriétés :** E[X] = {mu:.2f} | Var(X) = {sigma**2:.2f} | P(μ-σ < X < μ+σ) ≈ 68%")
        elif distribution == "Binomiale":
            st.info(f"**Propriétés :** E[X] = {n*p:.2f} | Var(X) = {n*p*(1-p):.2f}")
        elif distribution == "Poisson":
            st.info(f"**Propriétés :** E[X] = {lambda_val:.2f} | Var(X) = {lambda_val:.2f}")

with tab2:
    st.header("Calculateurs de Tests Statistiques")
    
    test_type = st.selectbox(
        "Choisissez un test :",
        ["Test Z (moyenne)", "Test t de Student", "Test du Chi²", "Intervalle de confiance", "Taille d'échantillon"]
    )
    
    if test_type == "Test Z (moyenne)":
        st.subheader("Test Z pour une moyenne")
        
        col1, col2 = st.columns(2)
        
        with col1:
            x_bar = st.number_input("Moyenne observée (x̄)", value=105.0)
            mu_0 = st.number_input("Moyenne sous H₀ (μ₀)", value=100.0)
            sigma = st.number_input("Écart-type population (σ)", value=15.0, min_value=0.1)
            n = st.number_input("Taille échantillon (n)", value=30, min_value=1)
        
        with col2:
            alpha = st.select_slider("Niveau de significativité (α)", options=[0.01, 0.05, 0.1], value=0.05)
            alternative = st.radio("Hypothèse alternative", ["bilatéral", "unilatéral droite", "unilatéral gauche"])
        
        z_stat = (x_bar - mu_0) / (sigma / np.sqrt(n))
        
        if alternative == "bilatéral":
            p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
            z_critical = stats.norm.ppf(1 - alpha/2)
            reject = abs(z_stat) > z_critical
        elif alternative == "unilatéral droite":
            p_value = 1 - stats.norm.cdf(z_stat)
            z_critical = stats.norm.ppf(1 - alpha)
            reject = z_stat > z_critical
        else:
            p_value = stats.norm.cdf(z_stat)
            z_critical = stats.norm.ppf(alpha)
            reject = z_stat < z_critical
        
        st.markdown("---")
        st.subheader("Résultats")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Statistique Z", f"{z_stat:.4f}")
        col2.metric("P-value", f"{p_value:.4f}")
        col3.metric("Décision", "Rejeter H₀" if reject else "Ne pas rejeter H₀")
        
        if reject:
            st.error(f"✅ **Conclusion :** On rejette H₀ au niveau {alpha}. La différence est statistiquement significative.")
        else:
            st.success(f"❌ **Conclusion :** On ne rejette pas H₀ au niveau {alpha}. Pas de différence significative.")
        
        st.info(f"**Valeur critique :** Z_critique = ±{z_critical:.4f}" if alternative == "bilatéral" else f"**Valeur critique :** Z_critique = {z_critical:.4f}")
    
    elif test_type == "Test t de Student":
        st.subheader("Test t pour une moyenne")
        
        col1, col2 = st.columns(2)
        
        with col1:
            x_bar = st.number_input("Moyenne observée (x̄)", value=105.0)
            mu_0 = st.number_input("Moyenne sous H₀ (μ₀)", value=100.0)
            s = st.number_input("Écart-type échantillon (s)", value=15.0, min_value=0.1)
            n = st.number_input("Taille échantillon (n)", value=25, min_value=2)
        
        with col2:
            alpha = st.select_slider("Niveau de significativité (α)", options=[0.01, 0.05, 0.1], value=0.05)
            alternative = st.radio("Hypothèse alternative", ["bilatéral", "unilatéral droite", "unilatéral gauche"], key="t_test")
        
        df = n - 1
        t_stat = (x_bar - mu_0) / (s / np.sqrt(n))
        
        if alternative == "bilatéral":
            p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))
            t_critical = stats.t.ppf(1 - alpha/2, df)
            reject = abs(t_stat) > t_critical
        elif alternative == "unilatéral droite":
            p_value = 1 - stats.t.cdf(t_stat, df)
            t_critical = stats.t.ppf(1 - alpha, df)
            reject = t_stat > t_critical
        else:
            p_value = stats.t.cdf(t_stat, df)
            t_critical = stats.t.ppf(alpha, df)
            reject = t_stat < t_critical
        
        st.markdown("---")
        st.subheader("Résultats")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Statistique t", f"{t_stat:.4f}")
        col2.metric("P-value", f"{p_value:.4f}")
        col3.metric("ddl", f"{df}")
        col4.metric("Décision", "Rejeter H₀" if reject else "Ne pas rejeter H₀")
        
        if reject:
            st.error(f"✅ **Conclusion :** On rejette H₀ au niveau {alpha}. La différence est statistiquement significative.")
        else:
            st.success(f"❌ **Conclusion :** On ne rejette pas H₀ au niveau {alpha}. Pas de différence significative.")
    
    elif test_type == "Intervalle de confiance":
        st.subheader("Intervalle de confiance pour une moyenne")
        
        col1, col2 = st.columns(2)
        
        with col1:
            x_bar = st.number_input("Moyenne observée (x̄)", value=105.0)
            s = st.number_input("Écart-type (s)", value=15.0, min_value=0.1)
            n = st.number_input("Taille échantillon (n)", value=30, min_value=1)
        
        with col2:
            confidence = st.select_slider("Niveau de confiance", options=[0.90, 0.95, 0.99], value=0.95)
            known_sigma = st.checkbox("Écart-type population connu (utiliser Z)", value=True)
        
        alpha = 1 - confidence
        
        if known_sigma or n >= 30:
            z_critical = stats.norm.ppf(1 - alpha/2)
            margin_error = z_critical * (s / np.sqrt(n))
            distribution_used = "Z (loi normale)"
        else:
            t_critical = stats.t.ppf(1 - alpha/2, n-1)
            margin_error = t_critical * (s / np.sqrt(n))
            distribution_used = f"t (Student avec {n-1} ddl)"
        
        lower = x_bar - margin_error
        upper = x_bar + margin_error
        
        st.markdown("---")
        st.subheader("Résultats")
        
        st.success(f"**Intervalle de confiance à {confidence*100}% :** [{lower:.2f}, {upper:.2f}]")
        st.info(f"**Marge d'erreur :** ±{margin_error:.2f}")
        st.info(f"**Distribution utilisée :** {distribution_used}")

with tab3:
    st.header("Exercices Pratiques")
    
    DATA_FILE = Path("data/stats_exercises.json")
    
    exercises = [
        {
            "id": 1,
            "niveau": "B1",
            "question": "Une variable aléatoire X suit une loi normale N(100, 15²). Quelle est la probabilité que X soit supérieure à 115 ?",
            "options": ["0.16", "0.32", "0.68", "0.84"],
            "correct": 0,
            "explication": "P(X > 115) = P(Z > 1) = 1 - Φ(1) ≈ 1 - 0.84 = 0.16"
        },
        {
            "id": 2,
            "niveau": "B1",
            "question": "On lance 20 fois une pièce équilibrée. Quelle est la probabilité d'obtenir exactement 10 fois pile ?",
            "options": ["0.176", "0.25", "0.5", "0.10"],
            "correct": 0,
            "explication": "X ~ B(20, 0.5). P(X=10) = C(20,10) × 0.5²⁰ ≈ 0.176"
        },
        {
            "id": 3,
            "niveau": "B2",
            "question": "Un test statistique donne une p-value de 0.03. Au seuil α=0.05, quelle est la décision ?",
            "options": ["Rejeter H₀", "Ne pas rejeter H₀", "Impossible à décider", "Refaire le test"],
            "correct": 0,
            "explication": "p-value (0.03) < α (0.05), donc on rejette l'hypothèse nulle H₀"
        },
        {
            "id": 4,
            "niveau": "B2",
            "question": "Pour un échantillon de taille n=25 avec s=10, quelle distribution utiliser pour l'IC de la moyenne ?",
            "options": ["Loi de Student", "Loi normale", "Loi du Chi²", "Loi de Poisson"],
            "correct": 0,
            "explication": "Pour n<30 et σ inconnu, on utilise la loi de Student avec n-1=24 degrés de liberté"
        },
        {
            "id": 5,
            "niveau": "B3",
            "question": "Quel test utiliser pour comparer les moyennes de 3 groupes indépendants ?",
            "options": ["ANOVA", "Test t de Student", "Test Z", "Test du Chi²"],
            "correct": 0,
            "explication": "L'ANOVA (Analysis of Variance) est utilisée pour comparer plus de 2 moyennes"
        }
    ]
    
    niveau_filter = st.selectbox("Filtrer par niveau", ["Tous", "B1", "B2", "B3"])
    
    filtered_exercises = exercises if niveau_filter == "Tous" else [e for e in exercises if e["niveau"] == niveau_filter]
    
    for ex in filtered_exercises:
        with st.expander(f"📝 Exercice {ex['id']} - Niveau {ex['niveau']}"):
            st.markdown(f"**Question :** {ex['question']}")
            
            answer = st.radio(
                "Votre réponse :",
                ex["options"],
                key=f"ex_{ex['id']}"
            )
            
            if st.button("Vérifier", key=f"btn_{ex['id']}"):
                selected_index = ex["options"].index(answer)
                if selected_index == ex["correct"]:
                    st.success("✅ Bonne réponse !")
                    st.info(f"**Explication :** {ex['explication']}")
                else:
                    st.error(f"❌ Mauvaise réponse. La bonne réponse est : {ex['options'][ex['correct']]}")
                    st.info(f"**Explication :** {ex['explication']}")

with tab4:
    st.header("📖 Formulaire de Statistiques")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Statistiques Descriptives")
        st.markdown("""
        **Moyenne :**
        $$\\bar{x} = \\frac{1}{n}\\sum_{i=1}^{n} x_i$$
        
        **Variance :**
        $$s^2 = \\frac{1}{n-1}\\sum_{i=1}^{n} (x_i - \\bar{x})^2$$
        
        **Écart-type :**
        $$s = \\sqrt{s^2}$$
        
        **Coefficient de variation :**
        $$CV = \\frac{s}{\\bar{x}} \\times 100\\%$$
        """)
        
        st.subheader("📈 Lois de Probabilité")
        st.markdown("""
        **Loi Normale :** $X \\sim N(\\mu, \\sigma^2)$
        $$f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}} e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}$$
        
        **Loi Binomiale :** $X \\sim B(n, p)$
        $$P(X=k) = C_n^k p^k (1-p)^{n-k}$$
        
        **Loi de Poisson :** $X \\sim P(\\lambda)$
        $$P(X=k) = \\frac{\\lambda^k e^{-\\lambda}}{k!}$$
        """)
    
    with col2:
        st.subheader("🧮 Tests d'Hypothèses")
        st.markdown("""
        **Test Z (moyenne) :**
        $$Z = \\frac{\\bar{x} - \\mu_0}{\\sigma/\\sqrt{n}}$$
        
        **Test t de Student :**
        $$t = \\frac{\\bar{x} - \\mu_0}{s/\\sqrt{n}}$$
        (avec $n-1$ degrés de liberté)
        
        **Intervalle de confiance (95%) :**
        $$IC = \\bar{x} \\pm 1.96 \\times \\frac{\\sigma}{\\sqrt{n}}$$
        
        **Test du Chi² (indépendance) :**
        $$\\chi^2 = \\sum \\frac{(O_{ij} - E_{ij})^2}{E_{ij}}$$
        """)
        
        st.subheader("📏 Corrélation & Régression")
        st.markdown("""
        **Coefficient de corrélation :**
        $$r = \\frac{Cov(X,Y)}{\\sigma_X \\sigma_Y}$$
        
        **Régression linéaire :**
        $$y = a + bx$$
        $$b = \\frac{Cov(X,Y)}{Var(X)}$$
        $$a = \\bar{y} - b\\bar{x}$$
        """)
