from dotenv import load_dotenv
import os

load_dotenv()

FROM_EMAIL = os.environ.get("FROM_EMAIL")
FROM_PWD = os.environ.get("FROM_PWD")
SMTP_SERVER = os.environ.get("SMTP_SERVER")
FOLDER_PENDING = os.environ.get("FOLDER_PENDING")
FOLDER_DONE = os.environ.get("FOLDER_DONE")
NOTION_KEY = os.environ.get("NOTION_KEY")
DATABASE_ID = os.environ.get("DATABASE_ID")
