#!/usr/bin/env python3
"""
Create placeholder images for team members
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(name, filename, size=(400, 400)):
    """Create a placeholder image with the person's name"""
    try:
        # Create a new image with gradient background
        img = Image.new('RGB', size, color='#667eea')
        draw = ImageDraw.Draw(img)
        
        # Create gradient effect
        for y in range(size[1]):
            color_value = int(255 * (y / size[1]))
            color = (102 + color_value // 3, 126 + color_value // 3, 234 - color_value // 3)
            draw.line([(0, y), (size[0], y)], fill=color)
        
        # Add a circle in the center
        circle_size = min(size) // 2
        circle_x = (size[0] - circle_size) // 2
        circle_y = (size[1] - circle_size) // 2
        
        # Draw circle background
        draw.ellipse([circle_x, circle_y, circle_x + circle_size, circle_y + circle_size], 
                    fill=(255, 255, 255, 50), outline='white', width=3)
        
        # Add person icon (simple stick figure)
        icon_size = circle_size // 3
        icon_x = circle_x + circle_size // 2 - icon_size // 2
        icon_y = circle_y + circle_size // 2 - icon_size // 2
        
        # Draw head (circle)
        head_radius = icon_size // 4
        draw.ellipse([icon_x + icon_size//2 - head_radius, icon_y + icon_size//4 - head_radius,
                     icon_x + icon_size//2 + head_radius, icon_y + icon_size//4 + head_radius], 
                    fill='white')
        
        # Draw body (line)
        body_start_y = icon_y + icon_size//4 + head_radius
        body_end_y = icon_y + icon_size - icon_size//4
        draw.line([icon_x + icon_size//2, body_start_y, icon_x + icon_size//2, body_end_y], 
                 fill='white', width=3)
        
        # Draw arms
        arm_y = body_start_y + (body_end_y - body_start_y) // 3
        draw.line([icon_x + icon_size//2 - icon_size//3, arm_y, icon_x + icon_size//2 + icon_size//3, arm_y], 
                 fill='white', width=3)
        
        # Draw legs
        leg_start_y = body_end_y
        leg_end_y = icon_y + icon_size
        draw.line([icon_x + icon_size//2, leg_start_y, icon_x + icon_size//2 - icon_size//4, leg_end_y], 
                 fill='white', width=3)
        draw.line([icon_x + icon_size//2, leg_start_y, icon_x + icon_size//2 + icon_size//4, leg_end_y], 
                 fill='white', width=3)
        
        # Add name text
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
        
        # Get text size
        if font:
            bbox = draw.textbbox((0, 0), name, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            text_width = len(name) * 10
            text_height = 20
        
        # Position text at bottom
        text_x = (size[0] - text_width) // 2
        text_y = size[1] - text_height - 20
        
        # Draw text background
        padding = 10
        draw.rectangle([text_x - padding, text_y - padding, 
                       text_x + text_width + padding, text_y + text_height + padding], 
                      fill=(0, 0, 0, 180))
        
        # Draw text
        draw.text((text_x, text_y), name, fill='white', font=font)
        
        # Save the image
        img.save(filename, 'JPEG', quality=85)
        return True
        
    except Exception as e:
        print(f"Error creating image for {name}: {e}")
        return False

def create_team_placeholders():
    """Create placeholder images for all team members"""
    try:
        # Create uploads directory if it doesn't exist
        uploads_dir = 'static/uploads'
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Team members data
        team_members = [
            {'name': 'Alex Rodriguez', 'filename': 'team_1_alex_rodriguez.jpg'},
            {'name': 'Sarah Chen', 'filename': 'team_2_sarah_chen.jpg'},
            {'name': 'Mike Thompson', 'filename': 'team_3_mike_thompson.jpg'}
        ]
        
        created_count = 0
        for member in team_members:
            filepath = os.path.join(uploads_dir, member['filename'])
            if create_placeholder_image(member['name'], filepath):
                print(f"✅ Created placeholder image: {member['filename']}")
                created_count += 1
            else:
                print(f"❌ Failed to create image for {member['name']}")
        
        print(f"\n✅ Created {created_count} placeholder images")
        return True
        
    except Exception as e:
        print(f"❌ Error creating team placeholders: {e}")
        return False

if __name__ == "__main__":
    print("Creating placeholder images for team members...")
    success = create_team_placeholders()
    if success:
        print("\n✅ Team placeholder images created successfully!")
    else:
        print("\n❌ Failed to create team placeholder images.")
