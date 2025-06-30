"""File handling utilities."""

import os
import shutil
import platform
import subprocess
import matplotlib.pyplot as plt
from datetime import datetime
from config.settings import OUTPUT_DIR, IMAGE_DPI

def setup_output_directory():
    """Setup output directory."""
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_image_path() -> str:
    """Generate unique image path."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(OUTPUT_DIR, f"plot_{timestamp}.png")

def save_plot(image_path: str):
    """Save matplotlib plot."""
    plt.tight_layout()
    plt.savefig(image_path, dpi=IMAGE_DPI, bbox_inches='tight')
    plt.close()

def open_image(image_path: str):
    """Open image based on OS."""
    try:
        if platform.system() == 'Windows':
            os.startfile(image_path)
        elif platform.system() == 'Darwin':
            subprocess.call(['open', image_path])
        else:
            subprocess.call(['xdg-open', image_path])
    except Exception:
        print(f"Image saved at: {os.path.abspath(image_path)}")