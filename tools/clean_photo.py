from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove

# ----------------------------
# Configuration
# ----------------------------

INPUT = Path("assets/photo.jpg")
OUTPUT = Path("assets/photo-ready1.png")

# ----------------------------
# Remove background
# ----------------------------

img = Image.open(INPUT).convert("RGBA")
cutout = remove(img)

rgba = np.array(cutout)

rgb = cv2.cvtColor(rgba, cv2.COLOR_RGBA2RGB)
alpha = rgba[:, :, 3]

# ----------------------------
# Improve contrast
# ----------------------------

gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

clahe = cv2.createCLAHE(
    clipLimit=2.0,
    tileGridSize=(8, 8)
)

gray = clahe.apply(gray)

rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGBA)

# Put the original alpha channel back
rgb[:, :, 3] = alpha

# ----------------------------
# Save WITH transparency
# ----------------------------

Image.fromarray(rgb).save(OUTPUT)

print(f"Saved -> {OUTPUT}")