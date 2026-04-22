# 🤖 Discord Bot — Python Project

A feature-rich Discord bot built with Python and discord.py, featuring 16 commands across utilities, games, encryption, and more. Includes CLI versions of all games and a full project portfolio.

\---

## 📋 Table of Contents

* [Features](#-features)
* [Commands](#-commands)
* [Project Structure](#-project-structure)
* [Tech Stack](#-tech-stack)
* [Setup \& Installation](#-setup--installation)
* [Configuration](#-configuration)
* [CLI Games](#-cli-games)
* [Web Projects](#-web-projects)
* [Hardware Projects](#-hardware-projects)
* [Certifications](#-certifications)

\---

## ✨ Features

* 16 bot commands spanning utilities, games, security, and fun
* Channel-restricted command execution for moderation control
* Automatic DM welcome messages for new members
* Online announcement on bot startup
* Full CLI (terminal) game suite independent of Discord
* Fernet-based message encryption and decryption
* External API integration for random quotes
* Secure password generation

\---

## 💬 Commands

### 🔧 Utilities

|Command|Description|
|-|-|
|`!ping`|Check the bot's current latency|
|`!say <message>`|Make the bot send a message|
|`!repeat <message>`|Repeat a message back|
|`!reply <message>`|Reply directly to the user|
|`!help`|Display the custom embedded help menu|

### 🎮 Games

|Command|Description|
|-|-|
|`!rps`|Rock Paper Scissors — solo or multiplayer|
|`!guess`|3-point number guessing game with difficulties|
|`!number`|Guess a number between 1–20 in 5 attempts|

### 🛠️ Tools

|Command|Description|
|-|-|
|`!calc`|Multi-operation calculator|
|`!passgen`|Generate a cryptographically secure password|
|`!encrypt <message>`|Encrypt a message using Fernet symmetric encryption|
|`!decrypt <token>`|Decrypt a previously encrypted message|
|`!quote`|Fetch a random inspirational quote from an API|
|`!picker <items>`|Pick a random item from a custom list|

### 🍽️ Other

|Command|Description|
|-|-|
|`!cafe`|Interactive restaurant ordering system|

\---

\---

## 🧰 Tech Stack

|Technology|Purpose|
|-|-|
|Python 3.x|Core language|
|discord.py|Discord API wrapper|
|python-dotenv|Environment variable management|
|cryptography|Fernet encryption (`!encrypt`, `!decrypt`)|
|requests|HTTP calls for `!quote` API|

\---

## ⚙️ Setup \& Installation

### 1\. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo/Main
```

### 2\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3\. Configure Environment Variables

Create a `.env` file in the `Main/` directory:

```env
DISCORD\_TOKEN=your\_bot\_token\_here
DISCORD\_CHANNEL=your\_announcement\_channel\_id
ALLOWED\_CHANNEL\_ID=your\_commands\_channel\_id
```

> ⚠️ \*\*Never share your `DISCORD\_TOKEN`.\*\* This file is in `.gitignore` and will not be pushed to GitHub.

### 4\. Run the Bot

```bash
python Bot.py
```

\---

## 🔐 Configuration

|Variable|Description|
|-|-|
|`DISCORD\_TOKEN`|Your bot's secret token from the Discord Developer Portal|
|`DISCORD\_CHANNEL`|Channel ID where the bot announces it's online|
|`ALLOWED\_CHANNEL\_ID`|Channel ID where commands are accepted (others are ignored)|

\---

## 🖥️ CLI Games

All games have standalone terminal versions in the `Games/` folder. Run them directly with Python — no Discord required.

```bash
python Games/Rock\_Paper\_Scissors.py
python Games/Guessing\_Game.py
python Games/Password\_Generator.py
# etc.
```

|File|Game|
|-|-|
|`Age\_Checker.py`|Calculates your age from birth year|
|`Calculator.py`|Arithmetic with input validation|
|`Cafe.py`|Restaurant ordering simulation|
|`Encrypt\_Decrypt.py`|Fernet message encryption/decryption|
|`Guessing\_Game.py`|3-point number guessing with difficulty settings|
|`Number\_Game.py`|Guess 1–20 in 5 attempts|
|`Password\_Generator.py`|Secure random password generator|
|`Random\_Picker.py`|Build a list and pick a random item|
|`Rock\_Paper\_Scissors.py`|Best-of-3 RPS against the computer|
|`Text\_Search.py`|Search for words inside large text blocks|

\---

## 🌐 Web Projects

### `js-practice/`

An interactive JavaScript dashboard featuring 20+ mini-projects demonstrating DOM manipulation, event handling, APIs, and more.

### `80-archives/`

A resource hub providing links to free tools, internet configs, and job resources.

\---

## 🔌 Hardware Projects

### Reaction Time Trainer (`reaction\_game.ino`)

A two-player Arduino reaction game that measures and compares player response times.

* **Platform:** Arduino Uno
* **Language:** C++ (Arduino)
* **Players:** 2
* See [`Hardware/README.md`](Hardware/README.md) for full component list and wiring pinout.

\---

## 🏆 Certifications

|Certificate|Issuer|
|-|-|
|Data Storage — Huawei ICT Academy|Huawei|
|Cloud Computing — Huawei ICT Academy|Huawei|
|Artificial Intelligence — Huawei ICT Academy|Huawei|
|*(+ 3 additional Huawei certifications)*|Huawei|
|MCIT Egypt Nanodegree|Udacity|

See [`Certificates/README.md`](Certificates/README.md) for full details.

\---

## 📄 License

This project is for educational and portfolio purposes.

\---

> Built with ❤️ using Python and discord.py

