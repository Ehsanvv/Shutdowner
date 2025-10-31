# ⚠️ ShutDowner

**ShutDowner** is a Python-based GUI login system built with Tkinter that demonstrates user authentication, timeout handling, and optional system shutdown behavior. It is designed for educational purposes only — to explore GUI design, PyInstaller packaging, and basic system interactions.

> ❗ This project is not intended for malicious use. It should only be run in safe, controlled environments for learning or demonstration.

---

## 🧩 Features

- Login screen with username/password validation
- Timeout mechanism (auto-triggered after 12 seconds of inactivity)
- Optional system shutdown on failed login or timeout (disabled in test mode)
- GUI built with Tkinter and styled for clarity
- PyInstaller integration for `.exe` packaging

---

## 🚀 Getting Started

### Requirements

- Python 3.8+
- Tkinter (comes with Python)
- PyInstaller (optional, for building `.exe`)

### Run in Test Mode (No Shutdown)

```bash
python ShutDowner.py
