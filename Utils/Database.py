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
        (
            guild_id,
            channel_id,
        ),
    )
    conn.commit()
    conn.close()
