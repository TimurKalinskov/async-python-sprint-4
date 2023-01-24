from pydantic import BaseSettings, PostgresDsn


class AppSettings(BaseSettings):
    app_title: str = "URLs shorts"
    database_dsn: PostgresDsn
    project_host: str = '0.0.0.0'
    project_port: int = 8000
    length_url: int = 6
    domain_prefix: str = ''  # for example, 'test.ru/'

    class Config:
        env_file = '.env'


app_settings = AppSettings()
