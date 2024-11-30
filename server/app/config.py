import logging
from cachetools import TTLCache, LRUCache
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize caches
document_cache = TTLCache(maxsize=100, ttl=3600)  # 1-hour TTL
analysis_cache = LRUCache(maxsize=1000)

# Constants
SUPPORTED_FILE_TYPES = {'pdf', 'txt'}
MODEL_CONFIGS = {
    'qa_model': 'deepset/roberta-base-squad2',
    'summarizer': 'facebook/bart-large-cnn',
    'spacy_model': 'en_core_web_sm'
}
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Patterns
PATTERNS = {
    'citation': r'\d+\s+[A-Za-z\.]+\s+\d+|[A-Z]+\s+v\.\s+[A-Z]+|\[\d+\]\s+[A-Za-z\s]+\s+\d+',
    'monetary': r'\$\s*\d+(?:,\d{3})*(?:\.\d{2})?|\d+\s+dollars',
    'date': r'\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}'
}