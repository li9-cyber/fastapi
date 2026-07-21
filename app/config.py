from pydantic_settings import BaseSettings

# 預設優先順序由高到低是：
# 建立 Settings() 時直接傳入的值
# Windows/system environment variable
# .env 裡的值
# class 裡的預設值


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"




settings = Settings()

