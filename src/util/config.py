from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_URL: str
    JWT_SECRET_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Config()
