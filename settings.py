from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    def get_db_url(self) -> AnyUrl:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class AppSettings(PostgresSettings):    # add other classes with settings
    pass

# os.getenv()


settings = AppSettings()

print(settings.get_db_url())
