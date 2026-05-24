import sqlite3
from datetime import datetime

DATABASE_FILE = "quiz_leaderboard.db"


def initialize_database():
    """Initialize the leaderboard database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            percentage REAL NOT NULL,
            difficulty TEXT NOT NULL,
            date_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def save_score(username, score, total_questions, difficulty):
    """Save a player's score to the database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    percentage = (score / total_questions) * 100
    
    cursor.execute('''
        INSERT INTO leaderboard (username, score, total_questions, percentage, difficulty)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, score, total_questions, percentage, difficulty))
    
    conn.commit()
    conn.close()
    
    return True


def get_leaderboard(limit=10, difficulty=None):
    """Get top players from leaderboard"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    if difficulty:
        cursor.execute('''
            SELECT username, score, total_questions, percentage, difficulty, date_played, id
            FROM leaderboard
            WHERE difficulty = ?
            ORDER BY percentage DESC, score DESC, date_played DESC
            LIMIT ?
        ''', (difficulty, limit))
    else:
        cursor.execute('''
            SELECT username, score, total_questions, percentage, difficulty, date_played, id
            FROM leaderboard
            ORDER BY percentage DESC, score DESC, date_played DESC
            LIMIT ?
        ''', (limit,))
    
    results = cursor.fetchall()
    conn.close()
    
    return results


def get_player_stats(username):
    """Get statistics for a specific player"""
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


def get_player_history(username, limit=10):
    """Get recent game history for a player"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT username, score, total_questions, percentage, difficulty, date_played
        FROM leaderboard
        WHERE username = ?
        ORDER BY date_played DESC
        LIMIT ?
    ''', (username, limit))
    
    results = cursor.fetchall()
    conn.close()
    
    return results


def get_ranking(username, difficulty=None):
    """Get player's ranking"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
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
