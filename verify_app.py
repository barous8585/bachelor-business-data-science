#!/usr/bin/env python3
"""
Script de vérification complète de l'application UCO Data Science Hub
Vérifie que tous les modules peuvent être importés sans erreur
"""

import sys
from pathlib import Path

# Ajouter le répertoire courant au path
sys.path.insert(0, str(Path(__file__).parent))

def test_module(module_path: str, module_name: str):
    """Test l'import d'un module"""
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Créer un namespace pour l'exécution
        namespace = {}
        exec(code, namespace)
        
        print(f"✅ {module_name:30s} OK")
        return True
    except Exception as e:
        print(f"❌ {module_name:30s} ERREUR: {str(e)[:80]}")
        return False

def main():
    print("=" * 80)
    print("🔍 VÉRIFICATION COMPLÈTE DE L'APPLICATION")
    print("=" * 80)
    print()
    
    # Test database
    print("📦 Test du module database...")
    try:
        from modules.database import (
            create_user, get_user_by_username, create_course, get_courses,
            create_exercise, get_exercises, create_project, get_projects,
            create_flashcard, get_flashcards, create_forum_post, get_forum_posts,
            create_or_update_portfolio, get_portfolio_by_student,
            add_portfolio_project, get_portfolio_projects,
            add_portfolio_skill, get_portfolio_skills,
            mark_post_as_resolved, get_project_by_id,
            get_flashcards_by_matiere, get_posts_by_matiere,
            update_project_status, update_portfolio_info,
            delete_portfolio_project, update_portfolio_skill,
            create_business_case_submission, get_business_case_submissions
        )
        print("✅ database.py                  OK - Toutes les fonctions importées")
    except ImportError as e:
        print(f"❌ database.py                  ERREUR: {e}")
        return False
    
    print()
    print("📦 Test des modules Streamlit...")
    
    modules_to_test = [
        ("modules/teacher_space.py", "teacher_space.py"),
        ("modules/project_manager.py", "project_manager.py"),
        ("modules/revision_planner.py", "revision_planner.py"),
        ("modules/forum.py", "forum.py"),
        ("modules/portfolio_generator.py", "portfolio_generator.py"),
        ("modules/business_cases.py", "business_cases.py"),
        ("modules/stats_proba.py", "stats_proba.py"),
        ("modules/code_assistant.py", "code_assistant.py"),
        ("modules/resources_library.py", "resources_library.py"),
        ("modules/interview_simulator.py", "interview_simulator.py"),
        ("modules/dataset_generator.py", "dataset_generator.py"),
    ]
    
    results = []
    for module_path, module_name in modules_to_test:
        if Path(module_path).exists():
            results.append(test_module(module_path, module_name))
        else:
            print(f"⚠️  {module_name:30s} FICHIER NON TROUVÉ")
            results.append(False)
    
    print()
    print("=" * 80)
    
    success_count = sum(results)
    total_count = len(results)
    
    if all(results):
        print(f"✅ SUCCÈS ! Tous les {total_count} modules testés sont OK")
        print("🚀 L'application est prête à être utilisée")
        return True
    else:
        print(f"⚠️  {success_count}/{total_count} modules OK")
        print(f"❌ {total_count - success_count} module(s) avec des erreurs")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
