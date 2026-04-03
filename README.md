# 🌅 Morning Ritual Gate

A macOS app that **blocks your computer every morning** until you've meditated and written 10 blessings.

Once you complete your ritual, your Mac unlocks. Your blessings are saved to a daily journal with the date, time, and your current streak.

![Morning Ritual Gate screenshot](screenshot.png)

---

## What it does

- 🔒 Fullscreen gate appears every time you **open your laptop lid** (or restart)
- 🧘 Requires you to check off that you've meditated
- 🙏 Requires you to write 10 things you're grateful for
- 🔥 Tracks your **daily streak**
- 📓 Saves every entry to a **journal file** with date, time & streak day
- ✅ If you've already completed it today, it auto-dismisses

### Journal entry example
```
────────────────────────────────────────────────────────────────
  Thursday, April 3, 2026  ·  7:42 AM  ·  Day 4 🔥
────────────────────────────────────────────────────────────────
   1. I'm grateful for my health
   2. I'm grateful for my family
   ...
```

---

## Requirements

- macOS
- Python 3 — download from [python.org](https://www.python.org) or install via Homebrew

---

## Install

**1. Clone or download this repo, then open Terminal and run:**

```bash
bash ~/Documents/MorningRitual/setup.sh
```

That's it. The setup script will:
- Install [Homebrew](https://brew.sh) (if you don't have it)
- Install `sleepwatcher` (triggers the gate on lid open / wake from sleep)
- Register the app to run at every login too

**2. Test it works:**

```bash
python3 ~/Documents/MorningRitual/morning_ritual.py
```

---

## Journal location

Your blessings are saved to:

```
~/Documents/MorningRitual/blessings_journal.txt
```

If iCloud Drive is enabled on your Mac, it saves there instead and syncs to your iPhone/iPad automatically.

---

## Uninstall

```bash
launchctl unload ~/Library/LaunchAgents/com.morningritual.gate.plist
rm ~/Library/LaunchAgents/com.morningritual.gate.plist
rm ~/.wakeup
```

---

## Inspiration

I built this because I wanted my morning meditation and gratitude practice to be non-negotiable — not optional. If the computer won't work until I do it, I do it.
