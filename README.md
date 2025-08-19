# 🧠 LLM RPG Game - AI Dialogue Edition

> A retro-style LLM RPG Game where **NPCs are powered by AI** — and you can **watch them think in real time**.

![Game Screenshot](/Assets/main.png)  
*NPCs with personalities, powered by local LLMs, showing their thoughts as they talk.*

---

## 🌟 Features

### 🔍 Real-Time AI Thinking
- NPCs **"think"** before replying
- `<think>...</think>` tags reveal reasoning
- Cleaned response shown after thought
- **Transparent AI** — no hidden magic

### 🤖 AI-Powered NPC Personalities
Every NPC reacts differently:
- **friendly** – warm and helpful  
- **wise** – deep and philosophical  
- **playful** – lighthearted and fun  
- **mysterious** – cryptic and secretive  
- **programmer** – logical with dry humor  

### 🧩 Powered by Local LLM (Ollama + qwen3:8b)
- Works **fully offline**
- Uses [Ollama](https://ollama.com) with `qwen3:8b`
- Streaming text for smooth, natural dialogue

### 🎮 Interactive Gameplay
- **Arrow keys** → Move  
- **Z** → Talk to NPCs  
- **Enter** → Send text  
- **↑↓** → Scroll responses  
- **ESC** → Exit dialogue  

---

## 🚀 How It Works

Not just a chatbot — each NPC is an **AI agent** with:
- Memory  
- Personality  
- Visible thoughts  

Example:

**Player:**  
> "Why is the coffee machine broken?"

**NPC Thinking (visible):**
```xml
<think>
The player is asking about the coffee machine.
I know it's broken because Li Zhongjie spilled water on it.
Since I'm playful, I'll tease a little instead of telling the full truth.
</think>
```

**NPC Response:**  
> "Oh, that old thing? It’s been broken for days…"

---

## 📂 Project Structure

```
RoomAdventureRPG/
├── main.py                 # Entry point
├── Game/
│   └── Game.py             # Main game loop
├── Player/
│   ├── Player.py           # Player movement/animation
│   └── NPC.py              # AI-powered NPCs
├── LLM/
│   └── OllamaAPI.py        # Streaming API to Ollama
├── Env/
│   └── RoomEnvironment.py  # Room layout & objects
├── Setting/
│   ├── Configuration.py    # Constants & settings
│   ├── FontManager.py      # Fixes CN/EN font issues
│   └── DialogueSystem.py   # Dialogue + <think> handling
└── assets/
    └── img/                # Sprites/UI
```

---

## ⚙️ Setup & Requirements

### 1. Install Python Dependencies
```bash
pip install pygame requests
```

### 2. Install Ollama
Download from: [https://ollama.com](https://ollama.com)

### 3. Pull the Model
```bash
ollama pull qwen3:8b
```

### 4. Run the Game
```bash
python main.py
```

---

## 🤝 Contributing

We welcome contributions!  
Ideas:
- Add new NPC personalities  
- Voice input/output  
- Save/load conversations  
- Emotional states (angry, happy, curious)  
- Support more LLMs (Llama3, Mistral, etc.)  

Fork → make changes → open PR 🚀

---

## 📜 License
MIT License – free to use, modify, and share.
---

## 🙏 Acknowledgments
- **Ollama** – local LLM serving  
- **Qwen Team** – `qwen3:8b` model  
- **Pygame** – 2D game engine  
---
