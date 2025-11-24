"""
Create simple placeholder PNG icons for PWA
Run this to generate basic icons without external dependencies
"""

from pathlib import Path
import base64

# Simple 1x1 blue pixel PNG (will be stretched by browser)
BLUE_PNG_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

SIZES = [72, 96, 128, 144, 152, 192, 384, 512]
ICON_DIR = Path(__file__).parent / "static" / "icons"
ICON_DIR.mkdir(parents=True, exist_ok=True)

print("Creating placeholder PWA icons...")

# Decode base64 PNG
png_data = base64.b64decode(BLUE_PNG_BASE64)

for size in SIZES:
    output_file = ICON_DIR / f"icon-{size}x{size}.png"
    with open(output_file, "wb") as f:
        f.write(png_data)
    print(f"✓ Created {output_file.name}")

print(f"\n✅ Created {len(SIZES)} placeholder icons!")
print("\n📱 PWA is ready! To create better icons:")
print("1. Visit https://realfavicongenerator.net/")
print("2. Upload a 512x512 image or your logo")
print("3. Download and replace files in static/icons/")
