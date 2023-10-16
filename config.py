import os
import dotenv

dotenv.load_dotenv()

WEBHOOK_URL = os.environ['WEBHOOK_URL']
BOT_TOKEN = os.environ['BOT_TOKEN']
DB_URL = os.environ['DB_URL']
