import streamlit as st
import json
from pathlib import Path
import base64

st.title("💼 Portfolio Generator")
st.markdown("**Créez un portfolio professionnel pour présenter vos projets**")

DATA_FILE = Path("data/portfolio.json")
DATA_FILE.parent.mkdir(exist_ok=True)

def load_portfolio():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"info": {}, "projets": [], "competences": {}}

def save_portfolio(portfolio):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(portfolio, f, ensure_ascii=False, indent=2)

tab1, tab2, tab3, tab4 = st.tabs(["👤 Informations", "📁 Projets", "💪 Compétences", "🌐 Aperçu & Export"])

portfolio = load_portfolio()

with tab1:
    st.header("👤 Informations Personnelles")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Photo de profil**")
        uploaded_file = st.file_uploader("Upload photo (optionnel)", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            st.image(uploaded_file, width=200)
    
    with col2:
        nom = st.text_input("Nom complet *", value=portfolio.get('info', {}).get('nom', ''))
        titre = st.text_input("Titre professionnel", 
                              value=portfolio.get('info', {}).get('titre', ''),
                              placeholder="Ex: Étudiant en Data Science | Aspirant Data Analyst")
    
    bio = st.text_area("Biographie", 
                      value=portfolio.get('info', {}).get('bio', ''),
                      height=120,
                      placeholder="Présentez-vous en quelques lignes...")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        email = st.text_input("Email", value=portfolio.get('info', {}).get('email', ''))
    with col2:
        github = st.text_input("GitHub", 
                              value=portfolio.get('info', {}).get('github', ''),
                              placeholder="username")
    with col3:
        linkedin = st.text_input("LinkedIn", 
                                value=portfolio.get('info', {}).get('linkedin', ''),
                                placeholder="username")
    
    if st.button("💾 Sauvegarder les informations"):
        portfolio['info'] = {
            'nom': nom,
            'titre': titre,
            'bio': bio,
            'email': email,
            'github': github,
            'linkedin': linkedin
        }
        save_portfolio(portfolio)
        st.success("✅ Informations sauvegardées !")

with tab2:
    st.header("📁 Mes Projets")
    
    st.markdown("### ➕ Ajouter un Projet")
    
    titre_projet = st.text_input("Titre du projet")
    description_projet = st.text_area("Description courte", height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        categorie = st.selectbox("Catégorie", 
                                 ["Machine Learning", "Data Analysis", "Data Visualization", 
                                  "Web Scraping", "NLP", "Deep Learning", "Autre"])
    with col2:
        duree = st.text_input("Durée", placeholder="Ex: 2 semaines")
    
    technologies_projet = st.multiselect(
        "Technologies utilisées",
        ["Python", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch",
         "Matplotlib", "Seaborn", "Plotly", "SQL", "MongoDB", "Streamlit",
         "Flask", "FastAPI", "Docker", "Git", "Jupyter", "R"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        github_link = st.text_input("Lien GitHub", placeholder="https://github.com/...")
    with col2:
        demo_link = st.text_input("Lien démo (optionnel)", placeholder="https://...")
    
    resultats_projet = st.text_area("Résultats & Impact", 
                                   placeholder="Ex: Précision de 95%, Réduction du temps de traitement de 40%",
                                   height=80)
    
    if st.button("➕ Ajouter le projet"):
        if titre_projet and description_projet:
            nouveau_projet = {
                'titre': titre_projet,
                'description': description_projet,
                'categorie': categorie,
                'duree': duree,
                'technologies': technologies_projet,
                'github': github_link,
                'demo': demo_link,
                'resultats': resultats_projet
            }
            
            if 'projets' not in portfolio:
                portfolio['projets'] = []
            
            portfolio['projets'].append(nouveau_projet)
            save_portfolio(portfolio)
            st.success("✅ Projet ajouté !")
            st.rerun()
        else:
            st.error("Titre et description sont obligatoires")
    
    st.markdown("---")
    st.markdown("### 📂 Projets Enregistrés")
    
    if portfolio.get('projets'):
        for i, projet in enumerate(portfolio['projets']):
            with st.expander(f"📊 {projet['titre']} - {projet['categorie']}"):
                st.markdown(f"**Description :** {projet['description']}")
                st.markdown(f"**Durée :** {projet['duree']}")
                st.markdown(f"**Technologies :** {', '.join(projet['technologies'])}")
                if projet.get('resultats'):
                    st.markdown(f"**Résultats :** {projet['resultats']}")
                if projet.get('github'):
                    st.markdown(f"🔗 [Code GitHub]({projet['github']})")
                if projet.get('demo'):
                    st.markdown(f"🔗 [Démo en ligne]({projet['demo']})")
                
                if st.button("🗑️ Supprimer", key=f"del_proj_{i}"):
                    portfolio['projets'].pop(i)
                    save_portfolio(portfolio)
                    st.rerun()
    else:
        st.info("Aucun projet ajouté pour le moment")

with tab3:
    st.header("💪 Compétences")
    
    st.markdown("### Niveau de Maîtrise")
    
    categories_comp = {
        "Langages": ["Python", "R", "SQL", "JavaScript"],
        "Libraries Data": ["Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch"],
        "Visualisation": ["Matplotlib", "Seaborn", "Plotly", "Tableau", "Power BI"],
        "Outils": ["Git", "Docker", "Jupyter", "VS Code", "Linux"],
        "Soft Skills": ["Communication", "Travail d'équipe", "Résolution de problèmes", "Gestion de projet"]
    }
    
    if 'competences' not in portfolio:
        portfolio['competences'] = {}
    
    for categorie, competences in categories_comp.items():
        st.markdown(f"#### {categorie}")
        
        for comp in competences:
            niveau = st.select_slider(
                comp,
                options=["Débutant", "Intermédiaire", "Avancé", "Expert"],
                value=portfolio['competences'].get(comp, "Débutant"),
                key=f"comp_{comp}"
            )
            portfolio['competences'][comp] = niveau
    
    if st.button("💾 Sauvegarder les compétences"):
        save_portfolio(portfolio)
        st.success("✅ Compétences sauvegardées !")

with tab4:
    st.header("🌐 Aperçu du Portfolio")
    
    if not portfolio.get('info', {}).get('nom'):
        st.warning("⚠️ Veuillez d'abord remplir vos informations personnelles")
    else:
        st.markdown("---")
        
        st.markdown(f"# {portfolio['info'].get('nom', '')}")
        st.markdown(f"### {portfolio['info'].get('titre', '')}")
        
        if portfolio['info'].get('bio'):
            st.markdown(portfolio['info']['bio'])
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        if portfolio['info'].get('email'):
            col1.markdown(f"📧 {portfolio['info']['email']}")
        if portfolio['info'].get('github'):
            col2.markdown(f"💻 [GitHub](https://github.com/{portfolio['info']['github']})")
        if portfolio['info'].get('linkedin'):
            col3.markdown(f"💼 [LinkedIn](https://linkedin.com/in/{portfolio['info']['linkedin']})")
        
        if portfolio.get('projets'):
            st.markdown("---")
            st.markdown("## 📁 Projets")
            
            for projet in portfolio['projets']:
                st.markdown(f"### {projet['titre']}")
                st.markdown(f"**{projet['categorie']}** | {projet['duree']}")
                st.markdown(projet['description'])
                
                if projet.get('technologies'):
                    st.markdown("**Technologies :** " + ", ".join([f"`{t}`" for t in projet['technologies']]))
                
                if projet.get('resultats'):
                    st.info(f"**📊 Résultats :** {projet['resultats']}")
                
                links = []
                if projet.get('github'):
                    links.append(f"[Code]({projet['github']})")
                if projet.get('demo'):
                    links.append(f"[Démo]({projet['demo']})")
                if links:
                    st.markdown(" | ".join(links))
                
                st.markdown("---")
        
        if portfolio.get('competences'):
            st.markdown("## 💪 Compétences")
            
            comp_by_level = {"Expert": [], "Avancé": [], "Intermédiaire": [], "Débutant": []}
            
            for comp, niveau in portfolio['competences'].items():
                comp_by_level[niveau].append(comp)
            
            for niveau in ["Expert", "Avancé", "Intermédiaire", "Débutant"]:
                if comp_by_level[niveau]:
                    st.markdown(f"**{niveau} :** " + ", ".join([f"`{c}`" for c in comp_by_level[niveau]]))
        
        st.markdown("---")
        st.markdown("---")
        
        st.subheader("📥 Export")
        
        html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{portfolio['info'].get('nom', 'Portfolio')} - Data Science Portfolio</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background: #f4f4f4; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 40px; }}
        header {{ text-align: center; padding: 40px 0; border-bottom: 3px solid #667eea; }}
        h1 {{ color: #667eea; font-size: 2.5em; margin-bottom: 10px; }}
        h2 {{ color: #667eea; margin-top: 30px; margin-bottom: 15px; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        .subtitle {{ color: #666; font-size: 1.3em; margin-bottom: 15px; }}
        .bio {{ max-width: 800px; margin: 20px auto; text-align: center; color: #555; }}
        .contact {{ text-align: center; margin: 20px 0; }}
        .contact a {{ color: #667eea; text-decoration: none; margin: 0 15px; }}
        .projet {{ background: #f9f9f9; padding: 20px; margin: 20px 0; border-left: 4px solid #667eea; border-radius: 5px; }}
        .projet h3 {{ color: #333; margin-bottom: 10px; }}
        .tech {{ display: inline-block; background: #667eea; color: white; padding: 5px 10px; margin: 5px 5px 5px 0; border-radius: 3px; font-size: 0.9em; }}
        .competences {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 15px 0; }}
        .comp-item {{ background: #eef; padding: 8px 15px; border-radius: 5px; }}
        .results {{ background: #e8f5e9; padding: 15px; border-radius: 5px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{portfolio['info'].get('nom', '')}</h1>
            <div class="subtitle">{portfolio['info'].get('titre', '')}</div>
            <div class="bio">{portfolio['info'].get('bio', '')}</div>
            <div class="contact">
        """
        
        if portfolio['info'].get('email'):
            html_content += f"<a href='mailto:{portfolio['info']['email']}'>📧 {portfolio['info']['email']}</a>"
        if portfolio['info'].get('github'):
            html_content += f"<a href='https://github.com/{portfolio['info']['github']}' target='_blank'>💻 GitHub</a>"
        if portfolio['info'].get('linkedin'):
            html_content += f"<a href='https://linkedin.com/in/{portfolio['info']['linkedin']}' target='_blank'>💼 LinkedIn</a>"
        
        html_content += """
            </div>
        </header>
        """
        
        if portfolio.get('projets'):
            html_content += "<h2>📁 Projets</h2>"
            for projet in portfolio['projets']:
                html_content += f"""
                <div class="projet">
                    <h3>{projet['titre']}</h3>
                    <p><strong>{projet['categorie']}</strong> | {projet.get('duree', '')}</p>
                    <p>{projet['description']}</p>
                """
                
                if projet.get('technologies'):
                    for tech in projet['technologies']:
                        html_content += f"<span class='tech'>{tech}</span>"
                
                if projet.get('resultats'):
                    html_content += f"<div class='results'><strong>📊 Résultats :</strong> {projet['resultats']}</div>"
                
                if projet.get('github') or projet.get('demo'):
                    html_content += "<p>"
                    if projet.get('github'):
                        html_content += f"<a href='{projet['github']}' target='_blank'>Code GitHub</a>"
                    if projet.get('demo'):
                        html_content += f" | <a href='{projet['demo']}' target='_blank'>Démo</a>"
                    html_content += "</p>"
                
                html_content += "</div>"
        
        if portfolio.get('competences'):
            html_content += "<h2>💪 Compétences</h2>"
            comp_by_level = {"Expert": [], "Avancé": [], "Intermédiaire": [], "Débutant": []}
            
            for comp, niveau in portfolio['competences'].items():
                comp_by_level[niveau].append(comp)
            
            for niveau in ["Expert", "Avancé", "Intermédiaire", "Débutant"]:
                if comp_by_level[niveau]:
                    html_content += f"<p><strong>{niveau} :</strong> "
                    for comp in comp_by_level[niveau]:
                        html_content += f"<span class='comp-item'>{comp}</span> "
                    html_content += "</p>"
        
        html_content += """
    </div>
</body>
</html>
        """
        
        st.download_button(
            label="📥 Télécharger en HTML",
            data=html_content,
            file_name="portfolio.html",
            mime="text/html"
        )
        
        st.info("💡 **Astuce :** Vous pouvez héberger ce fichier HTML gratuitement sur GitHub Pages, Netlify ou Vercel !")
