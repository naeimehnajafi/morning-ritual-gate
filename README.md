# 🌅 Morning Ritual Gate

I built this in April 2026, during my PhD.

PhD life is strange. Nobody tells you what to do or when to show up. No schedule, no manager, no structure unless you create it yourself. That freedom sounds great until you realise how easy it is to drift. Days blur together. Motivation comes and goes. And the first thing that disappears when things get hard is the small habits that actually keep you grounded.

I had been trying to meditate every morning and write 10 things I was grateful for. Not because anyone told me to, but because it genuinely made my days better. I use [Headspace](https://www.headspace.com) for meditation — if you are a student, they have a subscription for $10/year which is honestly one of the best deals out there. The problem was that "trying" was not enough. Some mornings I would open my laptop, get sucked into emails or research, and the ritual just would not happen.

So I thought: what if the computer simply did not work until I did it?

No willpower needed. No reminders to ignore. Just: you open your laptop, the gate is there, and your day does not start until your ritual is done.

This is the first step of my daily routine to keep myself productive and grounded. I thought I would share it with others too, in case it helps someone else going through the same thing.

![Morning Ritual Gate screenshot](screenshot.png)

---

## What it does

- 🔒 Fullscreen gate appears every time you open your laptop lid (or restart)
- 🧘 Requires you to check off that you have meditated
- 🙏 Requires you to write 10 things you are grateful for
- 🔥 Tracks your daily streak
- 📓 Saves every entry to a journal file with date, time and streak day
- ✅ If you have already completed it today, it auto-dismisses

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
