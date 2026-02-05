"""
Script de migration des données JSON vers SQLite
Transfère toutes les données existantes des fichiers JSON vers la base de données SQLite
"""

import json
from pathlib import Path
from datetime import datetime
from modules.database import (
    create_course, create_exercise, create_project, create_flashcard,
    create_forum_post, add_forum_reply, create_or_update_portfolio, 
    add_portfolio_project, add_portfolio_skill
)

def migrate_courses():
    """Migrer les cours depuis courses_list.json"""
    courses_file = Path("data/courses/courses_list.json")
    if not courses_file.exists():
        print("❌ Aucun fichier courses_list.json trouvé")
        return 0
    
    with open(courses_file, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    migrated = 0
    for course in courses:
        try:
            create_course(course)
            migrated += 1
        except Exception as e:
            print(f"⚠️ Erreur cours '{course.get('chapitre')}': {e}")
    
    print(f"✅ {migrated} cours migrés")
    return migrated

def migrate_exercises():
    """Migrer les exercices depuis exercises.json"""
    exercises_file = Path("data/exercises/exercises.json")
    if not exercises_file.exists():
        print("❌ Aucun fichier exercises.json trouvé")
        return 0
    
    with open(exercises_file, 'r', encoding='utf-8') as f:
        exercises = json.load(f)
    
    migrated = 0
    for exercise in exercises:
        try:
            create_exercise(exercise)
            migrated += 1
        except Exception as e:
            print(f"⚠️ Erreur exercice: {e}")
    
    print(f"✅ {migrated} exercices migrés")
    return migrated

def migrate_projects():
    """Migrer les projets depuis projects.json"""
    projects_file = Path("data/projects.json")
    if not projects_file.exists():
        print("❌ Aucun fichier projects.json trouvé")
        return 0
    
    with open(projects_file, 'r', encoding='utf-8') as f:
        projects = json.load(f)
    
    migrated = 0
    for project in projects:
        try:
            project['student_id'] = None
            create_project(project)
            migrated += 1
        except Exception as e:
            print(f"⚠️ Erreur projet '{project.get('nom')}': {e}")
    
    print(f"✅ {migrated} projets migrés")
    return migrated

def migrate_flashcards():
    """Migrer les flashcards depuis flashcards.json"""
    flashcards_file = Path("data/flashcards.json")
    if not flashcards_file.exists():
        print("❌ Aucun fichier flashcards.json trouvé")
        return 0
    
    with open(flashcards_file, 'r', encoding='utf-8') as f:
        flashcards = json.load(f)
    
    migrated = 0
    for flashcard in flashcards:
        try:
            flashcard['student_id'] = None
            create_flashcard(flashcard)
            migrated += 1
        except Exception as e:
            print(f"⚠️ Erreur flashcard: {e}")
    
    print(f"✅ {migrated} flashcards migrées")
    return migrated

def migrate_forum():
    """Migrer les posts du forum depuis forum_posts.json"""
    forum_file = Path("data/forum_posts.json")
    if not forum_file.exists():
        print("❌ Aucun fichier forum_posts.json trouvé")
        return 0
    
    with open(forum_file, 'r', encoding='utf-8') as f:
        posts = json.load(f)
    
    migrated_posts = 0
    migrated_replies = 0
    
    for post in posts:
        try:
            post_data = {
                'auteur': post['auteur'],
                'student_id': None,
                'titre': post['titre'],
                'matiere': post['matiere'],
                'contenu': post['contenu'],
                'code': post.get('code'),
                'tags': post.get('tags', []),
                'resolu': post.get('resolu', False)
            }
            
            post_id = create_forum_post(post_data, user_id=None)
            migrated_posts += 1
            
            if 'reponses' in post:
                for reply in post['reponses']:
                    try:
                        add_forum_reply(post_id, {
                            'auteur': reply['auteur'],
                            'contenu': reply['contenu'],
                            'code': reply.get('code')
                        }, user_id=None)
                        migrated_replies += 1
                    except Exception as e:
                        print(f"⚠️ Erreur réponse forum: {e}")
        
        except Exception as e:
            print(f"⚠️ Erreur post forum '{post.get('titre')}': {e}")
    
    print(f"✅ {migrated_posts} posts forum et {migrated_replies} réponses migrés")
    return migrated_posts + migrated_replies

def migrate_portfolio():
    """Migrer le portfolio depuis portfolio.json"""
    portfolio_file = Path("data/portfolio.json")
    if not portfolio_file.exists():
        print("❌ Aucun fichier portfolio.json trouvé")
        return 0
    
    with open(portfolio_file, 'r', encoding='utf-8') as f:
        portfolio_data = json.load(f)
    
    info = portfolio_data.get('info', {})
    if not info.get('nom'):
        print("❌ Aucune information portfolio à migrer")
        return 0
    
    try:
        portfolio_id = create_or_update_portfolio({
            'nom': info.get('nom', ''),
            'titre': info.get('titre', ''),
            'bio': info.get('bio', ''),
            'email': info.get('email', ''),
            'github': info.get('github', ''),
            'linkedin': info.get('linkedin', '')
        }, user_id=1)
        
        migrated = 1
        
        projets = portfolio_data.get('projets', [])
        for projet in projets:
            try:
                add_portfolio_project(portfolio_id, {
                    'titre': projet['titre'],
                    'description': projet['description'],
                    'categorie': projet['categorie'],
                    'duree': projet.get('duree', ''),
                    'technologies': projet.get('technologies', []),
                    'github_link': projet.get('github', ''),
                    'demo_link': projet.get('demo', ''),
                    'resultats': projet.get('resultats', '')
                })
                migrated += 1
            except Exception as e:
                print(f"⚠️ Erreur projet portfolio: {e}")
        
        competences = portfolio_data.get('competences', {})
        for nom, niveau in competences.items():
            try:
                add_portfolio_skill(portfolio_id, nom, niveau)
                migrated += 1
            except Exception as e:
                print(f"⚠️ Erreur compétence portfolio: {e}")
        
        print(f"✅ Portfolio migré ({migrated} éléments)")
        return migrated
    
    except Exception as e:
        print(f"⚠️ Erreur migration portfolio: {e}")
        return 0

def backup_json_files():
    """Créer une sauvegarde des fichiers JSON"""
    backup_dir = Path("data/backup_json")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    json_files = [
        "data/courses/courses_list.json",
        "data/exercises/exercises.json",
        "data/projects.json",
        "data/flashcards.json",
        "data/forum_posts.json",
        "data/portfolio.json"
    ]
    
    backed_up = 0
    for json_file in json_files:
        src = Path(json_file)
        if src.exists():
            dst = backup_dir / src.name
            import shutil
            shutil.copy2(src, dst)
            backed_up += 1
    
    print(f"✅ {backed_up} fichiers JSON sauvegardés dans {backup_dir}")
    return backed_up

def main():
    """Exécuter la migration complète"""
    print("=" * 60)
    print("🔄 MIGRATION DES DONNÉES JSON → SQLite")
    print("=" * 60)
    print()
    
    print("📦 Étape 1 : Sauvegarde des fichiers JSON...")
    backup_json_files()
    print()
    
    print("📦 Étape 2 : Migration des cours...")
    courses_count = migrate_courses()
    print()
    
    print("📦 Étape 3 : Migration des exercices...")
    exercises_count = migrate_exercises()
    print()
    
    print("📦 Étape 4 : Migration des projets...")
    projects_count = migrate_projects()
    print()
    
    print("📦 Étape 5 : Migration des flashcards...")
    flashcards_count = migrate_flashcards()
    print()
    
    print("📦 Étape 6 : Migration du forum...")
    forum_count = migrate_forum()
    print()
    
    print("📦 Étape 7 : Migration du portfolio...")
    portfolio_count = migrate_portfolio()
    print()
    
    print("=" * 60)
    print("✅ MIGRATION TERMINÉE !")
    print("=" * 60)
    print(f"Total migré :")
    print(f"  - Cours : {courses_count}")
    print(f"  - Exercices : {exercises_count}")
    print(f"  - Projets : {projects_count}")
    print(f"  - Flashcards : {flashcards_count}")
    print(f"  - Forum : {forum_count}")
    print(f"  - Portfolio : {portfolio_count}")
    print()
    print("💡 Les fichiers JSON originaux ont été sauvegardés dans data/backup_json/")
    print("💡 Vous pouvez maintenant lancer l'application avec la base SQLite !")

if __name__ == "__main__":
    main()
