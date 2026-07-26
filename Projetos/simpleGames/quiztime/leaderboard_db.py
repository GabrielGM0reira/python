import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_FILE = str(BASE_DIR / "quiz_leaderboard.db")

def get_current_season():
    """Get current season string (e.g., 'Spring 2026', 'Summer 2026')"""
    month = datetime.now().month
    year = datetime.now().year
    
    if month in [3, 4, 5]:
        season = "Spring"
    elif month in [6, 7, 8]:
        season = "Summer"
    elif month in [9, 10, 11]:
        season = "Autumn"
    else:
        season = "Winter"
    
    return f"{season} {year}"


def initialize_database():
    """Initialize the leaderboard database with seasonal support"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Check if season column exists, if not, add it
    cursor.execute("PRAGMA table_info(leaderboard)")
    columns = [column[1] for column in cursor.fetchall()]
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            percentage REAL NOT NULL,
            difficulty TEXT NOT NULL,
            season TEXT DEFAULT 'Spring 2026',
            date_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Add season column if it doesn't exist (for existing databases)
    if 'season' not in columns:
        try:
            cursor.execute('ALTER TABLE leaderboard ADD COLUMN season TEXT DEFAULT "Spring 2026"')
        except sqlite3.OperationalError:
            pass  # Column already exists
    
    conn.commit()
    conn.close()


def save_score(username, score, total_questions, difficulty):
    """Save a player's score to the database with current season"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    percentage = (score / total_questions) * 100
    season = get_current_season()
    
    cursor.execute('''
        INSERT INTO leaderboard (username, score, total_questions, percentage, difficulty, season)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, score, total_questions, percentage, difficulty, season))
    
    conn.commit()
    conn.close()
    
    return True


def get_leaderboard(limit=10, difficulty=None, season=None):
    """Get top players from leaderboard, optionally filtered by season"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Build WHERE clause based on filters
    where_clause = "1=1"
    params = []
    
    if difficulty:
        where_clause += " AND difficulty = ?"
        params.append(difficulty)
    
    if season:
        where_clause += " AND season = ?"
        params.append(season)
    
    params.append(limit)
    
    cursor.execute(f'''
        SELECT username, score, total_questions, percentage, difficulty, date_played, id, season
        FROM leaderboard
        WHERE {where_clause}
        ORDER BY percentage DESC, score DESC, date_played DESC
        LIMIT ?
    ''', params)
    
    results = cursor.fetchall()
    conn.close()
    
    return results


def get_player_stats(username):
    """Get all-time statistics for a specific player"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) as total_plays,
               ROUND(AVG(percentage), 2) as avg_score,
               MAX(percentage) as best_score,
               MAX(score) as best_score_raw,
               MAX(total_questions) as best_total_q
        FROM leaderboard
        WHERE username = ?
    ''', (username,))
    
    result = cursor.fetchone()
    conn.close()
    
    return result


def get_seasonal_stats(username, season=None):
    """Get seasonal statistics for a specific player"""
    if season is None:
        season = get_current_season()
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) as total_plays,
               ROUND(AVG(percentage), 2) as avg_score,
               MAX(percentage) as best_score,
               MAX(score) as best_score_raw,
               MAX(total_questions) as best_total_q
        FROM leaderboard
        WHERE username = ? AND season = ?
    ''', (username, season))
    
    result = cursor.fetchone()
    conn.close()
    
    return result


def get_all_seasons():
    """Get list of all seasons with scores"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT DISTINCT season
        FROM leaderboard
        ORDER BY season DESC
    ''')
    
    seasons = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return seasons


def get_player_history(username, limit=10, season=None):
    """Get recent game history for a player, optionally filtered by season"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    if season:
        cursor.execute('''
            SELECT username, score, total_questions, percentage, difficulty, date_played, season
            FROM leaderboard
            WHERE username = ? AND season = ?
            ORDER BY date_played DESC
            LIMIT ?
        ''', (username, limit, season))
    else:
        cursor.execute('''
            SELECT username, score, total_questions, percentage, difficulty, date_played, season
            FROM leaderboard
            WHERE username = ?
            ORDER BY date_played DESC
            LIMIT ?
        ''', (username, limit))
    
    results = cursor.fetchall()
    conn.close()
    
    return results


def get_ranking(username, difficulty=None, season=None):
    """Get player's ranking, optionally filtered by season"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    if season:
        if difficulty:
            cursor.execute('''
                SELECT COUNT(*) + 1 as ranking
                FROM (
                    SELECT DISTINCT username, MAX(percentage) as max_percentage
                    FROM leaderboard
                    WHERE difficulty = ? AND season = ?
                    GROUP BY username
                    HAVING max_percentage > (
                        SELECT MAX(percentage)
                        FROM leaderboard
                        WHERE username = ? AND difficulty = ? AND season = ?
                    )
                )
            ''', (difficulty, season, username, difficulty, season))
        else:
            cursor.execute('''
                SELECT COUNT(*) + 1 as ranking
                FROM (
                    SELECT DISTINCT username, MAX(percentage) as max_percentage
                    FROM leaderboard
                    WHERE season = ?
                    GROUP BY username
                    HAVING max_percentage > (
                        SELECT MAX(percentage)
                        FROM leaderboard
                        WHERE username = ? AND season = ?
                    )
                )
            ''', (season, username, season))
    else:
        if difficulty:
            cursor.execute('''
                SELECT COUNT(*) + 1 as ranking
                FROM (
                    SELECT DISTINCT username, MAX(percentage) as max_percentage
                    FROM leaderboard
                    WHERE difficulty = ?
                    GROUP BY username
                    HAVING max_percentage > (
                        SELECT MAX(percentage)
                        FROM leaderboard
                        WHERE username = ? AND difficulty = ?
                    )
                )
            ''', (difficulty, username, difficulty))
        else:
            cursor.execute('''
                SELECT COUNT(*) + 1 as ranking
                FROM (
                    SELECT DISTINCT username, MAX(percentage) as max_percentage
                    FROM leaderboard
                    GROUP BY username
                    HAVING max_percentage > (
                        SELECT MAX(percentage)
                        FROM leaderboard
                        WHERE username = ?
                    )
                )
            ''', (username,))
    
    result = cursor.fetchone()
    conn.close()
    
    ranking = result[0] if result[0] else 1
    return ranking


def clear_database():
    """Clear all leaderboard data (admin function)"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM leaderboard')
    conn.commit()
    conn.close()
