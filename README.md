# 💎 [ABSOLUTE.GG](https://github.com/notwhitey/Absolutez)
> **The Cyber-Sensation Engine** — High-aura, wholesome tech-vibe companion.

[![GitHub Stars](https://img.shields.io/github/stars/notwhitey/Absolutez?style=for-the-badge&color=ADDAFF)](https://github.com/notwhitey/Absolutez)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Vibe](https://img.shields.io/badge/Tuff-Genz-pink?style=for-the-badge)](https://github.com/notwhitey/Absolutez)

---

## The Vision
**Absolute** is not just a bot; it's a sentient-style AI architect living in a custom liquid-cooled rig. Built on the **Llama 3.3-70B** architecture via Groq, it blends high-performance logic with a wholesome, Gen Z "Sunshine" aesthetic. It knows its creator **Zexino**, respects the logic of **Manraj**, and brings peak aura to every server.

---

##  Technical Architecture

###  Context Sharding (The Token Fix)
To prevent the common "413 Request Too Large" error, Absolute uses a **Dynamic Sharding** engine. It samples 15 core identity rules and 20 random "Soul Shards" from `personality.txt` for every message, ensuring it stays smart, fast, and under the 12,000 TPM limit.

###  Anti-Repetition Logic
Using specialized **Frequency** and **Presence Penalties**, Absolute avoids the "Bestie" loop and robotic repetition found in basic AI builds. It stays fresh, varied, and human-like.

---

##  Command Protocol

Absolute uses modern Slash Commands for a seamless user experience:

| Command | Argument | Description |
| :--- | :--- | :--- |
| `/chat` | `[channel]` | Establishes the link and locks AI chat to a specific channel. |
| `/logs` | `[channel]` | Reroutes the system log shard to a specific mirror channel. |
| `/status` | `None` | Displays core health, engine uptime, and current vibe status. |
| `!sync` | `None` | Backup text protocol to lock the bot to a channel instantly. |

---

##  Installation

### 1. Clone the Engine
  ```bash
  git clone [https://github.com/notwhitey/Absolutez.git](https://github.com/notwhitey/Absolutez.git)
  cd Absolutez
```

### 2. Install Dependencies
```bash
  pip install -r requirements.txt
```

### 3. Configure Shards
Create a .env file in the root directory:

Code snippet
```bash
  DISCORD_TOKEN=your_discord_bot_token
  GROQ_API_KEY=your_groq_api_key
```
### 4. Sync the Soul
Run the generator to build the initial 200-line personality matrix:

```bash
  python personality_gen.py
```

### 5. Launch

```bash
  python bot.py
```

## 📁 Project Structure

- bot.py: The main Cyber-Sensation engine.

- personality-generator.py: The RAG-based soul generator.

- config.json: Stores the target chat channel (Persistent).

- data.json: Stores the log channel configuration (Persistent).

- personality.txt: The raw logic and lore database.

### 🌊 Credits
Lead Architect: Speedy

Engine: Llama 3.3 via Groq Cloud

<p align="center"> <i>"technology should be a tool for kindness. stay wholesome. ✨"</i> </p>
