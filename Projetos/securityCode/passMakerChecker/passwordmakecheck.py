import string
import random
import re

# Common weak passwords to check against
WEAK_PASSWORDS = [
    'password', '123456', 'qwerty', 'abc123', 'admin', 'letmein',
    '111111', '123123', 'welcome', 'dragon', 'master', 'monkey',
    'princess', 'admin123', 'password123', 'qwerty123'
]

# Keyboard patterns (common sequences)
KEYBOARD_PATTERNS = [
    'qwerty', 'asdf', 'zxcv', '123456', '789', 'qazwsx', '1234567890'
]

def check_strength(password):
    """Calculate password strength score"""
    strength = 0
    feedback = []
    
    # Length check
    if len(password) >= 8:
        strength += 1
    if len(password) >= 12:
        strength += 1
    if len(password) >= 16:
        strength += 1
    
    # Character variety
    if re.search('[0-9]', password):
        strength += 1
    else:
        feedback.append("❌ Add numbers (0-9)")
    
    if re.search('[a-z]', password):
        strength += 1
    else:
        feedback.append("❌ Add lowercase letters (a-z)")
    
    if re.search('[A-Z]', password):
        strength += 1
    else:
        feedback.append("❌ Add uppercase letters (A-Z)")
    
    if re.search(r'[#?!@$%^&*\-_=+\[\]{};:\'",.<>?/\\|`~]', password):
        strength += 1
    else:
        feedback.append("❌ Add special characters (!@#$%^&*)")
    
    return strength, feedback

def check_common_patterns(password):
    """Check for common weak patterns"""
    issues = []
    
    # Check for common weak passwords
    if password.lower() in WEAK_PASSWORDS:
        issues.append("⚠️  This is a commonly used weak password")
    
    # Check for keyboard patterns
    for pattern in KEYBOARD_PATTERNS:
        if pattern in password.lower():
            issues.append(f"⚠️  Avoid keyboard patterns like '{pattern}'")
    
    # Check for repeated characters (3+ in a row)
    if re.search(r'(.)\1{2,}', password):
        issues.append("⚠️  Avoid repeating characters (aaa, 111, etc)")
    
    # Check for sequential numbers
    if re.search(r'(?:012|123|234|345|456|567|678|789|890)', password):
        issues.append("⚠️  Avoid sequential numbers (123, 456, etc)")
    
    # Check for sequential letters
    if re.search(r'(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
        issues.append("⚠️  Avoid sequential letters (abc, bcd, etc)")
    
    return issues

def validate(password):
    """Comprehensive password validation"""
    print("\n" + "=" * 60)
    print("🔐 PASSWORD SECURITY ANALYSIS")
    print("=" * 60)
    
    strength, feedback = check_strength(password)
    pattern_issues = check_common_patterns(password)
    
    # Display strength meter
    strength_levels = ["Very Weak", "Weak", "Fair", "Good", "Strong", "Very Strong", "Excellent", "Excellent+"]
    strength_colors = ["🔴", "🟠", "🟡", "🟢", "🟢", "💚", "💚", "💚"]
    
    print(f"\n📊 Password Strength: {strength_colors[min(strength, 7)]} {strength_levels[min(strength, 7)]}")
    print(f"   Score: {strength}/8")
    
    # Display feedback
    if feedback:
        print("\n📋 Suggestions for Improvement:")
        for item in feedback:
            print(f"   {item}")
    
    # Display pattern warnings
    if pattern_issues:
        print("\n⚠️  Security Warnings:")
        for issue in pattern_issues:
            print(f"   {issue}")
    
    # Display password length
    print(f"\n📏 Password Length: {len(password)} characters", end="")
    if len(password) < 8:
        print(" (⚠️ Too short - recommend 12+ characters)")
    elif len(password) < 12:
        print(" (⚠️ Consider making it longer - 12+ recommended)")
    else:
        print(" (✓ Good length)")
    
    # Final verdict
    print("\n" + "-" * 60)
    if strength >= 7 and not pattern_issues:
        print("✅ EXCELLENT! Your password is very secure!")
    elif strength >= 5 and len(pattern_issues) <= 1:
        print("✅ GOOD! Your password is reasonably secure.")
    elif strength >= 4:
        print("⚠️  FAIR! Consider implementing the suggestions above.")
    else:
        print("❌ WEAK! Please create a stronger password.")
    print("=" * 60 + "\n")

def generate_secure_password(length):
    """Generate a secure random password"""
    # Ensure all character types are included
    password = []
    password.append(random.choice(string.ascii_lowercase))
    password.append(random.choice(string.ascii_uppercase))
    password.append(random.choice(string.digits))
    password.append(random.choice(string.punctuation))
    
    # Fill the rest with random characters from all sets
    all_chars = string.ascii_letters + string.digits + string.punctuation
    for i in range(length - 4):
        password.append(random.choice(all_chars))
    
    # Shuffle to avoid predictable patterns
    random.shuffle(password)
    return ''.join(password)

# Main program
print("\n" + "=" * 60)
print("🔑 PASSWORD GENERATOR & SECURITY CHECKER")
print("=" * 60)

# Getting password length
while True:
    try:
        length = int(input("\nEnter password length (minimum 8, recommended 12+): "))
        if length < 8:
            print("❌ Password length should be at least 8 (recommended 12 or more)")
            continue
        break
    except ValueError:
        print("❌ Please enter a valid number")

print(f'\n📋 Choose character set for password:')
print(f'   1. Digits (0-9)')
print(f'   2. Letters (a-z, A-Z)')
print(f'   3. Special characters (!@#$%^&*)')
print(f'   4. Generate Secure Password (Recommended)')
print(f'   5. Exit')

characterList = ""
use_secure = False

# Getting character set for password
while True:
    try:
        choice = int(input("\n👉 Pick a number (1-5): "))
        if choice == 1:
            characterList += string.digits
            print("✓ Added digits")
        elif choice == 2:
            characterList += string.ascii_letters
            print("✓ Added letters")
        elif choice == 3:
            characterList += string.punctuation
            print("✓ Added special characters")
        elif choice == 4:
            use_secure = True
            print("✓ Using secure password generation")
            break
        elif choice == 5:
            print("Exiting...")
            exit()
        else:
            print("❌ Please pick a valid option (1-5)!")
            continue
        
        next_choice = input("Add more character types? (y/n): ").lower()
        if next_choice != 'y':
            break
    except ValueError:
        print("❌ Please enter a valid number")

if use_secure:
    password = generate_secure_password(length)
    print("\n" + "=" * 60)
    print("🔐 Generated Secure Password:")
    print("=" * 60)
    print(f"Password: {password}\n")
else:
    if not characterList:
        print("❌ No character set selected! Using default (all characters)")
        characterList = string.ascii_letters + string.digits + string.punctuation
    
    password = []
    for i in range(length):
        randomchar = random.choice(characterList)
        password.append(randomchar)
    
    password_str = "".join(password)
    print("\n" + "=" * 60)
    print("🔐 Generated Password:")
    print("=" * 60)
    print(f"Password: {password_str}\n")
    password = password_str

validate(password)