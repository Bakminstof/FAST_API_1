from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Cook API"


settings = Settings()
app = FastAPI()
