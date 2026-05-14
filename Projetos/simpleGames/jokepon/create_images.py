"""Create images for Rock, Paper, Scissors game"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_hand_images():
    """Create rock, paper, scissors hand images"""
    
    # Create images folder if it doesn't exist
    images_folder = os.path.join(os.path.dirname(__file__), 'images')
    os.makedirs(images_folder, exist_ok=True)
    
    # Image dimensions
    width, height = 200, 200
    background_color = (255, 255, 255)
    
    # Create Rock image
    rock_img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(rock_img)
    # Draw a circle representing rock (fist)
    draw.ellipse([50, 50, 150, 150], fill=(100, 100, 100), outline=(0, 0, 0), width=3)
    rock_img.save(os.path.join(images_folder, 'rock.png'))
    
    # Create Paper image
    paper_img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(paper_img)
    # Draw a rectangle representing paper (open hand)
    draw.rectangle([40, 60, 160, 140], fill=(200, 200, 200), outline=(0, 0, 0), width=3)
    # Draw fingers
    draw.rectangle([50, 30, 70, 60], fill=(200, 200, 200), outline=(0, 0, 0), width=3)
    draw.rectangle([80, 20, 100, 60], fill=(200, 200, 200), outline=(0, 0, 0), width=3)
    draw.rectangle([110, 30, 130, 60], fill=(200, 200, 200), outline=(0, 0, 0), width=3)
    draw.rectangle([140, 50, 160, 80], fill=(200, 200, 200), outline=(0, 0, 0), width=3)
    paper_img.save(os.path.join(images_folder, 'paper.png'))
    
    # Create Scissors image
    scissors_img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(scissors_img)
    # Draw two circles for scissors handles
    draw.ellipse([30, 70, 70, 110], fill=(150, 150, 150), outline=(0, 0, 0), width=3)
    draw.ellipse([130, 70, 170, 110], fill=(150, 150, 150), outline=(0, 0, 0), width=3)
    # Draw scissors blades
    draw.line([70, 90, 130, 50], fill=(100, 100, 100), width=4)
    draw.line([70, 90, 130, 130], fill=(100, 100, 100), width=4)
    scissors_img.save(os.path.join(images_folder, 'scissors.png'))
    
    print("✓ Images created successfully in 'images' folder")

if __name__ == '__main__':
    create_hand_images()
