from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class DatabaseConfig:
    name: str
    host: str
    user: str
    password: str


@dataclass
class Config:
    bot: TgBot
    db: DatabaseConfig



def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        db=DatabaseConfig(
            name=env('DB_NAME'),
            host=env('DB_HOST'),
            user=env('DB_USER'),
            password=env('DB_PASSWORD')
        )
    )
