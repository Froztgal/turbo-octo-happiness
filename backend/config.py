# Imports
from pydantic import BaseSettings, BaseModel

# Postgres 
class PostgresDB(BaseModel):
    user: str
    password: str
    host: str
    port: str
    database: str

    @property
    def DSN(self):
        return f"{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

# Security
class Security(BaseModel):
    secret_key: str
    token_expire: int
    algorithm: str

# Settings
class Settings(BaseSettings):
    app_name: str
    admin_email: str
    security: Security
    postgres_db: PostgresDB

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = "__"

# Singletone
settings = Settings()