#!/usr/bin/env python3
"""
Script de nettoyage et optimisation du code
"""

import os
import re
from pathlib import Path

def fix_use_container_width(content):
    """Remplace use_container_width par width"""
    # Remplacer use_container_width=True par width="stretch"
    content = re.sub(
        r'use_container_width\s*=\s*True',
        'width="stretch"',
        content
    )
    # Remplacer use_container_width=False par width="content"
    content = re.sub(
        r'use_container_width\s*=\s*False',
        'width="content"',
        content
    )
    return content

def fix_empty_labels(content):
    """Corrige les radio buttons avec labels vides"""
    # Trouver les radio avec label vide et ajouter label_visibility
    content = re.sub(
        r'st\.radio\(\s*""\s*,',
        'st.radio("Options", label_visibility="collapsed",',
        content
    )
    return content

def process_file(filepath):
    """Traite un fichier Python"""
    print(f"📝 Traitement de {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Appliquer les corrections
    content = fix_use_container_width(content)
    content = fix_empty_labels(content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Corrections appliquées")
        return True
    else:
        print(f"  ⏭️  Aucune correction nécessaire")
        return False

def main():
    """Fonction principale"""
    base_dir = Path("/Users/thiernoousmanebarry/Desktop/bachelor business data science")
    
    # Fichiers à traiter
    files_to_process = [
        base_dir / "app.py",
        base_dir / "modules" / "stats_proba.py",
        base_dir / "modules" / "code_assistant.py",
        base_dir / "modules" / "business_cases.py",
        base_dir / "modules" / "project_manager.py",
        base_dir / "modules" / "revision_planner.py",
        base_dir / "modules" / "resources_library.py",
        base_dir / "modules" / "interview_simulator.py",
        base_dir / "modules" / "portfolio_generator.py",
        base_dir / "modules" / "forum.py",
        base_dir / "modules" / "dataset_generator.py",
        base_dir / "modules" / "teacher_space.py",
    ]
    
    print("🚀 Démarrage du nettoyage du code...\n")
    
    corrected_count = 0
    for filepath in files_to_process:
        if filepath.exists():
            if process_file(filepath):
                corrected_count += 1
        else:
            print(f"⚠️  Fichier introuvable: {filepath}")
    
    print(f"\n✅ Nettoyage terminé ! {corrected_count} fichier(s) corrigé(s)")

if __name__ == "__main__":
    main()
