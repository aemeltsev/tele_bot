from environs import Env
from dataclasses import dataclass

''' 
We define a bot class with token and admin ID fields. We use the @dataclass decorator.
All class fields defined with type annotation will be used in the corresponding methods of the resulting class.
'''

@dataclass
class Bots:
    bot_token: str
    admin_id: int

@dataclass
class BotSettings:
    bots: Bots

@dataclass
class GeocodeSettings:
    geocode_token: str

'''
Using the get_bot_settings() function, we read the settings from the configuration file
'''
def get_bot_settings(path: str) -> BotSettings:
    env = Env()
    env.read_env(path)

    return BotSettings(
        bots=Bots(
            bot_token = env.str("TOKEN"),
            admin_id = env.int("ADMIN_ID")
        )
    )

def get_geocode_settings(path: str) -> GeocodeSettings:
    env = Env()
    env.read_env(path)

    return GeocodeSettings(geocode_token = env.str("GEOCODE_TOKEN"))

settings = get_bot_settings('config.py')
settings_geocode = get_geocode_settings('config.py')