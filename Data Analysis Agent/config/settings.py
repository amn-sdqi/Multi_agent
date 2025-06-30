"""Configuration settings for the Data Analysis Agent."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama3-70b-8192"
LLM_TEMPERATURE = 0

# Display Configuration
MAX_DISPLAY_ROWS = 20
MAX_OUTPUT_LENGTH = 1000

# Output Configuration
OUTPUT_DIR = "output"
IMAGE_DPI = 300

# Security Configuration
DANGEROUS_PATTERNS = [
    '__', 'os.system', 'subprocess', 'eval(', 'exec(', 
    'open(', 'input(', 'sys.exit'
]

# Supported File Types
SUPPORTED_EXTENSIONS = ['.csv', '.json']
ENCODING_OPTIONS = ['utf-8', 'latin1', 'iso-8859-1', 'utf-16']