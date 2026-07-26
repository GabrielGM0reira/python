import sys
import json
import random
import threading
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QRadioButton, QButtonGroup, QProgressBar,
    QDialog, QLineEdit, QListWidget, QListWidgetItem, QComboBox,
    QMessageBox, QScrollArea, QFrame, QDesktopWidget, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from leaderboard_db import (
    initialize_database, save_score, get_leaderboard, 
    get_player_stats, get_player_history, get_ranking,
    get_current_season, get_seasonal_stats, get_all_seasons
)

# Vaporwave Color Palette
COLORS = {
    'dark_bg': '#0a0e27',      # Very dark purple/blue
    'darker_bg': '#050812',    # Even darker
    'primary_purple': '#b026ff',  # Neon purple
    'secondary_purple': '#9d4edd',  # Medium purple
    'neon_pink': '#ff006e',    # Hot pink
    'neon_cyan': '#00d9ff',    # Cyan
    'neon_magenta': '#ff10f0', # Magenta
    'text_primary': '#ffffff', # White
    'text_secondary': '#b0b0ff', # Light purple
    'accent_gold': '#ffd60a',  # Gold accent
    'correct_green': '#06ffa5', # Neon green
    'wrong_red': '#ff006e',    # Neon red/pink
}

# Vaporwave Stylesheet
VAPORWAVE_STYLE = f"""
    QMainWindow {{
        background-color: {COLORS['dark_bg']};
    }}
    
    QWidget {{
        background-color: {COLORS['dark_bg']};
        color: {COLORS['text_primary']};
    }}
    
    QLabel {{
        color: {COLORS['text_primary']};
        background-color: transparent;
        font-family: Arial;
        font-weight: bold;
    }}
    
    QPushButton {{
        background-color: {COLORS['secondary_purple']};
        color: {COLORS['text_primary']};
        border: 2px solid {COLORS['primary_purple']};
        border-radius: 8px;
        padding: 10px;
        font-weight: bold;
        font-size: 12px;
    }}
    
    QPushButton:hover {{
        background-color: {COLORS['primary_purple']};
        border: 2px solid {COLORS['neon_cyan']};
    }}
    
    QPushButton:pressed {{
        background-color: {COLORS['neon_magenta']};
    }}
    
    QLineEdit {{
        background-color: {COLORS['darker_bg']};
        color: {COLORS['neon_cyan']};
        border: 2px solid {COLORS['primary_purple']};
        border-radius: 6px;
        padding: 8px;
        font-size: 12px;
    }}
    
    QLineEdit:focus {{
        border: 2px solid {COLORS['neon_cyan']};
    }}
    
    QComboBox {{
        background-color: {COLORS['darker_bg']};
        color: {COLORS['text_primary']};
        border: 2px solid {COLORS['primary_purple']};
        border-radius: 6px;
        padding: 8px;
    }}
    
    QComboBox:focus {{
        border: 2px solid {COLORS['neon_cyan']};
    }}
    
    QComboBox::drop-down {{
        border: none;
        background-color: transparent;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {COLORS['secondary_purple']};
        color: {COLORS['text_primary']};
        selection-background-color: {COLORS['primary_purple']};
        border: 1px solid {COLORS['primary_purple']};
    }}
    
    QRadioButton {{
        color: {COLORS['text_primary']};
        spacing: 8px;
    }}
    
    QRadioButton::indicator {{
        width: 16px;
        height: 16px;
        border-radius: 8px;
    }}
    
    QRadioButton::indicator:unchecked {{
        background-color: {COLORS['darker_bg']};
        border: 2px solid {COLORS['primary_purple']};
    }}
    
    QRadioButton::indicator:checked {{
        background-color: {COLORS['neon_cyan']};
        border: 2px solid {COLORS['neon_cyan']};
    }}
    
    QProgressBar {{
        background-color: {COLORS['darker_bg']};
        border: 2px solid {COLORS['primary_purple']};
        border-radius: 6px;
        text-align: center;
        height: 25px;
    }}
    
    QProgressBar::chunk {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                          stop:0 {COLORS['primary_purple']},
                          stop:0.5 {COLORS['neon_magenta']},
                          stop:1 {COLORS['neon_cyan']});
    }}
    
    QListWidget {{
        background-color: {COLORS['darker_bg']};
        color: {COLORS['text_primary']};
        border: 2px solid {COLORS['primary_purple']};
        border-radius: 6px;
        outline: none;
    }}
    
    QListWidget::item {{
        padding: 5px;
        margin: 2px 0px;
    }}
    
    QListWidget::item:selected {{
        background-color: {COLORS['primary_purple']};
        border-radius: 3px;
    }}
    
    QListWidget::item:hover {{
        background-color: {COLORS['secondary_purple']};
        border-radius: 3px;
    }}
    
    QDialog {{
        background-color: {COLORS['dark_bg']};
    }}
"""

# Load questions from JSON
def load_questions():
    json_file = Path(__file__).parent / "questions.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# Responsive sizing utility functions
def get_responsive_window_size():
    """Calculate responsive window size based on screen dimensions"""
    screen = QDesktopWidget().screenGeometry()
    screen_width = screen.width()
    screen_height = screen.height()
    
    # Use 80% of screen for windows up to 1920x1080, scale accordingly
    window_width = min(int(screen_width * 0.85), 1200)
    window_height = min(int(screen_height * 0.85), 900)
    
    # Minimum window size
    window_width = max(window_width, 800)
    window_height = max(window_height, 600)
    
    return window_width, window_height, screen_width, screen_height

def get_responsive_font_size(base_size, window_width=900):
    """Calculate font size based on window width"""
    # Scale font size proportionally to window width
    scale_factor = window_width / 900  # 900 is the base window width
    return max(int(base_size * scale_factor), base_size // 2)  # Don't shrink below 50%

def get_responsive_spacing(base_spacing, window_width=900):
    """Calculate spacing based on window width"""
    scale_factor = window_width / 900
    return max(int(base_spacing * scale_factor), 5)

class UsernameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🎯 Enter Your Username")
        
        # Responsive size based on parent
        if parent:
            parent_width = parent.width()
            parent_height = parent.height()
            dialog_width = max(350, int(parent_width * 0.4))
            dialog_height = max(150, int(parent_height * 0.25))
        else:
            dialog_width = 400
            dialog_height = 150
        
        self.setGeometry(0, 0, dialog_width, dialog_height)
        self.setMinimumSize(300, 120)
        self.setStyleSheet(VAPORWAVE_STYLE)
        self.username = ""
        self.init_ui()
        
        # Center dialog on parent
        if parent:
            self.move(parent.x() + (parent.width() - dialog_width) // 2,
                     parent.y() + (parent.height() - dialog_height) // 2)
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("👤 Enter Your Username")
        title_font = QFont("Arial", get_responsive_font_size(12, self.width()), QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {COLORS['neon_cyan']};")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("(2-20 characters)")
        instructions_font = QFont("Arial", get_responsive_font_size(9, self.width()))
        instructions.setFont(instructions_font)
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(instructions)
        
        # Input field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username...")
        self.username_input.setMinimumHeight(35)
        input_font = QFont("Arial", get_responsive_font_size(10, self.width()))
        self.username_input.setFont(input_font)
        self.username_input.returnPressed.connect(self.accept)
        layout.addWidget(self.username_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        ok_btn = QPushButton("✓ OK")
        ok_btn.setMinimumHeight(35)
        ok_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        ok_btn_font = QFont("Arial", get_responsive_font_size(10, self.width()), QFont.Bold)
        ok_btn.setFont(ok_btn_font)
        ok_btn.clicked.connect(self.validate_and_accept)
        button_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton("✕ Cancel")
        cancel_btn.setMinimumHeight(35)
        cancel_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        cancel_btn_font = QFont("Arial", get_responsive_font_size(10, self.width()), QFont.Bold)
        cancel_btn.setFont(cancel_btn_font)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def validate_and_accept(self):
        username = self.username_input.text().strip()
        if 2 <= len(username) <= 20:
            self.username = username
            self.accept()
        else:
            QMessageBox.warning(self, "Invalid Username", "Username must be 2-20 characters!")

class CategorySelectionDialog(QDialog):
    def __init__(self, categories, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📚 Select Categories")
        
        # Responsive size based on parent
        if parent:
            parent_width = parent.width()
            parent_height = parent.height()
            dialog_width = max(350, int(parent_width * 0.45))
            dialog_height = max(300, int(parent_height * 0.6))
        else:
            dialog_width = 400
            dialog_height = 400
        
        self.setGeometry(0, 0, dialog_width, dialog_height)
        self.setMinimumSize(300, 250)
        self.setStyleSheet(VAPORWAVE_STYLE)
        self.selected_categories = []
        self.categories = categories
        self.init_ui()
        
        # Center dialog on parent
        if parent:
            self.move(parent.x() + (parent.width() - dialog_width) // 2,
                     parent.y() + (parent.height() - dialog_height) // 2)
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        
        title = QLabel("📚 SELECT CATEGORIES")
        title_font = QFont("Arial", get_responsive_font_size(12, self.width()), QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {COLORS['neon_pink']};")
        layout.addWidget(title)
        
        # List of categories
        self.category_buttons = {}
        categories_layout = QVBoxLayout()
        categories_layout.setSpacing(8)
        
        for category in self.categories:
            btn = QPushButton(f"✓ {category}")
            btn.setCheckable(True)
            btn.setChecked(True)
            btn.setMinimumHeight(35)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            btn_font = QFont("Arial", get_responsive_font_size(10, self.width()), QFont.Bold)
            btn.setFont(btn_font)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['primary_purple']};
                    color: {COLORS['text_primary']};
                    border: 2px solid {COLORS['neon_cyan']};
                    border-radius: 6px;
                    padding: 5px;
                    font-weight: bold;
                }}
                QPushButton:checked {{
                    background-color: {COLORS['neon_cyan']};
                    color: {COLORS['dark_bg']};
                }}
            """)
            self.category_buttons[category] = btn
            categories_layout.addWidget(btn)
        
        # Scrollable area for categories
        categories_widget = QWidget()
        categories_widget.setLayout(categories_layout)
        scroll = QScrollArea()
        scroll.setWidget(categories_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll, 1)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        ok_btn = QPushButton("✓ Continue")
        ok_btn.setMinimumHeight(35)
        ok_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        ok_btn_font = QFont("Arial", get_responsive_font_size(10, self.width()), QFont.Bold)
        ok_btn.setFont(ok_btn_font)
        ok_btn.clicked.connect(self.accept_selection)
        button_layout.addWidget(ok_btn)
        
        all_btn = QPushButton("All Categories")
        all_btn.setMinimumHeight(35)
        all_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        all_btn_font = QFont("Arial", get_responsive_font_size(9, self.width()), QFont.Bold)
        all_btn.setFont(all_btn_font)
        all_btn.clicked.connect(self.select_all)
        button_layout.addWidget(all_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def select_all(self):
        for btn in self.category_buttons.values():
            btn.setChecked(True)
    
    def accept_selection(self):
        self.selected_categories = [cat for cat, btn in self.category_buttons.items() if btn.isChecked()]
        if self.selected_categories:
            self.accept()
        else:
            QMessageBox.warning(self, "No Selection", "Please select at least one category!")

class DifficultySelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🎮 Select Difficulty")
        
        # Responsive size based on parent
        if parent:
            parent_width = parent.width()
            parent_height = parent.height()
            dialog_width = max(350, int(parent_width * 0.45))
            dialog_height = max(350, int(parent_height * 0.65))
        else:
            dialog_width = 400
            dialog_height = 350
        
        self.setGeometry(0, 0, dialog_width, dialog_height)
        self.setMinimumSize(300, 300)
        self.setStyleSheet(VAPORWAVE_STYLE)
        self.difficulty_name = ""
        self.num_questions = 0
        self.init_ui()
        
        # Center dialog on parent
        if parent:
            self.move(parent.x() + (parent.width() - dialog_width) // 2,
                     parent.y() + (parent.height() - dialog_height) // 2)
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        
        title = QLabel("🎮 SELECT QUIZ MODE")
        title_font = QFont("Arial", get_responsive_font_size(12, self.width()), QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {COLORS['neon_magenta']};")
        layout.addWidget(title)
        
        self.button_group = QButtonGroup()
        
        difficulties = [
            ("🟢 EASY - 10 questions", "EASY", 10),
            ("🟡 MEDIUM - 30 questions", "MEDIUM", 30),
            ("🔴 HARD - All available", "HARD", None),
            ("⚙️  CUSTOM - Specify number", "CUSTOM", -1),
            ("📚 STUDY MODE - With explanations", "STUDY", 10),
        ]
        
        for idx, (label, name, num) in enumerate(difficulties):
            radio = QRadioButton(label)
            radio_font = QFont("Arial", get_responsive_font_size(10, self.width()))
            radio.setFont(radio_font)
            radio.setMinimumHeight(30)
            self.button_group.addButton(radio, idx)
            layout.addWidget(radio)
        
        self.button_group.button(0).setChecked(True)
        
        # Custom number input
        self.custom_input = QLineEdit()
        self.custom_input.setPlaceholderText("Enter number of questions...")
        self.custom_input.setEnabled(False)
        self.custom_input.setMinimumHeight(35)
        input_font = QFont("Arial", get_responsive_font_size(10, self.width()))
        self.custom_input.setFont(input_font)
        layout.addWidget(self.custom_input)
        
        self.button_group.idClicked.connect(self.on_difficulty_changed)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        ok_btn = QPushButton("✓ Continue")
        ok_btn.setMinimumHeight(35)
        ok_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        ok_btn_font = QFont("Arial", get_responsive_font_size(10, self.width()), QFont.Bold)
        ok_btn.setFont(ok_btn_font)
        ok_btn.clicked.connect(self.accept_difficulty)
        button_layout.addWidget(ok_btn)
        
        layout.addStretch()
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def on_difficulty_changed(self, id):
        self.custom_input.setEnabled(id == 3)  # Custom option
    
    def accept_difficulty(self):
        selected_id = self.button_group.checkedId()
        difficulties = ["EASY", "MEDIUM", "HARD", "CUSTOM", "STUDY"]
        self.difficulty_name = difficulties[selected_id]
        
        if selected_id == 0:
            self.num_questions = 10
        elif selected_id == 1:
            self.num_questions = 30
        elif selected_id == 2:
            self.num_questions = None
        elif selected_id == 3:
            try:
                self.num_questions = int(self.custom_input.text())
                if self.num_questions <= 0:
                    QMessageBox.warning(self, "Invalid Input", "Please enter a positive number!")
                    return
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Please enter a valid number!")
                return
        else:
            self.num_questions = 10
        
        self.accept()

class QuestionTierDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("❓ Question Difficulty")
        
        # Responsive size based on parent
        if parent:
            parent_width = parent.width()
            parent_height = parent.height()
            dialog_width = max(350, int(parent_width * 0.4))
            dialog_height = max(250, int(parent_height * 0.4))
        else:
            dialog_width = 400
            dialog_height = 250
        
        self.setGeometry(0, 0, dialog_width, dialog_height)
        self.setMinimumSize(300, 200)
        self.setStyleSheet(VAPORWAVE_STYLE)
        self.selected_tiers = []
        self.init_ui()
        
        # Center dialog on parent
        if parent:
            self.move(parent.x() + (parent.width() - dialog_width) // 2,
                     parent.y() + (parent.height() - dialog_height) // 2)
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        
        title = QLabel("❓ QUESTION DIFFICULTY TIER")
        title_font = QFont("Arial", get_responsive_font_size(12, self.width()), QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {COLORS['accent_gold']};")
        layout.addWidget(title)
        
        self.button_group = QButtonGroup()
        
        tiers = [
            ("🟢 Easy Only", 0),
            ("🟡 Medium Only", 1),
            ("🔴 Hard Only", 2),
            ("🎨 Mixed (All)", 3),
        ]
        
        for label, idx in tiers:
            radio = QRadioButton(label)
            radio_font = QFont("Arial", get_responsive_font_size(10, self.width()))
            radio.setFont(radio_font)
            radio.setMinimumHeight(30)
            self.button_group.addButton(radio, idx)
            layout.addWidget(radio)
        
        self.button_group.button(3).setChecked(True)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        ok_btn = QPushButton("✓ Continue")
        ok_btn.setMinimumHeight(35)
        ok_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        ok_btn_font = QFont("Arial", get_responsive_font_size(10, self.width()), QFont.Bold)
        ok_btn.setFont(ok_btn_font)
        ok_btn.clicked.connect(self.accept_tiers)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def accept_tiers(self):
        selected_id = self.button_group.checkedId()
        tiers_map = {
            0: ["Easy"],
            1: ["Medium"],
            2: ["Hard"],
            3: ["Easy", "Medium", "Hard"],
        }
        self.selected_tiers = tiers_map[selected_id]
        self.accept()

class QuizWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎯 QUIZ GAME - VAPORWAVE EDITION")
        
        # Set responsive window size
        window_width, window_height, screen_width, screen_height = get_responsive_window_size()
        
        # Center window on screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)
        
        # Set minimum and maximum size for responsiveness
        self.setMinimumSize(800, 600)
        self.setMaximumSize(screen_width, screen_height)
        
        self.setStyleSheet(VAPORWAVE_STYLE)
        
        # Load data
        self.quiz_data = load_questions()
        initialize_database()
        
        self.username = ""
        self.current_question_idx = 0
        self.score = 0
        self.time_remaining = 0
        self.timer = None
        self.guesses = []
        self.correct_answers = []
        self.questions_list = []
        self.difficulty_name = ""
        self.streak = 0
        self.best_streak = 0
        self._current_animation = None  # Store reference to animation
        self.current_window_width = window_width  # Track window width for responsive fonts
        
        self.show_welcome()
    
    def resizeEvent(self, event):
        """Handle window resize for responsive layout"""
        super().resizeEvent(event)
        self.current_window_width = self.width()
        # Re-show current screen to apply responsive changes
        if self.current_question_idx == 0 and not self.questions_list:
            # Only refresh on welcome screen
            pass
    
    def animate_transition(self, widget):
        """Animate transition to a new widget with fade effect"""
        # Set the new widget immediately
        self.setCentralWidget(widget)
        
        # Create opacity effect starting at 0 (invisible)
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.0)
        widget.setGraphicsEffect(opacity_effect)
        
        # Store reference to prevent garbage collection
        self._current_animation = QPropertyAnimation(opacity_effect, b"opacity")
        self._current_animation.setDuration(500)
        self._current_animation.setStartValue(0.0)
        self._current_animation.setEndValue(1.0)
        self._current_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self._current_animation.start()
        
    def show_welcome(self):
        """Show welcome screen"""
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(get_responsive_spacing(20, self.width()))
        
        # Title
        title = QLabel("🎯 WELCOME TO THE QUIZ GAME 🎯")
        title_font = QFont("Arial", get_responsive_font_size(28, self.width()), QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {COLORS['neon_cyan']};")
        title.setWordWrap(True)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("✨ V A P O R W A V E ✨")
        subtitle_font = QFont("Arial", get_responsive_font_size(16, self.width()), QFont.Bold)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"color: {COLORS['neon_pink']};")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)
        
        layout.addSpacing(max(20, self.height() // 15))
        
        # Start button
        start_btn = QPushButton("▶ START QUIZ")
        start_btn.setMinimumHeight(max(50, int(self.height() * 0.08)))
        start_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        start_btn_font = QFont("Arial", get_responsive_font_size(16, self.width()), QFont.Bold)
        start_btn.setFont(start_btn_font)
        start_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 {COLORS['primary_purple']},
                            stop:1 {COLORS['neon_magenta']});
                color: {COLORS['text_primary']};
                border: 3px solid {COLORS['neon_cyan']};
                border-radius: 10px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 {COLORS['neon_magenta']},
                            stop:1 {COLORS['primary_purple']});
                border: 3px solid {COLORS['accent_gold']};
            }}
        """)
        start_btn.clicked.connect(self.start_quiz)
        layout.addWidget(start_btn)
        
        # Leaderboard button
        leader_btn = QPushButton("🏆 VIEW LEADERBOARD")
        leader_btn.setMinimumHeight(max(45, int(self.height() * 0.06)))
        leader_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        leader_btn_font = QFont("Arial", get_responsive_font_size(13, self.width()), QFont.Bold)
        leader_btn.setFont(leader_btn_font)
        leader_btn.clicked.connect(self.show_leaderboard)
        layout.addWidget(leader_btn)
        
        # Exit button
        exit_btn = QPushButton("✕ EXIT")
        exit_btn.setMinimumHeight(max(45, int(self.height() * 0.06)))
        exit_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        exit_btn_font = QFont("Arial", get_responsive_font_size(13, self.width()), QFont.Bold)
        exit_btn.setFont(exit_btn_font)
        exit_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['wrong_red']};
                color: {COLORS['text_primary']};
                border: 2px solid {COLORS['text_primary']};
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['neon_magenta']};
            }}
        """)
        exit_btn.clicked.connect(self.close)
        layout.addWidget(exit_btn)
        
        layout.addStretch()
        
        central_widget.setLayout(layout)
        self.animate_transition(central_widget)
    
    def start_quiz(self):
        """Start quiz flow"""
        # Username dialog
        username_dialog = UsernameDialog(self)
        if username_dialog.exec_() == QDialog.Accepted:
            self.username = username_dialog.username
            
            # Category selection
            categories = list(self.quiz_data["categories"].keys())
            cat_dialog = CategorySelectionDialog(categories, self)
            if cat_dialog.exec_() == QDialog.Accepted:
                selected_categories = cat_dialog.selected_categories
                
                # Difficulty selection
                diff_dialog = DifficultySelectionDialog(self)
                if diff_dialog.exec_() == QDialog.Accepted:
                    self.difficulty_name = diff_dialog.difficulty_name
                    num_questions_specified = diff_dialog.num_questions
                    
                    # Question tier selection
                    tier_dialog = QuestionTierDialog(self)
                    if tier_dialog.exec_() == QDialog.Accepted:
                        question_tiers = tier_dialog.selected_tiers
                        
                        # Prepare questions
                        all_questions = []
                        for category in selected_categories:
                            all_questions.extend(self.quiz_data["categories"][category])
                        
                        filtered_questions = [q for q in all_questions if q.get("difficulty") in question_tiers]
                        
                        if not filtered_questions:
                            QMessageBox.warning(self, "No Questions", "No questions found for selected criteria!")
                            return
                        
                        random.shuffle(filtered_questions)
                        
                        if num_questions_specified:
                            self.questions_list = filtered_questions[:num_questions_specified]
                        else:
                            self.questions_list = filtered_questions
                        
                        self.current_question_idx = 0
                        self.score = 0
                        self.guesses = []
                        self.correct_answers = []
                        self.streak = 0
                        self.best_streak = 0
                        
                        self.show_question()
    
    def show_question(self):
        """Display current question"""
        if self.current_question_idx >= len(self.questions_list):
            self.show_results()
            return
        
        question_data = self.questions_list[self.current_question_idx]
        
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(get_responsive_spacing(12, self.width()))
        
        # Progress bar
        progress = (self.current_question_idx / len(self.questions_list)) * 100
        progress_bar = QProgressBar()
        progress_bar.setValue(int(progress))
        progress_bar.setTextVisible(True)
        progress_bar.setMinimumHeight(25)
        layout.addWidget(progress_bar)
        
        # Stats
        stats_label = QLabel(f"🔥 Streak: {self.streak} | Best: {self.best_streak}")
        stats_label.setAlignment(Qt.AlignCenter)
        stats_label_font = QFont("Arial", get_responsive_font_size(11, self.width()), QFont.Bold)
        stats_label.setFont(stats_label_font)
        stats_label.setStyleSheet(f"color: {COLORS['accent_gold']};")
        layout.addWidget(stats_label)
        
        # Question number and text
        q_num_label = QLabel(f"Question {self.current_question_idx + 1}/{len(self.questions_list)}")
        q_num_label.setAlignment(Qt.AlignCenter)
        q_num_font = QFont("Arial", get_responsive_font_size(10, self.width()))
        q_num_label.setFont(q_num_font)
        q_num_label.setStyleSheet(f"color: {COLORS['neon_cyan']};")
        layout.addWidget(q_num_label)
        
        question_label = QLabel(question_data["question"])
        question_font = QFont("Arial", get_responsive_font_size(13, self.width()), QFont.Bold)
        question_label.setFont(question_font)
        question_label.setAlignment(Qt.AlignCenter)
        question_label.setWordWrap(True)
        question_label.setStyleSheet(f"color: {COLORS['text_primary']}; padding: 15px;")
        layout.addWidget(question_label)
        
        # Shuffle options
        options_with_labels = list(enumerate(question_data["options"]))
        random.shuffle(options_with_labels)
        
        # Store correct answer
        correct_answer_new = None
        self.shuffled_options = []
        
        # Radio buttons for options
        self.option_group = QButtonGroup()
        
        # Create a scrollable area for options if needed
        options_layout = QVBoxLayout()
        options_layout.setSpacing(get_responsive_spacing(8, self.width()))
        
        for new_idx, (orig_idx, option) in enumerate(options_with_labels):
            label = chr(65 + new_idx)
            option_text = option.split('. ', 1)[1] if '. ' in option else option
            
            radio = QRadioButton(f"{label}. {option_text}")
            radio_font = QFont("Arial", get_responsive_font_size(11, self.width()))
            radio.setFont(radio_font)
            radio.setMinimumHeight(int(self.height() * 0.05))
            self.option_group.addButton(radio, new_idx)
            options_layout.addWidget(radio)
            
            self.shuffled_options.append(option)
            
            if question_data["answer"] in option:
                correct_answer_new = label
        
        # Add options to main layout with stretch
        options_widget = QWidget()
        options_widget.setLayout(options_layout)
        layout.addWidget(options_widget, 1)
        
        self.current_correct_answer = correct_answer_new
        
        # Submit button
        submit_btn = QPushButton("✓ SUBMIT ANSWER")
        submit_btn.setMinimumHeight(max(45, int(self.height() * 0.06)))
        submit_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        submit_btn_font = QFont("Arial", get_responsive_font_size(12, self.width()), QFont.Bold)
        submit_btn.setFont(submit_btn_font)
        submit_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                            stop:0 {COLORS['neon_cyan']},
                            stop:1 {COLORS['primary_purple']});
                color: {COLORS['dark_bg']};
                border: 2px solid {COLORS['text_primary']};
                border-radius: 8px;
                font-weight: bold;
            }}
        """)
        submit_btn.clicked.connect(self.submit_answer)
        layout.addWidget(submit_btn)
        
        # Skip button
        skip_btn = QPushButton("⏭️  SKIP")
        skip_btn.setMinimumHeight(max(45, int(self.height() * 0.06)))
        skip_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        skip_btn_font = QFont("Arial", get_responsive_font_size(12, self.width()), QFont.Bold)
        skip_btn.setFont(skip_btn_font)
        skip_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['secondary_purple']};
                color: {COLORS['text_primary']};
                border: 2px solid {COLORS['text_secondary']};
                border-radius: 8px;
            }}
        """)
        skip_btn.clicked.connect(self.skip_question)
        layout.addWidget(skip_btn)
        
        central_widget.setLayout(layout)
        self.animate_transition(central_widget)
    
    def submit_answer(self):
        """Submit answer and move to next question"""
        checked_button = self.option_group.checkedButton()
        
        if not checked_button:
            QMessageBox.warning(self, "No Answer", "Please select an answer!")
            return
        
        checked_idx = self.option_group.id(checked_button)
        answer_letter = chr(65 + checked_idx)
        
        self.guesses.append(answer_letter)
        self.correct_answers.append(self.current_correct_answer)
        
        if answer_letter == self.current_correct_answer:
            self.score += 1
            self.streak += 1
            if self.streak > self.best_streak:
                self.best_streak = self.streak
            
            QMessageBox.information(self, "✓ CORRECT!", f"🎉 Great job!\nStreak: {self.streak}")
        else:
            QMessageBox.warning(self, "✗ WRONG!", f"The correct answer was: {self.current_correct_answer}\nStreak ended at: {self.streak}")
            self.streak = 0
        
        self.current_question_idx += 1
        self.show_question()
    
    def skip_question(self):
        """Skip current question"""
        self.guesses.append("SKIP")
        self.correct_answers.append(self.current_correct_answer)
        self.streak = 0
        self.current_question_idx += 1
        self.show_question()
    
    def show_results(self):
        """Display quiz results"""
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(get_responsive_spacing(12, self.width()))
        
        # Title
        title = QLabel("🏆 QUIZ COMPLETED 🏆")
        title_font = QFont("Arial", get_responsive_font_size(20, self.width()), QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {COLORS['neon_cyan']};")
        layout.addWidget(title)
        
        # Player info
        player_info = QLabel(f"Player: {self.username}")
        player_info_font = QFont("Arial", get_responsive_font_size(12, self.width()))
        player_info.setFont(player_info_font)
        player_info.setAlignment(Qt.AlignCenter)
        player_info.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(player_info)
        
        # Score
        num_questions = len(self.questions_list)
        percentage = (self.score / num_questions * 100) if num_questions > 0 else 0
        
        score_label = QLabel(f"Score: {self.score}/{num_questions} ({percentage:.1f}%)")
        score_font = QFont("Arial", get_responsive_font_size(18, self.width()), QFont.Bold)
        score_label.setFont(score_font)
        score_label.setAlignment(Qt.AlignCenter)
        score_label.setWordWrap(True)
        
        if percentage == 100:
            score_label.setStyleSheet(f"color: {COLORS['correct_green']};")
            message = "🏆 PERFECT SCORE! You're a genius!"
        elif percentage >= 80:
            score_label.setStyleSheet(f"color: {COLORS['neon_cyan']};")
            message = "🥇 Excellent! Great job!"
        elif percentage >= 60:
            score_label.setStyleSheet(f"color: {COLORS['accent_gold']};")
            message = "🥈 Good effort! Keep learning!"
        elif percentage >= 40:
            score_label.setStyleSheet(f"color: {COLORS['neon_pink']};")
            message = "🥉 Not bad! Practice more!"
        else:
            score_label.setStyleSheet(f"color: {COLORS['wrong_red']};")
            message = "💪 Keep trying! You'll do better next time!"
        
        layout.addWidget(score_label)
        
        message_label = QLabel(message)
        message_font = QFont("Arial", get_responsive_font_size(13, self.width()), QFont.Bold)
        message_label.setFont(message_font)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setStyleSheet(f"color: {COLORS['neon_magenta']};")
        message_label.setWordWrap(True)
        layout.addWidget(message_label)
        
        # Streak info
        streak_info = QLabel(f"Best Streak: {self.best_streak}")
        streak_info_font = QFont("Arial", get_responsive_font_size(12, self.width()))
        streak_info.setFont(streak_info_font)
        streak_info.setAlignment(Qt.AlignCenter)
        streak_info.setStyleSheet(f"color: {COLORS['accent_gold']};")
        layout.addWidget(streak_info)
        
        layout.addSpacing(max(10, self.height() // 20))
        
        # Save score and show ranking
        save_score(self.username, self.score, num_questions, self.difficulty_name)
        ranking = get_ranking(self.username, self.difficulty_name)
        
        ranking_label = QLabel(f"📊 Your Ranking in {self.difficulty_name}: #{ranking}")
        ranking_font = QFont("Arial", get_responsive_font_size(11, self.width()))
        ranking_label.setFont(ranking_font)
        ranking_label.setAlignment(Qt.AlignCenter)
        ranking_label.setStyleSheet(f"color: {COLORS['neon_cyan']};")
        ranking_label.setWordWrap(True)
        layout.addWidget(ranking_label)
        
        layout.addSpacing(max(10, self.height() // 20))
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(get_responsive_spacing(10, self.width()))
        
        replay_btn = QPushButton("🔄 PLAY AGAIN")
        replay_btn.setMinimumHeight(max(45, int(self.height() * 0.06)))
        replay_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        replay_btn_font = QFont("Arial", get_responsive_font_size(11, self.width()), QFont.Bold)
        replay_btn.setFont(replay_btn_font)
        replay_btn.clicked.connect(self.show_welcome)
        button_layout.addWidget(replay_btn)
        
        leaderboard_btn = QPushButton("🏆 LEADERBOARD")
        leaderboard_btn.setMinimumHeight(max(45, int(self.height() * 0.06)))
        leaderboard_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        leaderboard_btn_font = QFont("Arial", get_responsive_font_size(11, self.width()), QFont.Bold)
        leaderboard_btn.setFont(leaderboard_btn_font)
        leaderboard_btn.clicked.connect(self.show_leaderboard)
        button_layout.addWidget(leaderboard_btn)
        
        exit_btn = QPushButton("✕ EXIT")
        exit_btn.setMinimumHeight(max(45, int(self.height() * 0.06)))
        exit_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        exit_btn_font = QFont("Arial", get_responsive_font_size(11, self.width()), QFont.Bold)
        exit_btn.setFont(exit_btn_font)
        exit_btn.clicked.connect(self.close)
        button_layout.addWidget(exit_btn)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        central_widget.setLayout(layout)
        self.animate_transition(central_widget)
    
    def show_leaderboard(self):
        """Display leaderboard"""
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(get_responsive_spacing(12, self.width()))
        
        title = QLabel("🏆 LEADERBOARD 🏆")
        title_font = QFont("Arial", get_responsive_font_size(18, self.width()), QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {COLORS['neon_cyan']};")
        layout.addWidget(title)
        
        # Get leaderboard
        leaderboard = get_leaderboard(limit=10, difficulty=None, season=None)
        
        # Display leaderboard
        list_widget = QListWidget()
        list_font = QFont("Arial", get_responsive_font_size(10, self.width()))
        list_widget.setFont(list_font)
        
        for idx, row in enumerate(leaderboard, 1):
            # Unpack all 8 values from the tuple
            username, score, total, percentage, difficulty, date_played, row_id, season = row
            item_text = f"#{idx} {username:<15} {score}/{total} ({percentage:.1f}%) - {difficulty}"
            
            item = QListWidgetItem(item_text)
            if idx == 1:
                item.setForeground(QColor(COLORS['accent_gold']))
            elif idx == 2:
                item.setForeground(QColor(COLORS['neon_cyan']))
            elif idx == 3:
                item.setForeground(QColor(COLORS['neon_pink']))
            else:
                item.setForeground(QColor(COLORS['text_secondary']))
            
            list_widget.addItem(item)
        
        layout.addWidget(list_widget, 1)
        
        # Back button
        back_btn = QPushButton("◀ BACK TO MENU")
        back_btn.setMinimumHeight(max(45, int(self.height() * 0.06)))
        back_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        back_btn_font = QFont("Arial", get_responsive_font_size(12, self.width()), QFont.Bold)
        back_btn.setFont(back_btn_font)
        back_btn.clicked.connect(self.show_welcome)
        layout.addWidget(back_btn)
        
        central_widget.setLayout(layout)
        self.animate_transition(central_widget)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = QuizWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
