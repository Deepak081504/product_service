from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "REST Product Service"
    APP_ENV: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    API_V1_PREFIX: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()