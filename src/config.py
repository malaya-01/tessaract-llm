import os
from dotenv import load_dotenv

load_dotenv()

# Tesseract configuration
TESSERACT_CMD = os.getenv('TESSERACT_CMD', 'C:/Program Files/Tesseract-OCR/tesseract.exe')

# Google Generative AI model configurations
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'models/embedding-001')
CHAT_MODEL = os.getenv('CHAT_MODEL', 'gemini-1.5-flash')
TEMPERATURE = float(os.getenv('TEMPERATURE', 0.4))
