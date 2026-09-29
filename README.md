<div align="center">

# 🔒 File Monitoring System

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-4B8BBE?style=for-the-badge&logo=python&logoColor=white)](#)
[![Stdlib only](https://img.shields.io/badge/Dependencies-None-brightgreen?style=for-the-badge)](#-tech-stack)

A desktop app that watches your folders and tells you the moment anything changes — files created, modified, or deleted — with SHA-256 integrity checks to catch silent tampering. Written entirely in Python's standard library, in a single file.

</div>

![Project preview](assets/hero.webp)

---

## ✨ Features

- **👀 Real-time file watching** — a background thread re-scans your folders every 3 seconds, so the GUI never freezes while it monitors.
- **🆕🔁🗑️ Change detection** — catches file creations, content/size modifications, and deletions by comparing each scan against a baseline.
- **🛡️ SHA-256 integrity checks** — modified files get their hash compared; if the hash changed, you get an instant popup alert.
- **🎨 Color-coded live event log** — red for deletions, orange for creations, blue for modifications, every entry timestamped.
- **📊 Live statistics dashboard** — running counts of total events, file changes, creations, and deletions.
- **📁 Custom folders** — starts with `Desktop`, `Documents`, and `Downloads`; add any folder through a file picker.
- **🧪 Built-in test button** — drops a test file on your Desktop so you can watch the detector catch it immediately.
- **📦 Zero dependencies** — `tkinter`, `threading`, `os`, `hashlib` — nothing to `pip install`.

## 🛠️ Tech Stack

| Module | Role |
|:-------|:-----|
| **tkinter / ttk** | GUI, styled widgets, live log panes |
| **threading** | Non-blocking directory scanner |
| **os** | Directory walking, file metadata (size, mtime, ctime) |
| **hashlib** | SHA-256 file integrity hashing |
| **datetime / json** | Timestamps and log formatting |

## 🚀 Getting Started

**1. Clone the repo**

```bash
git clone https://github.com/hussnainahmedd/file-monitoring-system.git
cd file-monitoring-system/file-monitoring-system
```

**2. Run it** (no install step — that's the point)

```bash
python code.py
```

> 💡 **Linux users:** if `tkinter` is missing, run `sudo apt install python3-tk`.

**3. Use it**

1. Press **🟢 Start System Monitoring** — the button turns red while it watches.
2. Add more folders with **📁 Add Folder**, or verify detection with **🧪 Create Test File**.
3. Watch creations, modifications, and deletions stream into the color-coded log with live stats.
4. **🧹 Clear Logs** resets the log and all counters.

## 📂 Project Structure

```
file-monitoring-system/
└── file-monitoring-system/
    └── code.py   # The entire app — GUI, scanner thread, integrity checks
```

---

<div align="center">

Built by [Hussnain Ahmad](https://github.com/hussnainahmedd) — a CS undergrad at Air University, Islamabad, who likes building tools that actually run on his own machine.

</div>
