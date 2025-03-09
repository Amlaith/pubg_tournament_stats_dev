import os
from dotenv import load_dotenv

load_dotenv()

PUBG_KEY = os.getenv("PUBG_KEY")

if not PUBG_KEY:
    raise ValueError('PUBG_KEY not found')