#!/usr/bin/env python3
"""
Generate a custom banner.png for GitHub profile (1280x360)
Dark/purple gradient aesthetic matching Kiran1689's style
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_banner():
    # Dimensions
    WIDTH = 1280
    HEIGHT = 360

    # Create base image with dark gradient background
    img = Image.new('RGB', (WIDTH, HEIGHT), color='#0d1117')
    draw = ImageDraw.Draw(img)

    # Create gradient background (dark to purple)
    for y in range(HEIGHT):
        # Gradient from dark (#0d1117) to purple (#1f0c36) to darker
        ratio = y / HEIGHT
        if ratio < 0.5:
            # Top half: dark to purple
            r = int(13 + (31 - 13) * (ratio * 2))
            g = int(17 + (12 - 17) * (ratio * 2))
            b = int(23 + (54 - 23) * (ratio * 2))
        else:
            # Bottom half: purple to darker
            r = int(31 + (13 - 31) * ((ratio - 0.5) * 2))
            g = int(12 + (17 - 12) * ((ratio - 0.5) * 2))
            b = int(54 + (23 - 54) * ((ratio - 0.5) * 2))
        color = (r, g, b)
        draw.line([(0, y), (WIDTH, y)], fill=color)

    # Add subtle grid pattern lines (very faint)
    for i in range(0, WIDTH, 64):
        draw.line([(i, 0), (i, HEIGHT)], fill='#1f1f3a', width=1)
    for i in range(0, HEIGHT, 64):
        draw.line([(0, i), (WIDTH, i)], fill='#1f1f3a', width=1)

    # Add glowing accent line (horizontal purple line)
    accent_y = HEIGHT // 3
    for x in range(WIDTH):
        alpha = int(100 * (1 - abs(x - WIDTH/2) / (WIDTH/2)))
        if alpha > 10:
            draw.point((x, accent_y), fill=(139, 92, 246, alpha))

    # Try to load fonts, fallback to default
    try:
        title_font = ImageFont.truetype("arialbd.ttf", 52)
        subtitle_font = ImageFont.truetype("arial.ttf", 24)
        info_font = ImageFont.truetype("arial.ttf", 20)
    except:
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            info_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            info_font = ImageFont.load_default()

    # Center title
    title = "MOHAMMED AMINE ELBOUHALI"
    subtitle = "WELCOME TO MY PROFILE"

    # Calculate positions
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (WIDTH - title_width) // 2
    title_y = HEIGHT // 2 - 60

    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (WIDTH - subtitle_width) // 2
    subtitle_y = title_y + 60

    # Draw title with glow effect (multiple layers)
    glow_color = (139, 92, 246)  # Purple
    for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2), (0, 2), (2, 0), (-2, 0), (0, -2)]:
        draw.text((title_x + offset[0], title_y + offset[1]), title, font=title_font, fill=glow_color)

    # Main title
    draw.text((title_x, title_y), title, font=title_font, fill='#ffffff')

    # Subtitle with subtle glow
    for offset in [(1, 1), (-1, -1)]:
        draw.text((subtitle_x + offset[0], subtitle_y + offset[1]), subtitle, font=subtitle_font, fill=glow_color)
    draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill='#a1a1aa')

    # Left side: GitHub
    github_text = "github.com/oblackx"
    github_bbox = draw.textbbox((0, 0), github_text, font=info_font)
    github_width = github_bbox[2] - github_bbox[0]
    github_x = 80
    github_y = HEIGHT - 80

    # Draw globe icon (simple circle with lines)
    icon_size = 24
    icon_x = github_x - 34
    icon_y = github_y - 2
    # Globe circle
    draw.ellipse([icon_x, icon_y, icon_x + icon_size, icon_y + icon_size], outline='#8b5cf6', width=2)
    # Globe lines
    cx, cy = icon_x + icon_size//2, icon_y + icon_size//2
    r = icon_size//2 - 2
    draw.line([(cx - r, cy), (cx + r, cy)], fill='#8b5cf6', width=1)
    draw.line([(cx, cy - r), (cx, cy + r)], fill='#8b5cf6', width=1)
    draw.ellipse([cx - r, cy - r//2, cx + r, cy + r//2], outline='#8b5cf6', width=1)

    draw.text((github_x, github_y), github_text, font=info_font, fill='#a1a1aa')

    # Right side: Email
    email_text = "amineelbouhali6@gmail.com"
    email_bbox = draw.textbbox((0, 0), email_text, font=info_font)
    email_width = email_bbox[2] - email_bbox[0]
    email_x = WIDTH - email_width - 80
    email_y = HEIGHT - 80

    # Draw mail icon (envelope)
    icon_x = email_x + email_width + 10
    icon_y = email_y - 2
    # Envelope shape
    draw.polygon([
        (icon_x, icon_y),
        (icon_x + 24, icon_y),
        (icon_x + 24, icon_y + 18),
        (icon_x + 12, icon_y + 10),
        (icon_x, icon_y + 18)
    ], outline='#8b5cf6', width=2)
    # Envelope flap
    draw.line([(icon_x + 2, icon_y + 16), (icon_x + 22, icon_y + 16)], fill='#8b5cf6', width=1)

    draw.text((email_x, email_y), email_text, font=info_font, fill='#a1a1aa')

    # Add subtle top decorative elements
    # Three small dots on top left
    for i in range(3):
        x = 40 + i * 18
        y = 30
        draw.ellipse([x, y, x + 8, y + 8], fill='#8b5cf6')

    # Version/badge on top right
    badge_text = "v2026.11"
    badge_bbox = draw.textbbox((0, 0), badge_text, font=info_font)
    badge_width = badge_bbox[2] - badge_bbox[0]
    draw.rounded_rectangle(
        [WIDTH - badge_width - 30, 20, WIDTH - 20, 48],
        radius=8,
        fill='#1e1e3f',
        outline='#8b5cf6'
    )
    draw.text((WIDTH - badge_width - 20, 22), badge_text, font=info_font, fill='#8b5cf6')

    # Save
    output_path = "banner.png"
    img.save(output_path, "PNG", quality=95)
    print(f"Banner saved to {output_path} ({WIDTH}x{HEIGHT})")
    return output_path

if __name__ == "__main__":
    create_banner()