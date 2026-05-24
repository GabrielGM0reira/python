# Quiz Game with Leaderboard System

## Overview
The quiz game now includes a comprehensive leaderboard system with SQLite database integration. Players can track their scores, rankings, and statistics across multiple game sessions.

## Features

### 🎮 Game Features
- **Username Input**: Each player enters a 2-20 character username at the start
- **Three Difficulty Levels**: Easy (10 questions), Medium (30 questions), Hard (70 questions)
- **Real-time Score Tracking**: Scores are automatically saved to the database
- **Ranking Display**: After each quiz, players see their ranking in that difficulty level

### 📊 Leaderboard System
- **Global Leaderboard**: Top 10 players overall (combined scores)
- **Difficulty-Specific Leaderboards**: Separate rankings for Easy, Medium, and Hard
- **Score Ranking**: Players ranked by percentage, then by raw score, then by date

### 👤 Player Statistics
- **Total Games Played**: Count of all quiz attempts
- **Average Score**: Average percentage across all attempts
- **Best Score**: Highest percentage achieved
- **Game History**: View last 10 games with scores, percentages, and difficulty
- **Overall Ranking**: Current position in global rankings

### 💾 Database Structure
The SQLite database (`quiz_leaderboard.db`) stores:
- Player username
- Score and total questions
- Percentage score
- Difficulty level
- Date and time played

## Main Menu Options

```
1. Play Quiz       - Start a new quiz game
2. View Leaderboard - Check global and difficulty-specific rankings
3. View My Statistics - See personal game stats and history
4. Exit Game       - Quit the application
```

## How to Play

### Starting the Game
```bash
python quizGame.py
```

1. Enter your username (2-20 characters)
2. Select an option from the main menu
3. Choose a difficulty level
4. Answer all questions
5. View your score and ranking
6. Return to main menu

### Viewing Leaderboard
- Select option 2 from main menu
- Choose between Overall or Difficulty-specific rankings
- See top 10 players with medals (🥇🥈🥉)

### Checking Statistics
- Select option 3 from main menu
- View personal stats and recent game history

## File Structure

```
quiztime/
├── quizGame.py              # Main game script
├── questions.py             # Quiz questions and answers
├── leaderboard_db.py        # Database module
└── quiz_leaderboard.db      # SQLite database (auto-created)
```

## Module: leaderboard_db.py

### Available Functions

#### `initialize_database()`
Creates the leaderboard table if it doesn't exist.

#### `save_score(username, score, total_questions, difficulty)`
Saves a player's quiz score to the database.

#### `get_leaderboard(limit=10, difficulty=None)`
Returns top players from the leaderboard.
- If `difficulty=None`: Returns overall top players
- If `difficulty="EASY"|"MEDIUM"|"HARD"`: Returns top players for that difficulty

#### `get_player_stats(username)`
Returns player statistics including:
- Total games played
- Average score
- Best score
- Best raw score

#### `get_player_history(username, limit=10)`
Returns recent games for a player (default: last 10 games)

#### `get_ranking(username, difficulty=None)`
Returns player's current ranking in the specified difficulty or overall.

#### `clear_database()`
Admin function to clear all leaderboard data.

## Example Usage

```python
from leaderboard_db import *

# Initialize database
initialize_database()

# Save a score
save_score("Alice", 8, 10, "EASY")

# Get top 10 players
leaderboard = get_leaderboard(limit=10, difficulty="EASY")
for rank, (username, score, total_q, percentage, difficulty, date, id) in enumerate(leaderboard, 1):
    print(f"#{rank}: {username} - {percentage:.1f}%")

# Get player stats
stats = get_player_stats("Alice")
print(f"Alice's average: {stats[1]}%")

# Get player ranking
ranking = get_ranking("Alice", "EASY")
print(f"Alice's EASY ranking: #{ranking}")
```

## Score Calculation

- **Percentage Score**: `(Correct Answers / Total Questions) × 100`
- **Rankings**: Sorted by percentage (descending), then by raw score (descending), then by date

## Badges and Medals

- 🥇 **1st Place** (Rank 1)
- 🥈 **2nd Place** (Rank 2)
- 🥉 **3rd Place** (Rank 3)
- 📊 **Your Ranking** - Shown after each quiz

## Tips

- Play multiple times to improve your average score
- Challenge yourself with higher difficulties
- Check the leaderboard to compare with other players
- View your statistics to track progress over time

## Future Enhancements

Possible improvements:
- Time-based rankings (weekly, monthly)
- Difficulty multipliers
- Achievement badges
- Export statistics to CSV
- Multiplayer real-time competition

---

**Enjoy the quiz game and good luck climbing the leaderboard!** 🎯
