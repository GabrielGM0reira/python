import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import string
import random
import re
from password_database import (
    initialize_database, save_password, get_all_passwords,
    delete_password, update_password, display_saved_passwords,
    view_password, get_password_by_name, clear_all_passwords
)

# Modern Color Palette
PRIMARY_COLOR = "#0F1419"       # Deep Dark
SECONDARY_COLOR = "#1E1E2E"     # Dark Charcoal
ACCENT_COLOR = "#00D4FF"        # Bright Cyan
GRADIENT_COLOR = "#0099CC"      # Deep Cyan
LIGHT_BG = "#F5F7FA"            # Light Gray
CARD_BG = "#FFFFFF"             # White Cards
TEXT_PRIMARY = "#1A1A1A"        # Dark Text
TEXT_SECONDARY = "#666666"      # Gray Text
SUCCESS_COLOR = "#00D97E"        # Green
WARNING_COLOR = "#FF6B35"        # Orange
ERROR_COLOR = "#E63946"          # Red

# Common weak passwords
WEAK_PASSWORDS = [
    'password', '123456', 'qwerty', 'abc123', 'admin', 'letmein',
    '111111', '123123', 'welcome', 'dragon', 'master', 'monkey',
    'princess', 'admin123', 'password123', 'qwerty123'
]

KEYBOARD_PATTERNS = [
    'qwerty', 'asdf', 'zxcv', '123456', '789', 'qazwsx', '1234567890'
]

class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Password Manager - Secure & Safe")
        self.root.geometry("900x700")
        self.root.configure(bg=LIGHT_BG)
        
        # Window styling with flexible sizing
        self.root.resizable(True, True)
        self.root.minsize(700, 500)
        
        # Responsive sizing variables
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.current_width = 900
        self.current_height = 700
        self.size_category = 'medium'
        
        # Bind resize event for responsive layout
        self.root.bind('<Configure>', self.on_window_resize)
        
        # Set window icon and center on screen
        self.center_window()
        
        # Configure style
        self.setup_styles()
        initialize_database()
        
        # Show main menu
        self.show_main_menu()
    
    def on_window_resize(self, event=None):
        """Handle window resize for responsive layout"""
        if event:
            self.current_width = event.width
            self.current_height = event.height
            self.update_size_category()
    
    def update_size_category(self):
        """Update size category based on current window dimensions"""
        if self.current_width < 800:
            self.size_category = 'small'
        elif self.current_width < 1000:
            self.size_category = 'medium'
        else:
            self.size_category = 'large'
    
    def get_responsive_font_size(self, base_size, category=None):
        """Calculate font size based on window size"""
        if category is None:
            category = self.size_category
        
        size_multiplier = {
            'small': 0.85,
            'medium': 1.0,
            'large': 1.15
        }
        
        return int(base_size * size_multiplier.get(category, 1.0))
    
    def get_responsive_padding(self, base_padding, category=None):
        """Calculate padding based on window size"""
        if category is None:
            category = self.size_category
        
        padding_multiplier = {
            'small': 0.75,
            'medium': 1.0,
            'large': 1.25
        }
        
        return int(base_padding * padding_multiplier.get(category, 1.0))
    
    def get_button_columns(self):
        """Get optimal number of button columns based on window width"""
        if self.current_width < 750:
            return 1
        elif self.current_width < 950:
            return 2
        else:
            return 3
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """Configure ttk styles with modern design"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for all elements
        style.configure('TFrame', background=LIGHT_BG)
        style.configure('TLabel', background=LIGHT_BG, foreground=TEXT_PRIMARY)
        
        # Modern Button styles
        style.configure('TButton', 
                       font=('Segoe UI', 10, 'bold'), 
                       padding=8,
                       relief='flat',
                       borderwidth=0)
        style.map('TButton',
                 background=[('active', ACCENT_COLOR), ('pressed', GRADIENT_COLOR)],
                 foreground=[('active', LIGHT_BG)],
                 relief=[('pressed', 'flat')])
        
        # Primary button (Cyan/Accent)
        style.configure('Primary.TButton', 
                       background=ACCENT_COLOR,
                       foreground=PRIMARY_COLOR,
                       borderwidth=0,
                       relief='flat',
                       font=('Segoe UI', 10, 'bold'))
        style.map('Primary.TButton',
                 background=[('active', GRADIENT_COLOR), ('pressed', '#0077AA')])
        
        # Secondary button (Dark)
        style.configure('Secondary.TButton',
                       background=SECONDARY_COLOR,
                       foreground=LIGHT_BG,
                       borderwidth=0,
                       relief='flat',
                       font=('Segoe UI', 10, 'bold'))
        style.map('Secondary.TButton',
                 background=[('active', PRIMARY_COLOR)])
        
        # Label styles
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 20, 'bold'),
                       background=LIGHT_BG,
                       foreground=PRIMARY_COLOR)
        
        style.configure('Heading.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       background=PRIMARY_COLOR,
                       foreground=LIGHT_BG)
        
        style.configure('Normal.TLabel',
                       font=('Segoe UI', 10),
                       background=LIGHT_BG,
                       foreground=TEXT_SECONDARY)
        
        # Scrollbar style
        style.configure('Vertical.TScrollbar', 
                       background=LIGHT_BG,
                       troughcolor=LIGHT_BG,
                       bordercolor=ACCENT_COLOR,
                       darkcolor=ACCENT_COLOR,
                       lightcolor=LIGHT_BG)
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        """Display main menu with modern card-based design"""
        self.clear_window()
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(0, weight=0)  # Header
        self.root.grid_rowconfigure(1, weight=1)  # Content
        self.root.grid_rowconfigure(2, weight=0)  # Footer
        self.root.grid_columnconfigure(0, weight=1)
        
        # Modern Header with gradient effect - responsive sizing
        header_height = 90 if self.size_category == 'large' else (80 if self.size_category == 'medium' else 70)
        header_frame = tk.Frame(self.root, bg=PRIMARY_COLOR, height=header_height)
        header_frame.grid(row=0, column=0, sticky='nsew')
        header_frame.grid_propagate(False)
        
        # Decorative accent line
        accent_line = tk.Frame(header_frame, bg=ACCENT_COLOR, height=3)
        accent_line.pack(fill=tk.X, side=tk.TOP)
        accent_line.pack_propagate(False)
        
        # Header content - responsive fonts
        title_font_size = self.get_responsive_font_size(22)
        subtitle_font_size = self.get_responsive_font_size(9)
        title_pady = self.get_responsive_padding(10)
        subtitle_pady = self.get_responsive_padding(8)
        
        title_label = tk.Label(header_frame, 
                              text="🔐 PASSWORD MANAGER", 
                              font=('Segoe UI', title_font_size, 'bold'),
                              bg=PRIMARY_COLOR, fg=ACCENT_COLOR, pady=title_pady)
        title_label.pack(anchor=tk.CENTER, expand=True)
        
        subtitle_label = tk.Label(header_frame, 
                                 text="Secure Password Management System",
                                 font=('Segoe UI', subtitle_font_size),
                                 bg=PRIMARY_COLOR, fg=TEXT_SECONDARY)
        subtitle_label.pack(anchor=tk.CENTER, pady=(0, subtitle_pady))
        
        # Main content frame with responsive layout
        content_wrapper = tk.Frame(self.root, bg=LIGHT_BG)
        content_wrapper.grid(row=1, column=0, sticky='nsew', padx=0, pady=0)
        content_wrapper.grid_rowconfigure(0, weight=1)
        content_wrapper.grid_columnconfigure(0, weight=1)
        
        # Scrollable content
        canvas = tk.Canvas(content_wrapper, bg=LIGHT_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_wrapper, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=LIGHT_BG)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Welcome card - responsive sizing
        welcome_padx = self.get_responsive_padding(15)
        welcome_pady = self.get_responsive_padding(15)
        welcome_title_font = self.get_responsive_font_size(14)
        welcome_text_font = self.get_responsive_font_size(9)
        welcome_frame = tk.Frame(scrollable_frame, bg=CARD_BG, relief=tk.FLAT, bd=0)
        welcome_frame.pack(fill=tk.X, padx=welcome_padx, pady=(welcome_pady, welcome_pady//3))
        self.add_shadow_effect(welcome_frame)
        
        welcome_title = tk.Label(welcome_frame, 
                                text="Welcome Back! 👋",
                                font=('Segoe UI', welcome_title_font, 'bold'),
                                bg=CARD_BG, fg=PRIMARY_COLOR)
        welcome_title.pack(anchor=tk.W, padx=welcome_padx, pady=(welcome_pady, welcome_pady//3))
        
        welcome_text = tk.Label(welcome_frame,
                               text="Manage your passwords securely with advanced encryption",
                               font=('Segoe UI', welcome_text_font),
                               bg=CARD_BG, fg=TEXT_SECONDARY, wraplength=self.current_width-40)
        welcome_text.pack(anchor=tk.W, padx=welcome_padx, pady=(0, welcome_pady))
        
        # Menu buttons in responsive grid
        buttons_frame = tk.Frame(scrollable_frame, bg=LIGHT_BG)
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 15))
        
        buttons_info = [
            ("🔨", "Generate\nPassword", self.show_password_generator, ACCENT_COLOR),
            ("📋", "View\nPasswords", self.show_saved_passwords, GRADIENT_COLOR),
            ("🔍", "Search\nPassword", self.show_search_password, ACCENT_COLOR),
            ("✏️", "Update\nPassword", self.show_update_password, GRADIENT_COLOR),
            ("🗑️", "Delete\nPassword", self.show_delete_password, WARNING_COLOR),
            ("⚠️", "Clear\nAll", self.show_clear_all, ERROR_COLOR),
        ]
        
        # Create responsive grid (1, 2, or 3 columns based on window width)
        num_cols = self.get_button_columns()
        button_padding = self.get_responsive_padding(5)
        button_font_size = self.get_responsive_font_size(11)
        
        for idx, (emoji, text, command, color) in enumerate(buttons_info):
            row = idx // num_cols
            col = idx % num_cols
            
            btn_container = tk.Frame(buttons_frame, bg=LIGHT_BG)
            btn_container.grid(row=row, column=col, sticky='nsew', padx=button_padding, pady=button_padding)
            buttons_frame.grid_columnconfigure(col, weight=1)
            
            # Modern card button
            btn_card = tk.Frame(btn_container, bg=CARD_BG, relief=tk.FLAT, bd=0)
            btn_card.pack(fill=tk.BOTH, expand=True)
            self.add_shadow_effect(btn_card)
            
            btn_text_color = LIGHT_BG if color != CARD_BG else TEXT_PRIMARY
            btn_padding_x = self.get_responsive_padding(15)
            btn_padding_y = self.get_responsive_padding(20)
            btn_wrap_length = 80 if num_cols > 1 else 100
            
            btn = tk.Button(btn_card, 
                           text=f"{emoji}\n{text}",
                           font=('Segoe UI', button_font_size, 'bold'),
                           bg=color, fg=btn_text_color,
                           command=command,
                           padx=btn_padding_x, pady=btn_padding_y,
                           relief=tk.FLAT,
                           cursor="hand2",
                           activebackground=color,
                           activeforeground=LIGHT_BG,
                           bd=0,
                           highlightthickness=0,
                           wraplength=btn_wrap_length,
                           justify=tk.CENTER)
            btn.pack(fill=tk.BOTH, expand=True)
            
            # Hover effect binding
            btn.bind('<Enter>', lambda e, b=btn, c=color: self.on_button_hover(b, c, True))
            btn.bind('<Leave>', lambda e, b=btn, c=color: self.on_button_hover(b, c, False))
        
        # Footer frame - responsive sizing
        footer_height = 70 if self.size_category in ['medium', 'large'] else 60
        footer_frame = tk.Frame(self.root, bg=PRIMARY_COLOR, height=footer_height)
        footer_frame.grid(row=2, column=0, sticky='nsew')
        footer_frame.grid_propagate(False)
        
        exit_btn_font = self.get_responsive_font_size(11)
        exit_btn_padx = self.get_responsive_padding(20)
        exit_btn_pady = self.get_responsive_padding(12)
        exit_btn = tk.Button(footer_frame, text="❌ Exit Application",
                            font=('Segoe UI', exit_btn_font, 'bold'),
                            bg=ERROR_COLOR, fg=LIGHT_BG,
                            command=self.root.quit,
                            padx=exit_btn_padx, pady=exit_btn_pady,
                            relief=tk.FLAT,
                            cursor="hand2",
                            activebackground=WARNING_COLOR,
                            activeforeground=LIGHT_BG,
                            bd=0,
                            highlightthickness=0)
        exit_btn.pack(pady=exit_btn_pady, padx=15, fill=tk.X)
        
        exit_btn.bind('<Enter>', lambda e, b=exit_btn: self.on_button_hover(b, ERROR_COLOR, True))
        exit_btn.bind('<Leave>', lambda e, b=exit_btn: self.on_button_hover(b, ERROR_COLOR, False))
    
    def add_shadow_effect(self, frame, shadow_color='#CCCCCC', offset=2):
        """Add simple shadow effect to frame"""
        frame.config(relief=tk.FLAT, bd=0)
    
    def on_button_hover(self, button, base_color, is_hover):
        """Handle button hover effect"""
        if is_hover:
            new_color = self.lighten_color(base_color, 0.15)
            button.config(bg=new_color)
        else:
            button.config(bg=base_color)
    
    def lighten_color(self, color, factor=1.15):
        """Lighten a hex color for hover effects"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        lightened = tuple(min(int(c * factor), 255) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*lightened)
    
    def show_password_generator(self):
        """Display password generator screen with modern card design"""
        self.clear_window()
        
        # Header
        self.create_header("🔨 Generate New Password", ACCENT_COLOR)
        
        # Create main frame
        main_container = tk.Frame(self.root, bg=LIGHT_BG)
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Scrollable content
        canvas = tk.Canvas(main_container, bg=LIGHT_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=LIGHT_BG)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Password Length section - Modern Card
        length_card = tk.Frame(scrollable_frame, bg=CARD_BG, relief=tk.FLAT, bd=0)
        length_card.pack(pady=15, padx=15, fill=tk.X)
        self.add_shadow_effect(length_card)
        
        tk.Label(length_card, text="📏 Password Length",
                font=('Segoe UI', 12, 'bold'),
                bg=CARD_BG, fg=PRIMARY_COLOR, pady=12, padx=15).pack(fill=tk.X, anchor=tk.W)
        
        self.length_var = tk.IntVar(value=16)
        
        length_display_frame = tk.Frame(length_card, bg=CARD_BG)
        length_display_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        tk.Label(length_display_frame, text="Length:",
                font=('Segoe UI', 9),
                bg=CARD_BG, fg=TEXT_SECONDARY).pack(side=tk.LEFT)
        
        self.length_label = tk.Label(length_display_frame, text="16 characters",
                                    font=('Segoe UI', 10, 'bold'),
                                    bg=CARD_BG, fg=ACCENT_COLOR)
        self.length_label.pack(side=tk.LEFT, padx=8)
        
        length_scale = tk.Scale(length_card, from_=8, to=32,
                               orient=tk.HORIZONTAL,
                               bg=CARD_BG, fg=ACCENT_COLOR,
                               highlightthickness=0,
                               variable=self.length_var,
                               troughcolor=LIGHT_BG,
                               command=self.update_length_label,
                               relief=tk.FLAT,
                               bd=0)
        length_scale.pack(fill=tk.X, padx=15, pady=(0, 5))
        
        tk.Label(length_card, text="Recommended: 16 characters or more",
                font=('Segoe UI', 8),
                bg=CARD_BG, fg=TEXT_SECONDARY).pack(padx=15, pady=(0, 12))
        
        # Character set options - Modern Card
        options_card = tk.Frame(scrollable_frame, bg=CARD_BG, relief=tk.FLAT, bd=0)
        options_card.pack(pady=15, padx=15, fill=tk.X)
        self.add_shadow_effect(options_card)
        
        tk.Label(options_card, text="⚙️  Character Set Options",
                font=('Segoe UI', 12, 'bold'),
                bg=CARD_BG, fg=PRIMARY_COLOR, pady=12, padx=15).pack(fill=tk.X, anchor=tk.W)
        
        options_inner = tk.Frame(options_card, bg=CARD_BG)
        options_inner.pack(fill=tk.X, padx=15, pady=(0, 12))
        
        self.lowercase_var = tk.BooleanVar(value=True)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=True)
        
        for var, label in [
            (self.lowercase_var, "📝 Lowercase letters (a-z)"),
            (self.uppercase_var, "📝 Uppercase letters (A-Z)"),
            (self.numbers_var, "🔢 Numbers (0-9)"),
            (self.special_var, "⚡ Special characters (!@#$%^&*)")
        ]:
            chk_frame = tk.Frame(options_inner, bg=CARD_BG)
            chk_frame.pack(anchor=tk.W, pady=6, fill=tk.X)
            
            tk.Checkbutton(chk_frame, text=label,
                          variable=var,
                          font=('Segoe UI', 9),
                          bg=CARD_BG, fg=TEXT_PRIMARY,
                          activebackground=CARD_BG,
                          activeforeground=ACCENT_COLOR,
                          selectcolor=CARD_BG,
                          highlightthickness=0).pack(anchor=tk.W)
        
        # Generate button
        gen_btn = tk.Button(scrollable_frame, text="✨ GENERATE PASSWORD",
                           font=('Segoe UI', 11, 'bold'),
                           bg=ACCENT_COLOR, fg=PRIMARY_COLOR,
                           command=self.generate_password,
                           padx=20, pady=12,
                           relief=tk.FLAT,
                           cursor="hand2",
                           activebackground=GRADIENT_COLOR,
                           bd=0,
                           highlightthickness=0)
        gen_btn.pack(pady=15, padx=15, fill=tk.X, ipady=5)
        
        gen_btn.bind('<Enter>', lambda e, b=gen_btn: b.config(bg=GRADIENT_COLOR))
        gen_btn.bind('<Leave>', lambda e, b=gen_btn: b.config(bg=ACCENT_COLOR))
        
        # Password display frame
        self.password_display_frame = tk.Frame(scrollable_frame, bg=LIGHT_BG)
        self.password_display_frame.pack(pady=5, padx=15, fill=tk.BOTH, expand=True)
        
        # Back button at the end
        back_btn = tk.Button(scrollable_frame, text="← Back to Menu",
                            font=('Segoe UI', 9),
                            bg=SECONDARY_COLOR, fg=LIGHT_BG,
                            command=self.show_main_menu,
                            relief=tk.FLAT,
                            cursor="hand2",
                            bd=0,
                            highlightthickness=0,
                            padx=20, pady=10)
        back_btn.pack(fill=tk.X, pady=(0, 15), padx=15, ipady=3)
        
        back_btn.bind('<Enter>', lambda e, b=back_btn: b.config(bg=PRIMARY_COLOR))
        back_btn.bind('<Leave>', lambda e, b=back_btn: b.config(bg=SECONDARY_COLOR))
    
    def update_length_label(self, value):
        """Update length label with current value"""
        if hasattr(self, 'length_label'):
            self.length_label.config(text=f"{value} characters")
    
    def generate_password(self):
        """Generate password based on selected options"""
        length = self.length_var.get()
        
        # Build character set
        charset = ""
        if self.lowercase_var.get():
            charset += string.ascii_lowercase
        if self.uppercase_var.get():
            charset += string.ascii_uppercase
        if self.numbers_var.get():
            charset += string.digits
        if self.special_var.get():
            charset += string.punctuation
        
        if not charset:
            messagebox.showwarning("Warning", "Please select at least one character set!")
            return
        
        # Generate password
        password = ''.join(random.choice(charset) for _ in range(length))
        
        # Clear previous display
        for widget in self.password_display_frame.winfo_children():
            widget.destroy()
        
        # Display generated password in modern card
        result_card = tk.Frame(self.password_display_frame, bg=CARD_BG, relief=tk.FLAT, bd=0)
        result_card.pack(fill=tk.BOTH, expand=False, padx=0, pady=10)
        self.add_shadow_effect(result_card)
        
        # Title
        tk.Label(result_card, text="Generated Password",
                font=('Segoe UI', 11, 'bold'),
                bg=CARD_BG, fg=PRIMARY_COLOR, pady=12, padx=15).pack(fill=tk.X, anchor=tk.W)
        
        # Password display box
        pwd_box = tk.Frame(result_card, bg=LIGHT_BG, relief=tk.FLAT, bd=1)
        pwd_box.pack(fill=tk.X, padx=15, pady=(0, 12), ipady=10)
        
        pwd_label = tk.Label(pwd_box, text=password,
                            font=('Courier New', 10, 'bold'),
                            bg=LIGHT_BG, fg=ACCENT_COLOR,
                            wraplength=300, justify=tk.CENTER, padx=10)
        pwd_label.pack(fill=tk.BOTH, expand=True)
        
        # Copy button
        copy_btn = tk.Button(result_card, text="📋 Copy to Clipboard",
                            font=('Segoe UI', 9, 'bold'),
                            bg=ACCENT_COLOR, fg=PRIMARY_COLOR,
                            command=lambda: self.copy_to_clipboard(password),
                            relief=tk.FLAT,
                            padx=15, pady=8,
                            cursor="hand2",
                            bd=0,
                            highlightthickness=0)
        copy_btn.pack(pady=2, padx=15, fill=tk.X, ipady=2)
        
        copy_btn.bind('<Enter>', lambda e, b=copy_btn: b.config(bg=GRADIENT_COLOR))
        copy_btn.bind('<Leave>', lambda e, b=copy_btn: b.config(bg=ACCENT_COLOR))
        
        # Show strength analysis
        self.show_strength_analysis(result_card, password)
        
        # Save button
        save_btn = tk.Button(result_card, text="💾 Save This Password",
                            font=('Segoe UI', 10, 'bold'),
                            bg=SUCCESS_COLOR, fg=LIGHT_BG,
                            command=lambda: self.save_generated_password(password),
                            relief=tk.FLAT, padx=15, pady=8,
                            cursor="hand2",
                            bd=0,
                            highlightthickness=0)
        save_btn.pack(pady=(8, 15), padx=15, fill=tk.X, ipady=3)
        
        save_btn.bind('<Enter>', lambda e, b=save_btn: b.config(bg=self.lighten_color(SUCCESS_COLOR, 1.1)))
        save_btn.bind('<Leave>', lambda e, b=save_btn: b.config(bg=SUCCESS_COLOR))
    
    def show_strength_analysis(self, parent_frame, password):
        """Display password strength analysis"""
        strength = self.check_password_strength(password)
        issues = self.check_common_patterns(password)
        
        strength_map = {
            0: ("Very Weak", ERROR_COLOR),
            1: ("Weak", "#E67E22"),
            2: ("Fair", WARNING_COLOR),
            3: ("Good", "#F39C12"),
            4: ("Strong", SUCCESS_COLOR),
            5: ("Very Strong", SUCCESS_COLOR),
            6: ("Excellent", GRADIENT_COLOR),
            7: ("Excellent+", ACCENT_COLOR),
            8: ("Maximum", ACCENT_COLOR)
        }
        
        strength_label, strength_color = strength_map.get(strength, ("Unknown", TEXT_SECONDARY))
        
        # Strength display
        strength_frame = tk.Frame(parent_frame, bg=LIGHT_BG, relief=tk.FLAT, bd=0)
        strength_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(strength_frame, text="Password Strength:",
                font=('Segoe UI', 10, 'bold'),
                bg=LIGHT_BG, fg=PRIMARY_COLOR).pack(anchor=tk.W, pady=(0, 5))
        
        # Strength bar with percentage
        progress_frame = tk.Frame(strength_frame, bg=LIGHT_BG, relief=tk.FLAT, bd=0)
        progress_frame.pack(fill=tk.X)
        
        progress_bar = tk.Canvas(progress_frame, height=8, bg=LIGHT_BG,
                                highlightthickness=0, relief=tk.FLAT)
        progress_bar.pack(fill=tk.X, pady=3)
        
        progress_width = (strength / 8) * 300
        progress_bar.create_rectangle(0, 0, progress_width, 8,
                                     fill=strength_color, outline=strength_color)
        progress_bar.create_rectangle(progress_width, 0, 300, 8,
                                     fill=LIGHT_BG, outline=LIGHT_BG)
        
        # Strength text
        tk.Label(strength_frame, text=f"{strength_label} ({strength}/8)",
                font=('Segoe UI', 9, 'bold'),
                bg=LIGHT_BG, fg=strength_color).pack(anchor=tk.W, pady=(2, 0))
        
        # Issues or success
        if issues:
            issues_label = tk.Label(strength_frame, 
                                   text="⚠️  Improvement Suggestions:",
                                   font=('Segoe UI', 9, 'bold'),
                                   bg=LIGHT_BG, fg=WARNING_COLOR)
            issues_label.pack(anchor=tk.W, pady=(8, 3))
            
            issues_text = "\n".join([f"• {issue}" for issue in issues])
            tk.Label(strength_frame, text=issues_text,
                    font=('Segoe UI', 8),
                    bg=LIGHT_BG, fg=TEXT_SECONDARY, justify=tk.LEFT).pack(anchor=tk.W)
        else:
            success_label = tk.Label(strength_frame,
                                    text="✅ Excellent! No issues detected.",
                                    font=('Segoe UI', 9, 'bold'),
                                    bg=LIGHT_BG, fg=SUCCESS_COLOR)
            success_label.pack(anchor=tk.W, pady=(8, 0))
    
    def check_password_strength(self, password):
        """Calculate password strength score"""
        strength = 0
        
        if len(password) >= 8:
            strength += 1
        if len(password) >= 12:
            strength += 1
        if len(password) >= 16:
            strength += 1
        
        if re.search('[0-9]', password):
            strength += 1
        if re.search('[a-z]', password):
            strength += 1
        if re.search('[A-Z]', password):
            strength += 1
        if re.search(r'[#?!@$%^&*\-_=+\[\]{};:\'",.<>?/\\|`~]', password):
            strength += 1
        
        if not any(char in password.lower() for pattern in KEYBOARD_PATTERNS for char in pattern):
            strength += 1
        
        return min(strength, 8)
    
    def check_common_patterns(self, password):
        """Check for common weak patterns"""
        issues = []
        
        if password.lower() in WEAK_PASSWORDS:
            issues.append("This is a commonly used weak password")
        
        for pattern in KEYBOARD_PATTERNS:
            if pattern in password.lower():
                issues.append(f"Avoid keyboard patterns like '{pattern}'")
                break
        
        if re.search(r'(.)\1{2,}', password):
            issues.append("Avoid repeating characters")
        
        if re.search(r'(?:012|123|234|345|456|567|678|789|890)', password):
            issues.append("Avoid sequential numbers")
        
        return issues
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Success", "✅ Password copied to clipboard!")
    
    def save_generated_password(self, password):
        """Save the generated password"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Save Password")
        dialog.geometry("400x280")
        dialog.configure(bg=LIGHT_BG)
        dialog.resizable(False, False)
        
        # Center dialog
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Header
        header = tk.Frame(dialog, bg=PRIMARY_COLOR, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="💾 Save Password",
                font=('Segoe UI', 14, 'bold'),
                bg=PRIMARY_COLOR, fg=ACCENT_COLOR).pack(pady=12)
        
        # Content
        frame = tk.Frame(dialog, bg=LIGHT_BG)
        frame.pack(padx=20, pady=15, fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Password Name/Label:",
                font=('Segoe UI', 10, 'bold'),
                bg=LIGHT_BG, fg=PRIMARY_COLOR).pack(anchor=tk.W, pady=(0, 5))
        
        name_entry = tk.Entry(frame, font=('Segoe UI', 10), relief=tk.FLAT, bg=CARD_BG)
        name_entry.pack(fill=tk.X, pady=5, ipady=8)
        name_entry.focus()
        
        tk.Label(frame, text="Notes (optional):",
                font=('Segoe UI', 10, 'bold'),
                bg=LIGHT_BG, fg=PRIMARY_COLOR).pack(anchor=tk.W, pady=(10, 5))
        
        notes_text = tk.Text(frame, font=('Segoe UI', 9), height=3, relief=tk.FLAT, bg=CARD_BG)
        notes_text.pack(fill=tk.X, pady=5)
        
        button_frame = tk.Frame(frame, bg=LIGHT_BG)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        def save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("Warning", "Please enter a name for this password!")
                return
            
            notes = notes_text.get("1.0", tk.END).strip()
            strength = self.check_password_strength(password)
            
            if save_password(name, password, strength, notes):
                messagebox.showinfo("Success", f"✅ Password for '{name}' saved successfully!")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "❌ Failed to save password")
        
        save_btn = tk.Button(button_frame, text="💾 Save", font=('Segoe UI', 10, 'bold'),
                            bg=SUCCESS_COLOR, fg=LIGHT_BG, command=save,
                            relief=tk.FLAT, padx=15, pady=8, cursor="hand2",
                            bd=0, highlightthickness=0)
        save_btn.pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
        
        save_btn.bind('<Enter>', lambda e, b=save_btn: b.config(bg=self.lighten_color(SUCCESS_COLOR, 1.1)))
        save_btn.bind('<Leave>', lambda e, b=save_btn: b.config(bg=SUCCESS_COLOR))
        
        cancel_btn = tk.Button(button_frame, text="Cancel", font=('Segoe UI', 10),
                              bg=SECONDARY_COLOR, fg=LIGHT_BG, command=dialog.destroy,
                              relief=tk.FLAT, padx=15, pady=8, cursor="hand2",
                              bd=0, highlightthickness=0)
        cancel_btn.pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
        
        cancel_btn.bind('<Enter>', lambda e, b=cancel_btn: b.config(bg=PRIMARY_COLOR))
        cancel_btn.bind('<Leave>', lambda e, b=cancel_btn: b.config(bg=SECONDARY_COLOR))
    
    def show_saved_passwords(self):
        """Display saved passwords with modern card design"""
        self.clear_window()
        
        self.create_header("📋 Saved Passwords", GRADIENT_COLOR)
        
        passwords = get_all_passwords()
        
        if not passwords:
            content_frame = tk.Frame(self.root, bg=LIGHT_BG)
            content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            
            tk.Label(content_frame, text="📭 No saved passwords yet!",
                    font=('Segoe UI', 12, 'bold'),
                    bg=LIGHT_BG, fg=TEXT_SECONDARY).pack(pady=20)
            
            tk.Label(content_frame, text="Start by generating a new secure password",
                    font=('Segoe UI', 10),
                    bg=LIGHT_BG, fg=TEXT_SECONDARY).pack(pady=(0, 20))
            
            back_btn = tk.Button(content_frame, text="← Back to Menu",
                                font=('Segoe UI', 10, 'bold'),
                                bg=SECONDARY_COLOR, fg=LIGHT_BG,
                                command=self.show_main_menu,
                                relief=tk.FLAT, cursor="hand2",
                                padx=20, pady=10,
                                bd=0, highlightthickness=0)
            back_btn.pack(pady=10, fill=tk.X)
            back_btn.bind('<Enter>', lambda e, b=back_btn: b.config(bg=PRIMARY_COLOR))
            back_btn.bind('<Leave>', lambda e, b=back_btn: b.config(bg=SECONDARY_COLOR))
            return
        
        # Create scrollable content
        canvas_frame = tk.Frame(self.root, bg=LIGHT_BG)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        canvas = tk.Canvas(canvas_frame, bg=LIGHT_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=LIGHT_BG)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Strength map
        strength_map = {
            0: "Very Weak", 1: "Weak", 2: "Fair", 3: "Good",
            4: "Strong", 5: "Very Strong", 6: "Excellent", 7: "Excellent+", 8: "Maximum"
        }
        
        # Display each password as modern card
        for pwd_id, name, strength, created_at in passwords:
            pwd_card = tk.Frame(scrollable_frame, bg=CARD_BG, relief=tk.FLAT, bd=0)
            pwd_card.pack(fill=tk.X, padx=15, pady=8)
            self.add_shadow_effect(pwd_card)
            
            # Header with name and strength
            header_frame = tk.Frame(pwd_card, bg=CARD_BG)
            header_frame.pack(fill=tk.X, padx=15, pady=(12, 5))
            
            tk.Label(header_frame, text=f"🔐 {name}",
                    font=('Segoe UI', 11, 'bold'),
                    bg=CARD_BG, fg=PRIMARY_COLOR).pack(anchor=tk.W, side=tk.LEFT)
            
            # Strength indicator badge
            strength_colors = {
                0: ERROR_COLOR, 1: WARNING_COLOR, 2: "#E67E22", 3: "#F39C12",
                4: SUCCESS_COLOR, 5: ACCENT_COLOR, 6: GRADIENT_COLOR, 7: ACCENT_COLOR, 8: ACCENT_COLOR
            }
            
            strength_badge = tk.Frame(header_frame, bg=strength_colors.get(strength, TEXT_SECONDARY), relief=tk.FLAT, bd=0)
            strength_badge.pack(anchor=tk.E, side=tk.RIGHT, padx=5)
            
            tk.Label(strength_badge, text=f"💪 {strength_map.get(strength, 'Unknown')}",
                    font=('Segoe UI', 8, 'bold'),
                    bg=strength_colors.get(strength, TEXT_SECONDARY), fg=LIGHT_BG,
                    padx=8, pady=4).pack()
            
            # Created date
            tk.Label(pwd_card, text=f"Created: {created_at}",
                    font=('Segoe UI', 8),
                    bg=CARD_BG, fg=TEXT_SECONDARY).pack(anchor=tk.W, padx=15, pady=(0, 8))
            
            # Action buttons
            btn_frame = tk.Frame(pwd_card, bg=CARD_BG)
            btn_frame.pack(fill=tk.X, padx=15, pady=(0, 12))
            
            view_btn = tk.Button(btn_frame, text="👁️  View",
                                font=('Segoe UI', 9, 'bold'),
                                bg=ACCENT_COLOR, fg=PRIMARY_COLOR,
                                command=lambda n=name: self.view_password_detail(n),
                                relief=tk.FLAT, cursor="hand2",
                                padx=12, pady=6,
                                bd=0, highlightthickness=0)
            view_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
            view_btn.bind('<Enter>', lambda e, b=view_btn: b.config(bg=GRADIENT_COLOR))
            view_btn.bind('<Leave>', lambda e, b=view_btn: b.config(bg=ACCENT_COLOR))
            
            delete_btn = tk.Button(btn_frame, text="🗑️  Delete",
                                  font=('Segoe UI', 9, 'bold'),
                                  bg=ERROR_COLOR, fg=LIGHT_BG,
                                  command=lambda n=name: self.confirm_delete(n),
                                  relief=tk.FLAT, cursor="hand2",
                                  padx=12, pady=6,
                                  bd=0, highlightthickness=0)
            delete_btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
            delete_btn.bind('<Enter>', lambda e, b=delete_btn: b.config(bg=WARNING_COLOR))
            delete_btn.bind('<Leave>', lambda e, b=delete_btn: b.config(bg=ERROR_COLOR))
        
        # Back button at bottom
        back_frame = tk.Frame(self.root, bg=LIGHT_BG)
        back_frame.pack(fill=tk.X, padx=15, pady=12)
        
        back_btn = tk.Button(back_frame, text="← Back to Menu",
                            font=('Segoe UI', 10, 'bold'),
                            bg=SECONDARY_COLOR, fg=LIGHT_BG,
                            command=self.show_main_menu,
                            relief=tk.FLAT, cursor="hand2",
                            padx=20, pady=10,
                            bd=0, highlightthickness=0)
        back_btn.pack(fill=tk.X)
        back_btn.bind('<Enter>', lambda e, b=back_btn: b.config(bg=PRIMARY_COLOR))
        back_btn.bind('<Leave>', lambda e, b=back_btn: b.config(bg=SECONDARY_COLOR))
    
    def view_password_detail(self, name):
        """View password details in a modern popup"""
        result = get_password_by_name(name)
        
        if not result:
            messagebox.showerror("Error", f"Password '{name}' not found!")
            return
        
        password, strength, notes = result
        strength_map = {0: "Very Weak", 1: "Weak", 2: "Fair", 3: "Good",
                       4: "Strong", 5: "Very Strong", 6: "Excellent", 7: "Excellent+", 8: "Maximum"}
        
        strength_colors = {
            0: ERROR_COLOR, 1: WARNING_COLOR, 2: "#E67E22", 3: "#F39C12",
            4: SUCCESS_COLOR, 5: ACCENT_COLOR, 6: GRADIENT_COLOR, 7: ACCENT_COLOR, 8: ACCENT_COLOR
        }
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Password: {name}")
        dialog.geometry("450x300")
        dialog.configure(bg=LIGHT_BG)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Header
        header = tk.Frame(dialog, bg=PRIMARY_COLOR, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text=f"🔐 {name}",
                font=('Segoe UI', 14, 'bold'),
                bg=PRIMARY_COLOR, fg=ACCENT_COLOR).pack(pady=12)
        
        # Content card
        frame = tk.Frame(dialog, bg=LIGHT_BG)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        content_card = tk.Frame(frame, bg=CARD_BG, relief=tk.FLAT, bd=0)
        content_card.pack(fill=tk.BOTH, expand=True)
        self.add_shadow_effect(content_card)
        
        tk.Label(content_card, text="Password:",
                font=('Segoe UI', 10, 'bold'),
                bg=CARD_BG, fg=PRIMARY_COLOR).pack(anchor=tk.W, padx=15, pady=(12, 5))
        
        pwd_display = tk.Frame(content_card, bg=LIGHT_BG, relief=tk.FLAT, bd=1)
        pwd_display.pack(fill=tk.X, padx=15, pady=5, ipady=10)
        
        pwd_label = tk.Label(pwd_display, text=password,
                            font=('Courier New', 11, 'bold'),
                            bg=LIGHT_BG, fg=ACCENT_COLOR,
                            wraplength=350, justify=tk.CENTER)
        pwd_label.pack(fill=tk.BOTH, expand=True)
        
        # Strength
        strength_color = strength_colors.get(strength, TEXT_SECONDARY)
        tk.Label(content_card, text=f"💪 Strength: {strength_map.get(strength, 'Unknown')} ({strength}/8)",
                font=('Segoe UI', 10, 'bold'),
                bg=CARD_BG, fg=strength_color).pack(anchor=tk.W, padx=15, pady=10)
        
        # Notes
        if notes:
            tk.Label(content_card, text="📝 Notes:",
                    font=('Segoe UI', 10, 'bold'),
                    bg=CARD_BG, fg=PRIMARY_COLOR).pack(anchor=tk.W, padx=15, pady=(5, 2))
            
            notes_display = tk.Frame(content_card, bg=LIGHT_BG, relief=tk.FLAT, bd=1)
            notes_display.pack(fill=tk.X, padx=15, pady=5, ipady=8)
            
            tk.Label(notes_display, text=notes,
                    font=('Segoe UI', 9),
                    bg=LIGHT_BG, fg=TEXT_SECONDARY,
                    wraplength=350, justify=tk.LEFT).pack(fill=tk.BOTH, padx=8)
        
        # Action buttons
        btn_frame = tk.Frame(dialog, bg=LIGHT_BG)
        btn_frame.pack(fill=tk.X, padx=15, pady=12)
        
        copy_btn = tk.Button(btn_frame, text="📋 Copy Password",
                            font=('Segoe UI', 10, 'bold'),
                            bg=ACCENT_COLOR, fg=PRIMARY_COLOR,
                            command=lambda: self.copy_to_clipboard(password),
                            relief=tk.FLAT, cursor="hand2",
                            padx=15, pady=8,
                            bd=0, highlightthickness=0)
        copy_btn.pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
        copy_btn.bind('<Enter>', lambda e, b=copy_btn: b.config(bg=GRADIENT_COLOR))
        copy_btn.bind('<Leave>', lambda e, b=copy_btn: b.config(bg=ACCENT_COLOR))
        
        close_btn = tk.Button(btn_frame, text="Close",
                             font=('Segoe UI', 10),
                             bg=SECONDARY_COLOR, fg=LIGHT_BG,
                             command=dialog.destroy,
                             relief=tk.FLAT, cursor="hand2",
                             padx=15, pady=8,
                             bd=0, highlightthickness=0)
        close_btn.pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
        close_btn.bind('<Enter>', lambda e, b=close_btn: b.config(bg=PRIMARY_COLOR))
        close_btn.bind('<Leave>', lambda e, b=close_btn: b.config(bg=SECONDARY_COLOR))
    
    def confirm_delete(self, name):
        """Confirm password deletion"""
        if messagebox.askyesno("Confirm Delete", f"Delete password '{name}'? This action cannot be undone."):
            delete_password(name)
            messagebox.showinfo("Success", f"✅ Password '{name}' deleted!")
            self.show_saved_passwords()
    
    def show_search_password(self):
        """Search for a password with modern dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Search Password")
        dialog.geometry("400x180")
        dialog.configure(bg=LIGHT_BG)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Header
        header = tk.Frame(dialog, bg=PRIMARY_COLOR, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="🔍 Search Password",
                font=('Segoe UI', 14, 'bold'),
                bg=PRIMARY_COLOR, fg=ACCENT_COLOR).pack(pady=12)
        
        frame = tk.Frame(dialog, bg=LIGHT_BG)
        frame.pack(padx=20, pady=15, fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Password Name/Label:",
                font=('Segoe UI', 10, 'bold'),
                bg=LIGHT_BG, fg=PRIMARY_COLOR).pack(anchor=tk.W, pady=(0, 5))
        
        search_entry = tk.Entry(frame, font=('Segoe UI', 10), relief=tk.FLAT, bg=CARD_BG)
        search_entry.pack(fill=tk.X, pady=8, ipady=8)
        search_entry.focus()
        
        button_frame = tk.Frame(frame, bg=LIGHT_BG)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        def search():
            name = search_entry.get().strip()
            if not name:
                messagebox.showwarning("Warning", "Please enter a password name!")
                return
            
            if get_password_by_name(name):
                dialog.destroy()
                self.view_password_detail(name)
            else:
                messagebox.showerror("Not Found", f"Password '{name}' not found!")
        
        search_btn = tk.Button(button_frame, text="🔍 Search",
                              font=('Segoe UI', 10, 'bold'),
                              bg=ACCENT_COLOR, fg=PRIMARY_COLOR,
                              command=search, relief=tk.FLAT,
                              padx=15, pady=8, cursor="hand2",
                              bd=0, highlightthickness=0)
        search_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        search_btn.bind('<Enter>', lambda e, b=search_btn: b.config(bg=GRADIENT_COLOR))
        search_btn.bind('<Leave>', lambda e, b=search_btn: b.config(bg=ACCENT_COLOR))
        
        cancel_btn = tk.Button(button_frame, text="Cancel",
                              font=('Segoe UI', 10),
                              bg=SECONDARY_COLOR, fg=LIGHT_BG,
                              command=dialog.destroy,
                              relief=tk.FLAT, padx=15, pady=8, cursor="hand2",
                              bd=0, highlightthickness=0)
        cancel_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        cancel_btn.bind('<Enter>', lambda e, b=cancel_btn: b.config(bg=PRIMARY_COLOR))
        cancel_btn.bind('<Leave>', lambda e, b=cancel_btn: b.config(bg=SECONDARY_COLOR))
    
    def show_update_password(self):
        """Update existing password with modern dialog"""
        passwords = get_all_passwords()
        
        if not passwords:
            messagebox.showinfo("Info", "No saved passwords to update!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Password")
        dialog.geometry("420x240")
        dialog.configure(bg=LIGHT_BG)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Header
        header = tk.Frame(dialog, bg=PRIMARY_COLOR, height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="✏️  Update Password",
                font=('Segoe UI', 14, 'bold'),
                bg=PRIMARY_COLOR, fg=ACCENT_COLOR).pack(pady=12)
        
        frame = tk.Frame(dialog, bg=LIGHT_BG)
        frame.pack(padx=20, pady=15, fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Select Password:",
                font=('Segoe UI', 10, 'bold'),
                bg=LIGHT_BG, fg=PRIMARY_COLOR).pack(anchor=tk.W, pady=(0, 5))
        
        pwd_names = [pwd[1] for pwd in passwords]
        pwd_combo = ttk.Combobox(frame, values=pwd_names, font=('Segoe UI', 10),
                                state='readonly', width=35)
        pwd_combo.pack(fill=tk.X, pady=8, ipady=5)
        
        tk.Label(frame, text="New Password:",
                font=('Segoe UI', 10, 'bold'),
                bg=LIGHT_BG, fg=PRIMARY_COLOR).pack(anchor=tk.W, pady=(10, 5))
        
        new_pwd_entry = tk.Entry(frame, font=('Segoe UI', 10), relief=tk.FLAT, show="•", bg=CARD_BG)
        new_pwd_entry.pack(fill=tk.X, pady=8, ipady=8)
        
        button_frame = tk.Frame(frame, bg=LIGHT_BG)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        def update():
            name = pwd_combo.get()
            new_pwd = new_pwd_entry.get()
            
            if not name or not new_pwd:
                messagebox.showwarning("Warning", "Please select a password and enter a new one!")
                return
            
            strength = self.check_password_strength(new_pwd)
            if update_password(name, new_pwd, strength):
                messagebox.showinfo("Success", f"✅ Password '{name}' updated!")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "❌ Failed to update password")
        
        update_btn = tk.Button(button_frame, text="✏️  Update",
                              font=('Segoe UI', 10, 'bold'),
                              bg=ACCENT_COLOR, fg=PRIMARY_COLOR,
                              command=update, relief=tk.FLAT,
                              padx=15, pady=8, cursor="hand2",
                              bd=0, highlightthickness=0)
        update_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        update_btn.bind('<Enter>', lambda e, b=update_btn: b.config(bg=GRADIENT_COLOR))
        update_btn.bind('<Leave>', lambda e, b=update_btn: b.config(bg=ACCENT_COLOR))
        
        cancel_btn = tk.Button(button_frame, text="Cancel",
                              font=('Segoe UI', 10),
                              bg=SECONDARY_COLOR, fg=LIGHT_BG,
                              command=dialog.destroy,
                              relief=tk.FLAT, padx=15, pady=8, cursor="hand2",
                              bd=0, highlightthickness=0)
        cancel_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        cancel_btn.bind('<Enter>', lambda e, b=cancel_btn: b.config(bg=PRIMARY_COLOR))
        cancel_btn.bind('<Leave>', lambda e, b=cancel_btn: b.config(bg=SECONDARY_COLOR))
    
    def show_delete_password(self):
        """Delete a password with modern interface"""
        passwords = get_all_passwords()
        
        if not passwords:
            messagebox.showinfo("Info", "No saved passwords to delete!")
            return
        
        self.clear_window()
        self.create_header("🗑️  Delete Password", WARNING_COLOR)
        
        content_frame = tk.Frame(self.root, bg=LIGHT_BG)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        canvas = tk.Canvas(content_frame, bg=LIGHT_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=LIGHT_BG)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        tk.Label(scrollable_frame, text="Select a password to delete:",
                font=('Segoe UI', 11, 'bold'),
                bg=LIGHT_BG, fg=PRIMARY_COLOR).pack(anchor=tk.W, pady=10, padx=15)
        
        for pwd_id, name, strength, created_at in passwords:
            pwd_card = tk.Frame(scrollable_frame, bg=CARD_BG, relief=tk.FLAT, bd=0)
            pwd_card.pack(fill=tk.X, padx=15, pady=5)
            self.add_shadow_effect(pwd_card)
            
            info_frame = tk.Frame(pwd_card, bg=CARD_BG)
            info_frame.pack(fill=tk.X, padx=15, pady=12)
            
            tk.Label(info_frame, text=f"🔐 {name}",
                    font=('Segoe UI', 11, 'bold'),
                    bg=CARD_BG, fg=PRIMARY_COLOR).pack(anchor=tk.W, side=tk.LEFT, expand=True)
            
            delete_btn = tk.Button(info_frame, text="🗑️  Delete",
                                  font=('Segoe UI', 9, 'bold'),
                                  bg=ERROR_COLOR, fg=LIGHT_BG,
                                  command=lambda n=name: self.confirm_and_delete(n),
                                  relief=tk.FLAT, cursor="hand2",
                                  padx=15, pady=6,
                                  bd=0, highlightthickness=0)
            delete_btn.pack(anchor=tk.E, side=tk.RIGHT)
            delete_btn.bind('<Enter>', lambda e, b=delete_btn: b.config(bg=WARNING_COLOR))
            delete_btn.bind('<Leave>', lambda e, b=delete_btn: b.config(bg=ERROR_COLOR))
        
        # Back button
        back_frame = tk.Frame(self.root, bg=LIGHT_BG)
        back_frame.pack(fill=tk.X, padx=15, pady=12)
        
        back_btn = tk.Button(back_frame, text="← Back to Menu",
                            font=('Segoe UI', 10, 'bold'),
                            bg=SECONDARY_COLOR, fg=LIGHT_BG,
                            command=self.show_main_menu,
                            relief=tk.FLAT, cursor="hand2",
                            padx=20, pady=10,
                            bd=0, highlightthickness=0)
        back_btn.pack(fill=tk.X)
        back_btn.bind('<Enter>', lambda e, b=back_btn: b.config(bg=PRIMARY_COLOR))
        back_btn.bind('<Leave>', lambda e, b=back_btn: b.config(bg=SECONDARY_COLOR))
    
    def confirm_and_delete(self, name):
        """Confirm and delete a password"""
        if messagebox.askyesno("Confirm Delete", f"Delete password '{name}'? This action cannot be undone."):
            delete_password(name)
            messagebox.showinfo("Success", f"✅ Password '{name}' deleted!")
            self.show_delete_password()
    
    def show_clear_all(self):
        """Clear all passwords with confirmation"""
        if messagebox.askyesno("⚠️  WARNING", "Delete ALL saved passwords? This action is permanent and cannot be undone!"):
            clear_all_passwords()
            messagebox.showinfo("Success", "✅ All passwords cleared!")
            self.show_main_menu()
    
    def create_header(self, title, color=PRIMARY_COLOR):
        """Create modern header frame with accent color - responsive sizing"""
        header_height = 70 if self.size_category == 'small' else (75 if self.size_category == 'medium' else 85)
        header_frame = tk.Frame(self.root, bg=PRIMARY_COLOR, height=header_height)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Decorative accent bar
        accent_bar = tk.Frame(header_frame, bg=color, height=4)
        accent_bar.pack(fill=tk.X, side=tk.TOP)
        accent_bar.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg=PRIMARY_COLOR)
        header_content.pack(fill=tk.BOTH, expand=True, padx=15)
        
        header_font_size = self.get_responsive_font_size(18)
        header_pady = self.get_responsive_padding(12)
        title_label = tk.Label(header_content, text=title,
                              font=('Segoe UI', header_font_size, 'bold'),
                              bg=PRIMARY_COLOR, fg=color, pady=header_pady)
        title_label.pack(anchor=tk.CENTER)


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()
