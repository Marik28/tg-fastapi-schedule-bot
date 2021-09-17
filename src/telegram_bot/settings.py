from pydantic import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_API_TOKEN: str

    start_week: int = 35
    timezone_id: str = 'Asia/Almaty'

    api_base_url: str = "http://localhost:5050"
    lessons_endpoint: str = "/lessons/"
    groups_endpoint: str = "/groups/"
    assignments_endpoint: str = "/assignments/"
    subjects_endpoint: str = "/subjects/"

    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0
    available_groups_set_name: str = "available_groups"


settings = Settings()
