from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    PROJECT_ID = os.getenv("PROJECT_ID")
    TOPIC_ID=os.getenv("TOPIC_ID")

settings = Settings()