import streamlit as st
from pathlib import Path
from modules.database import (
    create_or_update_portfolio, get_portfolio_by_student, update_portfolio_info,
    add_portfolio_project, get_portfolio_projects, delete_portfolio_project,
    add_portfolio_skill, get_portfolio_skills, update_portfolio_skill
)

DB_AVAILABLE = True

st.title("💼 Portfolio Generator")
st.markdown("**Créez un portfolio professionnel pour présenter vos projets**")

tab1, tab2, tab3, tab4 = st.tabs(["👤 Informations", "📁 Projets", "💪 Compétences", "🌐 Aperçu & Export"])

student_id = 1

portfolio = get_portfolio_by_student(student_id)

if not portfolio:
    portfolio_id = create_or_update_portfolio({'full_name': '', 'titre': '', 'bio': '', 'email': '', 'github': '', 'linkedin': ''}, user_id=student_id)
    portfolio = get_portfolio_by_student(student_id)

with tab1:
    st.header("👤 Informations Personnelles")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Photo de profil**")
        uploaded_file = st.file_uploader("Upload photo (optionnel)", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            st.image(uploaded_file, width=200)
    
    with col2:
        nom = st.text_input("Nom complet *", value=portfolio.get('full_name', ''))
        titre = st.text_input("Titre professionnel", 
                              value=portfolio.get('titre', ''),
                              placeholder="Ex: Étudiant en Data Science | Aspirant Data Analyst")
    
    bio = st.text_area("Biographie", 
                      value=portfolio.get('bio', ''),
                      height=120,
                      placeholder="Présentez-vous en quelques lignes...")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        email = st.text_input("Email", value=portfolio.get('email', ''))
    with col2:
        github = st.text_input("GitHub", 
                              value=portfolio.get('github', ''),
                              placeholder="username")
    with col3:
        linkedin = st.text_input("LinkedIn", 
                                value=portfolio.get('linkedin', ''),
                                placeholder="username")
    
    if st.button("💾 Sauvegarder les informations"):
        update_portfolio_info(portfolio['id'], {
            'full_name': nom,
            'titre': titre,
            'bio': bio,
            'email': email,
            'github': github,
            'linkedin': linkedin
        })
        st.success("✅ Informations sauvegardées !")
        st.rerun()

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
            add_portfolio_project({
                'portfolio_id': portfolio['id'],
                'titre': titre_projet,
                'description': description_projet,
                'categorie': categorie,
                'duree': duree,
                'technologies': technologies_projet,
                'github_link': github_link,
                'demo_link': demo_link,
                'resultats': resultats_projet
            })
            st.success("✅ Projet ajouté !")
            st.rerun()
        else:
            st.error("Titre et description sont obligatoires")
    
    st.markdown("---")
    st.markdown("### 📂 Projets Enregistrés")
    
    projets = get_portfolio_projects(portfolio['id'])
    
    if projets:
        for i, projet in enumerate(projets):
            with st.expander(f"📊 {projet['titre']} - {projet['categorie']}"):
                st.markdown(f"**Description :** {projet['description']}")
                st.markdown(f"**Durée :** {projet['duree']}")
                technologies = projet.get('technologies', [])
                if technologies:
                    st.markdown(f"**Technologies :** {', '.join(technologies)}")
                if projet.get('resultats'):
                    st.markdown(f"**Résultats :** {projet['resultats']}")
                if projet.get('github_link'):
                    st.markdown(f"🔗 [Code GitHub]({projet['github_link']})")
                if projet.get('demo_link'):
                    st.markdown(f"🔗 [Démo en ligne]({projet['demo_link']})")
                
                if st.button("🗑️ Supprimer", key=f"del_proj_{projet['id']}"):
                    delete_portfolio_project(projet['id'])
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
    
    existing_skills = get_portfolio_skills(portfolio['id'])
    skills_dict = {skill['nom']: skill['niveau'] for skill in existing_skills}
    
    for categorie, competences in categories_comp.items():
        st.markdown(f"#### {categorie}")
        
        for comp in competences:
            niveau = st.select_slider(
                comp,
                options=["Débutant", "Intermédiaire", "Avancé", "Expert"],
                value=skills_dict.get(comp, "Débutant"),
                key=f"comp_{comp}"
            )
            skills_dict[comp] = niveau
    
    if st.button("💾 Sauvegarder les compétences"):
        for comp, niveau in skills_dict.items():
            existing = next((s for s in existing_skills if s['nom'] == comp), None)
            if existing:
                update_portfolio_skill(existing['id'], niveau)
            else:
                add_portfolio_skill({
                    'portfolio_id': portfolio['id'],
                    'nom': comp,
                    'niveau': niveau,
                    'categorie': next((cat for cat, comps in categories_comp.items() if comp in comps), 'Autre')
                })
        st.success("✅ Compétences sauvegardées !")
        st.rerun()

with tab4:
    st.header("🌐 Aperçu du Portfolio")
    
    if not portfolio.get('full_name'):
        st.warning("⚠️ Veuillez d'abord remplir vos informations personnelles")
    else:
        st.markdown("---")
        
        st.markdown(f"# {portfolio.get('full_name', '')}")
        st.markdown(f"### {portfolio.get('titre', '')}")
        
        if portfolio.get('bio'):
            st.markdown(portfolio['bio'])
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        if portfolio.get('email'):
            col1.markdown(f"📧 {portfolio['email']}")
        if portfolio.get('github'):
            col2.markdown(f"💻 [GitHub](https://github.com/{portfolio['github']})")
        if portfolio.get('linkedin'):
            col3.markdown(f"💼 [LinkedIn](https://linkedin.com/in/{portfolio['linkedin']})")
        
        projets = get_portfolio_projects(portfolio['id'])
        
        if projets:
            st.markdown("---")
            st.markdown("## 📁 Projets")
            
            for projet in projets:
                st.markdown(f"### {projet['titre']}")
                st.markdown(f"**{projet['categorie']}** | {projet['duree']}")
                st.markdown(projet['description'])
                
                technologies = projet.get('technologies', [])
                if technologies:
                    st.markdown("**Technologies :** " + ", ".join([f"`{t}`" for t in technologies]))
                
                if projet.get('resultats'):
                    st.info(f"**📊 Résultats :** {projet['resultats']}")
                
                links = []
                if projet.get('github_link'):
                    links.append(f"[Code]({projet['github_link']})")
                if projet.get('demo_link'):
                    links.append(f"[Démo]({projet['demo_link']})")
                if links:
                    st.markdown(" | ".join(links))
                
                st.markdown("---")
        
        skills = get_portfolio_skills(portfolio['id'])
        
        if skills:
            st.markdown("## 💪 Compétences")
            
            comp_by_level = {"Expert": [], "Avancé": [], "Intermédiaire": [], "Débutant": []}
            
            for skill in skills:
                comp_by_level[skill['niveau']].append(skill['nom'])
            
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
    <title>{portfolio.get('full_name', 'Portfolio')} - Data Science Portfolio</title>
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
            <h1>{portfolio.get('full_name', '')}</h1>
            <div class="subtitle">{portfolio.get('titre', '')}</div>
            <div class="bio">{portfolio.get('bio', '')}</div>
            <div class="contact">
        """
        
        if portfolio.get('email'):
            html_content += f"<a href='mailto:{portfolio['email']}'>📧 {portfolio['email']}</a>"
        if portfolio.get('github'):
            html_content += f"<a href='https://github.com/{portfolio['github']}' target='_blank'>💻 GitHub</a>"
        if portfolio.get('linkedin'):
            html_content += f"<a href='https://linkedin.com/in/{portfolio['linkedin']}' target='_blank'>💼 LinkedIn</a>"
        
        html_content += """
            </div>
        </header>
        """
        
        if projets:
            html_content += "<h2>📁 Projets</h2>"
            for projet in projets:
                html_content += f"""
                <div class="projet">
                    <h3>{projet['titre']}</h3>
                    <p><strong>{projet['categorie']}</strong> | {projet.get('duree', '')}</p>
                    <p>{projet['description']}</p>
                """
                
                technologies = projet.get('technologies', [])
                if technologies:
                    for tech in technologies:
                        html_content += f"<span class='tech'>{tech}</span>"
                
                if projet.get('resultats'):
                    html_content += f"<div class='results'><strong>📊 Résultats :</strong> {projet['resultats']}</div>"
                
                if projet.get('github_link') or projet.get('demo_link'):
                    html_content += "<p>"
                    if projet.get('github_link'):
                        html_content += f"<a href='{projet['github_link']}' target='_blank'>Code GitHub</a>"
                    if projet.get('demo_link'):
                        html_content += f" | <a href='{projet['demo_link']}' target='_blank'>Démo</a>"
                    html_content += "</p>"
                
                html_content += "</div>"
        
        if skills:
            html_content += "<h2>💪 Compétences</h2>"
            comp_by_level = {"Expert": [], "Avancé": [], "Intermédiaire": [], "Débutant": []}
            
            for skill in skills:
                comp_by_level[skill['niveau']].append(skill['nom'])
            
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
