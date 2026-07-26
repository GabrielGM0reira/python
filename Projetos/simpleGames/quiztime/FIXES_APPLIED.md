# PyQt5 Quiz Game - Fixes Applied

## Issues Fixed

### 1. **Unknown Properties in Stylesheet**
   - **Problem**: QRadioButton indicators had duplicate width/height properties (18px in main, 16px in unchecked/checked)
   - **Solution**: Consolidated to single 16px definition in main indicator selector
   - **Affected Lines**: QRadioButton::indicator styles

### 2. **Invalid CSS Properties**
   - **Problem**: `box-shadow` property doesn't work in PyQt5 stylesheets (not supported)
   - **Solution**: Removed box-shadow from QPushButton:hover
   - **Affected Lines**: QPushButton:hover

### 3. **Wrong Property Name for Gradient**
   - **Problem**: QProgressBar::chunk used `background-color` with gradient (should be `background`)
   - **Solution**: Changed to `background` property which supports gradients
   - **Affected Lines**: QProgressBar::chunk

### 4. **Leaderboard Data Unpacking**
   - **Problem**: Expected 4 values but database returned 8 (username, score, total, percentage, difficulty, date_played, id, season)
   - **Solution**: Updated unpacking to handle all 8 values: `username, score, total, percentage, difficulty, date_played, row_id, season = row`
   - **Affected Lines**: show_leaderboard() method

### 5. **Missing QComboBox Focus Style**
   - **Problem**: No focus state styling for QComboBox
   - **Solution**: Added `QComboBox:focus` with neon_cyan border
   - **Affected Lines**: QComboBox styling

### 6. **QListWidget Enhancement**
   - **Problem**: List items lacked padding and hover effects
   - **Solution**: Added item padding (5px), margin (2px), and hover styling
   - **Affected Lines**: QListWidget::item styling

## Installation & Running

```bash
# Install dependencies (already done)
pip install PyQt5

# Run the program
python quizGame_PyQt5.py
```

## Testing Status
✅ Syntax: Valid
✅ Imports: All successful
✅ Styling: All properties supported
✅ Leaderboard: Fixed unpacking

The program is now ready to run!
