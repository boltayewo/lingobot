import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "8525442823:AAEk1MtV_tMNgW035M8dzk3gQZpN_isXz1c")
ADMIN_ID = int(os.getenv("ADMIN_ID", "5801760148"))