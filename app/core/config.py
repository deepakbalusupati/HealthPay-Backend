from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "HealthPay Claim Processor"
    google_api_key: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()