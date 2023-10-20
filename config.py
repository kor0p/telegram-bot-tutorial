import os
import dotenv

dotenv.load_dotenv()

env = os.environ

DEV = env.get('DEVELOPMENT', False)
WEBHOOK_URL = env['WEBHOOK_URL']
BOT_TOKEN = env['BOT_TOKEN']
if 'DB_HOST' in env:  # vercel db config
    DB_URL = f"host={env['DB_HOST']} dbname={env['DB_DATABASE']} user={env['DB_USER']} password={env['DB_PASSWORD']}"
else:
    DB_URL = os.environ['DB_URL']
