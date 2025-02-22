import os

from dotenv import load_dotenv

load_dotenv(override=True)


class ConfigSetting:
    PROJECT_NAME: str = os.environ["PROJECT_NAME"]
    PAGE_ID: str = os.environ["PAGE_ID"]
    APP_ID: str = os.environ["APP_ID"]
    BOT_ID: str = os.environ["BOT_ID"]
    PAGE_ACCESS_TOKEN: str = os.environ["PAGE_ACCESS_TOKEN"]
    APP_SECRET: str = os.environ["APP_SECRET"]
    VERIFY_TOKEN: str = os.environ["VERIFY_TOKEN"]
    FACEBOOK_GRAPH_API: str = os.environ["FACEBOOK_GRAPH_API"]
    FACEBOOK_GRAPH_VERSION: str = os.environ["FACEBOOK_GRAPH_VERSION"]
    LLM_API: str = os.environ["LLM_API"]
    LLM_KEY: str = os.environ["LLM_KEY"].split(",")
    MODEL_NAME: str = "gemini-2.0-flash"
    DB_HOST: str = os.environ["DB_HOST"]
    DB_USERNAME: str = os.environ["DB_USERNAME"]
    DB_PASSWORD: str = os.environ["DB_PASSWORD"]
    DB_NAME: str = os.environ["DB_NAME"]
    DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    FACEBOOK_URL = f"{FACEBOOK_GRAPH_API}/{FACEBOOK_GRAPH_VERSION}/me/messages?access_token={PAGE_ACCESS_TOKEN}"


configsetting = ConfigSetting()
