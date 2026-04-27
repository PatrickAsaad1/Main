# Utils/Config.py
from Utils.Database import (
    get_channels as db_get_channels,
    add_channel as db_add_channel,
    remove_channel as db_remove_channel,
    set_lyrics_channel as db_set_lyrics,
    get_lyrics_channel as db_get_lyrics,
    setup_database,
    set_rap_news_channel as db_set_rap_news,
    get_rap_news_channel as db_get_rap_news,
)

setup_database()

def set_rap_news_channel(guild_id, channel_id):
    db_set_rap_news(guild_id, channel_id)

def get_rap_news_channel(guild_id):
    return db_get_rap_news(guild_id)
    
def get_allowed_channels(guild_id):
    results = db_get_channels(guild_id)
    return [row[0] for row in results]


def add_allowed_channel(guild_id, channel_id):
    return db_add_channel(guild_id, channel_id)


def remove_allowed_channel(guild_id, channel_id):
    return db_remove_channel(guild_id, channel_id)


def set_lyrics_channel(guild_id, channel_id):
    db_set_lyrics(guild_id, channel_id)


def get_lyrics_channel(guild_id):
    return db_get_lyrics(guild_id)
