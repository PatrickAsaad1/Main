# 🤖 Discord Bot — Python Project

> A feature-rich Discord bot built with Python and `discord.py`, featuring **29 commands** across utilities, games, fun, security, and admin tools. Includes CLI versions of all games and a full project portfolio.

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [💬 Commands](#-commands)
  - [🔧 Utilities](#-utilities-12)
  - [🎮 Games](#-games)
  - [🎉 Fun](#-fun-8)
  - [🔐 Security](#-security-3)
  - [⚙️ Admin](#-admin-3)
  - [🍽️ Other](#-other)
- [🧰 Tech Stack](#-tech-stack)
- [⚙️ Setup & Installation](#-setup--installation)
- [🖥️ CLI Games](#-cli-games)
- [🌐 Web Projects](#-web-projects)
- [🔌 Hardware Projects](#-hardware-projects)
- [🏆 Certifications](#-certifications)

---

## ✨ Features

- 29 bot commands spanning utilities, games, fun, security, and admin tools
- Channel-restricted command execution for moderation control
- Automatic DM welcome messages for new members
- Online announcement on bot startup
- Full CLI (terminal) game suite independent of Discord
- Fernet-based message encryption and decryption
- External API integration for quotes, weather, images, memes, and jokes
- Secure password generation
- QR code generator and Morse code converter
- Config managed via `config.json` for easy customization

---

## 💬 Commands

### 🔧 Utilities (12)

| Command                | Description                                 |
| ---------------------- | ------------------------------------------- |
| `!ping`                | Check the bot's current latency             |
| `!calc <expression>`   | Multi-operation calculator                  |
| `!weather <city>`      | Get current weather for any city            |
| `!remind <time> <msg>` | Set a reminder — bot DMs you when time's up |
| `!search`              | Search for words in large text blocks       |
| `!say <message>`       | Make the bot send a message                 |
| `!repeat <message>`    | Repeat a message back                       |
| `!reply <message>`     | Reply directly to the user                  |
| `!serverinfo`          | Display info about the current server       |
| `!qr <text>`           | Generate a QR code from any text or link    |
| `!morse <text>`        | Convert text to Morse code                  |
| `!help`                | Display the custom embedded help menu       |

### 🎮 Games

| Command   | Description                                    |
| --------- | ---------------------------------------------- |
| `!rps`    | Rock Paper Scissors — solo or multiplayer      |
| `!guess`  | 3-point number guessing game with difficulties |
| `!number` | Guess a number between 1–20 in 5 attempts      |

### 🎉 Fun (8)

| Command         | Description                           |
| --------------- | ------------------------------------- |
| `!quote`        | Fetch a random inspirational quote    |
| `!picker`       | Pick a random item from a custom list |
| `!cat`          | Get a random cute cat picture 🐱      |
| `!dog`          | Get a random dog picture 🐶           |
| `!coinflip`     | Flip a coin — heads or tails          |
| `!roll <sides>` | Roll a dice with any number of sides  |
| `!joke`         | Fetch a random joke from an API       |
| `!meme`         | Get a random meme from Reddit         |

### 🔐 Security (3)

| Command              | Description                                         |
| -------------------- | --------------------------------------------------- |
| `!passgen`           | Generate a cryptographically secure password        |
| `!encrypt <message>` | Encrypt a message using Fernet symmetric encryption |
| `!decrypt`           | Decrypt a previously encrypted message              |

### ⚙️ Admin (3)

| Command          | Description                                    |
| ---------------- | ---------------------------------------------- |
| `!setchannel`    | Set the allowed channel for bot commands       |
| `!removechannel` | Remove the current allowed channel restriction |
| `!channels`      | List all currently configured bot channels     |

### 🍽️ Other

| Command | Description                            |
| ------- | -------------------------------------- |
| `!cafe` | Interactive restaurant ordering system |

---

## 🧰 Tech Stack

| Technology      | Purpose                                    |
| --------------- | ------------------------------------------ |
| `Python 3.11`   | Core language                              |
| `discord.py`    | Discord API wrapper                        |
| `python-dotenv` | Environment variable management            |
| `cryptography`  | Fernet encryption (`!encrypt`, `!decrypt`) |
| `requests`      | HTTP calls for all APIs                    |

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/idk123-bot/Main.git
cd Main
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables

Create a `.env` file in the `Main/` directory:

```env
DISCORD_TOKEN=your_bot_token_here
```

> ⚠️ **Never share your `DISCORD_TOKEN`.** This file is listed in `.gitignore` and will not be pushed to GitHub.

### 4️⃣ Run the Bot

```bash
python Bot.py
```

---

## 🖥️ CLI Games

All games have **standalone terminal versions** in the `Games/` folder — no Discord required.

```bash
python Games/Rock_Paper_Scissors.py
python Games/Guessing_Game.py
python Games/Password_Generator.py
# ...and more
```

| File                     | Description                                      |
| ------------------------ | ------------------------------------------------ |
| `Age_Checker.py`         | Calculates your age from birth year              |
| `Cafe.py`                | Restaurant ordering simulation                   |
| `Calculator.py`          | Arithmetic with input validation                 |
| `Encrypt_Decrypt.py`     | Fernet message encryption & decryption           |
| `Guessing_Game.py`       | 3-point number guessing with difficulty settings |
| `Number_Game.py`         | Guess a number from 1–20 in 5 attempts           |
| `Password_Generator.py`  | Secure random password generator                 |
| `Random_Picker.py`       | Build a list and pick a random item              |
| `Rock_Paper_Scissors.py` | Best-of-3 RPS against the computer               |
| `Text_Search.py`         | Search for words inside large text blocks        |

---

## 🌐 Web Projects

### `js-practice/`

An interactive JavaScript dashboard featuring **20+ mini-projects** demonstrating DOM manipulation, event handling, APIs, and more.

### `80-archives/`

A resource hub providing links to free tools, internet configs, and job resources.

---

## 🔌 Hardware Projects

### ⚡ Reaction Time Trainer — `reaction_game.ino`

A two-player Arduino reaction game that measures and compares player response times.

| Detail       | Info          |
| ------------ | ------------- |
| **Platform** | Arduino Uno   |
| **Language** | C++ (Arduino) |
| **Players**  | 2             |

> 📄 See [`Hardware/README.md`](Hardware/README.md) for the full component list and wiring pinout.

---

## 🏆 Certifications

| Certificate                                  | Issuer  |
| -------------------------------------------- | ------- |
| Data Storage — Huawei ICT Academy            | Huawei  |
| Cloud Computing — Huawei ICT Academy         | Huawei  |
| Artificial Intelligence — Huawei ICT Academy | Huawei  |
| _(+ 3 additional Huawei certifications)_     | Huawei  |
| MCIT Egypt Nanodegree                        | Udacity |

> 📄 See [`Certificates/README.md`](Certificates/README.md) for full details.

---

## 📄 License

This project is for **educational and portfolio purposes**.

---

<div align="center">

Built with ❤️ using **Python** and **discord.py**

</div>
