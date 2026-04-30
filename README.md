# 🤖 Discord Bot — Python Project

> A feature-rich Discord bot built with Python and `discord.py`, featuring **36+ commands** across utilities, games, fun, security, and admin tools.

---

## ✨ Features

- 🚀 **36+ commands** across multiple categories
- 💾 **Per-server SQLite database** for persistent storage
- 🔒 Channel-restricted command execution
- 👋 Automatic DM welcome messages for new members
- 🧠 **AI chat with memory**
- 🐾 Hourly pet pictures
- 📢 Startup announcements
- 🎮 Full CLI game suite (no Discord needed)
- 🔐 Fernet-based encryption/decryption
- 🌐 External API integrations (weather, memes, quotes, etc.)
- 🔑 Secure password generation
- 📷 QR code generator & Morse converter
- ⚙️ **Owner-only admin panel**

---

## 💬 Commands

### 🔧 Utilities (13)

| Command                | Description       |
| ---------------------- | ----------------- |
| `!ping`                | Check bot latency |
| `!calc <expression>`   | Calculator        |
| `!weather <city>`      | Weather info      |
| `!remind <time> <msg>` | Set reminder      |
| `!search`              | Search text       |
| `!say <message>`       | Bot sends message |
| `!repeat <message>`    | Echo message      |
| `!reply <message>`     | Reply to user     |
| `!serverinfo`          | Server details    |
| `!qr <text>`           | Generate QR code  |
| `!morse <text>`        | Convert to Morse  |
| `!ask <question>`      | AI chatbot        |
| `!help`                | Help menu         |

---

### 🎮 Games

| Command   | Description                      |
| --------- | -------------------------------- |
| `!rps`    | Rock Paper Scissors              |
| `!guess`  | Guessing game (difficulty modes) |
| `!number` | Guess 1–20                       |

---

### 🎉 Fun (10)

| Command         | Description   |
| --------------- | ------------- |
| `!quote`        | Random quote  |
| `!picker`       | Random picker |
| `!cat`          | Cat image 🐱  |
| `!dog`          | Dog image 🐶  |
| `!coinflip`     | Heads/Tails   |
| `!roll <sides>` | Dice roll     |
| `!joke`         | Random joke   |
| `!meme`         | Reddit meme   |
| `!advice`       | Advice        |
| `!8ball`        | Magic 8-ball  |

---

### 🔐 Security (3)

| Command          | Description     |
| ---------------- | --------------- |
| `!passgen`       | Secure password |
| `!encrypt <msg>` | Encrypt message |
| `!decrypt`       | Decrypt message |

---

### ⚙️ Admin (3)

| Command          | Description        |
| ---------------- | ------------------ |
| `!setchannel`    | Restrict commands  |
| `!removechannel` | Remove restriction |
| `!channels`      | List channels      |

---

### 🍽️ Other

| Command | Description                 |
| ------- | --------------------------- |
| `!cafe` | Interactive ordering system |

---

## 🧰 Tech Stack

| Tech            | Purpose       |
| --------------- | ------------- |
| `Python 3.11`   | Core language |
| `discord.py`    | Discord API   |
| `python-dotenv` | Env variables |
| `cryptography`  | Encryption    |
| `requests`      | API calls     |
| `sqlite3`       | Database      |

---

## ⚙️ Setup & Installation

### 1️⃣ Clone Repo

```bash
git clone https://github.com/PatrickAsaad1/Main.git
cd Main
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Setup `.env`

```env
DISCORD_TOKEN=your_bot_token_here
```

⚠️ Never share your token.

### 4️⃣ Run Bot

```bash
python Bot.py
```

---

## 🖥️ CLI Games

Run games without Discord:

```bash
python Games/Rock_Paper_Scissors.py
python Games/Guessing_Game.py
python Games/Password_Generator.py
```

### 📁 Available Scripts

| File                     | Description         |
| ------------------------ | ------------------- |
| `Age_Checker.py`         | Calculate age       |
| `Cafe.py`                | Ordering simulation |
| `Calculator.py`          | Math tool           |
| `Encrypt_Decrypt.py`     | Encryption          |
| `Guessing_Game.py`       | Guessing game       |
| `Number_Game.py`         | 1–20 game           |
| `Password_Generator.py`  | Passwords           |
| `Random_Picker.py`       | Random choice       |
| `Rock_Paper_Scissors.py` | RPS                 |
| `Text_Search.py`         | Search tool         |

---

## 🌐 Web Projects

### `js-practice/`

- 20+ mini JS projects (DOM, APIs, events)

### `80-archives/`

- Free tools & resources hub

---

## 🔌 Hardware Projects

### ⚡ Reaction Time Trainer

| Detail   | Info        |
| -------- | ----------- |
| Platform | Arduino Uno |
| Language | C++         |
| Players  | 2           |

📄 See `Hardware/README.md` for wiring details.

---

## 🏆 Certifications

- Huawei ICT Academy (Data Storage, Cloud, AI + more)
- MCIT Egypt Nanodegree — Udacity

📄 See `Certificates/README.md`

---

## 📄 License

Educational & portfolio use only.

---

<div align="center">

**Built with ❤️ using Python & discord.py**

</div>
