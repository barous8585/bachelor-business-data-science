"""
Module de gestion de la base de données SQLite
Gère toutes les opérations CRUD pour UCO Data Science Hub
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any
import hashlib
import secrets

# Chemin de la base de données
DB_PATH = Path("data/uco_datascience.db")
DB_PATH.parent.mkdir(exist_ok=True)


class Database:
    """Classe principale de gestion de la base de données"""
    
    def __init__(self, db_path: str = None):
        """Initialise la connexion à la base de données"""
        self.db_path = db_path or str(DB_PATH)
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Établit la connexion à la base de données"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par nom
        self.cursor = self.conn.cursor()
        return self
    
    def close(self):
        """Ferme la connexion"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Support du context manager"""
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ferme la connexion automatiquement"""
        self.close()
    
    def execute(self, query: str, params: tuple = ()):
        """Exécute une requête SQL"""
        return self.cursor.execute(query, params)
    
    def fetchall(self) -> List[sqlite3.Row]:
        """Récupère tous les résultats"""
        return self.cursor.fetchall()
    
    def fetchone(self) -> Optional[sqlite3.Row]:
        """Récupère un résultat"""
        return self.cursor.fetchone()
    
    def commit(self):
        """Valide les changements"""
        self.conn.commit()
    
    def row_to_dict(self, row: sqlite3.Row) -> Dict:
        """Convertit une ligne SQL en dictionnaire"""
        return dict(row) if row else None
    
    def rows_to_dicts(self, rows: List[sqlite3.Row]) -> List[Dict]:
        """Convertit des lignes SQL en liste de dictionnaires"""
        return [dict(row) for row in rows]


def init_database():
    """
    Initialise la base de données avec toutes les tables
    """
    with Database() as db:
        # Table des utilisateurs (pour authentification)
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'student',
                full_name TEXT,
                promo TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                avatar_url TEXT,
                bio TEXT
            )
        """)
        
        # Table des cours
        db.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id TEXT UNIQUE NOT NULL,
                prof_id INTEGER,
                prof_name TEXT NOT NULL,
                matiere TEXT NOT NULL,
                chapitre TEXT NOT NULL,
                niveau TEXT NOT NULL,
                content TEXT NOT NULL,
                keywords TEXT,
                date_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                visible BOOLEAN DEFAULT 1,
                nb_exercises_generated INTEGER DEFAULT 0,
                FOREIGN KEY (prof_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)
        
        # Table des exercices
        db.execute("""
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exercise_id TEXT UNIQUE NOT NULL,
                course_id INTEGER,
                matiere TEXT NOT NULL,
                type TEXT NOT NULL,
                question TEXT NOT NULL,
                options TEXT,
                correct_index INTEGER,
                solution TEXT,
                explication TEXT,
                niveau TEXT NOT NULL,
                difficulte TEXT,
                concepts TEXT,
                temps_estime TEXT,
                source TEXT DEFAULT 'IA Gemini',
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            )
        """)
        
        # Table des projets étudiants
        db.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                nom TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT,
                date_debut DATE,
                date_fin DATE,
                status TEXT NOT NULL,
                technologies TEXT,
                taches TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Table des flashcards
        db.execute("""
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                matiere TEXT NOT NULL,
                question TEXT NOT NULL,
                reponse TEXT NOT NULL,
                explication TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                dernier_revu TIMESTAMP,
                difficulte TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Table des portfolios
        db.execute("""
            CREATE TABLE IF NOT EXISTS portfolios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                full_name TEXT,
                titre TEXT,
                bio TEXT,
                email TEXT,
                github TEXT,
                linkedin TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Table des projets de portfolio
        db.execute("""
            CREATE TABLE IF NOT EXISTS portfolio_projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                portfolio_id INTEGER,
                titre TEXT NOT NULL,
                description TEXT NOT NULL,
                categorie TEXT,
                duree TEXT,
                technologies TEXT,
                github TEXT,
                demo TEXT,
                resultats TEXT,
                FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE
            )
        """)
        
        # Table des compétences portfolio
        db.execute("""
            CREATE TABLE IF NOT EXISTS portfolio_skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                portfolio_id INTEGER,
                competence TEXT NOT NULL,
                niveau TEXT NOT NULL,
                FOREIGN KEY (portfolio_id) REFERENCES portfolios(id) ON DELETE CASCADE
            )
        """)
        
        # Table du forum
        db.execute("""
            CREATE TABLE IF NOT EXISTS forum_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                auteur TEXT NOT NULL,
                titre TEXT NOT NULL,
                matiere TEXT NOT NULL,
                contenu TEXT NOT NULL,
                code TEXT,
                tags TEXT,
                date_post TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolu BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)
        
        # Table des réponses forum
        db.execute("""
            CREATE TABLE IF NOT EXISTS forum_replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id INTEGER,
                auteur TEXT NOT NULL,
                contenu TEXT NOT NULL,
                code TEXT,
                date_reply TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES forum_posts(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)
        
        # Table des cas business
        db.execute("""
            CREATE TABLE IF NOT EXISTS business_cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                niveau TEXT NOT NULL,
                domaine TEXT NOT NULL,
                description TEXT NOT NULL,
                objectifs TEXT,
                competences TEXT,
                duree TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table de tracking des progrès étudiants
        db.execute("""
            CREATE TABLE IF NOT EXISTS student_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                exercise_id INTEGER NOT NULL,
                completed BOOLEAN DEFAULT 0,
                score REAL,
                attempts INTEGER DEFAULT 0,
                last_attempt TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (exercise_id) REFERENCES exercises(id) ON DELETE CASCADE,
                UNIQUE(user_id, exercise_id)
            )
        """)
        
        # Index pour améliorer les performances
        db.execute("CREATE INDEX IF NOT EXISTS idx_courses_matiere ON courses(matiere)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_courses_prof ON courses(prof_name)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_exercises_matiere ON exercises(matiere)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_exercises_course ON exercises(course_id)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_forum_matiere ON forum_posts(matiere)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)")
        
        db.commit()
        
        print("✅ Base de données initialisée avec succès !")
        print(f"📁 Fichier : {DB_PATH}")


def hash_password(password: str) -> str:
    """Hash un mot de passe avec SHA-256 + salt"""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${pwd_hash}"


def verify_password(password: str, password_hash: str) -> bool:
    """Vérifie un mot de passe"""
    try:
        salt, pwd_hash = password_hash.split('$')
        return hashlib.sha256((password + salt).encode()).hexdigest() == pwd_hash
    except:
        return False


# ==================== FONCTIONS CRUD ====================

# ========== USERS ==========

def create_user(username: str, email: str, password: str, role: str = 'student', 
                full_name: str = None, promo: str = None) -> Optional[int]:
    """Crée un nouvel utilisateur"""
    with Database() as db:
        try:
            password_hash = hash_password(password)
            db.execute("""
                INSERT INTO users (username, email, password_hash, role, full_name, promo)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, email, password_hash, role, full_name, promo))
            db.commit()
            return db.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None


def get_user_by_username(username: str) -> Optional[Dict]:
    """Récupère un utilisateur par son username"""
    with Database() as db:
        db.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = db.fetchone()
        return db.row_to_dict(row)


def get_user_by_id(user_id: int) -> Optional[Dict]:
    """Récupère un utilisateur par son ID"""
    with Database() as db:
        db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = db.fetchone()
        return db.row_to_dict(row)


def update_last_login(user_id: int):
    """Met à jour la date de dernière connexion"""
    with Database() as db:
        db.execute("UPDATE users SET last_login = ? WHERE id = ?", 
                  (datetime.now(), user_id))
        db.commit()


def get_all_users(role: str = None) -> List[Dict]:
    """Récupère tous les utilisateurs (optionnel: filtre par rôle)"""
    with Database() as db:
        if role:
            db.execute("SELECT * FROM users WHERE role = ? ORDER BY created_at DESC", (role,))
        else:
            db.execute("SELECT * FROM users ORDER BY created_at DESC")
        return db.rows_to_dicts(db.fetchall())


# ========== COURSES ==========

def create_course(course_data: Dict) -> int:
    """Crée un nouveau cours"""
    with Database() as db:
        db.execute("""
            INSERT INTO courses (course_id, prof_id, prof_name, matiere, chapitre, 
                               niveau, content, keywords, visible)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            course_data['course_id'],
            course_data.get('prof_id'),
            course_data['prof_name'],
            course_data['matiere'],
            course_data['chapitre'],
            course_data['niveau'],
            course_data['content'],
            json.dumps(course_data.get('keywords', [])),
            course_data.get('visible', True)
        ))
        db.commit()
        return db.cursor.lastrowid


def get_courses(matiere: str = None, prof_name: str = None, visible_only: bool = True) -> List[Dict]:
    """Récupère les cours avec filtres optionnels"""
    with Database() as db:
        query = "SELECT * FROM courses WHERE 1=1"
        params = []
        
        if visible_only:
            query += " AND visible = 1"
        if matiere:
            query += " AND matiere = ?"
            params.append(matiere)
        if prof_name:
            query += " AND prof_name = ?"
            params.append(prof_name)
        
        query += " ORDER BY date_upload DESC"
        
        db.execute(query, tuple(params))
        rows = db.fetchall()
        
        # Parser les keywords JSON
        courses = []
        for row in rows:
            course = db.row_to_dict(row)
            if course['keywords']:
                course['keywords'] = json.loads(course['keywords'])
            courses.append(course)
        
        return courses


def get_course_by_id(course_id: int) -> Optional[Dict]:
    """Récupère un cours par ID"""
    with Database() as db:
        db.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
        row = db.fetchone()
        if row:
            course = db.row_to_dict(row)
            if course['keywords']:
                course['keywords'] = json.loads(course['keywords'])
            return course
        return None


def update_course_exercises_count(course_id: int, count: int):
    """Met à jour le nombre d'exercices générés pour un cours"""
    with Database() as db:
        db.execute("UPDATE courses SET nb_exercises_generated = ? WHERE id = ?", 
                  (count, course_id))
        db.commit()


# ========== EXERCISES ==========

def create_exercise(exercise_data: Dict) -> int:
    """Crée un nouvel exercice"""
    with Database() as db:
        db.execute("""
            INSERT INTO exercises (exercise_id, course_id, matiere, type, question,
                                 options, correct_index, solution, explication,
                                 niveau, difficulte, concepts, temps_estime, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            exercise_data['exercise_id'],
            exercise_data.get('course_id'),
            exercise_data['matiere'],
            exercise_data['type'],
            exercise_data['question'],
            json.dumps(exercise_data.get('options', [])),
            exercise_data.get('correct_index'),
            exercise_data.get('solution'),
            exercise_data.get('explication'),
            exercise_data['niveau'],
            exercise_data.get('difficulte'),
            json.dumps(exercise_data.get('concepts', [])),
            exercise_data.get('temps_estime'),
            exercise_data.get('source', 'IA Gemini')
        ))
        db.commit()
        return db.cursor.lastrowid


def get_exercises(matiere: str = None, niveau: str = None, exercise_type: str = None,
                 course_id: int = None) -> List[Dict]:
    """Récupère les exercices avec filtres"""
    with Database() as db:
        query = "SELECT * FROM exercises WHERE 1=1"
        params = []
        
        if matiere:
            query += " AND matiere = ?"
            params.append(matiere)
        if niveau:
            query += " AND niveau = ?"
            params.append(niveau)
        if exercise_type:
            query += " AND type = ?"
            params.append(exercise_type)
        if course_id:
            query += " AND course_id = ?"
            params.append(course_id)
        
        query += " ORDER BY date_creation DESC"
        
        db.execute(query, tuple(params))
        rows = db.fetchall()
        
        exercises = []
        for row in rows:
            exercise = db.row_to_dict(row)
            if exercise['options']:
                exercise['options'] = json.loads(exercise['options'])
            if exercise['concepts']:
                exercise['concepts'] = json.loads(exercise['concepts'])
            exercises.append(exercise)
        
        return exercises


def get_exercise_by_id(exercise_id: int) -> Optional[Dict]:
    """Récupère un exercice par ID"""
    with Database() as db:
        db.execute("SELECT * FROM exercises WHERE id = ?", (exercise_id,))
        row = db.fetchone()
        if row:
            exercise = db.row_to_dict(row)
            if exercise['options']:
                exercise['options'] = json.loads(exercise['options'])
            if exercise['concepts']:
                exercise['concepts'] = json.loads(exercise['concepts'])
            return exercise
        return None


# Continuer avec les autres tables...

# ========== PROJECTS ==========

def create_project(project_data: Dict, user_id: int = None) -> int:
    """Crée un nouveau projet"""
    with Database() as db:
        db.execute("""
            INSERT INTO projects (user_id, nom, type, description, date_debut, date_fin,
                                status, technologies, taches)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            project_data['nom'],
            project_data['type'],
            project_data.get('description'),
            project_data.get('date_debut'),
            project_data.get('date_fin'),
            project_data['status'],
            json.dumps(project_data.get('technologies', [])),
            json.dumps(project_data.get('taches', []))
        ))
        db.commit()
        return db.cursor.lastrowid


def get_projects(user_id: int = None, status: str = None) -> List[Dict]:
    """Récupère les projets avec filtres"""
    with Database() as db:
        query = "SELECT * FROM projects WHERE 1=1"
        params = []
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY created_at DESC"
        
        db.execute(query, tuple(params))
        rows = db.fetchall()
        
        projects = []
        for row in rows:
            project = db.row_to_dict(row)
            if project['technologies']:
                project['technologies'] = json.loads(project['technologies'])
            if project['taches']:
                project['taches'] = json.loads(project['taches'])
            projects.append(project)
        
        return projects


def update_project(project_id: int, updates: Dict):
    """Met à jour un projet"""
    with Database() as db:
        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        query = f"UPDATE projects SET {set_clause}, updated_at = ? WHERE id = ?"
        params = list(updates.values()) + [datetime.now(), project_id]
        db.execute(query, tuple(params))
        db.commit()


def delete_project(project_id: int):
    """Supprime un projet"""
    with Database() as db:
        db.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        db.commit()


# ========== FLASHCARDS ==========

def create_flashcard(flashcard_data: Dict, user_id: int = None) -> int:
    """Crée une nouvelle flashcard"""
    with Database() as db:
        db.execute("""
            INSERT INTO flashcards (user_id, matiere, question, reponse, explication,
                                  dernier_revu, difficulte)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            flashcard_data['matiere'],
            flashcard_data['question'],
            flashcard_data['reponse'],
            flashcard_data.get('explication'),
            flashcard_data.get('dernier_revu'),
            flashcard_data.get('difficulte')
        ))
        db.commit()
        return db.cursor.lastrowid


def get_flashcards(user_id: int = None, matiere: str = None) -> List[Dict]:
    """Récupère les flashcards"""
    with Database() as db:
        query = "SELECT * FROM flashcards WHERE 1=1"
        params = []
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        if matiere:
            query += " AND matiere = ?"
            params.append(matiere)
        
        query += " ORDER BY date_creation DESC"
        
        db.execute(query, tuple(params))
        return db.rows_to_dicts(db.fetchall())


def update_flashcard_review(flashcard_id: int, difficulte: str):
    """Met à jour la difficulté et date de révision d'une flashcard"""
    with Database() as db:
        db.execute("""
            UPDATE flashcards 
            SET dernier_revu = ?, difficulte = ?
            WHERE id = ?
        """, (datetime.now(), difficulte, flashcard_id))
        db.commit()


# ========== PORTFOLIOS ==========

def create_or_update_portfolio(portfolio_data: Dict, user_id: int) -> int:
    """Crée ou met à jour un portfolio"""
    with Database() as db:
        # Vérifier si portfolio existe
        db.execute("SELECT id FROM portfolios WHERE user_id = ?", (user_id,))
        existing = db.fetchone()
        
        if existing:
            # Update
            portfolio_id = existing[0]
            db.execute("""
                UPDATE portfolios
                SET full_name = ?, titre = ?, bio = ?, email = ?,
                    github = ?, linkedin = ?, updated_at = ?
                WHERE user_id = ?
            """, (
                portfolio_data.get('full_name'),
                portfolio_data.get('titre'),
                portfolio_data.get('bio'),
                portfolio_data.get('email'),
                portfolio_data.get('github'),
                portfolio_data.get('linkedin'),
                datetime.now(),
                user_id
            ))
        else:
            # Insert
            db.execute("""
                INSERT INTO portfolios (user_id, full_name, titre, bio, email,
                                      github, linkedin)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                portfolio_data.get('full_name'),
                portfolio_data.get('titre'),
                portfolio_data.get('bio'),
                portfolio_data.get('email'),
                portfolio_data.get('github'),
                portfolio_data.get('linkedin')
            ))
            portfolio_id = db.cursor.lastrowid
        
        db.commit()
        return portfolio_id


def get_portfolio(user_id: int) -> Optional[Dict]:
    """Récupère un portfolio"""
    with Database() as db:
        db.execute("SELECT * FROM portfolios WHERE user_id = ?", (user_id,))
        return db.row_to_dict(db.fetchone())


def add_portfolio_project(portfolio_id: int, project_data: Dict) -> int:
    """Ajoute un projet au portfolio"""
    with Database() as db:
        db.execute("""
            INSERT INTO portfolio_projects (portfolio_id, titre, description,
                                           categorie, duree, technologies,
                                           github, demo, resultats)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            portfolio_id,
            project_data['titre'],
            project_data['description'],
            project_data.get('categorie'),
            project_data.get('duree'),
            json.dumps(project_data.get('technologies', [])),
            project_data.get('github'),
            project_data.get('demo'),
            project_data.get('resultats')
        ))
        db.commit()
        return db.cursor.lastrowid


def get_portfolio_projects(portfolio_id: int) -> List[Dict]:
    """Récupère les projets d'un portfolio"""
    with Database() as db:
        db.execute("SELECT * FROM portfolio_projects WHERE portfolio_id = ?", (portfolio_id,))
        rows = db.fetchall()
        
        projects = []
        for row in rows:
            project = db.row_to_dict(row)
            if project['technologies']:
                project['technologies'] = json.loads(project['technologies'])
            projects.append(project)
        
        return projects


def add_portfolio_skill(portfolio_id: int, competence: str, niveau: str) -> int:
    """Ajoute une compétence au portfolio"""
    with Database() as db:
        db.execute("""
            INSERT INTO portfolio_skills (portfolio_id, competence, niveau)
            VALUES (?, ?, ?)
        """, (portfolio_id, competence, niveau))
        db.commit()
        return db.cursor.lastrowid


def get_portfolio_skills(portfolio_id: int) -> List[Dict]:
    """Récupère les compétences d'un portfolio"""
    with Database() as db:
        db.execute("SELECT * FROM portfolio_skills WHERE portfolio_id = ?", (portfolio_id,))
        return db.rows_to_dicts(db.fetchall())


# ========== FORUM ==========

def create_forum_post(post_data: Dict, user_id: int = None) -> int:
    """Crée un nouveau post forum"""
    with Database() as db:
        db.execute("""
            INSERT INTO forum_posts (user_id, auteur, titre, matiere, contenu,
                                    code, tags, resolu)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            post_data['auteur'],
            post_data['titre'],
            post_data['matiere'],
            post_data['contenu'],
            post_data.get('code'),
            json.dumps(post_data.get('tags', [])),
            post_data.get('resolu', False)
        ))
        db.commit()
        return db.cursor.lastrowid


def get_forum_posts(matiere: str = None, resolu: bool = None) -> List[Dict]:
    """Récupère les posts du forum"""
    with Database() as db:
        query = "SELECT * FROM forum_posts WHERE 1=1"
        params = []
        
        if matiere:
            query += " AND matiere = ?"
            params.append(matiere)
        if resolu is not None:
            query += " AND resolu = ?"
            params.append(resolu)
        
        query += " ORDER BY date_post DESC"
        
        db.execute(query, tuple(params))
        rows = db.fetchall()
        
        posts = []
        for row in rows:
            post = db.row_to_dict(row)
            if post['tags']:
                post['tags'] = json.loads(post['tags'])
            posts.append(post)
        
        return posts


def add_forum_reply(post_id: int, reply_data: Dict, user_id: int = None) -> int:
    """Ajoute une réponse à un post"""
    with Database() as db:
        db.execute("""
            INSERT INTO forum_replies (post_id, user_id, auteur, contenu, code)
            VALUES (?, ?, ?, ?, ?)
        """, (
            post_id,
            user_id,
            reply_data['auteur'],
            reply_data['contenu'],
            reply_data.get('code')
        ))
        db.commit()
        return db.cursor.lastrowid


def get_forum_replies(post_id: int) -> List[Dict]:
    """Récupère les réponses d'un post"""
    with Database() as db:
        db.execute("""
            SELECT * FROM forum_replies 
            WHERE post_id = ? 
            ORDER BY date_reply ASC
        """, (post_id,))
        return db.rows_to_dicts(db.fetchall())


def mark_post_resolved(post_id: int):
    """Marque un post comme résolu"""
    with Database() as db:
        db.execute("UPDATE forum_posts SET resolu = 1 WHERE id = ?", (post_id,))
        db.commit()


def mark_post_as_resolved(post_id: int):
    """Alias pour mark_post_resolved"""
    return mark_post_resolved(post_id)


# ========== STATISTICS & ANALYTICS ==========

def get_database_stats() -> Dict:
    """Récupère les statistiques globales de la BDD"""
    with Database() as db:
        stats = {}
        
        # Compter les enregistrements par table
        tables = ['users', 'courses', 'exercises', 'projects', 'flashcards', 
                 'portfolios', 'forum_posts']
        
        for table in tables:
            db.execute(f"SELECT COUNT(*) as count FROM {table}")
            stats[table] = db.fetchone()[0]
        
        # Stats par rôle
        db.execute("SELECT role, COUNT(*) as count FROM users GROUP BY role")
        stats['users_by_role'] = {row[0]: row[1] for row in db.fetchall()}
        
        # Stats par matière (cours)
        db.execute("SELECT matiere, COUNT(*) as count FROM courses GROUP BY matiere")
        stats['courses_by_matiere'] = {row[0]: row[1] for row in db.fetchall()}
        
        # Stats par matière (exercices)
        db.execute("SELECT matiere, COUNT(*) as count FROM exercises GROUP BY matiere")
        stats['exercises_by_matiere'] = {row[0]: row[1] for row in db.fetchall()}
        
        return stats


# ========== ADDITIONAL HELPER FUNCTIONS ==========

def get_project_by_id(project_id: int) -> Dict:
    """Récupère un projet par son ID"""
    with Database() as db:
        db.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = db.fetchone()
        if row:
            project = db.row_to_dict(row)
            if project.get('technologies'):
                project['technologies'] = json.loads(project['technologies'])
            return project
        return None


def get_flashcards_by_matiere(matiere: str) -> List[Dict]:
    """Récupère les flashcards d'une matière"""
    with Database() as db:
        db.execute("SELECT * FROM flashcards WHERE matiere = ?", (matiere,))
        return db.rows_to_dicts(db.fetchall())


def get_portfolio_by_student(student_id: int) -> Dict:
    """Récupère le portfolio d'un étudiant"""
    with Database() as db:
        db.execute("SELECT * FROM portfolios WHERE user_id = ?", (student_id,))
        row = db.fetchone()
        if row:
            return db.row_to_dict(row)
        return None


def get_posts_by_matiere(matiere: str) -> List[Dict]:
    """Récupère les posts d'une matière"""
    with Database() as db:
        db.execute("""
            SELECT p.*, 
                   (SELECT COUNT(*) FROM forum_replies WHERE post_id = p.id) as nb_replies
            FROM forum_posts p
            WHERE p.matiere = ?
            ORDER BY p.date_post DESC
        """, (matiere,))
        
        rows = db.fetchall()
        posts = []
        for row in rows:
            post = db.row_to_dict(row)
            if post.get('tags'):
                post['tags'] = json.loads(post['tags'])
            # Récupérer les réponses
            post['replies'] = get_forum_replies(post['id'])
            posts.append(post)
        
        return posts


def create_business_case_submission(submission_data: Dict) -> int:
    """Crée une soumission de cas business"""
    # Note: Cette table n'existe pas dans le schéma actuel
    # On va la créer si elle n'existe pas
    with Database() as db:
        # Vérifier si la table existe
        db.execute("""
            CREATE TABLE IF NOT EXISTS business_case_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                case_id INTEGER,
                titre TEXT NOT NULL,
                description TEXT,
                resultats TEXT,
                niveau TEXT,
                date_submission DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users(id)
            )
        """)
        db.commit()
        
        # Insérer la soumission
        db.execute("""
            INSERT INTO business_case_submissions 
            (student_id, case_id, titre, description, resultats, niveau)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            submission_data.get('student_id'),
            submission_data.get('case_id'),
            submission_data['titre'],
            submission_data.get('description'),
            submission_data.get('resultats'),
            submission_data.get('niveau')
        ))
        db.commit()
        return db.cursor.lastrowid


def get_business_case_submissions() -> List[Dict]:
    """Récupère toutes les soumissions"""
    with Database() as db:
        # Vérifier si la table existe
        db.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='business_case_submissions'
        """)
        if not db.fetchone():
            return []
        
        db.execute("""
            SELECT * FROM business_case_submissions 
            ORDER BY date_submission DESC
        """)
        return db.rows_to_dicts(db.fetchall())


def update_project_status(project_id: int, status: str):
    """Met à jour le statut d'un projet"""
    with Database() as db:
        db.execute("UPDATE projects SET status = ? WHERE id = ?", (status, project_id))
        db.commit()


def add_project_task(project_id: int, task_name: str):
    """Ajoute une tâche à un projet (stockée en JSON dans le champ tasks)"""
    # Note: Cette fonction nécessite de récupérer les tâches existantes et les modifier
    pass


def update_task_status(project_id: int, task_index: int, done: bool):
    """Met à jour le statut d'une tâche"""
    # Note: Cette fonction nécessite de récupérer les tâches existantes et les modifier
    pass


def delete_task(project_id: int, task_index: int):
    """Supprime une tâche d'un projet"""
    # Note: Cette fonction nécessite de récupérer les tâches existantes et les modifier
    pass


def update_portfolio_info(portfolio_id: int, info_data: Dict):
    """Met à jour les informations d'un portfolio"""
    with Database() as db:
        db.execute("""
            UPDATE portfolios 
            SET full_name = ?, titre = ?, bio = ?, email = ?, github = ?, linkedin = ?
            WHERE id = ?
        """, (
            info_data.get('full_name'),
            info_data.get('titre'),
            info_data.get('bio'),
            info_data.get('email'),
            info_data.get('github'),
            info_data.get('linkedin'),
            portfolio_id
        ))
        db.commit()


def delete_portfolio_project(project_id: int):
    """Supprime un projet du portfolio"""
    with Database() as db:
        db.execute("DELETE FROM portfolio_projects WHERE id = ?", (project_id,))
        db.commit()


def update_portfolio_skill(skill_id: int, niveau: str):
    """Met à jour le niveau d'une compétence"""
    with Database() as db:
        db.execute("UPDATE portfolio_skills SET niveau = ? WHERE id = ?", (niveau, skill_id))
        db.commit()


# Continuer avec les autres tables... (projects, flashcards, etc.)
# Je vais créer les fonctions restantes dans la suite

if __name__ == "__main__":
    # Initialiser la base de données
    init_database()
    
    # Créer un utilisateur admin par défaut
    admin_id = create_user(
        username="admin",
        email="admin@uco.fr",
        password="admin123",
        role="admin",
        full_name="Administrateur UCO"
    )
    
    if admin_id:
        print(f"✅ Utilisateur admin créé (ID: {admin_id})")
    
    print("\n🎉 Configuration initiale terminée !")
