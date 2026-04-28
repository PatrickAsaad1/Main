# Utils/Database.py
import sqlite3
from Utils.Logger import setup_logging
import os

logging = setup_logging()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "bot.db")


def connect():
    connection = sqlite3.connect(DB_PATH)
    return connection


def setup_database():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS servers (guild_id INTEGER, channel_id INTEGER)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS lyrics_channels (guild_id INTEGER, channel_id INTEGER)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS rap_news_channels (guild_id INTEGER, channel_id INTEGER)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS pet_channels (guild_id INTEGER, channel_id INTEGER)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS game_news_channels (guild_id INTEGER, channel_id INTEGER)"
    )
    conn.commit()
    conn.close()


def add_channel(guild_id, channel_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO servers(guild_id, channel_id) VALUES (?, ?)",
        (guild_id, channel_id),
    )
    conn.commit()
    conn.close()


def get_channels(guild_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT channel_id FROM servers WHERE guild_id = ?", (guild_id,))
    data = cursor.fetchall()
    conn.close()
    return data


def remove_channel(guild_id, channel_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM servers WHERE guild_id = ? AND channel_id = ?",
        (guild_id, channel_id),
    )
    conn.commit()
    conn.close()


def set_lyrics_channel(guild_id, channel_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lyrics_channels WHERE guild_id = ?", (guild_id,))
    cursor.execute(
        "INSERT INTO lyrics_channels(guild_id, channel_id) VALUES (?, ?)",
        (guild_id, channel_id),
    )
    conn.commit()
    conn.close()


def get_lyrics_channel(guild_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT channel_id FROM lyrics_channels WHERE guild_id = ?", (guild_id,)
    )
    data = cursor.fetchone()
    conn.close()
    return data[0] if data else None


def remove_lyrics_channel(guild_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lyrics_channels WHERE guild_id = ?", (guild_id,))
    conn.commit()
    conn.close()


def set_rap_news_channel(guild_id, channel_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rap_news_channels WHERE guild_id = ?", (guild_id,))
    cursor.execute(
        "INSERT INTO rap_news_channels(guild_id, channel_id) VALUES (?, ?)",
        (guild_id, channel_id),
    )
    conn.commit()
    conn.close()


def get_rap_news_channel(guild_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT channel_id FROM rap_news_channels WHERE guild_id = ?", (guild_id,)
    )
    data = cursor.fetchone()
    conn.close()
    return data[0] if data else None


def set_pet_channel(guild_id, channel_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pet_channels WHERE guild_id = ?", (guild_id,))
    cursor.execute(
        "INSERT INTO pet_channels(guild_id, channel_id) VALUES (?, ?)",
        (guild_id, channel_id),
    )
    conn.commit()
    conn.close()


def get_pet_channel(guild_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT channel_id FROM pet_channels WHERE guild_id = ?", (guild_id,)
    )
    data = cursor.fetchone()
    conn.close()
    return data[0] if data else None


def set_game_news_channel(guild_id, channel_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM game_news_channels WHERE guild_id = ?", (guild_id,))
    cursor.execute(
        "INSERT INTO game_news_channels(guild_id, channel_id) VALUES (?, ?)",
        (guild_id, channel_id),
    )
    conn.commit()
    conn.close()


def get_game_news_channel(guild_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT channel_id FROM game_news_channels WHERE guild_id = ?", (guild_id,)
    )
    data = cursor.fetchone()
    conn.close()
    return data[0] if data else None


def remove_rap_news_channel(guild_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rap_news_channels WHERE guild_id = ?", (guild_id,))
    conn.commit()
    conn.close()


def remove_game_news_channel(guild_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM game_news_channels WHERE guild_id = ?", (guild_id,))
    conn.commit()
    conn.close()
