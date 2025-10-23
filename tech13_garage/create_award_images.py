#!/usr/bin/env python3
"""
Create placeholder award images for TECH13 Garage
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_award_image(filename, title, subtitle, bg_color=(102, 126, 234), text_color=(255, 255, 255)):
    """Create a placeholder award image"""
    
    # Create image with gradient background
    width, height = 400, 300
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Create gradient effect
    for y in range(height):
        ratio = y / height
        r = int(bg_color[0] * (1 - ratio) + 118 * ratio)
        g = int(bg_color[1] * (1 - ratio) + 75 * ratio)
        b = int(bg_color[2] * (1 - ratio) + 162 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Add border
    draw.rectangle([0, 0, width-1, height-1], outline=(255, 255, 255), width=3)
    
    # Add trophy icon
    trophy_size = 80
    trophy_x = (width - trophy_size) // 2
    trophy_y = 50
    
    # Trophy base
    draw.rectangle([trophy_x + 20, trophy_y + 60, trophy_x + 60, trophy_y + 80], fill=text_color)
    # Trophy handles
    draw.arc([trophy_x + 10, trophy_y + 40, trophy_x + 30, trophy_y + 60], 0, 180, fill=text_color, width=5)
    draw.arc([trophy_x + 50, trophy_y + 40, trophy_x + 70, trophy_y + 60], 0, 180, fill=text_color, width=5)
    # Trophy cup
    draw.ellipse([trophy_x + 25, trophy_y + 20, trophy_x + 55, trophy_y + 60], outline=text_color, width=5)
    
    # Add text
    try:
        # Try to use a system font
        title_font = ImageFont.truetype("arial.ttf", 24)
        subtitle_font = ImageFont.truetype("arial.ttf", 16)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Center text
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    
    # Draw text with shadow
    shadow_offset = 2
    draw.text((title_x + shadow_offset, 140 + shadow_offset), title, font=title_font, fill=(0, 0, 0, 128))
    draw.text((title_x, 140), title, font=title_font, fill=text_color)
    
    draw.text((subtitle_x + shadow_offset, 170 + shadow_offset), subtitle, font=subtitle_font, fill=(0, 0, 0, 128))
    draw.text((subtitle_x, 170), subtitle, font=subtitle_font, fill=text_color)
    
    # Add decorative elements
    for i in range(5):
        x = 50 + i * 70
        y = 220
        draw.ellipse([x-3, y-3, x+3, y+3], fill=text_color)
    
    # Save image
    image.save(filename, 'JPEG', quality=95)
    print(f"Created: {filename}")

def main():
    """Create all award images"""
    
    # Ensure directory exists
    os.makedirs('static/images/awards', exist_ok=True)
    
    # Award images to create
    awards = [
        {
            'filename': 'static/images/awards/racing-championship-2023.jpg',
            'title': 'Racing Championship 2023',
            'subtitle': '1st Place - National Motorcycle Racing',
            'bg_color': (220, 38, 38)  # Red for racing
        },
        {
            'filename': 'static/images/awards/best-service-2023.jpg',
            'title': 'Best Service Award 2023',
            'subtitle': 'Excellence in Customer Service',
            'bg_color': (34, 197, 94)  # Green for service
        },
        {
            'filename': 'static/images/awards/innovation-award-2022.jpg',
            'title': 'Innovation Award 2022',
            'subtitle': 'Technical Innovation in Racing',
            'bg_color': (59, 130, 246)  # Blue for innovation
        },
        {
            'filename': 'static/images/awards/team-championship-2023.jpg',
            'title': 'Team Championship 2023',
            'subtitle': 'Best Racing Team Performance',
            'bg_color': (168, 85, 247)  # Purple for team
        },
        {
            'filename': 'static/images/awards/quality-certification-2023.jpg',
            'title': 'Quality Certification 2023',
            'subtitle': 'ISO 9001 Quality Management',
            'bg_color': (245, 158, 11)  # Gold for quality
        },
        {
            'filename': 'static/images/awards/safety-award-2023.jpg',
            'title': 'Safety Award 2023',
            'subtitle': 'Excellence in Safety Standards',
            'bg_color': (16, 185, 129)  # Teal for safety
        },
        {
            'filename': 'static/images/awards/customer-choice-2023.jpg',
            'title': 'Customer Choice 2023',
            'subtitle': 'Most Trusted Motorcycle Service',
            'bg_color': (236, 72, 153)  # Pink for customer choice
        },
        {
            'filename': 'static/images/awards/performance-award-2022.jpg',
            'title': 'Performance Award 2022',
            'subtitle': 'Outstanding Racing Performance',
            'bg_color': (102, 126, 234)  # Blue for performance
        }
    ]
    
    # Create all award images
    for award in awards:
        create_award_image(
            award['filename'],
            award['title'],
            award['subtitle'],
            award['bg_color']
        )
    
    print(f"\n✅ Created {len(awards)} award images in static/images/awards/")

if __name__ == "__main__":
    main()
