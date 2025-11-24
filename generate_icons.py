"""
Generate PWA icons from SVG
Run: python generate_icons.py
Requires: pip install pillow cairosvg
"""

import os
from pathlib import Path

try:
    from cairosvg import svg2png
    from PIL import Image

    SIZES = [72, 96, 128, 144, 152, 192, 384, 512]
    ICON_DIR = Path(__file__).parent / "static" / "icons"
    SVG_FILE = ICON_DIR / "icon.svg"

    print("Generating PWA icons...")

    with open(SVG_FILE, "r") as f:
        svg_data = f.read()

    for size in SIZES:
        output_file = ICON_DIR / f"icon-{size}x{size}.png"
        svg2png(
            bytestring=svg_data.encode("utf-8"),
            write_to=str(output_file),
            output_width=size,
            output_height=size,
        )
        print(f"✓ Created {output_file.name}")

    print(f"\n✅ Successfully generated {len(SIZES)} icons!")
    print("\n📱 Your PWA is ready to install on Android!")

except ImportError:
    print("⚠️  cairosvg or pillow not installed.")
    print("\nTo generate icons automatically, install:")
    print("  pip install pillow cairosvg")
    print("\nAlternatively, you can:")
    print("1. Use online tools like https://realfavicongenerator.net/")
    print("2. Upload static/icons/icon.svg")
    print("3. Download generated icons to static/icons/")
    print("\nFor now, PWA will work but without icons.")
