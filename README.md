# BroCheck 🔥

> **The Open-Source AI Roaster CLI**  
> Built for the **Hacktoberfest 2026 (HF26) DEV Challenge: Build for a Friend** 🎯

`BroCheck` is a zero-RAM, multi-mode AI roaster CLI that hilariously critiques your friend's music playlists, spaghetti code, barren GitHub profiles, cringey bios, and transparent excuses using **Open-Source AI**.

---

## 🚀 Features

* 🎵 **Universal Music Roaster**: Drop any playlist link (**Spotify, Apple Music, YouTube Music, SoundCloud**), upload a `.txt`/`.m3u` file, or paste raw song lists.
* 💻 **Code Review Roaster**: Point to any `.py`, `.js`, `.ts`, `.cpp` file for a brutally honest critique of variable names and 6-level nested loops.
* 🐙 **GitHub Profile Roaster**: Enter any GitHub username to roast empty commit heatmaps, abandoned test repos, and buzzword-packed bios.
* 📱 **Social Bio & Status Roaster**: Savage fake-deep gym quotes and LinkedIn buzzwords.
* 💬 **Excuse & Chat Roaster**: Roast terrible excuses for being late to group hangs.
* 🎚️ **Adjustable Heat Levels**: `Mild 🌶️` • `Spicy 🌶️🌶️` • `Nuclear 💥🔥`
* 🎭 **Custom Personas**: `Best Friend` • `Gordon Ramsay` • `Tech Bro VC` • `Disappointed Parent`
* 🪶 **0 MB RAM Overhead**: Runs instantly on any machine (even with 4GB/6GB RAM) using open-weight models (`Llama-3.2`, `Qwen-2.5`, `Mistral`).

---

## 📦 Quick Start

### 1. Installation
```bash
git clone https://github.com/NICKSTER0506/Bro_Check.git
cd Bro_Check
pip install -r requirements.txt
```

### 2. Interactive Mode (Recommended)
Simply launch the interactive wizard:
```bash
python brocheck.py
```

### 3. CLI Flag Mode
Run directly with one-liners:

```bash
# Roast a music playlist (Spicy / Best Friend persona)
python brocheck.py --mode playlist --file demo_samples/friend_playlist.txt --heat spicy

# Roast a code file (Nuclear heat / Gordon Ramsay persona)
python brocheck.py --mode code --file demo_samples/bad_code.py --heat nuclear --persona gordon-ramsay

# Roast a GitHub developer profile (Tech Bro VC persona)
python brocheck.py --mode github --input "octocat" --persona techbro --heat spicy
```

---

## 🛠️ Architecture

```
User CLI Input
     │
     ▼
Format Detector (URL / File / Text / GitHub API)
     │
     ▼
Prompt & Persona Builder (Heat Level + Style)
     │
     ▼
Open-Weight AI Engine (Llama-3.2 / Qwen-2.5 / Mistral-7B)
     │
     ▼
Rich Terminal Fire Panel & Verdict Card 🔥
```

---

## 🌐 Why Open-Source AI Matters

1. **Zero Cost & Accessible**: Anyone with a low-spec laptop (even 4GB-6GB RAM) can run this without paying monthly subscription fees.
2. **Data Privacy**: Your friend's private code snippets, group chat messages, and playlist links never get locked into closed cloud silos.
3. **Model Choice & Customization**: Easily swap between `meta-llama/Llama-3.2-3B-Instruct`, `Qwen/Qwen2.5-Coder`, or `mistralai/Mistral-7B` depending on your desired comedy flavor.

---

## 📜 License
MIT License. Built with ❤️ and 🔥 for Hacktoberfest 2026.
