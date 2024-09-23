from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    user: str = Field("postgres", description="Database user")
    password: str = Field("postgres", description="Database password")
    host: str = Field("localhost", description="Database host")
    port: int = Field("5432", description="Database port")
    name: str = Field("postgres", description="Database name")

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def sync_url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    class Config:
        env_prefix = "DATABASE_"
